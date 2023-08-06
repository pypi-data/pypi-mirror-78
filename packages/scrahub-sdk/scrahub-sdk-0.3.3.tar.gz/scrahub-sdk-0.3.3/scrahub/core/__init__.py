import os

home = os.curdir

if 'HOME' in os.environ:
    home = os.environ['HOME']
elif os.name == 'posix':
    home = os.path.expanduser('~/')
elif os.name == 'nt':
    if 'HOMEPATH' in os.environ and 'HOMEDRIVE' in os.environ:
        home = os.environ['HOMEDRIVE'] + os.environ['HOMEPATH']
elif 'HOMEPATH' in os.environ:
    home = os.environ['HOMEPATH']

SCRAHUB_ROOT = os.path.join(home, '.scrahub')
SCRAHUB_TMP = os.path.join(SCRAHUB_ROOT, 'tmp')

if not os.path.exists(SCRAHUB_ROOT):
    os.mkdir(SCRAHUB_ROOT)

if not os.path.exists(SCRAHUB_TMP):
    os.mkdir(SCRAHUB_TMP)
