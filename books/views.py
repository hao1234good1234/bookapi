from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer
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
