from datetime import date, timedelta

from models.autor import Autor
from models.libro import Libro
from models.prestamo import Prestamo
from models.socio import Socio
from repositories.autor_repository import AutorRepository
from repositories.libro_repository import LibroRepository
from repositories.prestamo_repository import PrestamoRepository
from repositories.socio_repository import SocioRepository


def test_repositorios_basicos(session):
    autor_repo = AutorRepository(session)
    libro_repo = LibroRepository(session)
    socio_repo = SocioRepository(session)
    prestamo_repo = PrestamoRepository(session)

    autor = autor_repo.create(Autor(nombre="Adolfo Bioy Casares", nacionalidad="Argentina"))
    libro = libro_repo.create(
        Libro(titulo="La invención de Morel", isbn="ISBN-MOREL", stock=2, anio=1940)
    )
    libro = libro_repo.add_autor(libro, autor)
    assert len(libro.autores) == 1
    assert libro_repo.get_by_isbn("ISBN-MOREL") is not None
    assert libro_repo.has_prestamos(libro.id) is False

    socio = socio_repo.create(
        Socio(nombre="Elena", email="elena@ejemplo.com", activo=True)
    )
    assert socio_repo.get_by_email("elena@ejemplo.com") is not None

    fecha_inicio = date(2026, 11, 1)
    libro.stock -= 1
    prestamo = prestamo_repo.create_with_stock_update(
        Prestamo(
            socio_id=socio.id,
            libro_id=libro.id,
            fecha_prestamo=fecha_inicio,
            fecha_vencimiento=fecha_inicio + timedelta(days=14),
        ),
        libro,
    )
    assert prestamo_repo.count_activos_by_socio(socio.id) == 1
    assert len(prestamo_repo.get_by_socio(socio.id, activos=True)) == 1
    assert len(prestamo_repo.get_by_socio(socio.id, activos=False)) == 0
    assert libro_repo.has_prestamos(libro.id) is True