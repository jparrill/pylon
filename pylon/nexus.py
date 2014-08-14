import ConfigParser
import sys
import logging
import time
import os
from os.path import realpath
from os.path import dirname
import socket
from importlib import import_module
from beacons import beacon

class BeaconHandler(object):
    '''
    This Class will manage all beacons as a manager, register all beacons that
    it is in config file and call all of them in a row.
    (not async operations yet)
    '''
    graphite_namespace = None
    beacons = {}

    def __init__(self):
        self.get_config()
        self.logger()
        self.conn = self.setup_graphite()

    def get_config(self):
        # Configuration catcher
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
        self.loaded_beacons = config.get('Graphite', 'beacons')

    def logger(self):
        # Logger function
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
        # Register a Beacon, like a plugin activation
        class_name = new_beacon().__class__
        if class_name not in self.beacons:
            if isinstance(new_beacon(), beacon.Beacon):
                self.beacons[class_name] = new_beacon

    def setup_graphite(self):
        # Connect with graphite server
        try:
            sock = socket.socket()
            sock.connect((self.server, int(self.port)))
        except Exception as error:
            print "Couldn't connect to {} on port {}".format(
                self.server, self.port)
            print error
            sys.exit(1)

        return sock

    def beacon_loader(self, modules):
        # Dinamyc load of beacons
        for module in modules.split(","):
            mod = import_module('beacons.{}'.format(module.strip()))
            self.register(mod.Service)

    def send_to_graphite(self, namespace, value, timestamp):
        # Log all data catched and send to graphite
        logging.debug(u'{} {} {}'.format(
            namespace, 
            value,
            timestamp,
            )
        )
        
        # print u'{} {} {}'.format(
        #     namespace, 
        #     value,
        #     timestamp,
        #     )
        self.conn.sendall ('{} {} {} \n'.format(
            namespace,
            value,
            timestamp
            )
        )



    def run(self):
        # Get data from beacon to notify it to graphite
        for beacon_name,beacon_class in self.beacons.iteritems():
            beacon = beacon_class()
            for data in beacon.run():
                timestamp = int(time.time())
                path = u'{}.{}.{}.{}'.format(
                    self.domain,
                    self.initiative,
                    self.hostname,
                    data['graphite_namespace']
                    )
                self.send_to_graphite(
                    path,
                    data['value'],
                    timestamp,
                )

    def close_conn(self):
        self.conn.close()


if __name__ == "__main__":
    handler = BeaconHandler()
    handler.beacon_loader(handler.loaded_beacons)
    handler.run()
    handler.close_conn()
