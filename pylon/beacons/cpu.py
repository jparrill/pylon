import psutil
import os
from .beacon import Beacon

class Service(Beacon):
    '''
    This beacon is monitoring Cpu stuff
    Captain Obvious strikes!
    '''
    #name = "Cpu"
    graphite_namespace = "cpu"
    expose = ['load_5', 'usage']

    def expose_load_5(self):
        return dict(
            graphite_namespace="load_5",
            value=str(os.getloadavg()[0])[:4]
        )

    def expose_load_10(self):
        return dict(
            graphite_namespace="load_10",
            value=str(os.getloadavg()[1])[:4]
        )

    def expose_load_15(self):
        return dict(
            graphite_namespace="load_15",
            value=str(os.getloadavg()[2])[:4]
        )

    def expose_usage(self):
        return dict(
            graphite_namespace="usage_percent",
            value=psutil.cpu_percent(interval=1)
        )