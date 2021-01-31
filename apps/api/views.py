from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse

from apps.drones.models import Competition, Drone, DroneCategory, Pilot
from .serializers import (
    DroneSerializer,
    DroneCategorySerializer,
    PilotCompetitionSerializer,
    PilotSerializer,
    CompetitionSerializer,
)
from .custompermissions import IsCurrentUserOwnerOrReadOnly
from .filters import CompetitionFilter


class DroneCategoryListView(generics.ListCreateAPIView):
    serializer_class = DroneCategorySerializer
    queryset = DroneCategory.objects.all()
    filterset_fields = ("name",)
    search_fields = ("^name",)
    ordering_fields = ("name",)


class DroneCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DroneCategorySerializer
    queryset = DroneCategory.objects.all()


class DroneListView(generics.ListCreateAPIView):
    serializer_class = DroneSerializer
    queryset = Drone.objects.all()
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filterset_fields = (
        "name",
        "manufacturing_date",
        "has_it_competed",
    )
    search_fields = ("name",)
    ordering_fields = ("name", "manufacturing_date")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DroneDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DroneSerializer
    queryset = Drone.objects.all()
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsCurrentUserOwnerOrReadOnly,
    )


class PilotListView(generics.ListCreateAPIView):
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    # permission_classes = (permissions.IsAuthenticated,)


class PilotDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    # permission_classes = (permissions.IsAuthenticated,)


class CompetitionListView(generics.ListCreateAPIView):
    queryset = Competition.objects.all()
    serializer_class = PilotCompetitionSerializer
    ordering_fields = ("distance_in_feet", "distance_achievement_date")
    filter_class = CompetitionFilter


class CompetitionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Competition.objects.all()
    serializer_class = PilotCompetitionSerializer


# API root
class ApiRoot(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        return Response(
            {
                "categories": reverse("dronecategory-list", request=request),
                "drones": reverse("drone-list", request=request),
                "pilots": reverse("pilot-list", request=request),
                "competitions": reverse("competition-list", request=request),
            }
        )