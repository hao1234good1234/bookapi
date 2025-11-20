from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer
# 表示这个接口支持 GET（查看列表）和 POST（添加新书）。
@api_view(['GET', 'POST'])
def book_list(request):
    if request.method == 'GET':
        # 获取所有图书
        books = Book.objects.all()
        # 序列化：把多个Book对象转化成json
        # 因为是“多个对象”，所以要加 `many=True`。
        serializer = BookSerializer(books,many=True)
        # 返回JSON数据
        # 这是序列化后的 Python 字典（或列表），DRF 会自动转成 JSON。
        return Response(serializer.data)
    elif request.method == 'POST':
        # 接收前端发来的json数据
        serializer = BookSerializer(data=request.data)
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
