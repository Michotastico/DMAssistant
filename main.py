#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import time

from src.telegram_bot import DMAssistant

__author__ = "Michel Llorens"
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "mllorens@dcc.uchile.cl"


TOKEN = sys.argv[1]
DM_ID = int(sys.argv[2])

bot = DMAssistant(TOKEN, DM_ID)

while True:
    time.sleep(10)
