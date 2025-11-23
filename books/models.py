from django.db import models

# Create your models here.
# 定义一个叫 `Book` 的类，它继承自 `models.Model` → 表示这是一个数据库表。
class Book(models.Model):
    #`CharField` 表示“字符串字段”，`max_length=100` 表示最多100个字符。
    title = models.CharField(max_length=100, verbose_name="书名") # 书名 最多100个字
    author = models.CharField(max_length=50, verbose_name="作者") # 作者 最多50个字
    # `DecimalField` 是精确小数，适合钱。`max_digits=6` 表示总共最多6位数（比如 9999.99），`decimal_places=2` 表示小数点后2位。
    # `DecimalField`，但它只做 **数据类型检查**（比如是否是数字），不会阻止负数。
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="价格") # 价格 最多6位数字，其中2位是小数 比如：99.99
    # `DateField` 表示“日期”，格式是 `YYYY-MM-DD`。
    published_date = models.DateField(verbose_name="出版日期")  # 出版日期 比如：2024-02-03

    is_highlighted = models.BooleanField(default=False, verbose_name="是否高亮")


    # 这是一个“魔法方法”，当你在 Django 后台或打印对象时，会显示书名而不是 `<Book object>`。
    def __str__(self):
        return self.title # 在后台显示书名，而不是“Book object”

