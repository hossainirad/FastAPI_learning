from pydantic import BaseModel, validator
from validators import normalize_name, normalize_email


class Person(BaseModel):
	id: int
	name: str
	username = 'Default Username'
	email: str

	_normalize_name = validator('name', allow_reuse=True)(normalize_name)
	_normalize_email = validator('email', allow_reuse=True)(normalize_email)
