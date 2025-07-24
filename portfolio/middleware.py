from django.conf import settings
from django.http import HttpResponseForbidden

class AdminIPRestrictionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.admin_url_path = f'/{settings.ADMIN_URL}'
        self.allowed_ips = settings.ALLOWED_ADMIN_IPS

    def __call__(self, request):
        # request.path가 /my-secret-admin-page/ 로 시작하는지 확인
        if request.path.startswith(self.admin_url_path):
            # 사용자의 실제 IP 주소를 가져옴
            # X-Forwarded-For 헤더가 있으면 프록시를 통과한 실제 IP를 사용하고, 없으면 직접 접속한 IP를 사용
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            
            # 허용된 IP 목록에 사용자의 IP가 없으면 접근 거부
            if ip not in self.allowed_ips:
                return HttpResponseForbidden("Forbidden: You do not have permission to access this page.")

        response = self.get_response(request)
        return response 