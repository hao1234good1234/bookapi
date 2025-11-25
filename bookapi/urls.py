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
# from . import views # 导入当前目录的 views

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

]
