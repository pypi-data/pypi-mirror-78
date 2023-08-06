# Vidispine Python

Official Vidispine API client for Python projects.

- API version: 5.x
- Package version: 5.0.4
- Build package: org.openapitools.codegen.languages.PythonClientCodegen

For more information, please visit [http://support.vidispine.com/](http://support.vidispine.com/)

## Requirements

Python 2.7 and 3.4+

## Installation
### Via source

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

## Usage

Then import the package:
```python
import vidispine
```

## Getting Started

Please follow the [installation procedure](#installation) and then consider the following example:

### Getting vidispine server version information

```python
from __future__ import print_function
import vidispine
from vidispine.rest import ApiException
from pprint import pprint

configuration = vidispine.Configuration()
# Configure HTTP basic auth
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# Create an instance of the API class
system_api = vidispine.SystemApi(vidispine.ApiClient(configuration))

try:
    # Get version info
    api_response = system_api.get_version()
    pprint(api_response)
except ApiException as e:
    print("Exception when getting version info: %s\n" % e)
```

## Streaming and IO

When reading files, prefer to stream the response over handling it in memory.
Set the `_preload_content` parameter to `False` to stream the response:

```python
file_api = vidispine.FileApi(vidispine.ApiClient(configuration))
r = file_api.get_file_data("VX-364", _preload_content=False)
for chunk in r.stream(32):
    print(chunk)
r.release_conn()
```

See the [urllib3 documentation](https://urllib3.readthedocs.io/en/latest/advanced-usage.html#stream) for more information.

## Documentation

Please have a look at the documentation in the [`docs` directory](docs/).

## Testing

To run the provided testsuite run:

```sh
python setup.py test
```