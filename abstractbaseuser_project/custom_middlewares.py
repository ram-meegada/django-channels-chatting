from datetime import datetime


class CustomHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = datetime.now()
        response = self.get_response(request)
        end_time = datetime.now()
        elapsed_time = end_time-start_time
        response["time taken"] = str(elapsed_time)
        print(response["time taken"], '-----------response-----------------------')
        return response