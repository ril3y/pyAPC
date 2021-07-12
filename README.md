# pyAPC
Python library to control APC UPS PDU, specifically a AP7911A.  This may work with other models.

## Usage
Just import PyAPC and create a instance of the class object.  Then you can just send outlet commands like the following.  The 2nd parameter in the apply_outlet_command is a list of integers that correspond to the outlet number.  

```python
apc = PyAPC("http://192.168.1.218", "apc", "apc")
apc.login()
apc.apply_outlet_command(OutletCommand.OFF_IMMEDIATE, [14, 6])
```
Additional implemented (untested) command are:
```python
class OutletCommand(Enum):
    NO_ACTION = 1
    ON_IMMEDIATE = 2
    ON_DELAYED = 3
    OFF_IMMEDIATE = 4
    OFF_DELAYED = 5
    REBOOT_IMMEDIATE = 6
    REBOOT_DELAYED = 7
    CANCEL_PENDING_COMMANDS = 8
```
