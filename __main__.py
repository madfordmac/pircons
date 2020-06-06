#!/usr/bin/env python3
from . import NetWatcher, NetConfig
import asyncio
import signal
import socket
import functools
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
mode = parser.add_mutually_exclusive_group(required=True)
mode.add_argument('-d', '--daemon', action='store_true', help="Run in daemon mode and monitor system.")
mode.add_argument('-t', '--trip', action='store_true', help="Trip the system and activate secondary connection.")
mode.add_argument('-r', '--reset', action='store_true', help="Reset the system for the primary connection.")

class S(object):
	"""Collect some constants for the socket protocol"""
	def __init__(self):
		super(S, self).__init__()

	ACK = chr(6).encode('ascii')
	ENQ = chr(5).encode('ascii')
	STX = chr(2).encode('ascii')
	ETX = chr(3).encode('ascii')
	EOT = chr(4).encode('ascii')

def socket_client(mode):
	'''Client for Unix socket to communicate with daemon. See socket_handler for protocol description.
	Mode:
	 - 0: Trip watcher
	 - 1: Reset watcher
	:param mode: What message should be sent down the socket? (See above.)
	:return: None
	'''
	if mode not in [0,1]:
		raise RuntimeError("Mode must be 0 or 1.")
	mode = str(mode).encode('ascii')
	s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	s.connect('/run/pircons/sock')
	logger.debug('Connection to socket established.')
	s.sendall(S.ENQ)
	request = s.recv(1)
	if request != S.ACK:
		s.close()
		logger.warning('Socket communication did not receive ACK.')
		return False
	s.sendall(S.STX + mode + S.ETX)
	request = s.recv(1)
	if request != S.ACK:
		s.close()
		logger.warning('Socket communication did not receive ACK.')
	request = s.recv(1)
	if request != S.EOT:
		s.close()
		logger.warning('Socket communication did not receive EOT.')
	verb = 'trip' if mode == b'0' else 'reset'
	logger.debug('Successfully sent message to %s the watcher.' % verb)
	return True

async def socket_handler(reader, writer, nw):
	'''Unix socket for enabling/disabling the secondary connection.
	Protocol:
	  - Client sends ENQ
	  - Server sends ACK
	  - Client sends STX + (0/1) + ETX
	  - Server sends ACK
	  - Server processes message: 0 = No internet/activate external; 1 = good internet/disable external
	  - Server sends EOT
	:param reader: The read pipe (required by start_server)
	:param writer: The write pipe (required by start_server)
	:param nw: the active NetWatcher object
	:return: None
	'''
	logger.debug('Started socket_handler to handle a connection.')
	request = await reader.read(1)
	if request != S.ENQ:
		logger.warning('Socket communication did not begin with ENQ.')
		return None
	writer.write(S.ACK)
	await writer.drain()
	request = await reader.read(3)
	if (request[0:1] != S.STX) or (request[2:3] != S.ETX) or (request[1:2] not in b'01'):
		logger.warning('Socket communication message not of correct format.')
		return None
	writer.write(S.ACK)
	await writer.drain()
	if request[1:2] == b'0':
		logger.debug('Message received on socket to trip the watcher.')
		nw.trip()
	else:
		logger.debug('Message received on socket to reset the watcher.')
		nw.reset()
	writer.write(S.EOT)
	await writer.drain()

async def poll_handler(nw):
	'''Periodically poll for internet connection status.
	:param nw: the active NetWatcher object
	:return: None
	'''
	logger.debug('Started poll_handler to poll for connectivity status.')
	while True:
		nw.poll()
		await asyncio.sleep(60)

class CleanExitException(Exception):
	@classmethod
	def exit_handler(cls, sig_no, stack_frame):
		'''Catch SIGTERM so we can exit 0 on request and something else if we die.
		:param sig_no: the signal number (required by signal)
		:param stack_frame: the current stack frame (required by signal)
		:return: None
		'''
		logger.debug('Using CleanExitException to shut down service.')
		raise cls()

def main(args):
	cfg = NetConfig(args.config)
	nw = NetWatcher(cfg.query_class(cfg), cfg.notify_class(cfg), cfg.activate_class(cfg))
	if args.daemon:
		signal.signal(signal.SIGTERM, CleanExitException.exit_handler)
		loop = asyncio.get_event_loop()
		try:
			asyncio.ensure_future(poll_handler(nw))
			loop.create_task(asyncio.start_unix_server(functools.partial(socket_handler, nw=nw), path='/run/pircons/sock'))
			loop.run_forever()
		except (KeyboardInterrupt, CleanExitException):
			sys.exit(0)
	elif args.trip:
		socket_client(0)
	elif args.reset:
		socket_client(1)
	else:
		logger.debug("Don't know how we got here, but somehow no mode option was chosen. Guess we'll quit.")
		sys.exit(255)

if __name__ == '__main__':
	args = parser.parse_args()
	logger.debug("Pircons started with arguments: %r" % args)
	main(args)
	sys.exit(255) # Shouldn't get here.
