from django.urls import path
from rest_framework.routers import DefaultRouter

from huscy.attributes import views


router = DefaultRouter()
router.register('attributesets', views.AttributeSetViewSet, basename='attributeset')

urlpatterns = [
    path('attributeschema/', views.AttributeSchemaView.as_view(), name='attributeschema-detail'),
]

urlpatterns += router.urls
