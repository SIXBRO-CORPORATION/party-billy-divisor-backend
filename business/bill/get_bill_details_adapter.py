from uuid import UUID

from core.business.bill.get_bill_details_port import GetBillDetailsPort
from core.context import Context
from core.persistence.bill.bill_repository_port import BillRepositoryPort
from domain.bill.bill import Bill
from domain.exceptions.forbidden_exception import ForbiddenException
from domain.exceptions.not_found_exception import NotFoundException


class GetBillDetailsAdapter(GetBillDetailsPort):
    def __init__(self, repository: BillRepositoryPort):
        self.repository = repository

    async def execute(self, context: Context) -> Bill:
        bill_id = context.get_property("bill_id", UUID)
        owner_id = context.get_property("owner_id", UUID)

        bill = await self.repository.get(bill_id)

        if bill is None:
            raise NotFoundException("Conta não encontrada")

        if bill.owner_id != owner_id:
            raise ForbiddenException("Você não tem permissão para acessar essa conta")

        return bill
