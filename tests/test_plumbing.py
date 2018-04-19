def test_keybase_txt(client):
    FINGERPRINT = "4e69ca38ba02e8606fa0d78bed232f64bc5a4983"
    resp = client.get('/.well-known/keybase.txt')

    assert resp.status_code == 200
    assert FINGERPRINT in resp.get_data(as_text=True)


def test_pgp_key(client):
    HEADER = "-----BEGIN PGP PUBLIC KEY BLOCK-----"
    resp = client.get('/pgp')

    assert resp.status_code == 200
    assert resp.get_data(as_text=True).startswith(HEADER)
    assert (resp.headers.get('content-disposition').lower()
            .startswith('attachment'))
    assert resp.content_type.lower() == 'application/pgp-keys'


def test_authorized_keys(client):
    resp = client.get('/ssh')

    assert resp.status_code == 200
    assert resp.get_data(as_text=True).startswith('ssh-')
