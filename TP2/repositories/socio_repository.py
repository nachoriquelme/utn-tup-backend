from typing import List, Optional
from sqlmodel import Session, select

from models.socio import Socio


class SocioRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, socio: Socio) -> Socio:
        self.session.add(socio)
        self.session.commit()
        self.session.refresh(socio)
        return socio

    def get_all(self) -> List[Socio]:
        return list(self.session.exec(select(Socio)).all())

    def get_by_id(self, socio_id: int) -> Optional[Socio]:
        return self.session.get(Socio, socio_id)

    def get_by_email(self, email: str) -> Optional[Socio]:
        return self.session.exec(select(Socio).where(Socio.email == email)).first()

    def update(self, socio: Socio) -> Socio:
        self.session.add(socio)
        self.session.commit()
        self.session.refresh(socio)
        return socio

    def delete(self, socio: Socio) -> None:
        self.session.delete(socio)
        self.session.commit()