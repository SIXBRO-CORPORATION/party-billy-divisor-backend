from decimal import Decimal, ROUND_DOWN
from typing import List
from uuid import UUID, uuid4

from domain.bill.bill import Bill
from domain.bill.participant import Participant
from domain.bill.product import Product
from domain.bill.product_spec import ProductSpec
from domain.exceptions.business_exception import BusinessException

_CENTS = Decimal("0.01")


class BillSplitCalculator:

    @staticmethod
    def build_bill(owner_id: UUID, title: str, product_specs: List[ProductSpec]) -> Bill:
        if not product_specs:
            raise BusinessException("A conta precisa ter pelo menos um produto")

        participants_by_name = BillSplitCalculator._collect_participants(product_specs)

        products: List[Product] = []
        total_amount = Decimal("0")

        for spec in product_specs:
            product_total = (spec.unit_price * spec.quantity).quantize(_CENTS)
            assigned = [participants_by_name[name.strip()] for name in spec.participant_names]

            splits = BillSplitCalculator._split_evenly(product_total, len(assigned))
            for participant, split in zip(assigned, splits):
                participant.amount_owed += split

            products.append(
                Product(
                    id=uuid4(),
                    name=spec.name,
                    quantity=spec.quantity,
                    unit_price=spec.unit_price,
                    participant_ids=[p.id for p in assigned],
                )
            )

            total_amount += product_total

        bill = Bill(
            id=uuid4(),
            owner_id=owner_id,
            title=title,
            total_amount=total_amount,
            products=products,
            participants=list(participants_by_name.values()),
        )

        for product in bill.products:
            product.bill_id = bill.id
        for participant in bill.participants:
            participant.bill_id = bill.id

        return bill

    @staticmethod
    def _collect_participants(product_specs: List[ProductSpec]) -> dict:
        participants_by_name = {}

        for spec in product_specs:
            if spec.quantity <= 0:
                raise BusinessException(f"Quantidade inválida para o produto '{spec.name}'")

            if spec.unit_price < 0:
                raise BusinessException(f"Preço inválido para o produto '{spec.name}'")

            if not spec.participant_names:
                raise BusinessException(
                    f"O produto '{spec.name}' precisa de pelo menos uma pessoa vinculada"
                )

            for raw_name in spec.participant_names:
                name = raw_name.strip()

                if not name:
                    raise BusinessException("Nome de participante não pode ser vazio.")

                if name not in participants_by_name:
                    participants_by_name[name] = Participant(
                        id=uuid4(), name=name, amount_owed=Decimal("0"), paid=False
                    )

        return participants_by_name

    @staticmethod
    def _split_evenly(total: Decimal, participant_count: int) -> List[Decimal]:

        base_split = (total / participant_count).quantize(_CENTS, rounding=ROUND_DOWN)
        splits = [base_split] * participant_count

        remainder = total - (base_split * participant_count)
        splits[0] += remainder

        return splits
