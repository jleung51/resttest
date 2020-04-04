# resttest

Python 3 framework which provides a configured class for REST API testing.

_resttest_ combines the `unittest` and `requests` modules to create adapted functionality for tests created as REST API tests.

## Setup

If Python 3 is not yet installed, then install Python and pip:
```shell
sudo apt-get install python3 python3-pip
```

Install the required dependencies:
```shell
pip3 install -r requirements.txt
```

Or, copy the contents of `requirements.txt` into the same file in your own project, and do the same.

Copy the `resttest.py` module into your application.

In the source file where you plan to write unit tests, import the `ApiTest` class:
```python
from resttest import ApiTest
```

## Usage

Create a new subclass of the `ApiTest` class, which itself is a subclass of the unittest class.

Use this as you would any other `unittest` subclass. Make sure to use the provided `ApiTest` helper methods to send HTTP requests and assert response information, along with the usual Python `unittest` methods if you require.

### Example

```python
class LocationApis(ApiTest):
    url = 'http://localhost:8080/'
    headers = {'Content-Type': 'application/json'}

    def test_get(self):
        # Send the request
        resp = self.send_request(self.url, headers=self.headers)

        # Check if the response code is the expected value
        self.assert_resp_code(resp, requests.codes.ok)

        # Check if the JSON response body contains the following fields
        # as strings:
        #
        #     app.name
        #     author
        #
        self.get_resp_body_str(resp, 'app', 'name)
        self.get_resp_body_str(resp, 'author')
```

For a lengthier example, check out `example.py`.