# Locust Plugin to provide FAIL/PASS status for entire test run

## Links

* Locust Website: <a href="https://locust.io">locust.io</a>

## Description

This locust plugin extends Locust with the concept of test run PASS/FAIL

## Features

**Utility function to set result**

In your locustfile.py::

  from locust_plugin_result import RESULT_PASS, RESULT_FAIL, set_result

  ...
    # Inside event callback
    set_result(environment.runner, RESULT_FAIL, "Failed check of ...")

See examples/result.py for details.

**Endpoint to get status**::

  http://<locust-master>/status

Returns json::

  {
    'result': None,  # Result will be None until your locustfile sets it.
    'state': 'ready',
    'worker_count': None,  # None for LocalWorker - current number of workers if running distributed 
    'user_count': 0
  }

## Authors

Lars Hupfeldt Nielsen

## License

Open source licensed under the BSD license (see _LICENSE_ file for details).
