from decimal import Decimal
from typing import List, Optional

from domain.bill.bill import Bill
from domain.bill.participant import Participant
from domain.bill.product import Product
from persistence.model.bill.bill_entity import BillEntity
from persistence.model.bill.participant_entity import ParticipantEntity
from persistence.model.bill.product_entity import ProductEntity


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
            products=[self._product_to_domain(p) for p in (entity.products or [])],
            participants=[
                self._participant_to_domain(p) for p in (entity.participants or [])
            ],
        )

    def to_entity(self, bill: Bill) -> BillEntity:
        participant_entities: dict = {}
        participants: List[ParticipantEntity] = []

        for participant in bill.participants:
            participant_entity = self._participant_to_entity(participant, bill.id)
            participant_entities[participant.id] = participant_entity
            participants.append(participant_entity)

        products: List[ProductEntity] = []

        for product in bill.products:
            product_entity = self._product_to_entity(product, bill.id)
            product_entity.participants = [
                participant_entities[participant_id]
                for participant_id in product.participant_ids
                if participant_id in participant_entities
            ]
            products.append(product_entity)

        return BillEntity(
            id=bill.id,
            owner_id=bill.owner_id,
            title=bill.title,
            total_amount=bill.total_amount,
            created_at=bill.created_at,
            modified_at=bill.modified_at,
            active=bill.active,
            products=products,
            participants=participants,
        )

    def _participant_to_domain(self, entity: ParticipantEntity) -> Participant:
        return Participant(
            id=entity.id,
            bill_id=entity.bill_id,
            name=entity.name,
            amount_owed=entity.amount_owed or Decimal("0"),
            paid=entity.paid,
            created_at=entity.created_at,
            modified_at=entity.modified_at,
            active=entity.active,
        )

    def _participant_to_entity(
        self, participant: Participant, bill_id
    ) -> ParticipantEntity:
        return ParticipantEntity(
            id=participant.id,
            bill_id=bill_id,
            name=participant.name,
            amount_owed=participant.amount_owed,
            paid=participant.paid,
            created_at=participant.created_at,
            modified_at=participant.modified_at,
            active=participant.active,
        )

    def _product_to_domain(self, entity: ProductEntity) -> Product:
        return Product(
            id=entity.id,
            bill_id=entity.bill_id,
            name=entity.name,
            quantity=entity.quantity,
            unit_price=entity.unit_price or Decimal("0"),
            participant_ids=[p.id for p in (entity.participants or [])],
            created_at=entity.created_at,
            modified_at=entity.modified_at,
            active=entity.active,
        )

    def _product_to_entity(self, product: Product, bill_id) -> ProductEntity:
        return ProductEntity(
            id=product.id,
            bill_id=bill_id,
            name=product.name,
            quantity=product.quantity,
            unit_price=product.unit_price,
            created_at=product.created_at,
            modified_at=product.modified_at,
            active=product.active,
        )
