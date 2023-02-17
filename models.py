from typing import Optional

from pydantic import BaseModel


class Person(BaseModel):
	id: int
	name: str
	username = 'Default Username'
	email: str
