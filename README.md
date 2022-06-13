# Kubernetes Leader Election Asyncio

The package is a copy-paste of the leader election code from the [Official Python client library for kubernetes](https://github.com/kubernetes-client/python) to make it compatible with it's [not so official asyncio counterpart](https://github.com/tomplus/kubernetes_asyncio).

It has been updated to support only Python 3.7+ (since that is required for async).
It also has had typing liberally applied for your convenience. 🧂

This is for demonstration purposes only.

Please check out `leaderelection/example.py`.

See `manifest/example.yaml` for a kick-start getting the example running in-cluster.
