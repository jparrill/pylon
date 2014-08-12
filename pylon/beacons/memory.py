import psutil
from .beacon import Beacon

class Service(Beacon):
    '''
    This beacon is monitoring memory stuff
    Captain Obvious strikes, again!!
    '''
    #name = "Memory"
    graphite_namespace = "memory"
    expose = ["percent", "used", "available", "total"]

    def expose_percent(self):
        return dict(
            graphite_namespace="percent",
            value=psutil.virtual_memory().percent
        )

    def expose_used(self):
        return dict(
            graphite_namespace="used",
            value=self.b_to_mb(psutil.virtual_memory().used)
        )

    def expose_available(self):
        return dict(
            graphite_namespace="available",
            value=self.b_to_mb(
                psutil.virtual_memory().total - psutil.virtual_memory().used)
        )

    def expose_sw_percent(self):
        return dict(
            graphite_namespace="sw_percent",
            value=psutil.virtual_memory().percent
        )

    def expose_sw_used(self):
        return dict(
            graphite_namespace="sw_used",
            value=self.b_to_mb(psutil.virtual_memory().used)
        )

    def expose_sw_available(self):
        return dict(
            graphite_namespace="sw_available",
            value=self.b_to_mb(
                psutil.virtual_memory().total - psutil.virtual_memory().used)
        )

    def b_to_mb(self, bytes):
        # Convert b to Mb
        return bytes/1000000
