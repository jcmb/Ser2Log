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

   parser.add_argument("--Seven","-7", action='store_true',default=False,help="Force data stream to be 7 bit ASCII")

   args = parser.parse_args()

   if args.Tell:
      print ("Port: {}".format(args.port))
      print ("Baud: {}".format(args.baud))
      print ("Seven Bit: {}".format(args.Seven))

   return(args.port, args.baud,args.Seven)

def main():

   (port,baud,seven)=get_args()
   logger.info('Processing started: {} @ {}. Seven Bit: {}'.format(port,baud,seven))
   comm=serial.Serial(port=port,baudrate=baud,timeout=1)
   while True:
      line=comm.readline().strip()
      org_line=line
      if seven:
         line=bytearray(line)
         index=0
         while index < len(line):
            if  (line[index]<32) or (line[index] > 127):
               line[index]=ord('.')
            index+=1
         line=line.decode() #Decode in UTF by default, if it fails try CP437
      else:
         try:
            line=line.decode() #Decode in UTF by default, if it fails try CP437
         except:
            try:
               line=line.decode("cp437")
            except:
               line="Decode failed"

      if line != '':
#         print (line)
#         print (org_line)
         if seven:
            logger.info(line)
         else:
            logger.info(line)
            logger.info(org_line)

if __name__ == "__main__":
#    print(sys.argv)
#    print(len(sys.argv))

    main()
