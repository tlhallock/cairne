import logging
import sys

import structlog

from cairne.serve.serve import serve

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    structlog.configure()
    serve()
