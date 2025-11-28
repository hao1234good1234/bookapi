from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging
from books.error_codes import INTERNAL_SERVER_ERROR,BAD_REQUEST,UNAUTHORIZED,NOT_FOUND,TOO_MANY_REQUESTS,FORBIDDEN,METHOD_NOT_ALLOWED
from books.exceptions import BookBusinessException


# - `exception_handler`：DRF 提供的默认异常处理函数，我们可以在此基础上扩展
# - `Response`：用于构造返回的 JSON 响应
# - `status`：HTTP 状态码常量
# - `logging`：记录错误日志，方便排查问题

# 获取日志记录器
logger = logging.getLogger(__name__)

# def custom_exception_handler(exc, context):
#     # 调用 DRF 默认的异常处理逻辑
#     # `response = exception_handler(exc, context)`：
#     # - 先让 DRF 自己处理一遍，获取原始响应
#     # - 如果能处理（如 400、404），`response` 就有值；否则为 `None`
#     response = exception_handler(exc, context)
#
#     # 如果DRF能处理这个异常（比如：ValidationError，response不为none
#     if response is not None:
#         # 构造统一的错误响应格式
#         custom_response_data = {
#             "success": False,
#             "error_code": get_error_code_from_status(response.status_code), # 比如：BAD_REQUEST
#             # response.data.get('detail', '请求失败')`：
#             # - 大多数 DRF 异常会返回 `{"detail": "..."}`，我们提取它作为 message
#             "message": response.data.get('detail', '请求失败'),
#             # `isinstance(response.data, dict)`：
#             # - 验证错误通常是字段级的字典（如 `{"title": [...]}`），直接当作 `details`
#             'details': response.data if isinstance(response.data, dict) else {}
#         }
#         return Response(custom_response_data, status=response.status_code)
#     else:
#         # 如果DRF不能处理这个异常（比如：服务器内部异常），手动处理
#         # `logger.error(...)`： 记录未捕获的异常（如数据库连接失败），方便开发调试
#         logger.error(f"Unhandled exception: {exc}", exc_info=True)
#         custom_response_data = {
#             'success': False,
#             'error_code': 'INTERNAL_SERVER_ERROR',
#             'message': '服务器内部错误，请稍后重试',
#             'details': {}
#         }
#         return Response(custom_response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#
# def custom_exception_handler(exc, context):
#     # 调用 DRF 默认的异常处理逻辑
#     # `response = exception_handler(exc, context)`：
#     # - 先让 DRF 自己处理一遍，获取原始响应
#     # - 如果能处理（如 400、404），`response` 就有值；否则为 `None`
#     response = exception_handler(exc, context)
#
#     # 如果DRF能处理这个异常（比如：ValidationError，response不为none
#     if response is not None:
#         # 判断是否是验证错误（字段级错误）
#         if isinstance(response.data, dict) and any(
#             key != 'detail' for key in response.data.keys()
#         ):
#             # 是字段验证错误
#             message = "提交的数据有误"
#             details = response.data
#             error_code = "VALIDATION_ERROR"
#         else:
#             # 是普通错误（如404，403）
#             message = response.data.get('detail', '请求失败')
#             details = {}
#             error_code = get_error_code_from_status(response.status_code)
#         custom_response_data = {
#             'success': False,
#             'error_code': error_code,
#             'message': message,
#             'details': details
#         }
#         return Response(custom_response_data, status=response.status_code)
#     else:
#         # 如果DRF不能处理这个异常（比如：服务器内部异常），手动处理
#         # `logger.error(...)`： 记录未捕获的异常（如数据库连接失败），方便开发调试
#         logger.error(f"Unhandled exception: {exc}", exc_info=True)
#         custom_response_data = {
#             'success': False,
#             'error_code': 'INTERNAL_SERVER_ERROR',
#             'message': '服务器内部错误，请稍后重试',
#             'details': {}
#         }
#         return Response(custom_response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



def custom_exception_handler(exc, context):
    # 调用 DRF 默认的异常处理逻辑
    # `response = exception_handler(exc, context)`：
    # - 先让 DRF 自己处理一遍，获取原始响应
    # - 如果能处理（如 400、404），`response` 就有值；否则为 `None`
    response = exception_handler(exc, context)

    # 如果DRF能处理这个异常（比如：ValidationError，response不为none
    if response is not None:
        # 判断是否是 APIException （包括自定义的）
        # `hasattr(exc, 'default_code')`：判断是否是我们定义的 `APIException` 子类
        if isinstance(exc, APIException):
            error_code = exc.default_code
            # `str(exc.detail)`：获取异常的完整消息（支持多语言）
            message = str(exc.detail)  # 获取异常的详细信息
        else:
            error_code = get_error_code_from_status(response.status_code)
            message = response.data.get('detail', '请求失败')
        # 构造details：如果是字段验证错误，保留原始数据
        details = {}
        # 保留 `details` 用于字段级错误（不影响业务异常）
        if isinstance(response.data, dict) and 'detail' not in response.data:
            details = response.data

        custom_response_data = {
            'success': False,
            'error_code': error_code,
            'message': message,
            'details': details
        }
        return Response(custom_response_data, status=response.status_code)
    else:
        # 如果DRF不能处理这个异常（比如：服务器内部异常），手动处理
        # `logger.error(...)`： 记录未捕获的异常（如数据库连接失败），方便开发调试
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        custom_response_data = {
            'success': False,
            'error_code': INTERNAL_SERVER_ERROR,
            'message': '服务器内部错误，请稍后重试',
            'details': {}
        }
        return Response(custom_response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# 辅助函数，把状态码转成语义化错误码
# - 方便前端做 switch 判断（比如 `if (error_code === 'VALIDATION_ERROR')`）
def get_error_code_from_status(status_code):
    error_codes = {
        400: BAD_REQUEST,
        401: UNAUTHORIZED,
        403: FORBIDDEN,
        404: NOT_FOUND,
        405: METHOD_NOT_ALLOWED,
        429: TOO_MANY_REQUESTS,
        500: INTERNAL_SERVER_ERROR,
    }
    return error_codes.get(status_code, 'UNKNOWN_ERROR')