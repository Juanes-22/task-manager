from ..models.task import Task
from ..exceptions import BusinessError

from ..constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND


class TasksServices:

    def create_task(self, task: Task) -> None:
        existing_task = Task.get_by_title(task.title)
        if existing_task:
            raise BusinessError(
                message="Task with same title already exists",
                status_code=HTTP_400_BAD_REQUEST,
            )

        task.save()

    def get_all_tasks(self) -> list[Task]:
        return Task.get_all()

    def delete_task(self, id: int) -> None:
        task = Task.get_by_id(id)
        if not task:
            raise BusinessError(
                message="Task to delete not found",
                status_code=HTTP_404_NOT_FOUND,
            )

        task.delete()
