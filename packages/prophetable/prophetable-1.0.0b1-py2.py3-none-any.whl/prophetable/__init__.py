__version__ = "1.0.0b1"

import logging

log_format = "🔮Prophetable | %(asctime)s | %(name)s | %(levelname)s | %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)

from prophetable.prophetable import Prophetable
