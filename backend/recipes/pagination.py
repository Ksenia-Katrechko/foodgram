from rest_framework.pagination import PageNumberPagination

PAGE_SIZE = 6


class PageNumberPaginator(PageNumberPagination):
    page_size = PAGE_SIZE  # Вынесла в константу.
    page_size_query_param = 'limit'
