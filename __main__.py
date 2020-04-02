#!/usr/bin/env python3
from . import NetWatcher, NetConfig
import logging
import argparse
import sys,os

logger = logging.getLogger('pircons')
logger.setLevel(logging.DEBUG)
handlr = logging.StreamHandler()
frmttr = logging.Formatter('%(asctime)s : %(name)s[%(process)d] : %(levelname)s :: %(message)s')
if sys.stdout.isatty():
	handlr.setLevel(logging.DEBUG)
else:
	handlr.setLevel(logging.ERROR)
handlr.setFormatter(frmttr)
logger.addHandler(handlr)

parser = argparse.ArgumentParser(description="Monitor your Internet connection. Start a secondary connection and send you the IP if it goes down.")
parser.add_argument('-c', '--config', help="Config file. Default=/usr/local/etc/pircons.ini", default='/usr/local/etc/pircons.ini')

def main(args):
	cfg = NetConfig(args.config)
	nw = NetWatcher(cfg.query_class(), cfg.notify_class(), cfg.activate_class())
	nw.poll()
	sys.exit(0)

if __name__ == '__main__':
	args = parser.parse_args()
	logger.debug("Pircons started with arguments: %r" % args)
	main(args)
	sys.exit(255) # Shouldn't get here.