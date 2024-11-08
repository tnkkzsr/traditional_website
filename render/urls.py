from django.urls import path

from . import views

urlpatterns = [
    
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("asahiyaki/", views.asahiyaki, name="asahiyaki"),
    path("asahiyaki/learn/", views.asahiyaki_learn, name="asahiyaki_learn"),
    path('asahiyaki/result/', views.evaluation_results, name='asahiyaki_result'),
    path('asahiyaki/select_front/', views.asahiyaki_select_front, name='select_front'),
    path('asahiyaki/select_front/learn/', views.asahiyaki_front_select_learn, name='front_select_learn'),
    path('asahiyaki/select_front/result/', views.asahiyaki_front_select_result, name='front_select_result'),
    path("mokkogei/", views.mokkogei, name="mokkogei"),
    path("mokkogei/learn/", views.mokkogei_learn, name="mokkogei_learn"),
    path("mokkogei/result/", views.mokkogei_result, name="mokkogei_result"),
]
