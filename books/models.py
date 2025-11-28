from django.db import models
from django.contrib.auth.models import User
# | 代码                                               | 解释                         |
# | -------------------------------------------------- | ---------------------------- |
# | `class Author(models.Model):`                      | 定义一个叫 `Author` 的模型   |
# | `name = models.CharField(max_length=100)`          | 作者姓名，最多100字符        |
# | `email = models.EmailField(blank=True, null=True)` | 邮箱字段，可为空             |
# | `def __str__(self): return self.name`              | 打印对象时显示名字，方便调试 |
class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name="姓名")
    email = models.EmailField(blank=True, null=True, verbose_name="邮箱")
    def __str__(self):
        return self.name
# 新增标签模型，一本书可以有多个标签，一个标签可以属于多本书，这就是典型的多对多关系
# | 标签模型，比如 “小说”、“科幻”、“经典” |
class Tag(models.Model):
    # unique=True：确保标签名字唯一，不能重复
    name = models.CharField(max_length=50, unique=True, verbose_name="标签名字")
    def __str__(self):
        return self.name


# Create your models here.
# 定义一个叫 `Book` 的类，它继承自 `models.Model` → 表示这是一个数据库表。
class Book(models.Model):
    #`CharField` 表示“字符串字段”，`max_length=100` 表示最多100个字符。
    title = models.CharField(max_length=100, verbose_name="书名") # 书名 最多100个字
    # author = models.CharField(max_length=50, verbose_name="作者") # 作者 最多50个字

    # 外键：一本书属于一个作者 → `on_delete=models.CASCADE`：如果作者被删，这本书也删
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="作者")

    # 多对多关系：一本书可以有多个标签，blank=True：允许不填标签
    # 💡 Django 会自动创建中间表 `books_book_tags` 来存储关系。
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="标签")

    # `DecimalField` 是精确小数，适合钱。`max_digits=6` 表示总共最多6位数（比如 9999.99），`decimal_places=2` 表示小数点后2位。
    # `DecimalField`，但它只做 **数据类型检查**（比如是否是数字），不会阻止负数。
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="价格") # 价格 最多6位数字，其中2位是小数 比如：99.99
    # `DateField` 表示“日期”，格式是 `YYYY-MM-DD`。
    published_date = models.DateField(verbose_name="出版日期")  # 出版日期 比如：2024-02-03

    is_highlighted = models.BooleanField(default=False, verbose_name="是否高亮")

    # | 部分                | 含义                                 |
    # | ------------------- | ------------------------------------ |
    # | `owner`             | 字段名，代表“这本书的拥有者”         |
    # | `ForeignKey(User)`  | 关联到 Django 的用户模型             |
    # | `on_delete=CASCADE` | 用户删除时，自动删除其所有图书       |
    # | `null=True`         | 允许数据库中该字段为空（兼容旧数据） |
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name="拥有者")
    # | 代码                      | 解释                                                         |
    # | ------------------------- | ------------------------------------------------------------ |
    # | `models.ImageField(...)`  | 专门用于上传图片的字段类型，继承自 `FileField`               |
    # | `upload_to='covers/'`     | 指定上传文件存储的**子目录**，比如：`media/covers/1/cover.jpg` |
    # | `blank=True`              | 表单中可以不填（前端可选）                                   |
    # | `null=True`               | 数据库中允许为 `NULL`（不是空字符串）                        |
    # | `verbose_name="封面图片"` | 管理后台显示的名字                                           |
    # 新增图片字段
    # 💡 `ImageField` 会自动验证上传的是不是图片（jpg/png/gif），而 `FileField` 只检查是不是文件。
    cover_image = models.ImageField(
        upload_to='covers/', # 文件上传路径
        blank=True,         # 允许为空
        null=True,          # 数据库允许为空
        verbose_name='封面图片'
    )
    # 这是一个“魔法方法”，当你在 Django 后台或打印对象时，会显示书名而不是 `<Book object>`。
    def __str__(self):
        return self.title # 在后台显示书名，而不是“Book object”




