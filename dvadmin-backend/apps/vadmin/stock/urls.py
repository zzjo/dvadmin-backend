from django.urls import re_path
from rest_framework.routers import DefaultRouter

from apps.vadmin.stock.views import IndexModelViewSet, IndexHistoryModelViewSet

router = DefaultRouter()
router.register(r'stock', IndexModelViewSet, IndexHistoryModelViewSet)
urlpatterns = [

    re_path('index/getIndexData', IndexModelViewSet.as_view({'get': 'get_index_data'})),
    re_path('index/getIndexList', IndexModelViewSet.as_view({'get': 'get_index_list'})),
    re_path('index/getTimePeriod', IndexHistoryModelViewSet.as_view({'post': 'get_time_period'})),


]
urlpatterns += router.urls
