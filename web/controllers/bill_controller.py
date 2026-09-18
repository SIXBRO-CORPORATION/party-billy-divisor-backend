from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status

from core.business.bill.create_bill_port import CreateBillPort
from core.business.bill.get_bill_details_port import GetBillDetailsPort
from core.business.bill.list_bills_port import ListBillsPort
from core.business.bill.set_participant_payment_port import SetParticipantPaymentPort
from core.context import Context
from domain.bill.bill import Bill
from domain.bill.product_spec import ProductSpec
from domain.user.user import User
from web.commons.api_response import ApiResponse
from web.dependencies import (
    get_bill_details_port,
    get_create_bill_port,
    get_current_user,
    get_list_bills_port,
    get_set_participant_payment_port,
)
from web.mappers.bill_model_mapper import BillModelMapper
from web.models.request.bill.create_bill_request import CreateBillRequest
from web.models.request.bill.set_payment_request import SetPaymentRequest
from web.models.response.bill.bill_response import BillResponse
from web.models.response.bill.bill_summary_response import BillSummaryResponse
from web.models.response.bill.participant_response import ParticipantResponse

router = APIRouter(prefix="/api/bills", tags=["Bills"])

_mapper = BillModelMapper()


@router.post(
    "",
    response_model=ApiResponse[BillResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_bill(
    body: CreateBillRequest,
    current_user: User = Depends(get_current_user),
    create_bill_port: CreateBillPort = Depends(get_create_bill_port),
):
    context = Context(data=Bill(title=body.title, owner_id=current_user.id))
    context.put_property(
        "product_specs",
        [
            ProductSpec(
                name=item.name,
                quantity=item.quantity,
                unit_price=item.unit_price,
                participant_names=item.participant_names,
            )
            for item in body.products
        ],
    )

    bill = await create_bill_port.execute(context)

    return ApiResponse.success(
        data=_mapper.to_response(bill), message="Conta criada com sucesso"
    )


@router.get("", response_model=ApiResponse[List[BillSummaryResponse]])
async def list_bills(
    current_user: User = Depends(get_current_user),
    list_bills_port: ListBillsPort = Depends(get_list_bills_port),
):
    context = Context()
    context.put_property("owner_id", current_user.id)

    bills = await list_bills_port.execute(context)

    return ApiResponse.success(
        data=[_mapper.to_summary_response(bill) for bill in bills]
    )


@router.get("/{bill_id}", response_model=ApiResponse[BillResponse])
async def get_bill(
    bill_id: UUID,
    current_user: User = Depends(get_current_user),
    details_port: GetBillDetailsPort = Depends(get_bill_details_port),
):
    context = Context()
    context.put_property("bill_id", bill_id)
    context.put_property("owner_id", current_user.id)

    bill = await details_port.execute(context)

    return ApiResponse.success(data=_mapper.to_response(bill))


@router.patch(
    "/{bill_id}/participants/{participant_id}/payment",
    response_model=ApiResponse[ParticipantResponse],
)
async def set_participant_payment(
    bill_id: UUID,
    participant_id: UUID,
    body: SetPaymentRequest,
    current_user: User = Depends(get_current_user),
    set_payment_port: SetParticipantPaymentPort = Depends(
        get_set_participant_payment_port
    ),
):
    context = Context()
    context.put_property("bill_id", bill_id)
    context.put_property("participant_id", participant_id)
    context.put_property("owner_id", current_user.id)
    context.put_property("paid", body.paid)

    participant = await set_payment_port.execute(context)

    message = "Pagamento confirmado" if body.paid else "Pagamento desmarcado"

    return ApiResponse.success(
        data=_mapper.to_participant_response(participant), message=message
    )
