from passlib.context import CryptContext


crypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def encrypt_user_pwd(pwd: str) -> str:
    return crypt_context.hash(pwd)


def verify_user_pwd(pwd: str, hashed_pwd: str) -> bool:
    return crypt_context.verify(pwd, hashed_pwd)
