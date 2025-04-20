#! /bin/env python3

"""
This script turns on or off the output of a BK Precision power supply, model 1696-1698,
which is connected via serial to the computer.
"""
import argparse
from pprint import pprint
import sys
import time

try:
    import serial
except:
    sys.exit("Error: pyserial module not installed. Install using python -m pip install pyserial")

try:
    from psup import Supply
except:
    sys.exit("Error: psup module not installed. Install from https://github.com/sampsyo/bkp1696")



def get_args():
    """
    Get the command line arguments and return them as a dict
    """

    def float_range(min_val, max_val):
        """
        Creates a custom type function for ArgumentParser that checks if a float
        value is within the specified range.
        """
        def check_range(value):
            try:
                fvalue = float(value)
            except ValueError:
                raise argparse.ArgumentTypeError(f"'{value}' is not a valid float")
            if fvalue < min_val or fvalue > max_val:
                raise argparse.ArgumentTypeError(f"Value must be between {min_val} and {max_val} (inclusive)")
            return fvalue
        return check_range

    parser = argparse.ArgumentParser(description="Serial communication script.")
    parser.add_argument(
        "-p",
        "--port",
        required=False,
        help="Serial port device (e.g., /dev/ttyUSB0, COM3)",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=float,
        default=1.0,
        help="Read timeout in seconds (default: 1.0)",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true"
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--On",  action="store_true",  dest="action", help="Enable the setting.")
    group.add_argument("--Off", action="store_false", dest="action", help="Disable the setting.")

    parser.add_argument("--Voltage", type=float_range(0.0, 60.0),
        help="Voltage value when --On is provided. Otherwise Voltage is unchanged")
    parser.add_argument("--Current",  type=float_range(0.0, 10.0),
        help="Current value, in amps, when --On is provided. Otherwise Current is unchanged")


    args = parser.parse_args()
    return vars(args)


def main():
    """
    Display nicely formated the status of the power supply
    """
    args = get_args()
#    pprint(args)

    try:
        sup = Supply(ident=args["port"],timeout=args["timeout"],verbose=args["verbose"])
    except serial.serialutil.SerialException as e:
        sys.exit(f'Error: {e}')
    except:
        sys.exit(f'Error: Unknown Error creating power suppoy object.')



    #    pprint(sup.ser(indent)
    if args["verbose"]:
        if args["action"]:
            print(f"Enabling power output of BK Power Supply Connected to port: {sup.ser.port}")
        else:
            print(f"Enabling power output of BK Power Supply Connected to port: {sup.ser.port}")

    if args["action"]:
        if args["Voltage"]:
            if sup.voltage(args["Voltage"]) is None:
                sys.exit("Error: No response from setting Voltage")
        if args["Current"]:
            if sup.current(args["Current"]) is None:
                sys.exit("Error: No response from setting Current")
        if sup.enable() is None :
            sys.exit("Error: No response from setting output On")
    else:
        if sup.disable() is None:
            sys.exit("Error: No response from setting output Off")





if __name__ == "__main__":
    main()
