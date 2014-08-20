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
import simpledaemon

class BeaconHandler(object):
    '''
    This Class will manage all beacons, register all beacons that
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
            logging.info('Loading configuration')
            config.read(file_path + '/probe.ini')
        except Exception as err:
            logging.critical('Error reading config file')
            raise Exception('Error reading config file: %s' % err)

        logging.info('Configuration loaded correctly')
        self.server = config.get('Graphite', 'server')
        self.port = config.get('Graphite', 'port')
        self.delay = config.get('Graphite', 'delay')
        self.domain = config.get('Graphite', 'domain')
        self.initiative = config.get('Graphite', 'initiative')
        self.hostname = config.get('Graphite', 'hostname')
        if not self.hostname:
            self.hostname = socket.gethostname()

        self.loaded_beacons = config.get('Graphite', 'beacons')
        self.graphite_log = config.get('Graphite', 'logfile')
        self.logLevel = config.get('Graphite', 'loglevel')
        if not self.logLevel:
            self.logLevel = info

        self.daemonPid = config.get('Graphite', 'pidfile')

    def logger(self):
        # Logger function
        log_file = self.graphite_log
        level = self.logLevel
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
            logging.error("Couldn't connect to {} on port {}".format(
                self.server, self.port))
            logging.error(error)
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
        try:
            self.conn.sendall ('{} {} {} \n'.format(
                namespace,
                value,
                timestamp
                )
            )

            # print '{} {} {} \n'.format(
            #     namespace,
            #     value,
            #     timestamp
            #     )

        except Exception as err:
            logging.error("Error sending information to graphite: %s" % err)
            raise Exception('Error sending information to graphite: %s' % err)


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

class Nexus(simpledaemon.Daemon):
    '''
    This Class is a layer over the BeaconHandler to manage software as a daemons
    '''
    file_path = dirname(realpath(__file__))
    default_conf = file_path + '/probe.ini'
    section = 'Graphite'

    def run(self):
        handler = BeaconHandler()
        while True:
            handler.beacon_loader(handler.loaded_beacons)
            handler.run()
            time.sleep(int(handler.delay))

        handler.close_conn()

if __name__ == "__main__":
    Nexus().main()
    
