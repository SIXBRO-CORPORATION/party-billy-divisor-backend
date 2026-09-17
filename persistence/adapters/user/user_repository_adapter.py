from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.persistence.user.user_repository_port import UserRepositoryPort
from domain.user.user import User
from persistence.mappers.user.user_mapper import UserMapper
from persistence.model.user.user_entity import UserEntity


class UserRepositoryAdapter(UserRepositoryPort):
    def __init__(self, session: AsyncSession, mapper: UserMapper):
        self.session = session
        self.mapper = mapper

    async def get(self, entity_id: UUID) -> Optional[User]:
        stmt = select(UserEntity).where(UserEntity.id == entity_id)
        result = await self.session.execute(stmt)
        return self.mapper.to_domain(result.scalar_one_or_none())

    async def save(self, user: User) -> User:
        entity = self.mapper.to_entity(user)
        entity = await self.session.merge(entity)
        await self.session.flush()
        await self.session.refresh(entity)
        return self.mapper.to_domain(entity)

    async def find_by_email(self, email: str) -> Optional[User]:
        stmt = select(UserEntity).where(UserEntity.email == email)
        result = await self.session.execute(stmt)
        return self.mapper.to_domain(result.scalar_one_or_none())

    async def exists_by_email(self, email: str) -> bool:
        stmt = select(UserEntity.id).where(UserEntity.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def find_all(self) -> List[User]:
        stmt = select(UserEntity)
        result = await self.session.execute(stmt)
        return [self.mapper.to_domain(entity) for entity in result.scalars().all()]
