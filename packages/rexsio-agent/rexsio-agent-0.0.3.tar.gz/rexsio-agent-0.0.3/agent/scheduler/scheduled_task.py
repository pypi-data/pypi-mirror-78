import abc


class ScheduledTask(abc.ABC):
    @abc.abstractmethod
    def execute(self):
        """
        This method will be executed with intervals defined by #get_interval_seconds method
        """
        pass

    def get_interval_seconds(self):
        """
        Defines interval

        By default 20
        """
        return 20
