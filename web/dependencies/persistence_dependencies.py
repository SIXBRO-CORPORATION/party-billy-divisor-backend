from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.persistence.bill.bill_repository_port import BillRepositoryPort
from core.persistence.bill.participant_repository_port import ParticipantRepositoryPort
from core.persistence.user.user_repository_port import UserRepositoryPort
from persistence.adapters.bill.bill_repository_adapter import BillRepositoryAdapter
from persistence.adapters.bill.participant_repository_adapter import (
    ParticipantRepositoryAdapter,
)
from persistence.adapters.user.user_repository_adapter import UserRepositoryAdapter
from persistence.database import get_db
from persistence.mappers.bill.bill_mapper import BillMapper
from persistence.mappers.user.user_mapper import UserMapper


def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> UserRepositoryPort:
    return UserRepositoryAdapter(session, UserMapper())


def get_bill_repository(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> BillRepositoryPort:
    return BillRepositoryAdapter(session, BillMapper())


def get_participant_repository(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> ParticipantRepositoryPort:
    return ParticipantRepositoryAdapter(session)
