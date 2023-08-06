# Copyright 2020, castLabs GmbH

from .error import UnsupportedError

from os import environ

################################################################################

def detect_bin(fh):
  h = fh.peek(512)
  if h[:8] == b'\xcf\xfa\xed\xfe\x07\x00\x00\x01':
    return ('macho', 'darwin', 'x64')
  elif h[:2] == b'MZ':
    o = int.from_bytes(h[60:64], byteorder='little')
    if o < len(h):
      s = h[o:o + 6]
      if s == b'\x50\x45\x00\x00\x64\x86':
        return ('pe', 'win32', 'x64')
      elif s == b'\x50\x45\x00\x00\x4c\x01':
        return ('pe', 'win32', 'ia32')
  raise UnsupportedError('Binary type or archtecture not supported')

################################################################################

class _ForwardError_(Exception):
  def __init__(self, cls, msg):
    self._forward_class_name_ = cls
    super().__init__(msg)

class _ForwardArgs_(object):
  def __init__(self, fn, *args, **kwargs):
    self._fn_ = fn
    self._args_ = args
    self._kwargs_ = kwargs
  def __call__(self, *args, **kwargs):
    return self._fn_(*self._args_, *args, **self._kwargs_, **kwargs)

def conclude(e):
  j = {
    'errorType': getattr(e, '_forward_class_name_', e.__class__.__name__),
    'errorMessage': str(e),
  }
  if e.__cause__:
    j['errorCause'] = conclude(e.__cause__)
  return j

def gather(j):
  from . import error
  import builtins
  t = j.get('errorType', 'UnknownError')
  c = getattr(error, t, getattr(builtins, t, _ForwardArgs_(_ForwardError_, t)))
  e = c(j.get('errorMessage', j.get('message', 'No message')))
  if 'errorCause' in j:
    e.__cause__ = gather(j['errorCause'])
  return e

################################################################################

def die(e, code=1):
  if 'EVS_TRACE' in environ:
    raise e
  print('{}: {}'.format(getattr(e, '_forward_class_name_', e.__class__.__name__), e))
  e = e.__cause__
  while e:
    print(' <- {}: {}'.format(getattr(e, '_forward_class_name_', e.__class__.__name__), e))
    e = e.__cause__
  raise SystemExit(code)

################################################################################
