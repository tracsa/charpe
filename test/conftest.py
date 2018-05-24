from itacate import Config
import os
import pytest


@pytest.fixture
def config():
    ''' Returns a fully loaded configuration dict '''
    con = Config(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)), '..'
        )
    )

    con.from_object('charpe.settings')

    return con
