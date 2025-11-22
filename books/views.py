from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet


# 这个是函数视图（Function-based Views (FBV) ），函数视图用@api_view()
# **优点**：简单直观，适合小功能
# **缺点**：每个方法都要写 `if-elif`，代码冗长

# 表示这个接口支持 GET（查看列表）和 POST（添加新书）。
# 必须加装饰器才能用 DRF 的 request/response
@api_view(['GET', 'POST'])
def book_list(request):
    # ====== 打印请求信息（调试用）======
    print("\n" + "=" * 50)
    print("当前请求的方法：", request.method)
    print("请求路径", request.path) #请求路径 /api/books/
    print("GET参数：", dict(request.GET)) # 比如：浏览器中输入的请求url带的参数format=api（http://127.0.0.1:8000/api/books/?format=api）
    print("POST/PUT 数据（request.data）：", request.data) #  {'title': '西游记', 'author': '吴承恩', 'price': '90.50', 'published_date': '1920-01-01'}
    print("=" * 50 + "\n")

    if request.method == 'GET':
        # 获取所有图书
        books = Book.objects.all()
        # 序列化：把多个Book对象转化成json
        # 因为是“多个对象”，所以要加 `many=True`。
        serializer = BookSerializer(books,many=True)
        print("【序列化】instance =", serializer.instance)  # 会打印 QuerySet
        print("【序列化】data =", serializer.data)  # 已转成列表
        # 返回JSON数据
        # 这是序列化后的 Python 字典（或列表），DRF 会自动转成 JSON。
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        # 接收前端发来的json数据
        serializer = BookSerializer(data=request.data)
        print("【反序列化】data =", serializer.initial_data)  # 原始输入数据
        print("【反序列化】instance =", serializer.instance)  # 此时是 None
        # 验证数据是否合法
        # 检查前端发来的数据是否符合规则（比如价格是不是数字、日期格式对不对）。
        if serializer.is_valid():
            # 保存到数据库
            # 自动调用 `create()` 方法，把数据存进数据库。
            serializer.save()
            # 返回成功响应（带新数据）
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # 如果验证失败，返回错误信息
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 这个是类视图（Class-based Views (CBV) —— 类视图（更优雅））
# 用类代替函数，自动处理不同 HTTP 方法
# - 方法名 = HTTP 方法小写（get, post, put, delete）
# - `self` 是类实例，可以共享属性（比如权限、分页等）
# - 比 FBV 更结构化，适合复杂逻辑

# 定义一个类，继承自 `APIView`
class BookList(APIView):
    """
    列出所有图书 或 新建图书
    """
    # 自动处理 GET 请求
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # 自动处理 POST 请求
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 这个是通用视图（Generic Views），DRF 提供了 **预制好的类**，帮你自动完成常见操作。
# | `ListAPIView`                  | 只读列表（GET）            |
# | `CreateAPIView`                | 只创建（POST）             |
# | `ListCreateAPIView`            | 列表 + 创建（GET + POST）✅ |
# | `RetrieveUpdateDestroyAPIView` | 详情 + 修改 + 删除         |

# **不需要写 get/post 方法！** DRF 自动处理
class BookListCreate(ListCreateAPIView):
    queryset = Book.objects.all()  # 数据源 告诉 DRF “从哪取数据”
    serializer_class = BookSerializer # 使用哪个序列化器 告诉 DRF “用哪个 Serializer”


# 实现单个图书详情（Retrieve/Update/Delete 获取，修改，删除）
# - `RetrieveUpdateDestroyAPIView` 自动支持 GET/PUT/DELETE
# - 默认通过 `pk`（主键）查找对象，所以 URL 要带 `<int:pk>`
class BookDetail(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # DRF 自动根据 URL 中的 pk 查找对象


# 这个是ModelViewSet
# ModelViewSet = ListCreateAPIView + RetrieveUpdateDestroyAPIView
# BookViewSet 合并了 `BookListCreate` 和 `BookDetail`
class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
