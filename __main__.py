#!/usr/bin/env python3
from . import NetWatcher, NetConfig
import argparse
import sys,os

parser = argparse.ArgumentParser(description="Monitor your Internet connection. Start a secondary connection and send you the IP if it goes down.")
parser.add_argument('-c', '--config', help="Config file. Default=/usr/local/etc/pircons.ini", default='/usr/local/etc/pircons.ini')

def main(args):
	cfg = NetConfig(args.config)
	nw = NetWatcher(cfg.query_class(), cfg.notify_class(), cfg.activate_class())
	nw.poll()
	sys.exit(0)

if __name__ == '__main__':
	main(parser.parse_args())
	sys.exit(255) # Shouldn't get here.