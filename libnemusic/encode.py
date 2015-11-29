import config
import hashlib
import os
import json
import base64
from Crypto.Cipher import AES

_xor_key = None
_xor_key_len = -1

_rsa_modulus = -1
_rsa_pubkey  = -1

_aes_nonce = None

def encode_id(song_id):
	"""Convert the plain text song id to encoded version
	   song_id the song id to convert """
	global _xor_key, _xor_key_len
	if not _xor_key:
		_xor_key = bytearray(config.get_config("XorKey", required = True))
		_xor_key_len = len(_xor_key)
	song_id = bytearray(song_id)
	curpos = 0
	for i in xrange(len(song_id)):
		song_id[i] ^= _xor_key[i % _xor_key_len]
	ret = hashlib.md5(song_id)
	ret = ret.digest().encode("base64").strip().replace('/', '_').replace('+', '-')
	return ret

def _get_aes_key():
	return os.urandom(16).encode("hex")

def _do_rsa(message):
	global _rsa_modulus, _rsa_pubkey
	if _rsa_modulus == -1:
		_rsa_modulus = config.get_config("RSAModulus", required = True)
		_rsa_pubkey  = config.get_config("RSAPubKey", required = True)
	data = int(message[::-1].encode('hex'), 16) % _rsa_modulus
	expo = data
	indx = _rsa_pubkey
	ret = 1
	while indx > 0:
		if indx % 2 == 1:
			ret = (ret * expo) % _rsa_modulus
		expo = (expo * expo) % _rsa_modulus
		indx /= 2
	ret = "%x"%ret
	return ret.zfill(256)

def _do_aes(message, key):
    pad = 16 - len(message) % 16
    message = message + pad * chr(pad)
    encryptor = AES.new(key, 2, '0102030405060708')
    ciphertext = encryptor.encrypt(message)
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext

def encode_account(account, password, phone = False):
	"""Encode an account infomation for login
	   account: The account ID, or the phone number
	   password: The password is going to use
	   phone: If this account Id is the phone Number"""
	global _aes_nonce
	if not _aes_nonce:
		_aes_nonce = config.get_config("AESNonce", required = True)
	data = {'password' : password, 'rememberLogin' : 'true' }
	if phone: 
		data['phone'] = account
	else:
		data['username'] = account
	raw_data = json.dumps(data)
	aes_key = _get_aes_key()
	enc_data = _do_rsa(_do_aes(_do_aes(raw_data, _aes_nonce), aes_key))
	return {'params': enc_data, 'encSecKey': aes_key}
	

if __name__ == "__main__": 
	pass
