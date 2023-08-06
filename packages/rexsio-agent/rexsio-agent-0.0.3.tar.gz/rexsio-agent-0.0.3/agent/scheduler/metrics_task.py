from agent.commands.metrics import read_metrics
from agent.scheduler import logger
from agent.scheduler.scheduled_task import ScheduledTask
from agent.websocket.client import AgentWebSocketClient


class MetricsTask(ScheduledTask):

    def execute(self):
        metrics = read_metrics()
        AgentWebSocketClient.get_instance().safe_message_send(metrics)
        logger.info(f'Node metrics sent: {metrics}')
