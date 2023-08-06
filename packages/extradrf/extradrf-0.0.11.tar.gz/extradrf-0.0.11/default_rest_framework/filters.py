from . import interfaces


class CreatorOwnerFilterSet(interfaces.CreatorOwnerFilterSetInterface):
    """ CreatorOwnerFilterSet 
    add custom filter for specific field after get_queryset
    """

    def creator_filter(self, queryset, name, value):
        if not value:
            # if not set creator_field in query params explicitly, return queryset
            return queryset
        filter_query_set = queryset.filter(creator__has_key=str(value))

        return filter_query_set

    def owner_filter(self, queryset, name, value):
        if not value:
            return queryset
        filter_query_set = queryset.filter(owner__has_key=str(value))

        return filter_query_set
