import re

from django.core.exceptions import ValidationError


class LegacyPasswordValidator:
    """Compatibility password validator that enforces the project's legacy
    learning-oriented rules.

    Rules enforced:
    - length >= 10 and <= 16
    - at least one uppercase letter
    - at least one digit
    - at least one special character (non-word or underscore)
    """

    def validate(self, password, user=None):
        # reference the `user` param to avoid unused-argument lint warnings
        _ = user
        if password is None:
            raise ValidationError("Senha inválida.")

        if not (10 <= len(password) <= 16):
            raise ValidationError("A senha deve ter entre 10 e 16 caracteres (legado).")

        if not re.search(r"[A-Z]", password):
            raise ValidationError("A senha deve conter ao menos uma letra maiúscula.")

        if not re.search(r"\d", password):
            raise ValidationError("A senha deve conter ao menos um número.")

        if not re.search(r"[\W_]", password):
            raise ValidationError("A senha deve conter ao menos um caractere especial.")

    def get_help_text(self):
        return (
            "A senha deve ter entre 10 e 16 caracteres, incluir uma letra maiúscula, "
            "um número e um caractere especial."
        )
