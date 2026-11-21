def test_sin_header_rol_retorna_401(client):
    res = client.get("/libros", headers={"X-Role": ""})
    assert res.status_code == 401


def test_socio_no_puede_administrar_catalogo(client):
    headers_socio = {"X-Role": "socio", "X-Socio-Id": "1"}

    # Puede consultar catálogo
    assert client.get("/libros", headers=headers_socio).status_code == 200
    assert client.get("/autores", headers=headers_socio).status_code == 200

    # No puede crear/editar/eliminar libros ni autores
    assert (
        client.post(
            "/libros",
            headers=headers_socio,
            json={"titulo": "Prohibido", "isbn": "ISBN-PROH", "stock": 1, "anio": 2024},
        ).status_code
        == 403
    )
    assert (
        client.post(
            "/autores",
            headers=headers_socio,
            json={"nombre": "Autor Prohibido", "nacionalidad": "Argentina"},
        ).status_code
        == 403
    )


def test_socio_ve_unicamente_sus_prestamos(client):
    s1 = client.post(
        "/socios", json={"nombre": "Socio 1", "email": "s1@ejemplo.com", "activo": True}
    ).json()
    s2 = client.post(
        "/socios", json={"nombre": "Socio 2", "email": "s2@ejemplo.com", "activo": True}
    ).json()
    libro = client.post(
        "/libros", json={"titulo": "Rayuela", "isbn": "ISBN-RAY-1", "stock": 5, "anio": 1963}
    ).json()

    client.post("/prestamos", json={"socio_id": s1["id"], "libro_id": libro["id"]})
    client.post("/prestamos", json={"socio_id": s2["id"], "libro_id": libro["id"]})

    # Socio 1 ve sus propios préstamos
    res_propios = client.get(
        f"/socios/{s1['id']}/prestamos?activos=true",
        headers={"X-Role": "socio", "X-Socio-Id": str(s1["id"])},
    )
    assert res_propios.status_code == 200
    assert len(res_propios.json()) == 1
    assert res_propios.json()[0]["socio_id"] == s1["id"]

    # Socio 1 intenta ver préstamos de Socio 2 -> 403
    res_ajenos = client.get(
        f"/socios/{s2['id']}/prestamos?activos=true",
        headers={"X-Role": "socio", "X-Socio-Id": str(s1["id"])},
    )
    assert res_ajenos.status_code == 403