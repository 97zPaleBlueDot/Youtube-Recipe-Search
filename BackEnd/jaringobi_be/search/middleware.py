# from .models import RequestLog
# from django.utils.deprecation import MiddlewareMixin
# import urllib.parse

# class RequestLogMiddleware(MiddlewareMixin):

#     def process_request(self, request):
#         url = urllib.parse.unquote(request.get_full_path())
#         method = request.method

#         # 로그 저장
#         RequestLog.objects.create(request_url=url, http_method=method)
