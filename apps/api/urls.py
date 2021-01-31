from django.urls import path

from . import views

urlpatterns = [
    path("", views.ApiRoot.as_view(), name="api-root"),
    path("drones/", views.DroneListView.as_view(), name="drone-list"),
    path("drones/<uuid:pk>/", views.DroneDetailView.as_view(), name="drone-detail"),
    path(
        "categories/",
        views.DroneCategoryListView.as_view(),
        name="dronecategory-list",
    ),
    path(
        "categories/<uuid:pk>/",
        views.DroneCategoryDetailView.as_view(),
        name="dronecategory-detail",
    ),
    path("pilots/", views.PilotListView.as_view(), name="pilot-list"),
    path("pilots/<uuid:pk>/", views.PilotDetailView.as_view(), name="pilot-detail"),
    path("competitions/", views.CompetitionListView.as_view(), name="competition-list"),
    path(
        "competitions/<uuid:pk>/",
        views.CompetitionDetailView.as_view(),
        name="competition-detail",
    ),
]
