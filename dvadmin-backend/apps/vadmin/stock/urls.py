from django.urls import re_path
from rest_framework.routers import DefaultRouter

from apps.vadmin.stock.views import IndexModelViewSet, IndexHistoryModelViewSet, NewFundModelViewSet

router = DefaultRouter()
router.register(r'stock', IndexModelViewSet, IndexHistoryModelViewSet)
router.register(r'stock', NewFundModelViewSet)
urlpatterns = [

    re_path('index/getIndexData', IndexModelViewSet.as_view({'get': 'get_index_data'})),
    re_path('index/getIndexList', IndexModelViewSet.as_view({'get': 'get_index_list'})),
    re_path('index/getTimePeriod', IndexHistoryModelViewSet.as_view({'post': 'get_time_period'})),
    re_path('index/getIndexHistory', IndexHistoryModelViewSet.as_view({'post': 'get_index_history'})),
    re_path('index/getNewFund', NewFundModelViewSet.as_view({'post': 'get_new_fund'})),

]
urlpatterns += router.urls
