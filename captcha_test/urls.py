from django.urls import path

# from captcha1 import views
# from captcha2 import views
from . import views


urlpatterns = [
    path("", views.intro, name="intro"),
    path("OneMore", views.submit, name="submit"),
    path("captcha", views.captcha, name="captcha"),
    path("captcha1", views.captcha1, name="captcha1"),
    path("captcha2", views.captcha2, name="captcha2"),
    path("captcha3", views.captcha3, name="captcha3"),
    path("captcha4", views.captcha4, name="captcha4"),
    path("captcha5", views.captcha5, name="captcha5"),
    path("captcha6", views.captcha6, name="captcha6"),
    path("captcha7", views.captcha7, name="captcha7"),
    path("captcha8", views.captcha8, name="captcha8"),
    path("captcha9", views.captcha9, name="captcha9"),
    path("captcha10", views.captcha10, name="captcha10"),
    path("captcha11", views.captcha11, name="captcha11"),
    path("captcha12", views.captcha12, name="captcha12"),
]
