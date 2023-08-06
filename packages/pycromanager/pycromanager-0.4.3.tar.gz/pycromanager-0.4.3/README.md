<img src="docs/source/pycromanager_banner.png" width="600">

`pycromanager` is a Python library for enabling microscope acquisition control and data analysis. It works together with [Micro-manager](https://micro-manager.org/) and [Micro-magellan](https://micro-manager.org/wiki/MicroMagellan).

Check out to the [documentation](https://pycro-manager.readthedocs.io/en/latest/) for an idea of the capabilities and how to get started.

Have a cool example of something you've done with `pycromanager` or an idea for improvement? Reach out on the issues page. Contributions/ideas/examples welcome!

## Installing pycro-manager

1) Download the lastest version of [micro-manager 2.0](https://micro-manager.org/wiki/Micro-Manager_Nightly_Builds)
2) Install pycro-manager using `pip install pycromanager`
3) Run Micro-Manager, select tools-options, and check the box that says Run server on port 4827 (you only need to do this once)

To verify everything is working, run the following code: 

```
from pycromanager import Bridge

bridge = Bridge()
bridge.get_core()
```
which will give an output like:

```
Out[1]: JavaObjectShadow for : mmcorej.CMMCore
```

### Troubleshooting 

Upon creating the Bridge, you may see an error with something like:

```
UserWarning: Version mistmatch between Java ZMQ server and Python client.
Java ZMQ server version: 2.4.0
Python client expected version: 2.5.0
```

In this case case your Micro-manager version Pycro-manager versions are out of sync. The best fix is to download the latest versions of both. Uprgade to the latest Pycro-manager with: 

```
pip install pycromanager --upgrade
```
