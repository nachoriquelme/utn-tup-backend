def test_crud_libros_relacion_autores_y_disponibles(client):
    autor = client.post(
        "/autores", json={"nombre": "Julio Cortázar", "nacionalidad": "Argentina"}
    ).json()

    l1 = client.post(
        "/libros",
        json={"titulo": "Rayuela", "isbn": "978-8437604572", "stock": 2, "anio": 1963},
    )
    assert l1.status_code == 201
    libro1 = l1.json()

    l2 = client.post(
        "/libros",
        json={"titulo": "Bestiario", "isbn": "978-8420471839", "stock": 0, "anio": 1951},
    )
    assert l2.status_code == 201

    # Regla 8: ISBN duplicado -> 409
    dup = client.post(
        "/libros",
        json={"titulo": "Copia", "isbn": "978-8437604572", "stock": 1, "anio": 2000},
    )
    assert dup.status_code == 409

    # Relación N-N
    asoc = client.post(f"/libros/{libro1['id']}/autores/{autor['id']}")
    assert asoc.status_code == 200
    assert len(asoc.json()["autores"]) == 1
    assert asoc.json()["autores"][0]["id"] == autor["id"]

    # Filtro ?disponibles=true
    disp = client.get("/libros?disponibles=true").json()
    assert len(disp) == 1
    assert disp[0]["titulo"] == "Rayuela"

    # Eliminar libro y verificar 404
    assert client.delete(f"/libros/{libro1['id']}").status_code == 204
    assert client.get(f"/libros/{libro1['id']}").status_code == 404