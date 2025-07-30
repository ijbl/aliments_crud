from abc import ABC, abstractmethod
from domain.aliment import Aliment

class AlimentRepository(ABC):

    @abstractmethod
    def get_all(self) -> list[Aliment]:
        pass

    @abstractmethod
    def get_by_id(self,
                  aliment_id: int) -> Aliment:
        pass

    @abstractmethod
    def insert(self,
               aliment: Aliment) -> None:
        pass

    @abstractmethod
    def update(self,
               aliment: Aliment) -> None:
        pass

    @abstractmethod
    def delete(self,
               aliment_id: int) -> None:
        pass

    @abstractmethod
    def exists(self,
               aliment_id: int) -> bool:
        pass