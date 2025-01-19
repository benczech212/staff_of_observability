from prometheus_client import Gauge


class BaseSensor:
    def __init__(self, instance_name="sensor"):
        self.instance_name = instance_name
        self.base_labels = {'sensor': 'sensor', 'instance_name': instance_name}
        self.metrics = {}

    def update_metrics(self):
        """Update the sensor's Prometheus metrics."""
        raise NotImplementedError("Subclasses must implement update_metrics.")

    def get_or_create_metric_gauge(self, name, description, extra_labels=None):
        """
        Create or retrieve a Gauge metric with the specified name and description.

        :param name: Name of the metric.
        :param description: Description of the metric.
        :param extra_labels: Dictionary of additional labels to add to the metric.
        :return: A labeled Prometheus Gauge object.
        """
        if extra_labels is None:
            extra_labels = {}

        # Combine base labels and extra labels
        all_labels = {**self.base_labels, **extra_labels}

        # Check if the metric already exists
        if not hasattr(self, 'metrics'): self.metrics = {}
        existing_metric = self.metrics.get(name, None)
        if existing_metric:
            return existing_metric

        try:
            # Create and store the new metric
            gauge = Gauge(
                name,
                description,
                list(all_labels.keys())  # Label keys for the metric
            )
            labeled_metric = gauge.labels(**all_labels)
            self.metrics[name] = labeled_metric
            return labeled_metric
        except Exception as e:
            print(f"Error creating metric {name}: {e}")
            return None