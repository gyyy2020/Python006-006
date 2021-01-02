#!/usr/bin/env python
from pathlib import Path
import logging
import time


def test():
    time_today = time.strftime('%Y-%m-%d')
    log_dir = f'/var/log/python-{time_today}/'
    p = Path(log_dir)
    if not p.exists():
        p.mkdir()

    logging.basicConfig(
    level=logging.INFO,
    filename=log_dir + 'test.log',
    datefmt='%Y-%m-%d %H:%M:%S',
    format='%(asctime)s %(levelname)-5s [line:%(lineno)d] %(message)s')

    logging.info('function called')


if __name__ == '__main__':
    test()
