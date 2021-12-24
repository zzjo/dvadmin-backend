from django.urls import re_path
from rest_framework.routers import DefaultRouter

from apps.vadmin.stock.views import IndexModelViewSet

router = DefaultRouter()
router.register(r'stock', IndexModelViewSet)
urlpatterns = [

    re_path('/index/getIndexData', IndexModelViewSet.as_view({'get': 'get_index_data'})),
    re_path('/index/getIndexList', IndexModelViewSet.as_view({'get': 'get_index_list'})),
    # 导YModelViewSet.as_view({'get': 'importTemplate', 'post': 'importTemplate'})),

]
urlpatterns += router.urls
