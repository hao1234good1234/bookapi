from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list, name='book-list'), # 配置视图对应的路由
]