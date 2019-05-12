from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('query/', views.query, name='query'),
    path('show/query/', views.ShowQuery, name='ShowQuery'),
    path('question/', views.question, name='question'),
    path('show/question', views.showQuestion, name='ShowQuestion'),
]
