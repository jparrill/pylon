import ConfigParser
import sys
import logging
from os.path import realpath
from os.path import dirname
from socket import socket
import os
from beacons import *

class BeaconHandler(object):
    graphite_namespace = None
    beacons = {}

    def __init__(self):
        self.get_config()
        self.logger()
        #self.graphite_namespace = graphite_namespace
        #self.setup_graphite(graphite_config)

    def get_config(self):
        file_path = dirname(realpath(__file__))
        config = ConfigParser.RawConfigParser()
        try:
            logging.info('Reading configuration')
            config.read(file_path + '/probe.ini')
        except:
            logging.critical('Error reading config file')

        self.server = config.get('Graphite', 'server')
        self.port = config.get('Graphite', 'port')
        self.domain = config.get('Graphite', 'domain')
        self.initiative = config.get('Graphite', 'initiative')
        self.hostname = config.get('Graphite', 'hostname')
        if not self.hostname:
            self.hostname = socket.gethostname()

        self.graphite_log = config.get('Graphite', 'log_file')

    def logger(self):
        log_file = self.graphite_log
        logging.getLogger('').handlers = []
        if not os.path.exists(log_file):
            open(log_file, 'a').close()

        logging.basicConfig(
            filename=log_file,
            format='%(asctime)-15s %(name)-5s %(levelname)-8s %(message)s',
            level=logging.INFO
            )

        logging.info('Pylon has been Activated')


    def register(self, new_beacon):
        class_name = new_beacon().__class__.__name__
        if class_name not in self.beacons:
            if isinstance(new_beacon(), beacon.Beacon):
                self.beacons[class_name] = new_beacon

    def setup_graphite(self, graphite_config):
        pass
        # try:
        #     sock = socket.connect(server, port)
        # except:
        #     print "Couldn't connect to %s on port %d" % (server, port)
        #     sys.exit(1)

        # return sock

    def send_to_graphite(self, namespace, value):
        logging.debug(u'{}.{}.{}.{}: {}'.format(
            self.domain,
            self.initiative,
            self.hostname,
            namespace, 
            value
            )
        )
        print u'{}.{}.{}.{}: {}'.format(
            self.domain,
            self.initiative,
            self.hostname,
            namespace, 
            value
            )

    def run(self):
        for beacon_name,beacon_class in self.beacons.iteritems():
            beacon = beacon_class()
            for data in beacon.run():
                self.send_to_graphite(
                    data['graphite_namespace'],
                    data['value']
                )


if __name__ == "__main__":
    handler = BeaconHandler()
    handler.register(cpu.CPU)
    handler.register(memory.Memory)
    handler.run()
