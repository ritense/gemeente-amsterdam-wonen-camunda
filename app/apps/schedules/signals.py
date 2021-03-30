from apps.camunda.services import CamundaService
from apps.schedules.models import Schedule
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(
    post_save, sender=Schedule, dispatch_uid="schedule_create_complete_camunda_task"
)
def complete_camunda_task_create_schedule(sender, instance, created, **kwargs):
    task = CamundaService().get_task_by_task_name_id_and_camunda_id(
        "task_create_schedule", instance.case.camunda_id
    )
    if task:
        CamundaService().complete_task(task["id"])
