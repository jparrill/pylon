class Beacon(object):
    name = ""
    graphite_namespace = ''
    expose = []

    def join_namespaces(self, namespace):
        return u'{}.{}'.format(
            self.graphite_namespace,
            namespace
        )

    def run(self):
        for service in self.expose:
            method = getattr(self, 'expose_{}'.format(service), None)
            if method:  # Handle unexistant method!
                data = method()
                namespace = self.join_namespaces(data['graphite_namespace'])
                data['graphite_namespace'] = namespace
                yield data