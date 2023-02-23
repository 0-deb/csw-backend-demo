from rest_framework.pagination import LimitOffsetPagination


class Paginator():
    def Paginate(self, FilteredQueryset, request):
        self.pagination_class = LimitOffsetPagination
        self.PaginatedQueryset = self.paginator.paginate_queryset(FilteredQueryset, request)

        return self.paginator.get_paginated_response(self.PaginatedQueryset)