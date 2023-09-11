from rest_framework import pagination


class SellerProductCursorPagination(pagination.CursorPagination):
    page_size = 10
    ordering = '-id'
