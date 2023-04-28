
# Standardizing cpf format
def sanitize_cpf(cpf: str) -> str:
    try:
        return cpf.replace('.', '').replace('-', '')
    except:
        return cpf
