#!/usr/bin/env python3
from . import NetWatcher, NetConfig
import asyncio
import signal
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
	ACK = chr(6).encode('ascii')
	ENQ = chr(5).encode('ascii')
	STX = chr(2).encode('ascii')
	ETX = chr(3).encode('ascii')
	EOT = chr(4).encode('ascii')
	request = await reader.read(1)
	if request != ENQ:
		reader.close()
		writer.close()
		return None
	writer.write(ACK)
	await writer.drain()
	request = await reader.read(3)
	if (request[0] != STX) or (request[2] != ETX) or (request[1] not in b'01'):
		reader.close()
		writer.close()
		return None
	writer.write(ACK)
	await writer.drain()
	if request[1] == b'0':
		nw.trip()
	else:
		nw.reset()
	writer.write(EOT)
	await writer.drain()
	reader.close()
	writer.close()

async def poll_handler(nw):
	'''Periodically poll for internet connection status.
	:param nw: the active NetWatcher object
	:return: None
	'''
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
		raise cls()

def main(args):
	cfg = NetConfig(args.config)
	nw = NetWatcher(cfg.query_class(), cfg.notify_class(), cfg.activate_class())
	signal.signal(signal.SIGTERM, CleanExitException.exit_handler)
	loop = asyncio.get_event_loop()
	try:
		asyncio.ensure_future(poll_handler(nw))
		loop.create_task(asyncio.start_unix_server(functools.partial(socket_handler, nw=nw), path='/run/pircons/sock'))
		loop.run_forever()
	except (KeyboardInterrupt, CleanExitException):
		sys.exit(0)

if __name__ == '__main__':
	args = parser.parse_args()
	logger.debug("Pircons started with arguments: %r" % args)
	main(args)
	sys.exit(255) # Shouldn't get here.
