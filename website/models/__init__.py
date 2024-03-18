from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

ROLE_CHOICE = (
    (1, 'Author'),
    (2, 'Reader'),
)

MONTH_CHOICE = (
    (1, 'Janeiro'),
    (2, 'Fevereiro'),
    (3, 'Março'),
    (4, 'Abril'),
    (5, 'Maio'),
    (6, 'Junho'),
    (7, 'Julho'),
    (8, 'Agosto'),
    (9, 'Setembro'),
    (10, 'Outubro'),
    (11, 'Novembro'),
    (12, 'Dezembro'),
)

SOCIAL_MEDIA = (
    (1, 'Facebook'),
    (2, 'Instagram'),
    (3, 'LinkedIn'),
    (4, 'X'),
)

ACADEMIC_LEVEL = (
    (1, 'Graduado'),
    (2, 'Pós-graduado'),
    (3, 'Mestrado'),
    (4, 'Doutorado'),
)

from .PostModel import Post
from .AuthorModel import Author
from .GraduationsModel import Graduation
from .JobsModel import Job
from .AuthorSocialMediaModel import SocialMedia
from .ReaderModel import Reader