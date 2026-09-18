from uuid import UUID

from core.business.bill.set_participant_payment_port import SetParticipantPaymentPort
from core.context import Context
from core.persistence.bill.bill_repository_port import BillRepositoryPort
from core.persistence.bill.participant_repository_port import ParticipantRepositoryPort
from domain.bill.participant import Participant
from domain.exceptions.forbidden_exception import ForbiddenException
from domain.exceptions.not_found_exception import NotFoundException


class SetParticipantPaymentAdapter(SetParticipantPaymentPort):
    def __init__(
        self,
        bill_repository: BillRepositoryPort,
        participant_repository: ParticipantRepositoryPort,
    ):
        self.bill_repository = bill_repository
        self.participant_repository = participant_repository

    async def execute(self, context: Context) -> Participant:
        bill_id = context.get_property("bill_id", UUID)
        participant_id = context.get_property("participant_id", UUID)
        owner_id = context.get_property("owner_id", UUID)
        paid = context.get_property("paid", bool)

        bill = await self.bill_repository.get(bill_id)

        if bill is None:
            raise NotFoundException("Conta não encontrada")

        if bill.owner_id != owner_id:
            raise ForbiddenException("Você não tem permissão para alterar essa conta")

        participant_belongs_to_bill = any(p.id == participant_id for p in bill.participants)

        if not participant_belongs_to_bill:
            raise NotFoundException("Participante não encontrado nessa conta")

        return await self.participant_repository.set_paid(participant_id, paid)
