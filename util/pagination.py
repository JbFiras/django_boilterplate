from rest_framework import pagination
from rest_framework.response import Response


class PageNumberPaginationCustom(pagination.PageNumberPagination):
    """Page Number Pagination Custom Class"""

    def get_paginated_response(self, data):
        """
        Get a paginated response

        Parameters
        ----------
        data

        Returns
        -------
        Response

        """

        pagination_data = {
            "links": {
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
            },
            "page": self.page.number,
            "count": self.page.paginator.count,
            "page_size": self.page_size,
            "num_pages": self.page.paginator.num_pages,
            "results": data,
        }
        if self.page.has_next():
            pagination_data.update({"next_page": self.page.next_page_number()})
        if self.page.has_previous():
            pagination_data.update({"previous_page": self.page.previous_page_number()})

        return Response(pagination_data)
