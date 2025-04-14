from django.urls import path

from . import views
app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("randompage", views.randompage, name="randompage"),
    path("<str:name>/edit", views.edit, name="edit"),
    path("<str:name>", views.page, name="page"),
    
]
