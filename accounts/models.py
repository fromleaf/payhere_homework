from django.contrib.auth.models import AbstractUser
from django.db import models

from payhere.constants import const


class User(AbstractUser):
    username = None
    cellphone = models.CharField(
        "cellphone",
        max_length=const.MAX_LENGTH_DEFAULT_CHAR,
        unique=True,
        error_messages={
            "unique": "이미 등록된 핸드폰 번호입니다.",
        },
        help_text="사용자 핸드폰 번호. 로그인 ID로 사용됨"
    )
    name = models.CharField(
        max_length=const.MAX_LENGTH_NAME,
        help_text="사용자 이름"
    )

    USERNAME_FIELD = "cellphone"
