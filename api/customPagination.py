from django.core.paginator import Paginator
from rest_framework import status
from django.db.models import Q

class CustomPagination:
    def custom_pagination(self, request, model, search_keys, search_type, serializer, queryset):
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
            "response_object": serializer.data,
            "message": "OK",
            "code": status.HTTP_200_OK,
            "total_records": paginated_data.paginator.count,
            "length": length
        }
        return result
    

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger    
class CustomPaginationMobileView:

    def custom_pagination_mobile_view(self, request, model, search_keys, search_type, serializer, query, user=None):
        """
        Function to handle custom pagination for mobile view
        """

        length = request.data['length']

        start = request.data['start']

        page_no = int(int(start)/int(length) + 1)

        paginator = Paginator(query, length)


        try:
            paginated_data = paginator.page(page_no)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            paginated_data = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            return {"response_object": None, "total_records": 0}    


        serializer = serializer(paginated_data, context={'user': user}, many=True)

        return {"response_object": serializer.data, "total_records": paginated_data.paginator.count}    