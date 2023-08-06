from twisted.internet.task import LoopingCall

from agent.scheduler import logger
from agent.scheduler.metrics_task import MetricsTask
from agent.scheduler.status_task import StatusTask

TASKS = [
    StatusTask(),
    MetricsTask()
]


class ScheduledTaskManager:

    _instance = None

    @staticmethod
    def get_instance():
        if ScheduledTaskManager._instance is None:
            ScheduledTaskManager._instance = ScheduledTaskManager()
        return ScheduledTaskManager._instance

    def __init__(self):
        self.scheduled_tasks = list(map(lambda t: {'task': t, 'looping_call': LoopingCall(t.execute)}, TASKS))

    def start_executing(self):
        for scheduled_task in self.scheduled_tasks:
            if not scheduled_task["looping_call"].running:
                logger.info(f'Starting executing {scheduled_task["task"].__class__.__name__}...')
                scheduled_task["looping_call"].start(scheduled_task["task"].get_interval_seconds())

    def stop_executing(self):
        for scheduled_task in self.scheduled_tasks:
            if scheduled_task["looping_call"].running:
                logger.info(f'Stopping executing {scheduled_task["task"].__class__.__name__}...')
                scheduled_task["looping_call"].stop()
