from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Book, Author

# 🔍 逐行解释：
# - `TestCase`：Django 提供的测试基类，用于编写测试用例
# - `Client`：普通 HTTP 客户端（不推荐用于 DRF）
# - `reverse`：根据 URL 名称生成 URL 路径（避免硬编码）
# - `User`：Django 用户模型，用于模拟登录
# - `APIClient`：DRF 提供的专用客户端，支持 JSON、认证、权限等
# - `Book`, `Author`：你的模型，用于创建测试数据
class BookAPITest(TestCase):
    # 🔍 逐行解释：
    #
    # setUp()：每个测试方法执行前自动运行，用于初始化环境
    #
    # create_user()：创建一个普通用户，用户名和密码用于登录
    #
    # create()：直接创建数据库记录（无需保存）
    #
    # self.user、self.author、self.book：作为全局变量，在所有测试中可用
    def setUp(self):
        # 创建一个测试用户
        self.user = User.objects.create_user(
            username="lisi",
            password='xwz123456'
        )
        # 创建一个作者
        self.author = Author.objects.create(
            name='鲁迅',
            email='152525@163.com'
        )
        # 创建一本书
        self.book = Book.objects.create(
            title='呐喊',
            author=self.author,
            price=90.50,
            published_date='2023-02-02',
            is_highlighted=True,
            owner=self.user
        )
    # 测试未登录时访问接口（权限测试）
    # 🔍 逐行解释：
    #
    # - `test_list_books_unauthenticated`：测试方法名以 `test_` 开头，自动被发现
    # - `reverse('book-list')`：根据 URL 名称获取路径（如 `/api/books/`）
    #   - 必须确保你在 `urls.py` 中设置了命名空间（如 `name='book-list'`）
    # - `self.client.get(url)`：发送 GET 请求，返回 `Response` 对象
    # - `assertEqual(...)`：断言实际结果等于预期值
    # - `assertIn(...)`：断言某个键存在于字典中
    # - 最后一行：验证错误信息是否正确
    def test_list_books_unauthenticated(self):
        """测试未登录用户能否查看图书列表"""
        url = reverse('book-list') # 反向解析URL名称
        response = self.client.get(url) # 发送get请求
        self.assertEqual(response.status_code, 403) # 断言状态码为403
        self.assertIn('details', response.data) # 断言响应中有’detail‘字段
        self.assertEqual(response.data['message'], 'Authentication credentials were not provided.')
    # 测试登录后访问接口（认证测试）
    # 🔍 逐行解释：
    #
    # - `force_authenticate()`：强制让客户端模拟登录
    #   - 参数 `user=self.user` 表示使用测试用户
    #   - 这是测试中常用的方法，不需要真实输入用户名密码
    # - `response.data`：返回的 JSON 数据（已解析）
    # - `isinstance(..., list)`：断言数据是列表类型
    # - `len(...) == 1`：验证返回了我们创建的一本书
    def test_list_books_authenticated(self):
        """测试登录用户能否查看图书列表"""
        url = reverse('book-list')
        # 先登录
        self.client.force_login(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data.get('data').get('count'), 1)  # 应该返回一本书
    # 测试创建图书（业务逻辑测试）
    # 🔍 逐行解释：
    #
    # - `data`：要提交的数据，必须是字典格式
    # - `format='json'`：告诉 DRF 使用 JSON 格式发送数据
    # - `post(url, data, format='json')`：发送 POST 请求
    # - `status_code == 201`：创建成功应返回 201
    # - `assertIn('id', ...)`：新创建的对象应该有 `id`
    # - 验证标题是否正确
    def test_create_book_authenticated(self):
        """测试登录用户能否创建图书"""
        url = reverse('book-list')
        self.client.force_login(user=self.user)
        data = {
            'title': '彷徨',
            'author_id': self.author.id,
            'price': '30.50',
            'published_date': '2025-02-02',
            'is_highlighted': False,
            'owner': self.user
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.data.get("data"))
        self.assertEqual(response.data.get("data").get('book_title'), '彷徨')

    # 测试自定义业务异常（高亮图书不可删除）
    # 🔍 逐行解释：
    #
    # - `reverse('book-detail', args=[self.book.id])`：反向解析单个图书的 URL
    # - `is_highlighted = True`：修改状态，触发业务规则
    # - `delete(url)`：发送 DELETE 请求
    # - `status_code == 400`：业务异常返回 400
    # - `error_code`：验证是我们自定义的错误码
    # - `message`：确保有错误提示
    def test_delete_highlighted_book_forbidden(self):
        """测试高亮图书不能被删除"""
        # 先将这本书设置成高亮
        self.book.is_highlighted = True
        self.book.save()

        url = reverse('book-detail', args=[self.book.id])
        self.client.force_login(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error_code'], 'HIGHLIGHTED_BOOK_CANNOT_BE_DELETED')
        self.assertIn('message', response.data)
    # 测试验证错误（必填字段缺失）
    # 🔍 说明：
    #
    # - `title` 字段是必填的，所以会返回验证错误
    # - `response.data['title']` 是字段级错误列表
    # - 验证是否包含标准错误信息
    def test_create_book_missing_title(self):
        """测试创建图书时缺少标题"""
        url = reverse('book-list')
        self.client.force_login(user=self.user)
        data = {
            'author_id': self.author.id,
            'price': '20.5',
            'published_date': '2024-03-03'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('details', response.data)
        self.assertIn('This field is required.', response.data.get('details').get('title'))

