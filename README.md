# bkp1696-apps
 Applications for the BKP169x power supplies, which uses the psup library from [Adrian Sampson's] (https://github.com/sampsyo/) github bkp1696
 [project] (https://github.com/sampsyo/bkp1696/). With a local [copy](https://github.com/jcmb/bkp1696) if needed.
 
 There are 3 tools in the suite.
 
1. bkp_status.py ( Status of the power supply )
2. bkp_on_off.py ( Simple Control )
3. bkp_prog.py   ( Control of the programable timer )

## Common Parameters

All the applications have the following standard parameters 

* -p PORT, --port PORT  Serial port device (e.g., /dev/ttyUSB0, COM3). If not provided will auto detect and use the first com port that it finds

* -t TIMEOUT, --timeout TIMEOUT. Read timeout in seconds (default: 1.0), set to 0.0 for no timeout
 
* -v, --verbose. Output verbose information, mostly status of operation.

## bkp_status.py

Reports status of the power supply

`useage bkp_status.py [--Memory] [--Program]`

Optional parameters

1. Memory, display Memory presets
1. Program, display Timed Program values

By default will output information on the current status and capabilities of the power supply.

Note that it does not have a loop option, use the watch command `watch bkp_status.py` if desired

	Status of BK Power Supply Connected to port: /dev/ttyUSB0
	Current:        Voltage: 12.1 Amps: 2.13 Watts: 25.79
	Test Maximum:   Voltage: 12.1 Amps: 9.99
	Unit Maximum:   Voltage: 40.2 Amps: 5.02
	Output Enabled: True, Output Disabled: False
	Timer Enabled:  True
	Fault:          False
	
 If --Memory is provided then the memory presets are shown
 
```Stored Memory Values
Index Volts  Amps 
    1  24.4  2.22
    2  24.2   5.0
    3  24.2  2.22
    4   1.0  0.01
    5   1.0  0.01
    6   1.0  0.01
    7   1.0  0.01
    8   1.0  0.01
    9   1.0  0.01

```

 If --Program is provided then the timed program values are shown
 
 ```Stored Program Values
Index Volts  Amps Min Sec
    0  12.1  9.99   0  50
    1  18.1   9.5   0  15
    2  24.1   9.5   0  25
    3   0.0   0.0   0   5
    4   1.0  0.01   0   0
    5   1.0  0.01   0   0
    6   1.0  0.01   0   0
    7   1.0  0.01   0   0
    8   1.0  0.01   0   0
    9   1.0  0.01   0   0
   10   1.0  0.01   0   0
   11   1.0  0.01   0   0
   12   1.0  0.01   0   0
   13   1.0  0.01   0   0
   14   1.0  0.01   0   0
   15   1.0  0.01   0   0
   16   1.0  0.01   0   0
   17   1.0  0.01   0   0
   18   1.0  0.01   0   0
   19   1.0  0.01   0   0
 ```

## bkp_on_off.py

Basic control of the power supply

`usage: bkp_on_off.py [-h] [-p PORT] [-t TIMEOUT] [-v] (--On | --Off) [--Voltage VOLTAGE] [--Current CURRENT]
`

Optional parameters

1. Off. Turn power output off
1. On. Turn power output on
	1. Voltage. Turn power output on at this Voltage
	2. Current. Turn power output on at this max current

	
### Examples
`bkp_on_off.py --Off` 

Turn power output off

`bkp_on_off.py --On` 

Turn power output on with the previous Voltage and Current settings

`bkp_on_off.py   -t 2.0  --On --Voltage 15 --Current 8.2 -v` 

Turn power output on, with voltage of 15.0v and max current of 8.2 amp. With a verbose information and a timeout of 2 seconds for communications


## bkp_prog.py

`usage: bkp_prog.py [-h] [-p PORT] [-t TIMEOUT] [-v] (--Display | --Run | --Stop | --Prog PROG) [--Count [0-256]]`

Optional parameters

1. Display. Show the current programmed status
1. Stop. Stop running the current program
1. Run. Running the current program
	1. Count. The number of cycles to run the program. 0 is infinite. which is the default.
1. Prog. Program a step in the timer program.  Where the string parameter is of of the format Step, Voltage, Amp, Min, Seconds. eg. 1,12.1,3.0,0,55
	1. 	Step. 0-19 step the the power supply program to set
	1. Voltage to be output at this step
	1. Max Current at this step
	1. Number of minutes that this step will be run, 0-99
	1. Number of seconds that this step will be run, 0-59

	After setting the program step it will read the setting back from the device for confirmation of the setting.
	
	Setting a time of 0 Minutes, 0 Seconds tells the power supply the program cycle is ended. Steps after this will be ignored. 
	
	Note: After the timer program ends the power supply will revert to the Voltage and Current settings that were in use before, with power output enabled. 
	
	
	
	
### Examples

`bkp_prog.py --Display`

Displays the current program settings and if the timer is running. `bkp_status.py` provides more information.


`bkp_prog.py --Run`

Run the program for an infinite number of steps

`bkp_prog.py --Stop`

Stop the running program. No error will be provided if the power supply is not in timer mode.
	
```
bkp_prog.py --Prog 9,10,7,1,2
Step: 9 Volts: 10.0 Amps: 7.0 Minutes: 1 Seconds: 
```

Set program step 9 to the given parameters.


