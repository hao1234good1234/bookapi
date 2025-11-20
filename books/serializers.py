from rest_framework import serializers
from .models import Book

# 定义一个叫 `BookSerializer` 的类，它继承自 `ModelSerializer`（专门用来序列化模型的）。
# 💡 为什么用 `ModelSerializer`？
# 因为它能自动根据模型生成字段，还能自动处理“保存到数据库”的逻辑，省去大量代码！
class BookSerializer(serializers.ModelSerializer):
    # 这是一个“内部类”，用来告诉 DRF：我要序列化哪个模型？哪些字段？
    class Meta:
        # 指定要序列化的模型是 `Book`。
        model = Book
        # 表示序列化 **所有字段**（id, title, author, price, published_date）。你也可以写成 `['id', 'title', 'author']` 只选部分字段。
        fields = '__all__'
    # 添加自定义校验逻辑
    # def validate_price(self, value):`
    # 这是一个“特殊方法”，DRF 会在验证时自动调用。
    # 它的作用是：检查 `price` 字段的值是否合法。
    # 字段级验证：validate_<字段名>
    def validate_price(self,value):
        if value < 0:
            raise serializers.ValidationError("价格不能是负数")
        return value

    # 对象级验证：validate()
    def validate(self, data):
        if data['author'] == "吴承恩" and data['price'] > 100:
            raise serializers.ValidationError("吴承恩的书不能高于100元")
        return data

