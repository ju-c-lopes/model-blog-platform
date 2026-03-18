from website.models.user.UserModel import User  # noqa

ROLE_CHOICE = (
    (1, "Author"),
    (2, "Reader"),
)

GENDER_CHOICE = (
    (1, "M"),
    (2, "F"),
)

SOCIAL_MEDIA = (
    (1, "Facebook"),
    (2, "Instagram"),
    (3, "LinkedIn"),
    (4, "X"),
    (5, "GitHub"),
)

ACADEMIC_LEVEL = (
    (1, "Graduação"),
    (2, "Pós-graduação"),
    (3, "Mestrado"),
    (4, "Doutorado"),
)

STATUS_MAP = {
    1: {
        "M": ("Graduado", "Graduando"),
        "F": ("Graduada", "Graduanda"),
    },
    2: {
        "M": ("Pós-graduado", "Pós-graduando"),
        "F": ("Pós-graduada", "Pós-graduanda"),
    },
    3: {
        "M": ("Mestrado", "Mestrando"),
        "F": ("Mestrada", "Mestranda"),
    },
    4: {
        "M": ("Doutorado", "Doutorando"),
        "F": ("Doutorada", "Doutoranda"),
    }
}
