import nacl.secret
import nacl.utils
import nacl.pwhash
import nacl.encoding
import hashlib
import codecs


class crypto:

    @staticmethod
    def encrypt(key, pwl):
        keyhash = hashlib.md5(key.encode("utf-8")).digest() + hashlib.md5(
            codecs.encode(key, 'rot_13').encode("utf-8")).digest()
        box = nacl.secret.SecretBox(keyhash, nacl.encoding.RawEncoder)
        nonce = nacl.utils.random(box.NONCE_SIZE)
        e = box.encrypt(pwl.encode(), nonce, nacl.encoding.HexEncoder)
        return e.decode()

    @staticmethod
    def decrypt(key, encrypted):
        keyhash = hashlib.md5(key.encode("utf-8")).digest() + hashlib.md5(
            codecs.encode(key, 'rot_13').encode("utf-8")).digest()
        box = nacl.secret.SecretBox(keyhash, nacl.encoding.RawEncoder)
        ret = box.decrypt(encrypted, None, nacl.encoding.HexEncoder)
        return ret.decode()
