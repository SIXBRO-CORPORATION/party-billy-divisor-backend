from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from domain.bill.participant import Participant


class ParticipantRepositoryPort(ABC):
    @abstractmethod
    async def get(self, participant_id: UUID) -> Optional[Participant]:
        pass

    @abstractmethod
    async def set_paid(self, participant_id: UUID, paid: bool) -> Optional[Participant]:
        pass
