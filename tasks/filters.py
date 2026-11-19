import django_filters

from .models import Task


class TaskFilter(django_filters.FilterSet):

    title = django_filters.CharFilter(
        lookup_expr="icontains"
    )

    status = django_filters.ChoiceFilter(
        choices=Task.STATUS_CHOICES.choices
    )

    priority = django_filters.ChoiceFilter(choices=[
        ("low", "Low"), 
        ("medium", "Medium"), 
        ("high", "High")
        ], 
        method="filter_priority"
                                           )

    def filter_priority(self, queryset, name, value):
        priority_mopping = {"low": Task.PRIORITY_CHOICES.LOW,
                            "medium" : Task.PRIORITY_CHOICES.MEDIUM,
                            "high" : Task.PRIORITY_CHOICES.HIGH}
        return queryset.filter(priority=priority_mopping[value])

    class Meta:
        model = Task
        fields = ["title","priority", "status"]


