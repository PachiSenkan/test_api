from sqlalchemy.orm import Session
import statistics
from app.api import models, schemas


def get_attacks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DDoSInformation).offset(skip).limit(limit).all()


def get_attack_by_source_address(db: Session, source_addr: str):
    return (
        db.query(models.DDoSInformation)
        .filter(models.DDoSInformation.source_address == source_addr)
        .first()
    )


def update_attacks(db: Session, attacks: dict[str, list[float]]):
    added_attacks = []
    for source, durations in attacks.items():
        mean_duration = statistics.mean(durations)
        attack = get_attack_by_source_address(db, source)
        if not attack:
            db_attack = models.DDoSInformation(
                source_address=source, average_duration=mean_duration
            )
            db.add(db_attack)
            db.commit()
            db.refresh(db_attack)
        else:
            attack.average_duration = mean_duration
            db.commit()
            db.refresh(attack)
            added_attacks.append(attack)

    return added_attacks
