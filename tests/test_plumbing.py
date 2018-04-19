def test_keybase_txt(client):
    FINGERPRINT = "4e69ca38ba02e8606fa0d78bed232f64bc5a4983"
    resp = client.get('/.well-known/keybase.txt')

    assert resp.status_code == 200
    assert FINGERPRINT in resp.get_data(as_text=True)



