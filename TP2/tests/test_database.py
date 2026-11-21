from sqlmodel import Session, SQLModel, create_engine, select
from sqlmodel.pool import StaticPool

import database
from database import create_db_and_tables, get_session
from models.autor import Autor
from models.libro import Libro
from models.libro_autor import LibroAutor
from models.prestamo import Prestamo
from models.socio import Socio


def test_modelos_registrados_en_metadata():
    expected_tables = {"autor", "libro", "libroautor", "socio", "prestamo"}
    assert expected_tables.issubset(set(SQLModel.metadata.tables.keys()))


def test_create_db_and_tables_con_engine_en_memoria(monkeypatch):
    mem_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    monkeypatch.setattr(database, "engine", mem_engine)

    create_db_and_tables()

    with Session(mem_engine) as session:
        autor = Autor(nombre="Silvina Ocampo", nacionalidad="Argentina")
        session.add(autor)
        session.commit()
        session.refresh(autor)

        resultados = session.exec(select(Autor).where(Autor.id == autor.id)).all()
        assert len(resultados) == 1
        assert resultados[0].nombre == "Silvina Ocampo"


def test_get_session_genera_sesion_activa(monkeypatch):
    mem_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(mem_engine)
    monkeypatch.setattr(database, "engine", mem_engine)

    gen = get_session()
    session = next(gen)
    assert isinstance(session, Session)
    assert session.is_active

    try:
        next(gen)
    except StopIteration:
        pass