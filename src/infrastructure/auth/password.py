from passlib.context import CryptContext

# Contexto de hash usando Argon2 (recomendado)
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
)


def get_password_hash(password: str) -> str:
    """
    Gera o hash da senha usando Argon2.
    Não há limite de tamanho para a senha.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha informada corresponde ao hash armazenado.
    """
    return pwd_context.verify(plain_password, hashed_password)
