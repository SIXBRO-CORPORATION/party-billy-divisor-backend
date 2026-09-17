from abc import abstractmethod
from typing import List
from uuid import UUID

from core.persistence.commons.base_repository_port import BaseRepositoryPort
from domain.bill.bill import Bill


class BillRepositoryPort(BaseRepositoryPort[Bill]):
    @abstractmethod
    async def find_by_owner(self, owner_id: UUID) -> List[Bill]:
        pass
