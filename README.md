Pylon
=====
Pylon is a moduled collector of system metrics and all that you want to measure, using Graphite as a Backend

## Why?
Because I need an easy way to add some kind of information about all my nodes, starting with the system metrics, but here is the point...you can make your beacon to add any measure that you want...check logs, inodes of the system...is up you.

And you can make the Graphite tree as you want, following an structure that you will be able to show in Graphite.

## How it works
You only must to configure the file probe.ini to specify the graphite server and beacons that you will to load...and execute nexus.py

A simpleDaemon has been implemented but there are much work to do yet...
```sh
python nexus.py --start
python nexus.py --stop
```

The name of beacon that you will to load, must be the filename

## Make your own Beacon
Make a .py file inside of a beacons folder and create the Class "Service" inheriting from Beacon Class:

```python
from .beacon import Beacon

class Service(Beacon):
    graphite_namespace = "<NAME OF MEASURE>"
    expose = ["function_1_exposed", "function_2_exposed"]

    def expose_function_1_exposed(self):
        ...
        ...
        ...

    def expose_function_2_exposed(self):
        ...
        ...
        ...
```
You must to expose only the functions that you want to see, if you are making a new beacon function, it is not neccesary to not push to repo...just not expose it.

The functions must return a dict with 2 values, the measure name and the value (EG):

```python
def expose_percent(self):
        return dict(
            graphite_namespace="percent",
            value=psutil.virtual_memory().percent
        )
```

Now add the name of your .py file to probe.ini in beacons field...thats it, execute nexus .py and see in graphite your data ;).

## To much work todo
Some features that will be available in a future:

- Daemon mode
- Grouped metrics
- More beacons
- ...and much more

## Why this name?
Because of this [video](https://www.youtube.com/watch?v=T4Ox2t5c4As) :P.
