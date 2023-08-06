from agent.commands.service_restart import restart_services
from agent.commands.service_status import check_service_statuses
from agent.scheduler.scheduled_task import ScheduledTask
from agent.services.status_sender import send_statuses


class StatusTask(ScheduledTask):

    def execute(self):
        statuses_to_send, services_to_restart = check_service_statuses()
        send_statuses(statuses_to_send)
        restart_services(services_to_restart)
