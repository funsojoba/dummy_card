from enum import Enum



class EnvironmentType(Enum):
    DEVELOPMENT = "development"
    SANDBOX = "sandbox"
    PRODUCTION = "production"
    

class TransactionType(Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"
    REFUND = "REFUND"
    REVERSAL = "REVERSAL"
    