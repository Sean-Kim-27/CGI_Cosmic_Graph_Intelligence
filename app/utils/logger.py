"""
Cosmic Graph Intelligence - 로거 설정
"""

import logging
import sys


def get_logger(name: str) -> logging.Logger:
    """모듈별 로거를 생성한다."""
    logger = logging.getLogger(f"cgi.{name}")
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter(
                "[%(asctime)s] %(levelname)-7s %(name)s — %(message)s",
                datefmt="%H:%M:%S",
            )
        )
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
