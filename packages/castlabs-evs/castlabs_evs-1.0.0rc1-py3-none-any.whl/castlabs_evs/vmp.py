# Copyright 2020, castLabs GmbH

from .core.error import *
from .core.util import detect_bin, gather
from .auth import Auth

import builtins
from sys import maxsize
from os import environ, path, rename, remove
from datetime import datetime, timedelta
from binascii import a2b_base64, b2a_base64
import json
from glob import glob
from zlib import compress

from macholib import MachO, mach_o

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.hashes import Hash, SHA1, SHA512
from cryptography.x509 import load_der_x509_certificate, ObjectIdentifier
from cryptography.x509.oid import NameOID, ExtensionOID, ExtendedKeyUsageOID
from cryptography.hazmat.primitives.asymmetric.padding import PSS, MGF1
from cryptography.exceptions import InvalidSignature

import requests

################################################################################

DEFAULT_API_URL = 'https://evs-api.castlabs.com'

################################################################################

ExtensionOID.VMP_DEVELOPMENT = ObjectIdentifier('1.3.6.1.4.1.11129.4.1.2')
ExtensionOID.VMP_PERSISTENT = ObjectIdentifier('1.3.6.1.4.1.11129.4.1.3')

STREAMING_SIGNATURE='streaming'
PERSISTENT_SIGNATURE='persistent'

SUBJECT_KEY_IDENTIFIERS = {
  STREAMING_SIGNATURE: [ b'\x0f\x02\xae\xdf\xf7\xe5\xca\x19\nK\xc4$\xdb\xfat\xb5i\x97\x18\x8c' ],
  PERSISTENT_SIGNATURE: [ b'\nmV\xb5\xae\x8e\xaf\x17\x16Y\x0e#\xd2lUS\xea\x7fW\xb5' ]
}
AUTHORITY_KEY_IDENTIFIERS = [ b'\xca=\xd8\x8e\x0ftW\x7f\xd0\x9a\xd9\xe1!\xbfB\xfb#U)\x86' ]

################################################################################

class Signature(object):
  def __init__(self, fh):
    def decode_byte(fh):
      b = fh.read(1)
      return ord(b) if b else None
    def decode_leb128(f):
      shift = 0
      val = 0
      while True:
        b = decode_byte(f)
        if b is None:
          return None
        val |= (b & 0x7f) << shift
        if not (b & 0x80):
          break
        shift += 7
      return val
    def decode_bytes(fh):
      n = decode_leb128(fh)
      b = fh.read(n) if n is not None else None
      return b if b else None
    def decode_entry(f):
      return decode_byte(fh), decode_bytes(fh)
    self.version = decode_byte(fh)
    if self.version not in range(0, 1):
      raise UnsupportedError('Unsupported signature file version')
    self.cert, self.data, self.flags = None, None, None
    while True:
      tag, entry = decode_entry(fh)
      if tag is None:
        break
      if 1 == tag:
        self.cert = entry
      elif 2 == tag:
        self.data = entry
      elif 3 == tag:
        self.flags = entry
    if None in (self.cert, self.data, self.flags):
      raise InvalidDataError('Invalid signature file')
    if ord(self.flags) not in range(0, 2):
      raise InvalidDataError('Invalid signature file flags')

class Validator(object):
  def __init__(self, kind, min_days, block_size=2*1024*1024, backend=default_backend()):
    self.kind = kind
    self.min_days = min_days
    self.block_size = block_size
    self.backend = backend

  def _hash_macho_wv0(self, fh):
    headers = MachO.MachO(fh.name).headers
    hasher = Hash(SHA512(), self.backend)
    for header in headers:
      fh.seek(header.offset, 0)
      start, end = maxsize, 0
      for (lc, segment, sections) in header.commands:
        # The minimum section offset of all load commands is the start of VMP signing part
        if (lc.cmd in (mach_o.LC_SEGMENT_64, mach_o.LC_SEGMENT) and
          segment.segname.startswith(mach_o.SEG_TEXT.encode('utf-8'))):
          for section in sections:
            start = min(start, section.offset)
        # Expect the String Table is at the end of unsigned binary followed by the code
        # signature, so the end of String Table is the end of VMP signing part
        if (mach_o.LC_SYMTAB == lc.cmd):
          end = segment.stroff + segment.strsize
      if (start >= end):
        raise InvalidDataError('Failed to assemble VMP/Mach-O signing body: %d-%d' % (start, end))
      fh.seek(start, 1)
      while start < end:
        data = fh.read(min(end - start, self.block_size))
        start += len(data)
        hasher.update(data)
    return hasher.finalize()

  def _hash_pe_wv0(self, fh):
    hasher = Hash(SHA512(), self.backend)
    while True:
      data = fh.read(self.block_size)
      if not data: break
      hasher.update(data)
    return hasher.finalize()

  def _hash_bin(self, bin):
    with open(bin, 'rb') as fh:
      fmt, _, _ = detect_bin(fh)
      if fmt == 'macho':
        return self._hash_macho_wv0(fh)
      elif fmt == 'pe':
        return self._hash_pe_wv0(fh)
      raise UnsupportedError('Binary type or archtecture not supported')

  def verify(self, bin, sig, no_raise=False):
    try:
      with open(bin, 'rb') as fh:
        fmt, p, a = detect_bin(fh)
        if fmt == 'macho':
          vd = self._hash_macho_wv0(fh)
        elif fmt == 'pe':
          vd = self._hash_pe_wv0(fh)
        else:
          raise UnsupportedError('Binary type or archtecture not supported')
    except Exception as e:
      raise InvalidDataError('Failed to generate verification digest') from e

    if 'win32' == p:
      dir, name = path.split(bin)
      if name != 'electron.exe':
        o = path.join(dir, 'electron.exe.sig')
        if path.isfile(o):
          if not path.isfile(sig):
            rename(o, sig)
          elif not path.samefile(o, sig):
            remove(o)

    try:
      with open(sig, 'rb') as fh:
        s = Signature(fh)
    except Exception as e:
      raise InvalidDataError('Failed to decode signature') from e

    if ord(s.flags) != 1:
      raise ValidityError('Signature flags are not valid')

    try:
      cert = load_der_x509_certificate(s.cert, backend=self.backend)
    except Exception as e:
      raise InvalidDataError('Failed to load certificate') from e
    try:
      cert.public_key().verify(s.data, vd + s.flags, PSS(mgf=MGF1(SHA1()), salt_length=20), SHA1())
    except Exception as e:
      raise InvalidDataError('Failed to verify signature') from e

    now = datetime.now()
    if now < cert.not_valid_before:
      raise ValidityError('Certificate not yet valid')
    if self.min_days is not None and now > (cert.not_valid_after - timedelta(days=self.min_days)):
      raise ValidityError('Certificate expires in less than {} days'.format(self.min_days))

    ski = aki = ku = eku = vp = vd = None
    for e in cert.extensions:
      if ExtensionOID.SUBJECT_KEY_IDENTIFIER == e.oid:
        ski = e.value
      elif ExtensionOID.AUTHORITY_KEY_IDENTIFIER == e.oid:
        aki = e.value
      elif ExtensionOID.KEY_USAGE == e.oid:
        ku = e.value
      elif ExtensionOID.EXTENDED_KEY_USAGE == e.oid:
        eku = e.value
      elif ExtensionOID.VMP_PERSISTENT == e.oid:
        vp = e.value
      elif ExtensionOID.VMP_DEVELOPMENT == e.oid:
        vd = e.value
    if vd:
      raise ValidityError('Certificate is valid for development only')
    if (vp and STREAMING_SIGNATURE == self.kind) or (not vp and PERSISTENT_SIGNATURE == self.kind):
      raise ValidityError('Certificate doesn\'t match \'{}\' signature kind'.format(self.kind))
    if not eku or ExtendedKeyUsageOID.CODE_SIGNING not in eku:
      raise ValidityError('Certificate doesn\'t allow code signing')
    if not ku or not ku.digital_signature:
      raise ValidityError('Certificate doesn\'t allow digital signatures')
    if not aki or aki.key_identifier not in AUTHORITY_KEY_IDENTIFIERS:
      raise ValidityError('Certificate has invalid AuthorityKeyIdentifier')
    if not ski or ski.digest not in SUBJECT_KEY_IDENTIFIERS.get(self.kind, []):
      raise ValidityError('Certificate has invalid SubjectKeyIdentifier')

################################################################################

class VMP(Auth):
  def __init__(self, no_ask=True, api_url=None, **_):
    api_url = api_url or environ.get('EVS_API_URL', DEFAULT_API_URL)
    self.broker_url = '{}/{}'.format(api_url, 'broker')
    self.signer_url = '{}/{}'.format(api_url, 'signer')
    super().__init__(no_ask=no_ask)

  def _request_upload(self, gz=False):
    try:
      while True:
        r = requests.get(self.broker_url,
          params=None if not gz else {'gz': ''},
          headers={
            'Authorization': self._auth_id_token,
            'Accept': 'application/json',
          }
        )
        if r.status_code not in (401, 403) or not self._refresh_auth():
          break
    except Exception as e:
      raise RequestError('Request for upload URL failed') from e
    try:
      j = r.json()
    except Exception as e:
      raise InvalidDataError('Failed to parse JSON body in upload URL response') from e
    if r.status_code != 200 or 'errorMessage' in j or 'message' in j:
      e = gather(j)
      raise HTTPError('Request for upload URL failed: {} {}'.format(r.status_code, r.reason)) from e
    if 'key' not in j:
      raise InvalidDataError('No \'key\' returned in upload URL response')
    if 'url' not in j:
      raise InvalidDataError('No \'url\' returned in upload URL response')
    return (j['key'], j['url'])

  def _upload_data(self, data, gz=False):
    key, url = self._request_upload(gz)
    gz = key.endswith('.gz')
    try:
      r = requests.put(url,
        data=data if not gz else compress(data.read()),
        headers={
          'Content-Type': 'application/octet-stream' if not gz else 'application/gzip',
        }
      )
    except Exception as e:
      raise RequestError('Upload request failed') from e
    if r.status_code != 200:
      raise HTTPError('Upload request failed: {} {}'.format(r.status_code, r.reason))
    return key

  def _upload_file(self, bin, gz=False):
    with open(bin, 'rb') as fh:
      return self._upload_data(fh, gz)

  def _sign(self, key, kind):
    try:
      while True:
        r = requests.get(self.signer_url,
          params={'key': key, 'kind': kind},
          headers={
            'Authorization': self._auth_id_token,
            'Accept': 'application/json',
          }
        )
        if r.status_code not in (401, 403) or not self._refresh_auth():
          break
    except Exception as e:
      raise RequestError('Signing request failed') from e
    try:
      j = r.json()
    except Exception as e:
      raise InvalidDataError('Failed to parse JSON body in signing response') from e
    if r.status_code != 200 or 'errorMessage' in j or 'message' in j:
      e = gather(j)
      raise HTTPError('Signing request failed: {} {}'.format(r.status_code, r.reason)) from e
    if 'key' not in j:
      raise InvalidDataError('No \'key\' returned in signing response')
    if key != j['key']:
      raise InvalidDataError('Mismatching \'key\' returned in signing response')
    if 'sig' not in j:
      raise InvalidDataError('No \'sig\' returned in signing response')
    return a2b_base64(j['sig'])

  def _store(self, sig, sig_data):
    with open(sig, 'wb') as fh:
      fh.write(sig_data)

  def verify(self, bin, sig=None, kind=None, min_days=None, **_):
    sig = sig or (bin + '.sig')
    kind = kind or environ.get('EVS_KIND', STREAMING_SIGNATURE)
    print('Verifying any existing VMP signature')
    try:
      Validator(kind, min_days).verify(bin, sig)
      print(' - Signature is valid [{}, min {} days validity]'.format(kind, min_days))
    except Exception as e:
      print(' - Signature invalid:', e)
      raise

  def sign(self, bin, sig=None, kind=None, min_days=None, force=False, gz=False, account_name=None, passwd=None, **_):
    sig = sig or (bin + '.sig')
    key = environ.get('EVS_KEY', None)
    kind = kind or environ.get('EVS_KIND', STREAMING_SIGNATURE)
    force = force or 'EVS_FORCE' in environ
    if not force:
      print('Verifying any existing VMP signature')
      try:
        Validator(kind, min_days).verify(bin, sig)
        print(' - Signature is valid ({}, min {} days validity), {} signing'.format(kind, min_days, 'force' if force else 'forego'))
        if not force:
          return
      except Exception as e:
        print(' - Signature invalid:', e)
    print('Requesting VMP signature')
    self._check_auth(account_name, passwd)
    sig_data = self._sign(key or self._upload_file(bin, gz), kind)
    self._store(sig, sig_data)

  def _detect_pkg(self, dir, name=None):
    def _to_pattern(n):
      return ''.join(('[{}{}]'.format(c.upper(), c.lower()) if c.isalpha() else c) for c in n)
    def _try_app(app):
      if path.isdir(app):
        fwdir = 'Contents/Frameworks/Electron Framework.framework/Versions/A'
        fwbin = path.join(app, fwdir, 'Electron Framework')
        if path.isfile(fwbin):
          fwsig = path.join(app, fwdir, 'Resources/Electron Framework.sig')
          return (app, fwbin, fwsig)
      raise FileNotFoundError()
    def _try_exe(exe):
      if path.isfile(exe):
        sig = '{}.sig'.format(exe)
        return (exe, exe, sig)
      raise FileNotFoundError()
    ps = []
    if not name:
      ps.append(_to_pattern('electron'))
      ps.append('*')
    else:
      ps.append(_to_pattern(name))

    for p in ps:
      p = path.join(dir, p)
      try:
        for m in glob('{}.app'.format(p)):
          return _try_app(m)
      except FileNotFoundError:
        pass
      try:
        for m in glob('{}.exe'.format(p)):
          return _try_exe(m)
      except FileNotFoundError:
        pass
    raise FileNotFoundError()

  def verify_pkg(self, pkg, name=None, kind=None, min_days=None, **_):
    for pkg in pkg if isinstance(pkg, list) else [ pkg ]:
      try:
        nm, bin, sig = self._detect_pkg(pkg, name)
      except FileNotFoundError:
        continue
      print('Verifying: {}'.format(nm))
      self.verify(bin, sig, kind, min_days)

  def sign_pkg(self, pkg, name=None, kind=None, min_days=None, force=False, gz=False, account_name=None, passwd=None, **_):
    for pkg in pkg if isinstance(pkg, list) else [ pkg ]:
      try:
        nm, bin, sig = self._detect_pkg(pkg, name)
      except FileNotFoundError:
        continue
      print('Signing: {}'.format(nm))
      self.sign(bin, sig, kind, min_days, force, gz, account_name, passwd)

################################################################################

if __name__ == '__main__':
  from .cli.vmp import main
  main()

################################################################################
