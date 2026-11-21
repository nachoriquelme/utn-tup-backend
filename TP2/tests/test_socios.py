def test_crud_socios_email_duplicado_y_404(client):
    s1 = client.post(
        "/socios",
        json={"nombre": "Ana Pérez", "email": "ana@ejemplo.com", "activo": True},
    )
    assert s1.status_code == 201
    socio = s1.json()

    assert len(client.get("/socios").json()) == 1
    assert client.get(f"/socios/{socio['id']}").status_code == 200

    # Regla 8: Email duplicado -> 409
    dup = client.post(
        "/socios",
        json={"nombre": "Ana Duplicada", "email": "ana@ejemplo.com", "activo": True},
    )
    assert dup.status_code == 409

    upd = client.put(f"/socios/{socio['id']}", json={"activo": False})
    assert upd.status_code == 200
    assert upd.json()["activo"] is False

    assert client.delete(f"/socios/{socio['id']}").status_code == 204
    assert client.get(f"/socios/{socio['id']}").status_code == 404