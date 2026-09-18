from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.persistence.bill.bill_repository_port import BillRepositoryPort
from domain.bill.bill import Bill
from persistence.mappers.bill.bill_mapper import BillMapper
from persistence.model.bill.bill_entity import BillEntity
from persistence.model.bill.product_entity import ProductEntity


class BillRepositoryAdapter(BillRepositoryPort):
    def __init__(self, session: AsyncSession, mapper: BillMapper):
        self.session = session
        self.mapper = mapper

    def _with_eager_loading(self, stmt):
        return stmt.options(
            selectinload(BillEntity.participants),
            selectinload(BillEntity.products).selectinload(ProductEntity.participants),
        )

    async def get(self, entity_id: UUID) -> Optional[Bill]:
        stmt = self._with_eager_loading(
            select(BillEntity).where(BillEntity.id == entity_id)
        )
        result = await self.session.execute(stmt)
        return self.mapper.to_domain(result.scalar_one_or_none())

    async def create(self, bill: Bill) -> Bill:
        entity = self.mapper.to_entity(bill)
        self.session.add(entity)
        await self.session.flush()
        return self.mapper.to_domain(entity)

    async def save(self, bill: Bill) -> Bill:
        entity = self.mapper.to_entity(bill)
        entity = await self.session.merge(entity)
        await self.session.flush()
        await self.session.refresh(entity)
        return self.mapper.to_domain(entity)

    async def find_all(self) -> List[Bill]:
        stmt = self._with_eager_loading(select(BillEntity))
        result = await self.session.execute(stmt)
        return [self.mapper.to_domain(entity) for entity in result.scalars().all()]

    async def find_by_owner(self, owner_id: UUID) -> List[Bill]:
        stmt = self._with_eager_loading(
            select(BillEntity)
            .where(BillEntity.owner_id == owner_id)
            .order_by(BillEntity.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return [self.mapper.to_domain(entity) for entity in result.scalars().all()]
