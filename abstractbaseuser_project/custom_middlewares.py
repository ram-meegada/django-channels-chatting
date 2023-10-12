


class CustomHeaderMiddleware:
    def __init__(self, get_response):
        # print(1111111111111111111111111)
        self.get_response = get_response

    def __call__(self, request):
        # print(2222222222222222222222)
        response = self.get_response(request)
        # print(33333333333333333)
        
        # print(response, type(response), '----------------response-----------------')
        return response