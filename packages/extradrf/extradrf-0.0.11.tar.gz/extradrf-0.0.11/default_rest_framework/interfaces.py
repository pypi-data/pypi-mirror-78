class CreatorOwnerFilterSetInterface:
    """ CreatorOwnerFilterSetInterface """

    def creator_filter(self, queryset, name, value):
        NotImplementedError("this method must be implemented")

    def owner_filter(self, queryset, name, value):
        NotImplementedError("this method must be implemented")
