from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("asahiyaki/", views.asahiyaki, name="asahiyaki"),
    path("asahiyaki/learn/", views.asahiyaki_learn, name="asahiyaki_learn"),
    path("mokkogei", views.mokkogei, name="mokkogei"),
]
