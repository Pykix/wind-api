from rest_framework.pagination import PageNumberPagination


class WindReadingFromAnemometerPagination(PageNumberPagination):
    page_size = 3


class AllWindReadingPagination(PageNumberPagination):
    page_size = 50
