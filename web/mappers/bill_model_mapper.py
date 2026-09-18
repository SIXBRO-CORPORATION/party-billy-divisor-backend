from domain.bill.bill import Bill
from domain.bill.participant import Participant
from web.models.response.bill.bill_response import BillResponse
from web.models.response.bill.bill_summary_response import BillSummaryResponse
from web.models.response.bill.participant_response import ParticipantResponse
from web.models.response.bill.product_response import ProductResponse


class BillModelMapper:
    def to_response(self, bill: Bill) -> BillResponse:
        return BillResponse(
            id=bill.id,
            title=bill.title,
            total_amount=bill.total_amount,
            created_at=bill.created_at,
            products=[
                ProductResponse(
                    id=product.id,
                    name=product.name,
                    quantity=product.quantity,
                    unit_price=product.unit_price,
                    total_price=product.total_price,
                    participant_ids=product.participant_ids,
                )
                for product in bill.products
            ],
            participants=[
                self.to_participant_response(p) for p in bill.participants
            ],
        )

    def to_summary_response(self, bill: Bill) -> BillSummaryResponse:
        return BillSummaryResponse(
            id=bill.id,
            title=bill.title,
            total_amount=bill.total_amount,
            created_at=bill.created_at,
            participants_count=len(bill.participants),
            paid_count=sum(1 for p in bill.participants if p.paid),
        )

    def to_participant_response(self, participant: Participant) -> ParticipantResponse:
        return ParticipantResponse(
            id=participant.id,
            name=participant.name,
            amount_owed=participant.amount_owed,
            paid=participant.paid,
        )
