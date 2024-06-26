from pydantic import BaseModel


class AttackBase(BaseModel):
    source_address: str
    average_duration: float


class AttackCreate(AttackBase):
    pass


class Attack(AttackBase):
    pass
