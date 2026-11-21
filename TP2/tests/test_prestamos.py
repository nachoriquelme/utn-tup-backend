from datetime import date, timedelta


def test_regla_1_maximo_3_prestamos_activos(client):
    socio = client.post(
        "/socios", json={"nombre": "Carlos", "email": "carlos@ejemplo.com", "activo": True}
    ).json()

    libros = [
        client.post(
            "/libros",
            json={"titulo": f"Libro {i}", "isbn": f"ISBN-{i}", "stock": 5, "anio": 2020},
        ).json()
        for i in range(4)
    ]

    for i in range(3):
        res = client.post(
            "/prestamos", json={"socio_id": socio["id"], "libro_id": libros[i]["id"]}
        )
        assert res.status_code == 201

    activos = client.get(f"/socios/{socio['id']}/prestamos?activos=true").json()
    assert len(activos) == 3

    res_4 = client.post(
        "/prestamos", json={"socio_id": socio["id"], "libro_id": libros[3]["id"]}
    )
    assert res_4.status_code == 409


def test_regla_2_sin_stock_y_descuento(client):
    socio = client.post(
        "/socios", json={"nombre": "Lucía", "email": "lucia@ejemplo.com", "activo": True}
    ).json()
    libro = client.post(
        "/libros", json={"titulo": "Ficciones", "isbn": "ISBN-FICC", "stock": 1, "anio": 1944}
    ).json()

    p1 = client.post(
        "/prestamos", json={"socio_id": socio["id"], "libro_id": libro["id"]}
    )
    assert p1.status_code == 201
    assert client.get(f"/libros/{libro['id']}").json()["stock"] == 0

    p2 = client.post(
        "/prestamos", json={"socio_id": socio["id"], "libro_id": libro["id"]}
    )
    assert p2.status_code == 409


def test_regla_3_socio_inactivo(client):
    socio = client.post(
        "/socios", json={"nombre": "Inactivo", "email": "inac@ejemplo.com", "activo": False}
    ).json()
    libro = client.post(
        "/libros", json={"titulo": "El Aleph", "isbn": "ISBN-ALEPH", "stock": 3, "anio": 1949}
    ).json()

    res = client.post(
        "/prestamos", json={"socio_id": socio["id"], "libro_id": libro["id"]}
    )
    assert res.status_code == 403


def test_reglas_4_5_6_7_plazo_devolucion_multa_y_errores(client):
    socio = client.post(
        "/socios", json={"nombre": "Martín", "email": "martin@ejemplo.com", "activo": True}
    ).json()
    libro = client.post(
        "/libros", json={"titulo": "1984", "isbn": "ISBN-1984", "stock": 2, "anio": 1949}
    ).json()

    fecha_inicio = date(2026, 11, 1)
    prestamo = client.post(
        "/prestamos",
        json={
            "socio_id": socio["id"],
            "libro_id": libro["id"],
            "fecha_prestamo": fecha_inicio.isoformat(),
        },
    ).json()

    # Regla 4: +14 días
    assert prestamo["fecha_vencimiento"] == (fecha_inicio + timedelta(days=14)).isoformat()
    assert client.get(f"/libros/{libro['id']}").json()["stock"] == 1

    # Regla 5: 3 días de atraso -> multa $300 y reposición de stock
    fecha_dev = fecha_inicio + timedelta(days=17)
    dev = client.post(
        f"/prestamos/{prestamo['id']}/devolucion",
        json={"fecha_devolucion": fecha_dev.isoformat()},
    )
    assert dev.status_code == 200
    assert dev.json()["multa"] == 300.0
    assert client.get(f"/libros/{libro['id']}").json()["stock"] == 2

    # Regla 6: ya devuelto -> 409
    assert client.post(f"/prestamos/{prestamo['id']}/devolucion").status_code == 409

    # Regla 7: inexistente -> 404
    assert client.post("/prestamos/9999/devolucion").status_code == 404


def test_devolucion_a_tiempo_sin_multa(client):
    socio = client.post(
        "/socios", json={"nombre": "Sofía", "email": "sofia@ejemplo.com", "activo": True}
    ).json()
    libro = client.post(
        "/libros", json={"titulo": "Dune", "isbn": "ISBN-DUNE", "stock": 1, "anio": 1965}
    ).json()

    fecha_inicio = date(2026, 11, 1)
    prestamo = client.post(
        "/prestamos",
        json={
            "socio_id": socio["id"],
            "libro_id": libro["id"],
            "fecha_prestamo": fecha_inicio.isoformat(),
        },
    ).json()

    dev = client.post(
        f"/prestamos/{prestamo['id']}/devolucion",
        json={"fecha_devolucion": (fecha_inicio + timedelta(days=10)).isoformat()},
    )
    assert dev.status_code == 200
    assert dev.json()["multa"] == 0.0
