from typing import List

from core.command import Command
from domain.bill.bill import Bill


class ListBillsPort(Command[List[Bill]]):
    pass
