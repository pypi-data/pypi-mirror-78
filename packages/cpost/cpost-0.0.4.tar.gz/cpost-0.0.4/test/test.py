import sys
import unittest

sys.path.append(".")

# === unit tests ===
from test_api import *
from test_db import *
# ==================


# logging
if __name__ == "__main__":
    import logging
    logging.basicConfig(level = logging.WARNING)

# run unittests
if __name__ == "__main__":
    unittest.main()