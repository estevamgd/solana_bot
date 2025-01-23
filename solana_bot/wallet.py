import nacl.signing
import base58

def create_wallet():
    signing_key = nacl.signing.SigningKey.generate()
    verify_key = signing_key.verify_key

    public_key = base58.b58encode(verify_key.encode()).decode()
    private_key = base58.b58encode(signing_key.encode()).decode()

    return public_key, private_key
