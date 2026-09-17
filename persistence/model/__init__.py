from persistence.model.user.user_entity import UserEntity
from persistence.model.bill.bill_entity import BillEntity
from persistence.model.bill.participant_entity import ParticipantEntity
from persistence.model.bill.product_entity import ProductEntity

# Funções/triggers/views registrados via alembic-utils (nenhum por enquanto).
# migrations/env.py importa esta lista para que `alembic revision --autogenerate`
# também detecte mudanças nelas, e não apenas em tabelas/colunas.
PG_ENTITIES = []

__all__ = [
    "UserEntity",
    "BillEntity",
    "ParticipantEntity",
    "ProductEntity",
    "PG_ENTITIES",
]
