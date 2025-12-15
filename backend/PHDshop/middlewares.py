# middleware/rate_limit.py
import time
from django.core.cache import cache
from django.http import JsonResponse

class RateLimitMiddleware:
    RATE = 20
    WINDOW = 1  # second

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        key = f"rate:{ip}"

        data = cache.get(key, {"count": 0, "start": time.time()})

        now = time.time()
        if now - data["start"] > self.WINDOW:
            data = {"count": 1, "start": now}
        else:
            data["count"] += 1

        cache.set(key, data, timeout=2)

        if data["count"] > self.RATE:
            return JsonResponse(
                {"error": "Duy đẹp trai"},
                status=429
            )

        return self.get_response(request)