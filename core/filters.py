from rest_framework import filters

class IdsFilter(filters.BaseFilterBackend):
    """
    Filter against entity
    """
    def filter_queryset(self, request, queryset, view):
        if('ids' in request.query_params.keys()):
            ids_q = request.query_params.get('ids', None)
            ids = []
            print(ids_q)
            if(ids_q is not None):
                try:
                    return queryset.filter(pk__in=[int(v) for v in ids_q.split(',')]).distinct()
                except ValueError:
                    return queryset.none()
            else:
                return queryset.none()
        else:
            return queryset
