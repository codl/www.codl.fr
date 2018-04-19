import sys
from pathlib import Path
import pytest

# when pytest is run, it doesn't add the cwd to the python import path,
# so we need to do it ourselves
PROJDIR = str(Path(__file__).parent.parent)
if PROJDIR not in sys.path:
    print(PROJDIR)
    sys.path.append(PROJDIR)


@pytest.fixture
def app():
    from codl import app
    return app
