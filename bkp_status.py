#! /bin/env python3

"""
This script checks the status of a BK Precision power supply, model 1696-1698,
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
    parser = argparse.ArgumentParser(description="Serial communication script.")
    parser.add_argument(
        "-p",
        "--port",
        required=False,
        help="Serial port device (e.g., /dev/ttyUSB0, COM3). If not provided will auto detect",
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

    parser.add_argument(
        "--Memory",
        action="store_true"
    )

    parser.add_argument(
        "--Program",
        action="store_true"
    )


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
    print(f"Status of BK Power Supply Connected to port: {sup.ser.port}")

    reading=sup.reading()
    if reading is None:
        sys.exit("Error: Current voltage and current for the power supply can not be determined.")
    else:
        watts=reading[0]*(reading[1])
        print(f"Current:        Voltage: {reading[0]:.1f} Amps: {reading[1]:.2f} Watts: {watts:.2f}")

    settings=sup.settings()
    if settings is None:
        sys.exit("Error: Current voltage and max current set for the power supply can not be determined.")
    else:
        print(f"Test Maximum:   Voltage: {settings[0]:.1f} Amps: {settings[1]/10:.2f}")


    maxima=sup.maxima()
    if maxima is None:
        sys.exit("Error: Unit Max voltage and current settable by the power supply can not be determined.")
    else:
        print(f"Unit Maximum:   Voltage: {maxima[0]:.1f} Amps: {maxima[1]/10:.2f}")

    try:
        timer,fault, Output_On, Output_Off = sup.screen()
        print(f"Output Enabled: {Output_On}, Output Disabled: {Output_Off}")
        print(f"Timer Enabled:  {timer}")
        print(f"Fault:          {fault}")
    except:
        sys.exit("Error: could not get screen reading.")


    if args["Memory"]:
        mem_list=sup.memory()
        if mem_list is None:
            sys.exit("Error: could not get memory.")


        print(f"\nStored Memory Values")
        print(f"Index Volts  Amps ")

        for index, value in enumerate(mem_list):
            print(f"{index+1:5} {value[0]:5} {value[1]:5}")

    if args["Program"]:
        prog_list=sup.program()
        if prog_list is None:
            sys.exit("Error: could not get programmed steps.")

        print(f"\nStored Program Values")
        print(f"Index Volts  Amps Min Sec")

        for index, value in enumerate(prog_list):
#            print(value)
            print(f"{index:5} {value[0]:5} {value[1]:5} {value[2]:3} {value[3]:3}")




if __name__ == "__main__":
    main()
