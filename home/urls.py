from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path('topjucatori/', views.topjucatori, name="topjucatori"),
    path('contuser/', views.contuser, name="contuser"),
    path('contparola/', views.contparola, name="contparola"),
    path('faq/', views.faq, name="faq"),
    path('freeaccount/', views.freeaccount, name="freeaccount"),
    path('politicacookies/', views.politicacookies, name="politicacookies"),
    path('termeniconditii/', views.termeniconditii, name="termeniconditii"),
    path('politicaconfidentialitate/', views.politicaconfidentialitate, name="politicaconfidentialitate"),
]

