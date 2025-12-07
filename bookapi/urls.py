"""
URL configuration for bookapi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views # 导入当前目录的 views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from books.views import BookViewSet, AuthorViewSet, TagViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


# 创建路由器实例
router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/hello', views.hello_api), #新增api路由
    # path('api/hello-class/', views.HelloAPIView.as_view()), # 注意这里是 as_view()

    path('api/', include('books.urls')),  # 把books的路由包含进来

    # JWT 认证路由，这两个视图是 `simplejwt` 自动提供的，无需自己写！
    # | 配置                  | 说明                                                         |
    # | --------------------- | ------------------------------------------------------------ |
    # | `TokenObtainPairView` | 用户 POST 用户名/密码，返回 `{access: "...", refresh: "..."}` |
    # | `TokenRefreshView`    | 用户 POST `refresh` token，返回新的 `access` token           |
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 登录页面
    path('login/', views.user_login, name='login'),
    # 登出页面
    path('logout/', views.user_logout, name='logout'),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'), # openapi json接口，提供 `/api/schema/` 接口，返回 JSON 格式的 OpenAPI 规范。

    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'), #swagger ui页面，提供一个图形化的 Swagger UI 页面，用户可以在线测试接口。`url_name='schema'`：指向前面定义的 `schema` 路由名，确保两个视图能正确关联。
    path('', include(router.urls)),   # ← 包含所有视图集路由

]

# | 代码                                                         | 作用                                             |
# | ------------------------------------------------------------ | ------------------------------------------------ |
# | `static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)` | 将 `/media/` 映射到 `media/` 文件夹              |
# | `if settings.DEBUG:`                                         | 仅在开发环境启用（生产环境由 Nginx/Apache 处理） |
# 配置静态文件服务（开发环境）
# 浏览器可以直接访问：http://127.0.0.1:8000/media/covers/1/cover.jpg
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)