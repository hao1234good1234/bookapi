from rest_framework.throttling import UserRateThrottle
from django.contrib.auth.models import User

class AdminUserThrottle(UserRateThrottle):
    """
      统一处理三种用户：
      - 匿名用户 → 'anon' 规则
      - 管理员 → 不限流
      - 普通用户 → 'user' 规则
    """

    # - `AdminUserThrottle` 使用 `scope='admin'`
    # - 所以必须在 `DEFAULT_THROTTLE_RATES` 中定义 `'admin': '...'`
    # scope = 'admin' #告诉 DRF 用哪个速率规则

    # `get_cache_key()`：决定是否记录请求次数，返回 `None` 表示 **不记录该用户的请求次数** → 不限流
    def get_cache_key(self, request, view):
        print("=== AnonRateThrottle ===")
        print("用户:", request.user)
        print("是否认证:", request.user.is_authenticated)
        # 匿名用户：交给 AnonRateThrottle 处理，这里不干预
        if not request.user.is_authenticated:
            return None
        # 管理员：不限流
        if request.user.is_staff:
            return None
        # 普通用户：走默认的 UserRateThrottle 逻辑（按 user.id 限流）
        # “调用父类的 get_cache_key() 方法，让 DRF 按照默认规则生成限流缓存键。”
        # “如果不是管理员，就按 DRF 默认的方式去限流（生成缓存键、计数、判断是否超限）。”
        return super().get_cache_key(request, view)