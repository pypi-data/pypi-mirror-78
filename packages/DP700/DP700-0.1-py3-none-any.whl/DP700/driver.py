from DP700.dpPort import DPPort

import logging
import sys

logger = logging.getLogger(__name__)

class DP700():
    """Class that builds support for Rigol D700 series power supplies.
    Creates an instance of :class:`Serial` using :class:`DPPort`

    :param portName: Serial port (Uses pySerial serial_for_url)
    :portName type: str
    """

    def __init__(self, portName):
        """Constructor method
        """
        self.port = DPPort(portName)
        self.make, self.model, self.sn, self.version = self.identify()
        logger.info('Device name: ' + self.model)
        if "711" in self.model:
            self.channels = ('CH1', 'P30V')
            self.v_range = (0, 32)
            self.i_range = (0, 5.3)
        elif "712" in self.model:
            self.channels = ('CH1', 'P50V')
            self.v_range = (0, 53)
            self.i_range = (0, 3.2)
        else:
            print('Unable to identify connected model: ' + self.model)
            self.close()
            sys.exit(1)

    def close(self):
        """Close serial connection.
        """
        self.port.close()

    def apply(self, v, i, ch='CH1'):
        """Set the channel output voltage and current.

        :param v: voltage
        :v type: float (defaults to 0V)
        :param i: current in amps (defaults to 5A for DP711 and 3A for DP712)
        :i type: float
        :param ch: channel (defaults to CH1)
        :ch type: str
        """
        ch = ch.upper()
        if not (self.v_range[0] <= v <= self.v_range[1]):
            print('Voltage out of allowed range ({}, {})'.format(self.v_range[0], self.v_range[1]))
            return
        if not (self.i_range[0] <= i <= self.i_range[1]):
            print('Current out of allowed range ({}, {})'.format(self.i_range[0], self.i_range[1]))
            return
        if ch not in self.channels:
            print('Channel not recognized. Allowed channels are (' + self.channels[0] + ', ' + self.channels[1] + ')')
            return
        logger.info('Applying ' + str(v) + 'V, ' + str(i) + 'A to ' + ch)
        self.port.sendString(':APPLy ' + ch + ',' + str(v) + ',' + str(i) + '\n')

    def display(self, on_off):
        """Turns the display on or off.

        :param on_off: either 'ON' or 'OFF'
        :on_off type: str
        """
        on_off = on_off.upper()
        if on_off not in ('ON', 'OFF'):
            print("Parameter can either be ON or OFF")
            return
        logger.info('Turning display ' + on_off)
        self.port.sendString(':DISPlay ' + on_off + '\n')

    def identify(self):
        """Returns the device identification.

        :return: (<make>, <model>, <serial number>, <software version>)
        :rtype: tuple
        """
        id = self.port.sendString('*IDN?' + '\n')
        id_list = id.split(',')
        return id_list[0], id_list[1], id_list[2], id_list[3]

    def installation_status(self):
        """Returns the installation status of the following options:
        Trigger, Timer, and High Resolution

        :return: (<trigger state>, <timer state>, <high resolution state>)
        :rtype: tuple
        """
        options = self.port.sendString('*OPT?' + '\n')
        options_list = id.split(',')
        return options_list[0], options_list[1], options_list[2]

    def self_test(self):
        """Returns the self-test result.

        :return: self test result
        :rtype: str
        """
        result = self.port.sendString('*TST' + '\n')
        return result

    def measure_all(self, ch='CH1'):
        """Returns the measured voltage (V), current (A), and power (W) on the selected channel.

        :param ch: channel (defaults to CH1)
        :ch type: str
        :return: (<voltage>, <current>, <power>)
        :rtype: tuple
        """
        ch = ch.upper()
        if ch not in self.channels:
            print('Channel not recognized. Allowed channels are (' + self.channels[0] + ', ' + self.channels[1] + ')')
            return
        logger.info('Measuring ' + ch + '...')
        measurements = self.port.sendString(':MEASure:ALL? ' + ch + '\n')
        measurements_list = measurements.split(',')
        v = measurements_list[0]
        i = measurements_list[1]
        p = measurements_list[2]
        logger.info(ch + ' measurements: ' + v + 'V, ' + i + 'A, ' + p + 'W')
        return v, i, p

    def measure_current(self, ch='CH1'):
        """Returns the measured current on the selected channel.

        :param ch: channel (defaults to CH1)
        :ch type: str
        :return: current in amps
        :rtype: str
        """
        ch = ch.upper()
        if ch not in self.channels:
            print('Channel not recognized. Allowed channels are (' + self.channels[0] + ', ' + self.channels[1] + ')')
            return
        logger.info('Measuring current on ' + ch + '...')
        measurement = self.port.sendString(':MEASure:CURRent? ' + ch + '\n')
        logger.info(ch + ' current measurement: ' + measurement + 'A')
        return measurement

    def measure_power(self, ch='CH1'):
        """Returns the measured power on the selected channel.

        :param ch: channel (defaults to CH1)
        :ch type: str
        :return: power in watts
        :rtype: str
        """
        ch = ch.upper()
        if ch not in self.channels:
            print('Channel not recognized. Allowed channels are (' + self.channels[0] + ', ' + self.channels[1] + ')')
            return
        logger.info('Measuring power on ' + ch + '...')
        measurement = self.port.sendString(':MEASure:POWEr? ' + ch + '\n')
        logger.info(ch + ' power measurement: ' + measurement + 'W')
        return measurement

    def measure_voltage(self, ch='CH1'):
        """Returns the measured voltage on the selected channel.

        :param ch: channel (defaults to CH1)
        :ch type: str
        :return: voltage
        :rtype: str
        """
        ch = ch.upper()
        if ch not in self.channels:
            print('Channel not recognized. Allowed channels are (' + self.channels[0] + ', ' + self.channels[1] + ')')
            return
        logger.info('Measuring voltage on ' + ch + '...')
        measurement = self.port.sendString(':MEASure:VOLTage? ' + ch + '\n')
        logger.info(ch + ' voltage measurement: ' + measurement + 'V')
        return measurement

    def channel_mode(self, ch='CH1'):
        """Returns the channel mode. Returns either:
        'CC' (constant current)
        'CV' (constant voltage)
        'UR' (unregulated)

        :param ch: channel (defaults to CH1)
        :ch type: str
        :return: mode
        :rtype: str
        """

        ch = ch.upper()
        if ch not in self.channels:
            print('Channel not recognized. Allowed channels are (' + self.channels[0] + ', ' + self.channels[1] + ')')
            return
        mode = self.port.sendString(':OUTPut:CVCC? ' + ch + '\n')
        logger.info(ch + 'mode: ' + mode)
        return mode

    def is_ocp(self, ch='CH1'):
        """Returns whether overcurrent protection (OCP) has occurred.

        :param ch: channel (defaults to CH1)
        :ch type: str
        :return: 'YES' or 'NO'
        :rtype: str
        """
        ch = ch.upper()
        if ch not in self.channels:
            print('Channel not recognized. Allowed channels are (' + self.channels[0] + ', ' + self.channels[1] + ')')
            return
        ocp = self.port.sendString(':OUTPut:OCP:ALAR? ' + ch + '\n')
        logger.info('Has OCP occurred on ' + ch + '?... ' + ocp)
        return ocp

    def clear_ocp(self, ch='CH1'):
        """Clears the internal OCP flag.

        :param ch: channel (defaults to CH1)
        :ch type: str
        """
        ch = ch.upper()
        if ch not in self.channels:
            print('Channel not recognized. Allowed channels are (' + self.channels[0] + ', ' + self.channels[1] + ')')
            return
        logger.info('Clearing OCP on ' + ch)
        self.port.sendString(':OUTPut:OCP:CLEAR ' + ch + '\n')

    def ocp_on_off(self, on_off, ch='CH1'):
        """Enable or disable OCP.

        :param on_off: 'ON' or 'OFF'
        :on_off type: str
        :param ch: channel (defaults to CH1)
        :ch type: str
        """
        ch = ch.upper()
        if ch not in self.channels:
            print('Channel not recognized. Allowed channels are (' + self.channels[0] + ', ' + self.channels[1] + ')')
            return
        if on_off not in ('ON', 'OFF'):
            print("Parameter can either be ON or OFF")
            return
        logger.info('Turning OCP ' + on_off + ' on ' + ch)
        self.port.sendString(':OUTPut:OCP ' + ch + ',' + on_off + '\n')

    def ocp_value(self, i, ch='CH1'):
        """Sets the channel OCP value.

        :param i: ocp value in amps
        :i type: float
        :param ch: channel (defaults to CH1)
        :ch type: str
        """
        ch = ch.upper()
        if ch not in self.channels:
            print('Channel not recognized. Allowed channels are (' + self.channels[0] + ', ' + self.channels[1] + ')')
            return
        if not (self.i_range[0] <= i <= self.i_range[1]):
            print('Current out of allowed range ({}, {})'.format(self.i_range[0], self.i_range[1]))
            return
        logger.info('Setting ' + ch + ' OCP value to ' + str(i) + 'A')
        self.port.sendString(':OUTPut:OCP:VALue ' + ch + ',' + str(i) + '\n')

    def ocp_value_query(self, ch='CH1'):
        """Queries the channel OCP value.

        :param ch: channel (defaults to CH1)
        :ch type: str
        :return: OCP value in amps
        :rtype: str
        """
        ch = ch.upper()
        if ch not in self.channels:
            print('Channel not recognized. Allowed channels are (' + self.channels[0] + ', ' + self.channels[1] + ')')
            return
        ocp = self.port.sendString(':OUTPut:OCP:VALue? ' + ch)
        logger.info(ch + ' OCP value: ' + ocp + 'A')
        return ocp

    def is_ovp(self, ch='CH1'):
        """Returns whether overvoltage protection (OVP) has occurred.

        :param ch: channel (defaults to CH1)
        :ch type: str
        :return: 'YES' or 'NO'
        :rtype: str
        """
        ch = ch.upper()
        if ch not in self.channels:
            print('Channel not recognized. Allowed channels are (' + self.channels[0] + ', ' + self.channels[1] + ')')
            return
        ovp = self.port.sendString(':OUTPut:OVP:ALAR? ' + ch + '\n')
        logger.info('Has OVP occurred on ' + ch + '?... ' + ovp)
        return ovp

    def clear_ovp(self, ch='CH1'):
        """Clears the internal OVP flag.

        :param ch: channel (defaults to CH1)
        :ch type: str
        """
        ch = ch.upper()
        if ch not in self.channels:
            print('Channel not recognized. Allowed channels are (' + self.channels[0] + ', ' + self.channels[1] + ')')
            return
        logger.info('Clearing OVP on ' + ch)
        self.port.sendString(':OUTPut:OVP:CLEAR ' + ch + '\n')

    def ovp_on_off(self, on_off, ch='CH1'):
        """Enable or disable OVP.

        :param on_off: 'ON' or 'OFF'
        :on_off type: str
        :param ch: channel (defaults to CH1)
        :ch type: str
        """
        ch = ch.upper()
        if ch not in self.channels:
            print('Channel not recognized. Allowed channels are (' + self.channels[0] + ', ' + self.channels[1] + ')')
            return
        if on_off not in ('ON', 'OFF'):
            print("Parameter can either be ON or OFF")
            return
        logger.info('Turning OVP ' + on_off + ' on ' + ch)
        self.port.sendString(':OUTPut:OVP ' + ch + ',' + on_off + '\n')

    def ovp_value(self, v, ch='CH1'):
        """Sets the channel OVP value.

        :param v: ovp value in volts
        :v type: float
        :param ch: channel (defaults to CH1)
        :ch type: str
        """
        ch = ch.upper()
        if ch not in self.channels:
            print('Channel not recognized. Allowed channels are (' + self.channels[0] + ', ' + self.channels[1] + ')')
            return
        if not (self.v_range[0] <= v <= self.v_range[1]):
            print('Voltage out of allowed range ({}, {})'.format(self.v_range[0], self.v_range[1]))
            return
        logger.info('Setting ' + ch + ' OVP value to ' + str(v) + 'V')
        self.port.sendString(':OUTPut:OVP:VALue ' + ch + ',' + str(v) + '\n')

    def ovp_value_query(self, ch='CH1'):
        """Queries the channel OVP value.

        :param ch: channel (defaults to CH1)
        :ch type: str
        :return: OVP value in volts
        :rtype: str
        """
        ch = ch.upper()
        if ch not in self.channels:
            print('Channel not recognized. Allowed channels are (' + self.channels[0] + ', ' + self.channels[1] + ')')
            return
        ovp = self.port.sendString(':OUTPut:OVP:VALue? ' + ch)
        logger.info(ch + ' OVP value: ' + ovp + 'V')
        return ovp

    def channel_on_off(self, on_off, ch='CH1'):
        """Enable or disable the channel output.

        :param on_off: 'ON' or 'OFF'
        :on_off type: str
        :param ch: channel (defaults to CH1)
        :ch type: str
        """
        ch = ch.upper()
        if ch not in self.channels:
            print('Channel not recognized. Allowed channels are (' + self.channels[0] + ', ' + self.channels[1] + ')')
            return
        if on_off not in ('ON', 'OFF'):
            print("Parameter can either be ON or OFF")
            return
        logger.info('Turning ' + ch + ' output ' + on_off)
        self.port.sendString(':OUTPut:STATe ' + ch + ',' + on_off + '\n')

    def last_error(self):
        """Returns the last error message in the error queue and clears the error message.

        :return: error message
        :rtype: str
        """
        err = self.port.sendString(':SYSTem:ERRor?' + '\n')
        logger.info('Last error message: ' + err)
        return err

    def set_remote(self):
        """Enables the power supply to shift from local mode to remote mode.
        """
        logger.info('Shifting to remote mode')
        self.port.sendString(':SYSTem:REMote' + '\n')

    def set_local(self):
        """Enables the power supply to shift from remote mode to local mode.
        """
        logger.info('Shifting to local mode')
        self.port.sendString(':SYSTem:LOCal' + '\n')

    def timer_cycles(self, num_cycles):
        """Sets the number of cycles for the timer.

        :param num_cycles: Number of cycles. Allowed range is [1, 99999].
        :num_cycles type: int
        """
        num_cycles = int(num_cycles)
        if not (1 <= num_cycles <= 99999):
            print('Number of cycles is outside of allowed range [1, 99999]')
            return
        logger.info('Setting number of cycles for the timer to ' + str(num_cycles))
        self.port.sendString(':TIMEr:CYCLEs N,' + str(num_cycles) + '\n')

    def timer_cycles_infinite(self):
        """Sets the number of cycles to infinite.
        """
        logger.info('Setting number of cycles for the timer to Infinite')
        self.port.sendString(':TIMEr:CYCLEs I' + '\n')

    def timer_end_state(self, end_state):
        """Sets the end state of the timer. Allowed values for end_state are:
        OFF: output will be turned off after timer cycles are complete
        LAST: output will be kept at the state of the last group after cycles are complete

        :param end_state: 'OFF' or 'LAST'
        :end_state type: str
        """
        end_state = end_state.upper()
        if end_state not in ('OFF', 'LAST'):
            print('Parameter must either be OFF or LAST')
            return
        logger.info('Setting the end state of the timer to ' + end_state)
        self.port.sendString(':TIMEr:ENDState' + end_state + '\n')

    def timer_groups(self, num_groups):
        """Sets the number of output groups.

        :param num_groups: Number of output groups. Allowed range is [1, 2048].
        :num_groups type: int
        """
        num_groups = int(num_groups)
        if not (1 <= num_groups <= 2048):
            print('Number of groups is outside of allowed range [1, 2048]')
            return
        logger.info('Setting the number of output groups to ' + str(num_groups))
        self.port.sendString(':TIMEr:GROUPs ' + str(num_groups) + '\n')

    def timer_parameter(self, num, v, i, t):
        """Sets the timing parameters for a specified group.

        :param num: Group ID. Allowed range is [1, 2048]
        :num type: int
        :param v: Output voltage in volts
        :v type: float
        :param i: Output current in amps
        :i type: float
        :param t: Duration time in seconds. Allowed range is [0.01, 99999]
        :t type: float
        """
        num = int(num)
        if not (1 <= num <= 2048):
            print('Group ID is outside of allowed range [1, 2048]')
            return
        if not (self.v_range[0] <= v <= self.v_range[1]):
            print('Voltage out of allowed range ({}, {})'.format(self.v_range[0], self.v_range[1]))
            return
        if not (self.i_range[0] <= i <= self.i_range[1]):
            print('Current out of allowed range ({}, {})'.format(self.i_range[0], self.i_range[1]))
            return
        if not (0.01 <= t <= 99999):
            print('Duration time is outside of allowed range [0.01, 99999]')
            return
        logger.info('Setting group ' + str(num) + ' timing parameters: ' + str(v) + 'V, ' + str(i) + 'A, ' + str(t) + 's')
        self.port.sendString(':TIMEr:PARAmeter ' + str(num) + ',' + str(v) + ',' + str(i) + ',' + str(t) + '\n')

    def timer_on_off(self, on_off):
        """Enables or disables the timing output.

        :param on_off: 'ON' or 'OFF'
        :on_off type: str
        """
        on_off = on_off.upper()
        if on_off not in ('ON', 'OFF'):
            print('Parameter must be either ON or OFF')
            return
        logger.info('Turning timing output ' + on_off)
        self.port.sendString(':TIMEr ' + on_off + '\n')

    def timer_trigger(self, trig_mode='DEFAULT'):
        """Sets the trigger mode of the timer. Allowed options are:
        DEFAULT: when timing output is enabled, instrument automatically outputs based on timer parameters
        SINGLE: when time output is enabled, single press of OK button enables single output of single group

        :param trig_mode: 'DEFAULT' or 'SINGLE'
        :trig_mode type: str
        """
        trig_mode = trig_mode.upper()
        if trig_mode == 'DEFAULT':
            trig_mode = 'DEFault'
        elif trig_mode == 'SINGLE':
            trig_mode = 'SINGle'
        else:
            print('Parameter must be either DEFAULT or SINGLE')
            return
        logger.info('Setting the trigger mode of the timer to ' + trig_mode)
        self.port.sendString(':TIMEr:TRIGger ' + trig_mode + '\n')
