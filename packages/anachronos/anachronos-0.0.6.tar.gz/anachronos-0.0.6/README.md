# Anachronos
A testing framework for testing frameworks.

Anachronos is an end-to-end testing framework usable with a wide variety of applications.
To get started, define an `ApplicationRunner` which can be used to start your application. 
Then, write your test classes by inheriting from `anachronos.TestCase`. 

## How it works
The framework provides access to a special `Anachronos` object which is accessible both from the tested application, and from the testing suite.
This object effectively acts as a logger on which assertions can be run afterwards. Anachronos assertions are accessible by using the `self.assertThat` method from within a TestCase.
Below is a simple TestCase example taken from the Jivago framework.

```python
import anachronos
from e2e_test.runner import http
from e2e_test.testing_messages import SIMPLE_GET


class SimpleResourceTest(anachronos.TestCase):

    def test_simple_get(self):
        http.get("/")

        self.assertThat(SIMPLE_GET).is_stored()

    def test_post_dto(self):
        response = http.post("/", json={'name': 'Paul Atreides', 'age': 17}).json()

        self.assertEqual('Paul Atreides', response['name'])


if __name__ == '__main__':
    anachronos.run_tests()

```
With the matching application logic :

```python3
import anachronos
from e2e_test.app.components.dtos.request_dto import RequestDto
from e2e_test.app.components.dtos.response_dto import ResponseDto
from e2e_test.testing_messages import SIMPLE_GET
from jivago.lang.annotations import Inject
from jivago.wsgi.annotations import Resource
from jivago.wsgi.methods import GET, POST


@Resource("/")
class SimpleResource(object):

    def __init__(self):
        self.anachronos = anachronos.get_instance()

    @GET
    def simple_get(self) -> str:
        self.anachronos.store(SIMPLE_GET)
        return "OK"

    @POST
    def post_body(self, request: RequestDto) -> ResponseDto:
        return ResponseDto(request.name, True)

```
