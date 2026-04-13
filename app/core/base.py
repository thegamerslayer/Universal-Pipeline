from abc import ABC, abstractmethod
import logging

class BaseStage(ABC):
    def __init__(self, name: str, config: dict):
        self.name = name
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def run(self, data: any) -> any:
        """
        Execute the stage's logic.
        :param data: Input data from the previous stage.
        :return: Output data for the next stage.
        """
        pass
