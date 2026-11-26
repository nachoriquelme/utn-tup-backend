from typing import List, Optional
from sqlmodel import Session, select

from models.autor import Autor


class AutorRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, autor: Autor) -> Autor:
        self.session.add(autor)
        self.session.commit()
        self.session.refresh(autor)
        return autor

    def get_all(self) -> List[Autor]:
        return list(self.session.exec(select(Autor)).all())

    def get_by_id(self, autor_id: int) -> Optional[Autor]:
        return self.session.get(Autor, autor_id)

    def update(self, autor: Autor) -> Autor:
        self.session.add(autor)
        self.session.commit()
        self.session.refresh(autor)
        return autor

    def delete(self, autor: Autor) -> None:
        self.session.delete(autor)
        self.session.commit()