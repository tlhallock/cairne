import logging
import sys
from dotenv import load_dotenv


import structlog

from cairne.serve.serve import serve

if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    structlog.configure()
    serve()
