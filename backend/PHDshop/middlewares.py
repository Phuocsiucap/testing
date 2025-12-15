import time
from django.core.cache import cache
from django.http import JsonResponse

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        key = f"rl:{ip}"
        now = int(time.time())

        data = cache.get(key, {'count': 0, 'time': now})

        if data["time"] = now:
            data["count"] += 1
        else:
            data = {"count": 1, "time": now}
        
        if data["count"] > 20:
            return JsonResponse(
                {"detail": "Too many requests. Please try again later."},
                status=429
            )

        cache.set(key, data, timeout=2)
        return self.get_response(request)