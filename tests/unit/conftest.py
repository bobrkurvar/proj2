import pytest

from tests.fakes import FakeCRUD

@pytest.fixture
def crud():
    return FakeCRUD()
