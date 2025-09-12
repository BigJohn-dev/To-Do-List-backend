from dataclasses import dataclass

@dataclass
class RegistrationRequest:
    username: str
    email: str
    password: str



@dataclass
class RegistrationResponse:
    id: int
    username: str
    email: str
    message: str = "Registration successful"

