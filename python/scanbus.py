#!/usr/bin/python

import i2cpy
import argparse
import sys

                 
if __name__ == "__main__":
    ''' Main routine to scan the i2c bus.
    '''
    # Initialize
    lower = 0
    upper = 127

    # Parse the command line arguments.
    #
    parser = argparse.ArgumentParser(description='Set the frequency of an Si514 clock')
    parser.add_argument('-l', dest='lower', nargs=1, type=int, help='lower i2c address as decimal')
    parser.add_argument('-u', dest='upper', nargs=1, type=int, help='upper i2c address as decimal')
    args = parser.parse_args()

    # Validate the parameters.
    #
    if (lower < 0):
        sys.stderr.write("Error:  lower i2c address must be >= 0")
        sys.exit()
    if (upper > 127):
        sys.stderr.write("Error:  upper i2c address must be <= 127")
        sys.exit()
    if (lower > upper):
        sys.stderr.write("Error:  lower i2c address just be <= upper i2c address")
        sys.exit()
    
    # Scan the specified range of addresses.
    #
    try:
        i2c = i2cpy.core.Py2CStick(deviceAddress = None, delay=10)
    except Exception, e:
        sys.stderr.write("Error: " + str(e) + "\r\n")
        sys.exit()
    
    sys.stdout.write("Scanning i2c addresses from " + hex(lower) + " to " + hex(upper) + "\r\n")

    validAddresses = list()
    for address in range(lower, upper + 1):
        done = False
        while not(done):
            try:
                validAddress = i2c.ScanAddress(address)
                if validAddress:
                    validAddresses.append(address)
                done = True
            except Exception, e:
                pass

    # Print the valid addresses.
    #
    if (len(validAddresses) > 0):
        for item in validAddresses:
            sys.stdout.write("Device found at address " + hex(item) + "\r\n")
    else:
        sys.stdout.write("No devices found\r\n")
        
