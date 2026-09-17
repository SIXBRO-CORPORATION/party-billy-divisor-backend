from typing import Optional

from decimal import Decimal

from domain.bill.bill import Bill
from persistence.model.bill.bill_entity import BillEntity


class BillMapper:

    def to_domain(self, entity: Optional[BillEntity]) -> Optional[Bill]:
        if entity is None:
            return None

        return Bill(
            id=entity.id,
            owner_id=entity.owner_id,
            title=entity.title,
            total_amount=entity.total_amount or Decimal("0"),
            created_at=entity.created_at,
            modified_at=entity.modified_at,
            active=entity.active,
        )

    def to_entity(self, bill: Bill) -> BillEntity:
        return BillEntity(
            id=bill.id,
            owner_id=bill.owner_id,
            title=bill.title,
            total_amount=bill.total_amount,
            created_at=bill.created_at,
            modified_at=bill.modified_at,
            active=bill.active,
        )
