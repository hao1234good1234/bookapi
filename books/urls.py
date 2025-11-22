from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


# - `DefaultRouter()`：自动生成标准 RESTful 路由
# - `router.register(r'books', views.BookViewSet)`：注册后，自动创建：
#   - `GET /books/`
#   - `POST /books/`
#   - `GET /books/1/`
#   - `PUT /books/1/`
#   - `DELETE /books/1/`
#   - 还有额外的 API 文档页面！
# 创建路由器
router = DefaultRouter()
# 注册ViewSet，books-view-set是api的路由前缀，/api/books-view-set/1/
router.register(r'books-view-set', viewset=views.BookViewSet)



urlpatterns = [
    # FBV 函数视图
    path('books-fbv/', views.book_list, name='book-list-fbv'),
    # CBV 类视图
    path('books-cbv/', views.BookList.as_view(), name='book-list-cbv'),
    path('books-generic/', views.BookListCreate.as_view(), name='book-list-generic'),
    path('books/<int:pk>/', views.BookDetail.as_view(), name='book-detail'), #💡 `<int:pk>`：Django 的路径转换器，表示“这里是一个整数，变量名叫 pk”
    path('', include(router.urls)), # 包含所有自动生成的路由，包含：get获取全部图书，post添加图书，get/put/delete/patch单个图书获取或修改


]