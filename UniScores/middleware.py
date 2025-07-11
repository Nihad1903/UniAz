from django.http import HttpResponsePermanentRedirect

class DomainRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()
        if host == "uniaz.onrender.com":
            return HttpResponsePermanentRedirect("https://uniaz.info" + request.get_full_path())
        return self.get_response(request)
