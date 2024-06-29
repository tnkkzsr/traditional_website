from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("asahiyaki/", views.asahiyaki, name="asahiyaki"),
    path("asahiyaki/learn/", views.asahiyaki_learn, name="asahiyaki_learn"),
    path('evaluation_results/<uuid:user_uuid>/', views.evaluation_results, name='evaluation_results'),
    path('asahiyaki/select_front/', views.asahiyaki_select_front, name='select_front'),
    path('asahiyaki/select_front/learn', views.asahiyaki_front_select_learn, name='front_select_learn'),
    path("mokkogei", views.mokkogei, name="mokkogei"),
]
