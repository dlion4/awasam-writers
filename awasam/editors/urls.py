from django.urls import path


from . import views

app_name = "editors"

urlpatterns = [
    path("", view=views.editor_home_view, name="home"),
]
