from typing import List
from uuid import UUID

from core.business.bill.list_bills_port import ListBillsPort
from core.context import Context
from core.persistence.bill.bill_repository_port import BillRepositoryPort
from domain.bill.bill import Bill
from domain.exceptions.business_exception import BusinessException


class ListBillsAdapter(ListBillsPort):
    def __init__(self, repository: BillRepositoryPort):
        self.repository = repository

    async def execute(self, context: Context) -> List[Bill]:
        owner_id = context.get_property("owner_id", UUID)

        if owner_id is None:
            raise BusinessException("Usuário não identificado")

        return await self.repository.find_by_owner(owner_id)
