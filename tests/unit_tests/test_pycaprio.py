import os

import pytest

from pycaprio import Pycaprio
from pycaprio.core.exceptions import ConfigurationNotProvided


@pytest.mark.parametrize('host, auth', [(None, None),
                                        ('', (None, None)),
                                        ('host', (None, None)),
                                        ('', ('test', 'test'))
                                        ])
def test_pycaprio_no_host_raises_exception(host, auth):
    with pytest.raises(ConfigurationNotProvided):
        Pycaprio(host, auth)


def test_pycaprio_gets_host_from_os_env():
    os.environ['INCEPTION_HOST'] = 'host'
    try:
        Pycaprio(authentication=('a', 'b'))
    except:
        pytest.fail()


def test_pycaprio_gets_auth_from_os_env():
    os.environ['INCEPTION_USERNAME'] = 'test'
    os.environ['INCEPTION_PASSWORD'] = 'passwd'
    try:
        Pycaprio(inception_host="host")
    except:
        pytest.fail()
