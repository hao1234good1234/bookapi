from rest_framework.pagination import PageNumberPagination
# 自定义分页类，继承 DRF 的分页基类
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10                       # 默认每页10条
    page_size_query_param = 'page_size'  # 允许客户端通过 ?page_size=20 控制每页数量
    max_page_size = 100                 # 每页最大100条（防止滥用），防止用户设 `page_size=999999` 拖垮服务器
    page_query_param = 'p'              # 把 `?page=2` 改成 `?p=2`（更短，可选）