import django_filters
from .models import Book
# 按价格范围过滤，需要自定义过滤器
# URL示例：GET /api/books/?min_price=30&max_price=60
# 💡 `lookup_expr` 常见值：
# - `'gte'` → ≥
# - `'gt'` → >
# - `'lte'` → ≤
# - `'lt'` → <
# - `'icontains'` → 包含（模糊）

# `FilterSet` 是 `django-filter` 提供的基类，专门用于定义一组过滤规则。继承后，这个类就具备了“自动解析 URL 查询参数并生成数据库查询条件”的能力。
class BookFilter(django_filters.FilterSet):
    # | 部分                          | 说明                                                        |
    # | ----------------------------- | ----------------------------------------------------------- |
    # | `min_price`                   | 这是你在 URL 中使用的**查询参数名**。例如：`?min_price=30`  |
    # | `django_filters.NumberFilter` | 表示这是一个“数字类型”的过滤器（只接受数字输入）            |
    # | `field_name="price"`          | 告诉过滤器：**实际要过滤的是 `Book` 模型中的 `price` 字段** |
    # | `lookup_expr='gte'`           | 表示数据库查询操作符是 **“大于等于”（≥）**                  |
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    # | 部分                 | 说明                            |
    # | -------------------- | ------------------------------- |
    # | `max_price`          | URL 参数名，如 `?max_price=100` |
    # | `NumberFilter`       | 限定输入必须是数字              |
    # | `field_name="price"` | 依然作用于 `Book.price` 字段    |
    # | `lookup_expr='lte'`  | 表示 **“小于等于”（≤）**        |
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    # 开始定义内部配置类 `Meta`
    class Meta:
        model = Book  #指定这个 `FilterSet` 要作用于哪个 Django 模型
        fields = ['author']   #fields = ['author']   只自动加 author 过滤（`author`（自动创建，精确匹配）  ），price 用手动字段控制