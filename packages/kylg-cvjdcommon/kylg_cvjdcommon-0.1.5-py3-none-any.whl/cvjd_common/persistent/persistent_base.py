from abc import ABCMeta, abstractmethod

from cvjd_common.models.cv_match import CvMatch


class PersistentBase(metaclass=ABCMeta):
    """
    Base Persistent, which behaves like an interface for persistent job status
    """

    @abstractmethod
    def writeJobStatus(self, status: str, cvMatch: CvMatch):
        pass

    @abstractmethod
    def readJobStatus(self, cvId: str) -> CvMatch:
        pass
