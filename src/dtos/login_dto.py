from dataclasses import dataclass

@dataclass
class LoginRequest:
    email: str
    password: str

@dataclass
class LoginResponse:
    user: dict
    token: str
    message: str

