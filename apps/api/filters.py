from django_filters import rest_framework as filters
from django_filters import AllValuesFilter, DateTimeFilter, NumberFilter

from apps.drones.models import Competition


class CompetitionFilter(filters.FilterSet):
    from_achievement_date = DateTimeFilter(
        field_name="distance_achievement_date", lookup_expr="gte"
    )
    to_achievement_date = DateTimeFilter(
        field_name="distance_achievement_date", lookup_expr="lte"
    )
    min_distance_in_feet = NumberFilter(
        field_name="distance_in_feet", lookup_expr="gte"
    )
    max_distance_in_feet = NumberFilter(
        field_name="distance_in_feet", lookup_expr="lte"
    )
    drone_name = AllValuesFilter(field_name="drone__name")
    pilot_name = AllValuesFilter(field_name="pilot__name")

    class Meta:
        model = Competition
        fields = (
            "distance_in_feet",
            "from_achievement_date",
            "to_achievement_date",
            "min_distance_in_feet",
            "max_distance_in_feet",
            "drone_name",
            "pilot_name",
        )