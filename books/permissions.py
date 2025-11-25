from rest_framework import permissions


# → 表示这个类**继承自 DRF 提供的基类 `BasePermission`**。
# → 所有自定义权限类都必须继承这个基类，否则 DRF 不认识它！
class IsOwnerOrReadonly(permissions.BasePermission):
    """
    自定义权限：允许所有人读取图书，但只有创建该图书的用户（owner）才能修改或删除它。
    """
    # 注意：这个方法叫 `has_object_permission`，专门用于**判断对某个具体对象的操作是否允许**。
    # （还有另一个方法叫 `has_permission`，用于判断“能否访问整个视图”，我们后面会讲）
    # | 参数      | 类型                       | 含义                                                |
    # | --------- | -------------------------- | --------------------------------------------------- |
    # | `view`    | ViewSet 或 APIView 实例    | 当前正在调用的视图（比如 `BookViewSet`）            |
    # | `obj`     | 模型实例（如 `Book` 对象） | **当前要操作的具体数据对象**（比如 id=5 的那本书）  |
    def has_object_permission(self, request, view, obj):
        # 如果是 GET、HEAD、OPTIONS 请求，允许所有人读取
        # `permissions.SAFE_METHODS` 这是 DRF 预定义的一个元组，值为： ('GET', 'HEAD', 'OPTIONS')
        # → 这些方法被认为是“只读”的，**不会改变服务器状态**。
        # → 如果是安全方法（如 GET 查看图书），**直接允许访问**，不管是不是 owner！
        if request.method in permissions.SAFE_METHODS:
            return True
        # 非安全方法（如 PUT、PATCH、DELETE）需要额外检查。只有 owner 才能修改或删除
        return obj.owner == request.user