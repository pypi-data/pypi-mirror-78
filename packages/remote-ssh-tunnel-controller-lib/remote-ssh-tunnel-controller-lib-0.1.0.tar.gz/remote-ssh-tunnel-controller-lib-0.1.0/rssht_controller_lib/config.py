import os

LIB_DIR = os.path.dirname(__file__)

RSSHT_SERVER_ADDR = '192.168.1.243'
RSSHT_SERVER_PORT = 443
RSSHT_SERVER_USERNAME = 'rssht-server'
KEY_FILENAME = os.path.join(LIB_DIR, 'id_rsa')

RSSHT_SERVER_SWAP_DIR = '$HOME/rssht-swap-dir'

RSSHT_CMD = 'rssht'
TERM_RSSHT_CMD = 'term-rssht'
