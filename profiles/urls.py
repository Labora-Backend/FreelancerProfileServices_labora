from django.urls import path
from . import views


urlpatterns = [
    path("profile/add/", views.freelancer_profile_add),
    path("profile/update/", views.freelancer_profile_update),
    path("profile/view/", views.freelancer_profile_view),
    path("profile/delete/", views.freelancer_profile_delete),
]
