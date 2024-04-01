from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),
    path("menu", views.menu, name="menu"),
    path("weekday/<int:day>", views.weekday, name="weekday"),
    path("delete/<int:meal>/<int:meal_id>", views.delete_product, name="delete_product")
]
