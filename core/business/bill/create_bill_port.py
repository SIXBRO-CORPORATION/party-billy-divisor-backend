from core.command import Command
from domain.bill.bill import Bill


class CreateBillPort(Command[Bill]):
    pass
