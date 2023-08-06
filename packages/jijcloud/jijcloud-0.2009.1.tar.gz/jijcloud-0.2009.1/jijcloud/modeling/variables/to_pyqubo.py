from abc import ABCMeta, abstractmethod
import pyqubo


class ToPyQUBO(metaclass=ABCMeta):

    @abstractmethod
    def to_pyqubo(self)->pyqubo.Express:
        raise NotImplementedError()