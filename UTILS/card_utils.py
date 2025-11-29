import random
from datetime import datetime, timedelta

def generate_card_number(card_type: str = "visa"):
    """
    Generate a realistic-looking card number for Visa or MasterCard
    using the Luhn checksum algorithm.
    """
    card_type = card_type.lower()

    if card_type == "visa":
        # Visa BIN: starts with 4, usually 16 digits
        prefix = "4" + "".join(str(random.randint(0, 9)) for _ in range(5))  # 6-digit BIN

    elif card_type == "mastercard":
        # MasterCard BIN ranges:
        # 51–55 or 2221–2720
        mc_bins = []

        # Add 51-55
        mc_bins.extend([str(i) for i in range(510000, 560000)])

        # Add 2221-2720 (6-digit)
        mc_bins.extend([str(i) for i in range(222100, 272100)])

        prefix = random.choice(mc_bins)

    else:
        raise ValueError("Unsupported card type. Use 'visa' or 'mastercard'.")

    # Add random digits to make 15 digits (last is checksum)
    body_length = 15 - len(prefix)
    body = "".join(str(random.randint(0, 9)) for _ in range(body_length))

    partial = prefix + body

    # Luhn algorithm to compute the checksum
    digits = [int(x) for x in partial]
    
    # Reverse for Luhn processing
    for i in range(len(digits) - 1, -1, -2):
        doubled = digits[i] * 2
        digits[i] = doubled - 9 if doubled > 9 else doubled

    checksum = (10 - (sum(digits) % 10)) % 10

    return partial + str(checksum)



def generate_dummy_cvv():
    return f"{random.randint(100, 999)}"



def generate_dummy_expiry(months_in_future=24):
    """Generate MM/YY between now and +24 months."""
    future = datetime.now() + timedelta(days=30 * random.randint(6, months_in_future))
    return future.strftime("%m/%y")