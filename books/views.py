from pickle import FALSE

from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status
from .models import Book, Author, Tag
from .serializers import BookSerializer, AuthorSerializer, TagSerializer
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from .pagination import StandardResultsSetPagination
from .filters import BookFilter
from rest_framework.permissions import IsAuthenticated # 导入“仅认证用户可访问”的权限类
from rest_framework.permissions import IsAuthenticatedOrReadOnly # 登录用户可读写，匿名用户只读
from rest_framework.permissions import IsAdminUser # 只允许管理员访问
from .permissions import IsOwnerOrReadonly
from .throttling import AdminUserThrottle




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
    print("请求路径", request.path)  # 请求路径 /api/books/
    print("GET参数：", dict(request.GET))  # 比如：浏览器中输入的请求url带的参数format=api（http://127.0.0.1:8000/api/books/?format=api）
    print("POST/PUT 数据（request.data）：",
          request.data)  # {'title': '西游记', 'author': '吴承恩', 'price': '90.50', 'published_date': '1920-01-01'}
    print("=" * 50 + "\n")

    if request.method == 'GET':
        # 获取所有图书
        books = Book.objects.all()
        # 序列化：把多个Book对象转化成json
        # 因为是“多个对象”，所以要加 `many=True`。
        serializer = BookSerializer(books, many=True)
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
    serializer_class = BookSerializer  # 使用哪个序列化器 告诉 DRF “用哪个 Serializer”


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
    # ✅ 默认情况下，`ModelViewSet` 已经支持文件上传！只要你在 `serializer_class` 中正确处理了 `FileField`，就能接收 POST 请求中的文件。
    serializer_class = BookSerializer
    pagination_class = StandardResultsSetPagination # 指定自定义分页类，如果全局设置了分页，这里会 **覆盖全局设置**！
    filterset_class = BookFilter   # 使用自定义的过滤器


    # 权限控制
    # permission_classes = [IsAuthenticated]  # 强制登录才能访问，告诉 DRF：只有登录用户才能调用这个 ViewSet 的任何操作
    # permission_classes = [IsAuthenticatedOrReadOnly] # ← 匿名可读，登录可写
    # permission_classes = [IsAdminUser] # 只允许管理员访问
    # permission_classes = [
    #     IsAuthenticated,            # 先检查是否登录
    #     IsOwnerOrReadonly,          # 再检查是否是作者
    # ]
    permission_classes = [
        IsAuthenticatedOrReadOnly,   # 未登录
        # IsOwnerOrReadonly,  # 再检查是否是作者
    ]

    # throttle_classes = [AdminUserThrottle]  # 使用自定义限流类



    # 如何在创建图书时自动设置owner
    # `perform_create` 是 DRF 提供的钩子方法，在保存对象前调用。
    def perform_create(self, serializer):
        # 自动将当前登录用户设置为owner
        serializer.save(owner=self.request.user)

    # - get_queryset这是 DRF `ModelViewSet` 的核心方法之一。
    # - 它决定了 **列表（list）和详情（retrieve）接口返回哪些数据**。
    def get_queryset(self):
        # 防御：未认证用户返回空（避免 TypeError）
        if not self.request.user.is_authenticated:
            return Book.objects.none()
        # 如果你的 `Book` 模型经常需要显示 `owner.username`，可以优化数据库查询：
        # `select_related('owner')` 会在一次 SQL 中 JOIN 用户表，避免 N+1 查询问题。
        if self.request.user.is_staff:
            return Book.objects.select_related('owner') # 减少数据库查询次数
        return Book.objects.filter(owner = self.request.user)

    # === 1. 过滤字段（支持 ?author=张三&price=39.90）===
    # **作用**：允许客户端通过 URL 参数 **精确匹配** 这两个字段
    # URL示例：`GET /api/books/?author=张三&price=39.90`
    # 底层SQL：SELECT * FROM books WHERE author = '张三' AND price = 39.90;
    # ⚠️ 注意：`price` 是字符串比较！如果传 `price=40`，但数据库是 `40.00`，可能不匹配。
    # filterset_fields = ['price', 'author']

    # === 2. 搜索字段（支持 ?search=关键词）===
    # - **作用**：启用全文搜索，使用 `?search=关键词`
    # - **匹配方式**：默认是 **“包含”**（icontains）
    # URL示例：`GET /api/books/?search=Python` → 匹配《Python入门》《高级Python》等
    # 底层SQL：WHERE title ILIKE '%Python%' OR author ILIKE '%Python%';
    # > 💡 高级用法（可选）：
    # > - `^title` → 以...开头（startswith）
    # > - `=title` → 精确匹配（exact）
    # > - `@title` → 全文搜索（需 PostgreSQL）
    search_fields = ['title', 'author']

    # === 3. 排序字段（支持 ?ordering=price 或 ?ordering=-price）===
    # **作用**：允许客户端按这些字段排序
    # URL示例：
    # - `?ordering=-price` → 降序（贵到便宜）
    # - `?ordering=published_date` → 按出版日期升序
    ordering_fields = ['price', 'published_date']
    ordering = ['id']   # 默认排序规则，如果用户没传 `ordering`，就按 `id` 升序返回

    # `@action`：添加自定义操作Router，自动识别，无需手动路由，给viewset加一个额外的操作
    # `@action(detail=False)`：表示这个操作不针对单个对象（URL 是 `/books/recent/`）
    # 方法名recent = URL 路径的一部分，→ 所以最终 URL 是 `http://127.0.0.1:8000/api/books/recent/`

    # 这个 `recent` 接口非常实用，比如做“最新上架”、“热门推荐”等。
    # **如何添加一个 `detail=True` 的自定义操作？**  （比如 `/api/books/1/highlight/` 给某本书加高亮）
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """
        返回最近添加的5本书
        """
        # 按 `id` 字段 **降序排列**（`-` 表示倒序
        # 因为 `id` 越大表示创建越晚，所以最大的 5 个就是“最近添加的”
        recent_books = Book.objects.order_by('-id')[:5]
        # #### `self.get_serializer(...)`
        # - 这是 `ModelViewSet` 提供的便捷方法
        # - 自动使用你在类中定义的 `serializer_class = BookSerializer`
        # - 比直接写 `BookSerializer(...)` 更灵活（支持动态切换）
        serializer = self.get_serializer(recent_books, many=True)
        return Response(serializer.data)


    # 最终 URL：`/api/books/1/highlight/`
    # `detail=True`表示这个操作 **针对单个对象** → URL 会包含 `/pk/`
    # `pk=None` → DRF 会自动从 URL 中提取 `pk`（比如 `1`），并传进来
    @action(detail=True, methods=['post'])
    def highlight(self, request, pk=None):
        """
        给某本书加上高亮
        URL: /api/books/<id>/highlight/
        """
        # 1. 获取当前操作的Book实例（DRF自动根据pk进行查找）
        book = self.get_object() # 自动处理404
        # 2. 修改字段
        book.is_highlighted = True
        # book.is_highlighted = not book.is_highlighted  # 切换高亮状态，适用场景：用户可能重复点击“高亮”，这样每次点一次，就在 `true` 和 `false` 之间切换！
        book.save() # 别忘了保存到数据库
        # 3. 返回更新后的数据
        serializer = self.get_serializer(book)
        return Response(serializer.data, status= status.HTTP_200_OK)

# author对应的viewset
class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer



