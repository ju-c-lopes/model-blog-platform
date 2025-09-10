# Old password checks (kept for learning)

This file preserves the original password checks that were used in the project for historical and learning purposes.

## Rationale

These checks were helpful while learning about password policies. The project is migrating to Django's `AUTH_PASSWORD_VALIDATORS` and `validate_password()` for consistency and better integration with Django forms and admin. The original logic is kept here as documentation and reference.

## Original function (verbatim)

```python
def check_password_request(pass1, pass2):
    validations = [pass1 == pass2]
    validations.append(len(pass2) >= 10 and len(pass2) <= 16)
    upper_regex = re.compile(r"[A-Z]").search(pass2)
    validations.append(upper_regex)
    number_regex = re.compile(r"\d").search(pass2)
    validations.append(number_regex)
    special_regex = re.compile(r"[\W_]").search(pass2)
    validations.append(special_regex)
    return all(validations)
```

## Notes and why it changed

-   The maximum length limit (`<= 16`) prevents passphrases and is removed in favor of minimum-length and other validators.
-   Centralizing rules via `AUTH_PASSWORD_VALIDATORS` is preferable because validators are automatically used by Django forms and are pluggable.
-   If you want to reintroduce the same checks, implement them as a custom password validator class (example below) so the behavior integrates with `validate_password()`.

## Example custom validator (how to port the checks)

```python
from django.core.exceptions import ValidationError

class RequireUpperNumberSpecialValidator:
    def validate(self, password, user=None):
        import re
        if not re.search(r'[A-Z]', password):
            raise ValidationError('Password must contain an uppercase letter.')
        if not re.search(r'\d', password):
            raise ValidationError('Password must contain a number.')
        if not re.search(r'[\W_]', password):
            raise ValidationError('Password must contain a special character.')

    def get_help_text(self):
        return 'Password must include an uppercase letter, a number and a special character.'
```

Add this validator to `AUTH_PASSWORD_VALIDATORS` in `settings.py` to re-enable the original behaviour in a pluggable way.
