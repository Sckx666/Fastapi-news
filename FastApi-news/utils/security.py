import argon2
from argon2 import PasswordHasher, exceptions


# 创建密码哈希工厂
ph = PasswordHasher()


# 密码加密
def get_hash_password(password: str):
    return ph.hash(password)


def verify_password(plain_password, hashed_password):
    try:
        ph.verify(hashed_password,plain_password)
        return True
    except exceptions.VerifyMismatchError:
        return False
