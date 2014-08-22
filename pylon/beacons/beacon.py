class Beacon(object):
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
                if type(data) is dict:
                    namespace = self.join_namespaces(
                        data['graphite_namespace']
                        )
                    data['graphite_namespace'] = namespace
                    yield data

                elif type(data) is list:
                    for inner_data in data:
                        new_data = {}
                        new_data['graphite_namespace'] = str(
                            inner_data.keys()).strip('[]\''
                            )
                        new_data['value'] = str(
                            inner_data.values()
                            ).strip('[]')
                        namespace = self.join_namespaces(
                            new_data['graphite_namespace']
                            )
                        new_data['graphite_namespace'] = namespace
                        yield new_data