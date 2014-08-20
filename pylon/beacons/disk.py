import psutil
import os
from .beacon import Beacon

class Service(Beacon):
    '''
    Get usage disk information and other stuff
    '''
    graphite_namespace = "disk"
    expose = ['percent_usage']

    def expose_percent_usage(self):
        data = []
        for part in psutil.disk_partitions():
            partitions = {}
            temp_device = self.format(part.device)
            partitions[temp_device] = psutil.disk_usage(part.mountpoint).percent
            data.append(partitions)

        return data

    def format(self, device):
        return device.split('/')[-1]
