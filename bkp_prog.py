#! /bin/env python3

"""
This script controls the program functions of a BK Precision power supply,
model 1696-1698, which is connected via serial to the computer.
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
    group.add_argument("--Display", action="store_true",
        help="Display the current program settings.")
    group.add_argument("--Run",  action="store_true", help="Run the program starting at location 0.")
    group.add_argument("--Stop", action="store_true", help="Stop the program.")
    group.add_argument("--Prog", type=str,
        help="Where the string parameter is of of the format Step, Voltage, Amp, Min, Seconds. eg. 1,12.1,3.0,0,55")

    parser.add_argument(
        "--Count",
        type=int,
        choices=range(0, 256),
        metavar="[0-256]",
        default=0,
        help="Optional Cycles to run. 0 is infinte.",
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
    if args["Display"]:

        timer,fault, Output_On, Output_Off = sup.screen()
        print(f"Timer Enabled: {timer}")
        print(f"Fault: {fault}")


        prog_list=sup.program()


        print(f"\nStored Program Values")
        print(f"Index Volts  Amps Min Sec")

        for index, value in enumerate(prog_list):
#            print(value)
            print(f"{index:5} {value[0]:5} {value[1]:5} {value[2]:3} {value[3]:3}")

    elif args["Run"]:
        if sup.enable() is None:
            sys.exit("Error: Could not enable power output.")
        if sup.program_run(args["Count"]) is None:
            sys.exit("Error: Could not enable timer.")
    elif args["Stop"]:
        if sup.program_stop() is None:
            sys.exit("Error: Could not cancel timer.")

    elif args["Prog"]:
        params=args["Prog"].split(",")

        if len(params) != 5:
            sys.exit(f"Invalid format for Prog options, incorrect number of values {len(params)} expected 5")

        try:
            step = int(params[0])
        except ValueError as e:
            sys.exit(f"Error: Could not convert step '{params[0]}' to an integer. {e}")


        if (step <0) or (step > 19):
            sys.exit(f"Error: step '{step}' out of the valid range of 0..19")

        try:
            voltage = float(params[1])
        except ValueError as e:
            sys.exit(f"Error: Could not convert voltage '{params[1]}' to a float. {e}")


        if (voltage <0) or (voltage > 60):
            sys.exit(f"Error: Voltage '{voltage}' out of the valid range of 0..60")

        try:
            amps = float(params[2])
        except ValueError as e:
            sys.exit(f"Error: Could not convert amps '{params[2]}' to a float. {e}")


        if (amps <0) or (amps > 10):
            sys.exit(f"Error: Amps '{amps}' out of the valid range of 0..10")


        try:
            minutes = int(params[3])
        except ValueError as e:
            sys.exit(f"Error: Could not convert minutes '{params[3]}' to an integer. {e}")


        if (minutes <0) or (minutes > 99):
            sys.exit(f"Error: minutes '{minutes}' out of the valid range of 0..99")

        try:
            seconds = int(params[4])
        except ValueError as e:
            sys.exit(f"Error: Could not convert minutes '{params[4]}' to an integer. {e}")


        if (seconds <0) or (seconds > 59):
            sys.exit(f"Error: seconds '{seconds}' out of the valid range of 0..59")


        if sup.program_set_step(step,voltage,amps,minutes,seconds) is None:
            sys.exit("Error: Could not program step.")
        else:
            voltage,amps,minutes,seconds=sup.program_get_step(step)
            print(f"Step: {step} Volts: {voltage} Amps: {amps} Minutes: {minutes} Seconds: {seconds}")

    else:
        print("Error: unknown parameter")




if __name__ == "__main__":
    main()
