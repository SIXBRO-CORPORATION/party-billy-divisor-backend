from typing import Annotated

from fastapi import Depends

from business.bill.create_bill_adapter import CreateBillAdapter
from business.bill.get_bill_details_adapter import GetBillDetailsAdapter
from business.bill.list_bills_adapter import ListBillsAdapter
from business.bill.set_participant_payment_adapter import SetParticipantPaymentAdapter
from core.business.bill.create_bill_port import CreateBillPort
from core.business.bill.get_bill_details_port import GetBillDetailsPort
from core.business.bill.list_bills_port import ListBillsPort
from core.business.bill.set_participant_payment_port import SetParticipantPaymentPort
from core.persistence.bill.bill_repository_port import BillRepositoryPort
from core.persistence.bill.participant_repository_port import ParticipantRepositoryPort
from web.dependencies.persistence_dependencies import (
    get_bill_repository,
    get_participant_repository,
)


def get_create_bill_port(
    bill_repository: Annotated[BillRepositoryPort, Depends(get_bill_repository)],
) -> CreateBillPort:
    return CreateBillAdapter(bill_repository)


def get_list_bills_port(
    bill_repository: Annotated[BillRepositoryPort, Depends(get_bill_repository)],
) -> ListBillsPort:
    return ListBillsAdapter(bill_repository)


def get_bill_details_port(
    bill_repository: Annotated[BillRepositoryPort, Depends(get_bill_repository)],
) -> GetBillDetailsPort:
    return GetBillDetailsAdapter(bill_repository)


def get_set_participant_payment_port(
    bill_repository: Annotated[BillRepositoryPort, Depends(get_bill_repository)],
    participant_repository: Annotated[
        ParticipantRepositoryPort, Depends(get_participant_repository)
    ],
) -> SetParticipantPaymentPort:
    return SetParticipantPaymentAdapter(bill_repository, participant_repository)
