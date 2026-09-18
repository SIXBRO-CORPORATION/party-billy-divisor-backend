from decimal import Decimal
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.persistence.bill.participant_repository_port import ParticipantRepositoryPort
from domain.bill.participant import Participant
from persistence.model.bill.participant_entity import ParticipantEntity


class ParticipantRepositoryAdapter(ParticipantRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, participant_id: UUID) -> Optional[Participant]:
        stmt = select(ParticipantEntity).where(ParticipantEntity.id == participant_id)
        result = await self.session.execute(stmt)
        return self._to_domain(result.scalar_one_or_none())

    async def set_paid(self, participant_id: UUID, paid: bool) -> Optional[Participant]:
        stmt = select(ParticipantEntity).where(ParticipantEntity.id == participant_id)
        result = await self.session.execute(stmt)
        entity = result.scalar_one_or_none()

        if entity is None:
            return None

        entity.paid = paid
        await self.session.flush()
        await self.session.refresh(entity)

        return self._to_domain(entity)

    def _to_domain(self, entity: Optional[ParticipantEntity]) -> Optional[Participant]:
        if entity is None:
            return None

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
