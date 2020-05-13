from django.urls import path, include
from fileManage import views

urlpatterns = [
    path("verify/", views.djangoServer),
]
