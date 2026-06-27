from django.urls import path
from . import views
from .views import InternalFreelancerListView

urlpatterns = [
    path("freelancer/add/", views.freelancer_profile_add),
    path("freelancer/update/", views.freelancer_profile_update),
    path("freelancer/view/", views.freelancer_profile_view),
    path("freelancer/delete/", views.freelancer_profile_delete),
path(
    "internal/freelancers/<int:user_id>/rating/",
    views.update_freelancer_rating,
    name="update-freelancer-rating"
),
    path(
        "internal/freelancers/",
        InternalFreelancerListView.as_view()
    ),
]
