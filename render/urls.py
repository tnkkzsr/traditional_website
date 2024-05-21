from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("asahiyaki/<uuid:uuid>", views.asahiyaki, name="asahiyaki"),
    path("mokkogei", views.mokkogei, name="mokkogei"),
]
