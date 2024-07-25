from rest_framework.pagination import PageNumberPagination
from constants import PAGE_SIZE


class PageNumberPaginator(PageNumberPagination):
    page_size = PAGE_SIZE  # Вынесла в константу.
    page_size_query_param = 'limit'
