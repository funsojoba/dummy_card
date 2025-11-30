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
    
    
class CardType(Enum):
    MASTERCARD = "mastercard"
    VISA = "visa"
    

class CardTransactionLimit(Enum):
    FIVE_THOUSAND = 500000
    TEN_THOUSAND = 1000000