from rest_framework.exceptions import APIException
from .error_codes import COVER_IMAGE_TOO_LARGE, HIGHLIGHTED_BOOK_CANNOT_BE_DELETED,BOOK_BUSINESS_ERROR,BOOK_OUT_OF_STOCK,BOOK_ALREADY_BORROWED,AUTHOR_BANNED

class BookBusinessException(APIException):
    """
    所有图书相关业务异常的基类
    """
    # - 继承 `APIException`：这是 DRF 异常的基类，会被 DRF 自动捕获
    # - `status_code`：HTTP 状态码，默认 400（客户端错误）
    # - `default_detail`：默认错误消息
    # - `default_code`：机器可读的错误码，前端可用于判断
    status_code = 400 # 默认状态码
    default_code = BOOK_BUSINESS_ERROR # 默认错误码
    default_detail = '图书业务错误'


# - 每个异常都有**明确语义**
# - 可以设置不同 `status_code`（400 表示客户端错，403 表示权限问题）
# - `default_code` 是给前端用的“错误类型标识”
class BookOutOfStockError(BookBusinessException):
    status_code = 400
    default_code = BOOK_OUT_OF_STOCK
    default_detail = '图书库存不足，无法借阅'

class BookAlreadyBorrowedError(BookBusinessException):
    status_code = 400
    default_code = BOOK_ALREADY_BORROWED
    default_detail = '该书已被借出，无法重复借阅'

class AuthorBannedError(BookBusinessException):
    status_code = 403 # 权限类错误用403
    default_code = AUTHOR_BANNED
    default_detail = '该作者已被封禁，不能发布新书'

# 禁止删除高亮图书
class HighlightedBookCannotBeDeletedError(BookBusinessException):
    status_code = 400
    default_code = HIGHLIGHTED_BOOK_CANNOT_BE_DELETED
    default_detail = '高亮图书不可删除'
# 封面图片文件过大
class CoverImageTooLargeError(BookBusinessException):
    status_code = 400
    default_code = COVER_IMAGE_TOO_LARGE
    default_detail = '封面图片不能超过5MB'