from typing import Any


class ExampleMiddlewareClass:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args: Any, **kwds: Any) -> Any:
        # print(request.META, '===========================')
        # print('came to exampleMiddleware--------------------------')
        response = self.get_response(request)
        # print(response, '------------------- response ---------------------')
        return response