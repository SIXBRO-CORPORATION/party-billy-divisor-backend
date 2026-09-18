from typing import List
from uuid import UUID

from core.business.bill.create_bill_port import CreateBillPort
from core.context import Context
from core.persistence.bill.bill_repository_port import BillRepositoryPort
from domain.bill.bill import Bill
from domain.bill.bill_split_calculator import BillSplitCalculator
from domain.bill.product_spec import ProductSpec
from domain.exceptions.business_exception import BusinessException


class CreateBillAdapter(CreateBillPort):
    def __init__(self, repository: BillRepositoryPort):
        self.repository = repository

    async def execute(self, context: Context) -> Bill:
        bill_data = context.get_data(Bill)

        if bill_data is None or not bill_data.title:
            raise BusinessException("Título da conta é obrigatório")

        if bill_data.owner_id is None:
            raise BusinessException("Conta precisa estar vinculada a um usuário")

        product_specs: List[ProductSpec] = context.get_property("product_specs", list) or []

        bill = BillSplitCalculator.build_bill(
            owner_id=bill_data.owner_id,
            title=bill_data.title.strip(),
            product_specs=product_specs,
        )

        return await self.repository.create(bill)
