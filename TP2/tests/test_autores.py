def test_crud_autores_y_404(client):
    res = client.post(
        "/autores", json={"nombre": "Jorge Luis Borges", "nacionalidad": "Argentina"}
    )
    assert res.status_code == 201
    autor = res.json()
    assert autor["nombre"] == "Jorge Luis Borges"

    assert len(client.get("/autores").json()) == 1
    assert client.get(f"/autores/{autor['id']}").status_code == 200

    upd = client.put(f"/autores/{autor['id']}", json={"nacionalidad": "Argentino"})
    assert upd.status_code == 200
    assert upd.json()["nacionalidad"] == "Argentino"

    assert client.delete(f"/autores/{autor['id']}").status_code == 204
    assert client.get(f"/autores/{autor['id']}").status_code == 404