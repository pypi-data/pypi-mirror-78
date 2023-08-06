import os

from prometheus_client import push_to_gateway, Gauge, CollectorRegistry, Counter, Summary, Histogram, Info, REGISTRY

HOSTNAME = os.getenv("HOSTNAME")


def get_metric_pushgateway():
    return os.getenv('PAPERSPACE_METRIC_PUSHGATEWAY', 'http://prom-aggregation-gateway:80')


def _get_env_var_or_raise(*env_vars):
    rv = None
    for env_var in env_vars:
        rv = os.getenv(env_var)
        if not rv:
            break

    if rv is None:
        msg = "{} environment variable(s) not found".format(", ".join(env_vars))
        raise ValueError(msg)

    return rv


def _get_experiment_id():
    if os.getenv('PAPERSPACE_EXPERIMENT_ID'):
        return os.getenv('PAPERSPACE_EXPERIMENT_ID')
    try:
        experiment_id = HOSTNAME.split('-')[1]
        return experiment_id
    except IndexError:
        msg = "Experiment ID not found"
        raise ValueError(msg)


def get_job_id():
    return _get_experiment_id()


class MetricsLogger:
    """Prometheus wrapper for logging custom metrics

    Examples:
        >>> from gradient_utils import MetricsLogger
        >>> m_logger = MetricsLogger()
        >>> m_logger.add_gauge("some_metric_1")
        >>> m_logger.add_gauge("some_metric_2")
        >>> m_logger["some_metric_1"].set(3)
        >>> m_logger["some_metric_1"].inc()
        >>> m_logger["some_metric_2"].set_to_current_time()
        >>> m_logger.push_metrics()

    """

    def __init__(self, job_id=None, registry=REGISTRY, push_gateway=None):
        """
        :param str job_id:
        :param CollectorRegistry registry:
        :param str push_gateway:
        """
        self.id = job_id or get_job_id()
        self.registry = registry
        self.grouping_key = {"label_metrics_experiment_handle": self.id}
        self.push_gateway = push_gateway or get_metric_pushgateway()

        self._metrics = dict()

    def __getitem__(self, item):
        """
        :param str item:

        :rtype Gauge|Counter|Summary|Histogram|Info
        """
        return self._metrics[item].labels(self.id, HOSTNAME)

    def add_gauge(self, name):
        self._add_metric(Gauge, name)

    def add_counter(self, name):
        self._add_metric(Counter, name)

    def add_summary(self, name):
        self._add_metric(Summary, name)

    def add_histogram(self, name):
        self._add_metric(Histogram, name)

    def add_info(self, name):
        self._add_metric(Info, name)

    def _add_metric(self, cls, name, documentation=""):
        new_metric = cls(name, documentation=documentation, registry=self.registry,
                         labelnames=["label_metrics_experiment_handle", "pod"])
        self._metrics[name] = new_metric

    def push_metrics(self, timeout=30):
        push_to_gateway(
            gateway=self.push_gateway,
            job=self.id,
            registry=self.registry,
            grouping_key=self.grouping_key,
            timeout=timeout,
        )
