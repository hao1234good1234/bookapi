from django.contrib.auth.views import PasswordChangeView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView #导入APIView类视图
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect

@api_view(['GET'])
def hello_api(request):
    return Response({"message": "hello, this is your first drf api"})

class HelloAPIView(APIView):
    def get(self, request):
        return Response({"message": "hello from class-based APIView"})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/api/books/')
        else:
            messages.error(request, "用户名或密码错误")
    return render(request, ' login.html')
def user_logout(request):
    """用户登出，清除session，重定向到登录页面"""
    # `logout(request)` 会：
    # - 删除用户的 session
    # - 将 `request.user` 设为 `AnonymousUser`
    # - 安全地结束登录状态
    logout(request)
    return redirect('/login/')
