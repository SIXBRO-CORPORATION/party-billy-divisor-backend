from pydantic import BaseModel


class SetPaymentRequest(BaseModel):
    paid: bool
