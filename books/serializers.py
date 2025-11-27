from rest_framework import serializers
from .models import Book, Author, Tag
from django.contrib.auth.models import User

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'name')  # 隐藏字段email

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

# 定义一个叫 `BookSerializer` 的类，它继承自 `ModelSerializer`（专门用来序列化模型的）。
# 💡 为什么用 `ModelSerializer`？
# 因为它能自动根据模型生成字段，还能自动处理“保存到数据库”的逻辑，省去大量代码！
class BookSerializer(serializers.ModelSerializer):
    # === 读取时：嵌套显示 author 和 owner ===
    # 嵌套序列化器，把Author的信息也包含进来
    # ⭐️ 关键：嵌套序列化器 → 把 `Author` 的信息作为 `book.author` 返回 → `read_only=True`：前端不能修改作者
    author = AuthorSerializer(read_only=True) # read_only = True, 表示只读，不能修改
    owner = serializers.StringRelatedField(read_only=True) # 显示username
    # 输出（GET）：查询的时候需要
    # **`many=True`**表示 `Book.tags` 是一个**多对多关系**，会返回**多个标签**，所以结果是一个**列表**
    # "tags": [
    #   {"id": 1, "name": "经典"},
    #   {"id": 3, "name": "小说"}
    # ]
    # **`read_only=True`** 表示这个字段**只用于读取（GET）**，DRF 在处理 POST/PUT 请求时会**忽略它**——即使前端传了 `tags` 字段，也不会用它来创建或更新数据
    tags = TagSerializer(many=True, read_only=True)

    # === 写入时：用独立字段接收 ID ===
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        write_only=True,
        source='author'      # 关键：把 author_id 的值赋给 book.author
    )

    owner_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        required=False,   # owner 可选（因为模型里 null=True）
        source='owner'
    )

    # 嵌套：多对多
    # | 参数                         | 作用                         |
    # | ---------------------------- | ---------------------------- |
    # | `many=True`                  | 表示这是一个列表（多个标签） |
    # | `queryset=Tag.objects.all()` | 允许选择的标签范围           |
    # | `write_only=True`            | 不显示在 GET 返回中          |
    # | `required=False`             | 可以不传                     |

    # ✅ `tags` 是一个**数组**，每个元素是一个完整的 `Tag` 对象！
    # 写入时：接收 tag ID 列表
    # 输入（POST/PUT）： 新增或修改的时候需要
    # 这一行的作用是 —— **当用户 POST/PUT 一本书时，通过传 `tag_ids: [1,2]` 来关联已有标签，并自动保存到数据库**。
    # 各字段是啥意思：
    # - **`tag_ids = ...`**
    #   定义了一个**新的字段名**叫 `tag_ids`（注意不是 `tags`！），专门用于接收前端传来的**标签 ID 列表**。
    #
    # - **`PrimaryKeyRelatedField`**
    #   DRF 提供的字段类型，专门用于处理外键或多对多关系，**接收主键（ID）作为输入**。
    #
    # - **`many=True`**
    #   因为 `Book.tags` 是多对多，所以前端要传一个**ID 数组**，比如：
    #   "tag_ids": [1, 3, 5]
    #
    # - **`queryset=Tag.objects.all()`**
    #   DRF 会自动校验这些 ID 是否真实存在。
    #   ➤ 如果传了 `999`（但数据库没有 ID=999 的标签），会返回错误：`"Invalid pk \"999\" - object does not exist."`
    #
    # - **`write_only=True`**
    #   表示这个字段**只用于写入（POST/PUT）**，**不会出现在 GET 响应中**。
    #   → 所以你 GET 一本书时，**看不到 `tag_ids` 字段**。
    #
    # - **`required=False`**
    #   允许前端不传这个字段（因为你的模型中 `tags` 是 `blank=True`）。
    #
    # - **`source='tags'`** ⭐️ **最关键的一行！**
    #   告诉 DRF：虽然这个字段在 API 中叫 `tag_ids`，但它实际上对应的是模型中的 `book.tags` 字段。
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        write_only=True,
        required=False,
        source='tags' # 新增的时候会自动绑定到模型的tags字段
    )


    # ### 🔄 整体效果对比
    #
    # | 场景                 | 前端发送 / 接收 | 字段名    | 内容示例                                           |
    # | -------------------- | --------------- | --------- | -------------------------------------------------- |
    # | **创建图书（POST）** | 发送            | `tag_ids` | `[1, 3]`                                           |
    # | **获取图书（GET）**  | 接收            | `tags`    | `[{"id":1,"name":"经典"}, {"id":3,"name":"小说"}]` |



    # | 重写此方法可完全控制最终输出格式 |
    def to_representation(self, instance):
        # 获取原始数据
        data = super().to_representation(instance)
        # 自定义字段名
        data['writer'] = data.pop('author') # 把author改成writer
        data['book_title'] = data.pop('title') # 把title改成book_title
        return  data

    # 这是一个“内部类”，用来告诉 DRF：我要序列化哪个模型？哪些字段？
    class Meta:
        # 指定要序列化的模型是 `Book`。
        model = Book
        # 表示序列化 **所有字段**（id, title, author, price, published_date）。你也可以写成 `['id', 'title', 'author']` 只选部分字段。
        fields = '__all__' # 包含所有字段（含 read_only 和 write_only）

    def create(self, validated_data):
        # DRF 已自动处理 author 和 tags（因为用了 source）
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
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
        # 使用 .get() 避免 KeyError
        author = data.get('author')
        price = data.get('price')
        if author == "吴承恩" and price is not None and price > 100:
            raise serializers.ValidationError("吴承恩的书不能高于100元")
        return data

