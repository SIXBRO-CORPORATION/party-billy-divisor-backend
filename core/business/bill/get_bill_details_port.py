from core.command import Command
from domain.bill.bill import Bill


class GetBillDetailsPort(Command[Bill]):
    pass
