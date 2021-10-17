from django.urls import path

# from captcha1 import views
# from captcha2 import views
from . import views


urlpatterns = [
    path("intro", views.intro, name="intro"),
    path("captcha", views.captcha, name="captcha"),
    path("captcha5", views.captcha5, name="captcha5"),
    path("captcha6", views.captcha6, name="captcha6"),
    path("captcha7", views.captcha7, name="captcha7"),
    path("captcha8", views.captcha8, name="captcha8"),
    path("submit", views.submit, name="submit"),
]
