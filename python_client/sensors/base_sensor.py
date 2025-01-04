class BaseSensor:
    def __init__(self):
        """Initialize the sensor."""
        pass

    def update_metrics(self):
        """Update the sensor's Prometheus metrics."""
        raise NotImplementedError("Subclasses must implement update_metrics.")
