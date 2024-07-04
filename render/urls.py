from django.urls import path

from . import views

urlpatterns = [
    
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("asahiyaki/", views.asahiyaki, name="asahiyaki"),
    path("asahiyaki/learn/", views.asahiyaki_learn, name="asahiyaki_learn"),
<<<<<<< HEAD
    path('asahiyaki/result/', views.asahiyaki_result, name='asahiyaki_result'),
=======
    path('evaluation_results/<uuid:user_uuid>/', views.evaluation_results, name='evaluation_results'),
>>>>>>> dev
    path('asahiyaki/select_front/', views.asahiyaki_select_front, name='select_front'),
    path('asahiyaki/select_front/learn', views.asahiyaki_front_select_learn, name='front_select_learn'),
    path("mokkogei", views.mokkogei, name="mokkogei"),
    path("mokkogei/learn", views.mokkogei_learn, name="mokkogei_learn"),
    path("mokkogei/result", views.mokkogei_result, name="mokkogei_result"),
]
