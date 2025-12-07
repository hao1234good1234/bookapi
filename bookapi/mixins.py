# 如果你不想每个方法都重写，可以用 **Mixin 类**。 自动注入到所有 ViewSet
from bookapi.utils import success_response
from rest_framework import status

class UnifiedResponseMixin:
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return success_response(data=response.data)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return success_response(data=response.data)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return success_response(data=response.data, message="创建成功",status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return success_response(data=response.data)

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return success_response(data=response.data, message="删除成功", status=status.HTTP_204_NO_CONTENT)