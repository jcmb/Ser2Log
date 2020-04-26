#!/usr/bin/env python3

import sys

try:
   import serial
except:
   print ("Module serial must be available")

import argparse

import logging
import logging.handlers
#import syslog

logger = logging.getLogger("Ser2Log.py")
#logging.basicConfig(format='%(process)d-%(levelname)s-%(message)s')

handler = logging.handlers.SysLogHandler(address='/dev/log')
formatter = logging.Formatter('%(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.setLevel(logging.INFO)



def get_args():
   parser = argparse.ArgumentParser(description='Sends data from a serila port to syslog')

   parser.add_argument('--port', type=str, default="/dev/ttyUSB0", help='Serial port to listen on, default ttyUSB0')

   parser.add_argument("--baud", type=int, default=57600,help='Baud rate to listen on. Default is 57600')

   parser.add_argument("-T","--Tell", action='store_true',help="Tell the settings before starting")

   args = parser.parse_args()

   if args.Tell:
      print ("Port: {}".format(args.port))
      print ("Baud: {}".format(args.baud))

   return(args.port, args.baud)

def main():

   (port,baud)=get_args()
   logger.info('Processing started')
   comm=serial.Serial(port=port,baudrate=baud,timeout=1)
   while True:
      line=comm.readline().strip()
      line=line.decode("cp1252")
      if line != '':
         print (line)
         logger.info(line)

if __name__ == "__main__":
#    print(sys.argv)
#    print(len(sys.argv))

    main()
