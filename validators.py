from pydantic import ValidationError


def normalize_name(name: str) -> str:
    if " " in name:
        raise ValidationError("name has invalid space!")
    # return all words in capitalize mode
    return ' '.join((word.capitalize()) for word in name.split(' '))


def normalize_email(email: str) -> str:
    if ' ' in email or not email.endswith('@yahoo.com'):
        raise ValidationError("Gie me valid email.")
    return ' '.join((word.lower()) for word in email.split(' '))
