import os
import sys

import src.main as runner

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

if __name__ == "__main__":
    runner.auto()
