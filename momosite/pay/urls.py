from django.urls import path
from . import views

urlpatterns = [
    path('', views.selectType, name='selectType'),
    path('czsow/', views.czStuOrWater, name='czsow'),
    path('czem/', views.czElec, name='czem'),
    path('solve/', views.solve, name='solve'),
    path('get/', views.get, name='get'),
    path('test/', views.test, name='test'),
]
