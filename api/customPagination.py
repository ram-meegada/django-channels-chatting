from django.core.paginator import Paginator
from rest_framework import status
from django.db.models import Q

class CustomPagination:
    def custom_pagination(self, request, queryset, model, serializer, search_keys):
        length = request.data.get("length")
        page = request.data.get("page_no")
        search = request.data.get("search")
        if search:
            filters = Q()
            for key in search_keys:
                filters |= Q(**{key:search})
            print(filters, '-------filters-------------')
            queryset = queryset.filter(filters)    
        paginator = Paginator(queryset, length)
        paginated_data = paginator.page(page)
        serializer = serializer(paginated_data, many=True)
        result = {
            "data": serializer.data,
            "message": "OK",
            "code": status.HTTP_200_OK,
            "page": paginated_data.number,
            "length": length
        }
        return result