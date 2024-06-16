from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("asahiyaki/", views.asahiyaki, name="asahiyaki"),
    path("asahiyaki/learn/", views.asahiyaki_learn, name="asahiyaki_learn"),
    path('evaluation_results/<uuid:user_uuid>/', views.evaluation_results, name='evaluation_results'),

    path("mokkogei", views.mokkogei, name="mokkogei"),
]
