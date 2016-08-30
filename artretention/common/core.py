import sys
import os
import datetime
import getpass

_credentials = {}

_epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return int((dt - _epoch).total_seconds() * 1000.0)

def progress (count, total, prefix = '', suffix = '', decimals = 2):
    bar_length = 20
    if total > 0:
        filled_len = int(round(bar_length * count / float(total)))
        percents = round(100.0 * count / float(total), 1)
    else:
        filled_len = int(round(bar_length * 1 / float(1)))
        percents = round(100.0 * 1 / float(1), 1)

    bar = '=' * filled_len + '-' * (bar_length - filled_len)

    sys.stdout.write('%s[%s] %s%s - %s\r' % (prefix, bar, percents, '%', suffix.ljust(38)[:37]))
    sys.stdout.flush()

def get_credentials(credentialType, user_env='USER', password_env='PASSWORD'):
  global _credentials

  if credentialType not in _credentials:
    usernameVar = '%s_%s' % (credentialType.upper(), user_env.upper())
    username = os.environ.get(usernameVar, os.environ.get('USER', None))

    passwordVar = '%s_%s' % (credentialType.upper(), password_env.upper())
    password = None
    if passwordVar in os.environ:
      password = os.environ[passwordVar]
    else:
      password = getpass.getpass('%s Password (%s): ' % (username, credentialType))

    _credentials[credentialType] = (username,password)

  return _credentials[credentialType]

def echo(string,nl=True):
  if nl:
    sys.stdout.write(string+'\n')
  else:
    sys.stdout.write(string)
  sys.stdout.flush()
