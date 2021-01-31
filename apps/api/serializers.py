from rest_framework import serializers

from apps.drones.models import (
    DroneCategory,
    Drone,
    Pilot,
    Competition,
)


class DroneCategorySerializer(serializers.HyperlinkedModelSerializer):
    drones = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="drone-detail"
    )

    class Meta:
        model = DroneCategory
        fields = ("url", "pk", "name", "drones")


class DroneSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    category = serializers.SlugRelatedField(
        slug_field="name", queryset=DroneCategory.objects.all()
    )

    class Meta:
        model = Drone
        fields = (
            "url",
            "pk",
            "name",
            "category",
            "has_it_competed",
            "owner",
            "manufacturing_date",
            "created_at",
            "updated_at",
        )


class CompetitionSerializer(serializers.HyperlinkedModelSerializer):
    """
    Use to serialize competition instaces as the detail of a pilot
    """

    drone = DroneSerializer()

    class Meta:
        model = Competition
        fields = ("url", "pk", "drone", "distance_in_feet", "distance_achievement_date")


class PilotSerializer(serializers.HyperlinkedModelSerializer):
    gender = serializers.ChoiceField(choices=Pilot.GENDER_CHOICES)
    gender_description = serializers.CharField(
        source="get_gender_display", read_only=True
    )
    competitions = CompetitionSerializer(many=True, read_only=True)

    class Meta:
        model = Pilot
        fields = (
            "url",
            "pk",
            "name",
            "gender",
            "gender_description",
            "races_count",
            "competitions",
        )


class PilotCompetitionSerializer(serializers.ModelSerializer):
    """
    Uses to serialize competition instance
    """

    pilot = serializers.SlugRelatedField(
        slug_field="name", queryset=Pilot.objects.all()
    )
    drone = serializers.SlugRelatedField(
        slug_field="name", queryset=Drone.objects.all()
    )

    class Meta:
        model = Competition
        fields = (
            "url",
            "pk",
            "distance_in_feet",
            "distance_achievement_date",
            "pilot",
            "drone",
        )
