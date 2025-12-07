from rest_framework.response import Response

# 创建统一的成功响应函数
# 🔍 说明：
#
# - `data`：可以是字典、列表、None
# - `error_code`：成功时设为 `null`（JSON 中为 `null`）
# - `message`：可自定义，如“创建成功”、“删除成功”
# - 返回 `Response` 对象，可直接在 view 中 return
def success_response(data=None, message='操作成功', status=200):
    """
    统一的成功响应格式
    :param data: 返回的数据（如列表、对象）
    :param message: 提示信息
    :param status: HTTP 状态码
    :return: Response对象
    """
    return Response({
        'success': True,
        'error_code': None,
        'message': message,
        'data': data if data is not None else {}
    }, status=status)
# 创建统一的错误响应函数
# - `details` 可以是字典（如 `{"title": [...]}`）
# - `error_code` 使用你定义的常量（如 `VALIDATION_ERROR`）
def error_response(error_code, message, details=None, status=400):
    """
    统一的错误响应格式
    :param error_code: 错误码（如 VALIDATION_ERROR）
    :param message: 用户提示信息
    :param details: 字段级错误详情（如 serializer.errors）
    :param status: HTTP 状态码
    :return: Response 对象
    """
    return Response({
        'success': False,
        'error_code': error_code,
        'message': message,
        'details': details or {}
    }, status=status)
