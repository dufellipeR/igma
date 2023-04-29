# Standardizing cpf format
def sanitize_cpf(cpf: str) -> str:
    try:
        return cpf.replace('.', '').replace('-', '')
    except:
        return cpf


def make_safe_digit(digits_sum: int) -> str:
    remainder = digits_sum % 11
    if remainder >= 2:
        return str(11 - remainder)
    else:
        return '0'


def sum_digits(digits: str) -> int:
    digit_sum = 0

    i = len(digits) + 1

    for char in digits:
        digit_sum += int(char) * i
        i -= 1

    return digit_sum


# Receives a sanitized cpf
def validate_cpf(cpf: str) -> bool:
    if len(cpf) != 11:
        return False

    unsafe_digits = cpf[9:]
    safe_digits = ""

    digits = cpf[:9]

    # Making first safe digit
    safe_digits += make_safe_digit(sum_digits(digits))

    # Making second safe digit
    safe_digits += make_safe_digit(sum_digits(digits+safe_digits))

    return unsafe_digits == safe_digits
