from cairne.serve.serve import serve

import logging
import structlog
import sys


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    structlog.configure()
    serve()
