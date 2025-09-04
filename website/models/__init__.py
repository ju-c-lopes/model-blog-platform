from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from website.models.UserModel import User

ROLE_CHOICE = (
    (1, "Author"),
    (2, "Reader"),
)

MONTH_CHOICE = (
    (1, "Janeiro"),
    (2, "Fevereiro"),
    (3, "Março"),
    (4, "Abril"),
    (5, "Maio"),
    (6, "Junho"),
    (7, "Julho"),
    (8, "Agosto"),
    (9, "Setembro"),
    (10, "Outubro"),
    (11, "Novembro"),
    (12, "Dezembro"),
)

SOCIAL_MEDIA = (
    (1, "Facebook"),
    (2, "Instagram"),
    (3, "LinkedIn"),
    (4, "X"),
)

ACADEMIC_LEVEL = (
    (1, "Graduado"),
    (2, "Pós-graduado"),
    (3, "Mestrado"),
    (4, "Doutorado"),
)

from .AuthorModel import *  # noqa: F401,F403
from .AuthorSocialMediaModel import *  # noqa: F401,F403
from .GraduationsModel import *  # noqa: F401,F403
from .JobsModel import *  # noqa: F401,F403
from .PostModel import *  # noqa: F401,F403
from .ReaderModel import *  # noqa: F401,F403
from .UserModel import *  # noqa: F401,F403
