from typing import List, Optional
from sqlmodel import Session, select

from models.libro import Libro
from models.prestamo import Prestamo

class PrestamoRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, prestamo_id: int) -> Optional[Prestamo]:
        return self.session.get(Prestamo, prestamo_id)

    def count_activos_by_socio(self, socio_id: int) -> int:
        activos = self.session.exec(
            select(Prestamo).where(
                Prestamo.socio_id == socio_id,
                Prestamo.fecha_devolucion == None,  # noqa: E711
            )
        ).all()
        return len(activos)

    def get_by_socio(
        self, socio_id: int, activos: Optional[bool] = None
    ) -> List[Prestamo]:
        query = select(Prestamo).where(Prestamo.socio_id == socio_id)
        if activos is True:
            query = query.where(Prestamo.fecha_devolucion == None)  # noqa: E711
        elif activos is False:
            query = query.where(Prestamo.fecha_devolucion != None)  # noqa: E711
        return list(self.session.exec(query).all())

    def create_with_stock_update(self, prestamo: Prestamo, libro: Libro) -> Prestamo:
        self.session.add(libro)
        self.session.add(prestamo)
        self.session.commit()
        self.session.refresh(prestamo)
        return prestamo

    def update_with_stock_update(self, prestamo: Prestamo, libro: Libro) -> Prestamo:
        self.session.add(libro)
        self.session.add(prestamo)
        self.session.commit()
        self.session.refresh(prestamo)
        return prestamo