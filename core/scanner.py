# Contains base classes and scanning logic

from abc import ABC, abstractmethod

class Scanner(ABC):
    """
    Abstract base class for scanners.
    """

    def __init__(self, target: str, command: str):
        self.target = target
        self.command = command

    @abstractmethod
    def scan(self):
        """
        Abstract method to be implemented by subclasses.
        Each subclass should provide its own scanning logic.
        """
        pass
