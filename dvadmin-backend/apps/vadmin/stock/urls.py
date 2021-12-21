from django.urls import re_path
from rest_framework.routers import DefaultRouter

from apps.vadmin.stock.views import IndexModelViewSet

router = DefaultRouter()
router.register(r'stock', IndexModelViewSet)
urlpatterns = [

    re_path('stock/getIndexData', IndexModelViewSet.as_view({'get': 'get_index_data'})),
    # 导YModelViewSet.as_view({'get': 'importTemplate', 'post': 'importTemplate'})),

]
urlpatterns += router.urls
