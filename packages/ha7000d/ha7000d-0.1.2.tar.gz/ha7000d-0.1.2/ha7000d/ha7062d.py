"""Holzworth HA7062D phase noise analyzer"""
import re
import sys
import asyncio
import itertools
from dataclasses import dataclass
from unyt import unyt_array
from ha7000d.common import HA7000DBase, Subsystem

PREFIXES = "YZEPTGMkh_dcmµnpfazy"
FACTORS = {
    "Y": 10 ** 24,
    "Z": 10 ** 21,
    "E": 10 ** 18,
    "P": 10 ** 15,
    "T": 10 ** 12,
    "G": 10 ** 9,
    "M": 10 ** 6,
    "k": 10 ** 3,
    "h": 10 ** 2,
    "da": 10 ** 1,
    "d": 10 ** -1,
    "c": 10 ** -2,
    "m": 10 ** -3,
    "µ": 10 ** -6,
    "n": 10 ** -9,
    "p": 10 ** -12,
    "f": 10 ** -15,
    "a": 10 ** -18,
    "z": 10 ** -21,
    "y": 10 ** -24,
}


@dataclass
class State:
    """Signal for controlling asyncio tasks"""

    running: bool = False


class AcquisitionError(Exception):
    """Raise when there's an acquisition error"""


class HA7062D(HA7000DBase):
    """HA7062D Phase Noise Analyzer

    Parameters
    ----------
        sock : `~socket.socket`
    """

    def __init__(self, sock):
        super().__init__(sock)
        self.setup = MeasurementSetup(self)
        self._state = State()

    @property
    def model(self):
        """(str): the model number"""
        return self._idn.model

    @property
    def serial_number(self):
        """(str): the serial number"""
        return self._idn.serial_number

    @property
    def firmware_version(self):
        """(str): the firmware version"""
        return self._idn.firmware_version

    def __repr__(self):
        address, port = self._sock.getpeername()
        return f"<Holzworth {self.model} at {address}:{port}>"

    async def _show_spinner(self):
        """Show an in-progress spinner during phase noise measurement"""
        glyph = itertools.cycle(["-", "\\", "|", "/"])
        try:
            while self._state.running:
                sys.stdout.write(next(glyph))
                sys.stdout.flush()
                sys.stdout.write("\b")
                await asyncio.sleep(0.5)
            return 0
        except asyncio.CancelledError:
            pass
        finally:
            sys.stdout.write("\b \b")

    async def _acquire(self):
        self._write(":INIT:PN:IMM")
        resp = self._read()
        try:
            while True:
                resp = self._query(":SENS:PN:CORE:STATUS?")
                if resp == "Data not ready":
                    # an error occurred
                    self._state.running = False
                    return 1
                if resp.endswith("initialized"):
                    break
                await asyncio.sleep(1)
            while True:
                resp = self._query(":STAT:OPER:COND?")
                if resp == "Instrument Busy":
                    await asyncio.sleep(1)
                else:
                    self._state.running = False
                    return 0
        except asyncio.CancelledError:
            pass

    async def _start_task(self, timeout):
        self._state.running = True
        task = asyncio.gather(self._show_spinner(), self._acquire())
        try:
            ret_value = await asyncio.wait_for(task, timeout)
        except asyncio.TimeoutError:
            raise TimeoutError("Phase noise measurement timed out") from None
        else:
            return ret_value

    def read(self, timeout=None, previous=True):
        """Read measurement data and return tuple (X, Y)

        Parameters
        ----------
            timeout : int
                timeout in seconds or None
            previous : bool
                read existing trace data if True, else start a new acquisition
        """
        if not previous:
            ret_value = asyncio.run(self._start_task(timeout))
            if ret_value is None:
                return None
            if ret_value[1] > 0:
                err = self._query(":SENS:PN:CORE:ERROR?")
                raise AcquisitionError(err)
        # n_points = int(self._query(":SENS:PN:SWE:POIN?"))
        resp = self._query(":CALC:PN:DATA:XDAT?")
        x = list(map(float, resp.split(",")))
        x = unyt_array(x, "Hz")
        resp = self._query(":CALC:PN:DATA:FDAT?")
        y = list(map(float, resp.split(",")))
        y = unyt_array(y, "dBc/Hz")
        return (x, y)

    def measure_input(self, channel):
        """Measure CHx input frequency and power level

        Parameters
        ----------
        channel : str {CH1, CH2}

        Returns
        -------
        (frequency, power) : two-tuple of frequency (Hz) and power (dBm)
        """
        resp = self._query(f":CALC:FP:DATA:CARR:{channel}?")
        return tuple(map(lambda s: s.strip(), resp.split(",")))

    def measure_lo(self, lo):
        """Measure LOx frequency and power level

        Parameters
        ----------
        lo : str {LO1, LO2}

        Returns
        -------
        (frequency, power) : two-tuple of frequency (Hz) and power (dBm)
        """
        resp = self._query(f":CALC:FP:DATA:{lo}?")
        return tuple(map(lambda s: s.strip(), resp.split(",")))


class MeasurementSetup(Subsystem, kind="MeasurementSetup"):
    """Measurement subsystem

    Parameters
    ----------
    instr : HA7000D
    """

    def _check_resp(self, expected_response):
        if (resp := self._read()) != expected_response:
            raise Exception(f"Unexpected response '{resp}'")

    @property
    def measurement_type(self):
        """value : str, {absolute, additive, AM noise, baseband}"""
        return self._query(":SENS:PN:MEAS:TYPE?")

    @measurement_type.setter
    def measurement_type(self, value):
        value = value.upper()
        self._set_parameter(f":SENS:PN:MEAS:TYPE:{value}")
        set_value = self.measurement_type.upper()
        if set_value != value:
            raise ValueError(f"Invalid measurement type '{value}'")

    @property
    def correlations(self):
        """value : int, number of cross-correlations to perform"""
        return int(self._query(":SENS:PN:CORR:COUN?"))

    @correlations.setter
    def correlations(self, value):
        self._set_parameter(f":SENS:PN:CORR:COUN:{value}")
        if self.correlations != value:
            raise ValueError(f"Invalid number of cross-correlations '{value}'")

    @staticmethod
    def _parse_quantity(value):
        pattern = r"([0-9]+\.?[0-9]*) (da|[{}])?([a-zA-Z]+)".format(PREFIXES)
        if (m := re.match(pattern, str(value))) is None:
            return value
        n, p, u = m.groups()
        n = float(n)
        p = FACTORS[p]
        return ({p * n}, u)

    @property
    def offset_span(self):
        """value : 2-tuple e.g. ('10 Hz', '10 MHz')"""
        start = self._query(":SENS:PN:FREQ:STAR?")
        stop = self._query(":SENS:PN:FREQ:STOP?")
        return (float(start), float(stop))

    @offset_span.setter
    def offset_span(self, value):
        start, stop = value
        start = start.replace(" ", "")
        stop = stop.replace(" ", "")
        self._set_parameter(f":SENS:PN:FREQ:STAR:{start}")
        self._set_parameter(f":SENS:PN:FREQ:STOP:{stop}")

    @property
    def data_type(self):
        """value : str {Channel 1, Channel 2, Cross}"""
        return self._query(":SENS:PN:DATA:TYPE?")

    @data_type.setter
    def data_type(self, value):
        self._set_parameter(f":SENS:PN:DATA:TYPE:{value}")

    @property
    def trigger_type(self):
        """value : str {Single, Each, Continuous, Persist}"""
        return self._query(":SENS:PN:MODE?")

    @trigger_type.setter
    def trigger_type(self, value):
        self._set_parameter(f":SENS:PN:MODE:{value}")

    @property
    def samples(self):
        """value : int {64, 128, 256, 512, 1024}"""
        return int(self._query(":SENS:PN:SAMPLES:COUN?"))

    @samples.setter
    def samples(self, value):
        self._set_parameter(f":SENS:PN:SAMPLES:{value}")

    @property
    def mixer_conversion(self):
        """value : str {Automatic, Manual}"""
        return self._query(":SENS:PN:MCONV?")

    @mixer_conversion.setter
    def mixer_conversion(self, value):
        self._set_parameter(f":SENS:PN:MCONV:{value}")

    @property
    def pll_bandwidth(self):
        """value : str {Wide, Normal}"""
        LU = {"VCO Measurement Enabled": "Wide", "VCO Measurement Disabled": "Normal"}
        resp = self._query(":SENS:PN:VCO?")
        return LU.get(resp, resp)

    @pll_bandwidth.setter
    def pll_bandwidth(self, value):
        LU = {"Wide": True, "Normal": False}
        value = LU[value]
        self._set_parameter(f":SENS:PN:VCO:{value}")

    @property
    def if_gain(self):
        """value : str or int {Auto, 0, 14, 28, 42} dB"""
        return self._query(":SENS:PN:GAIN?")

    @if_gain.setter
    def if_gain(self, value):
        self._set_parameter(f":SENS:PN:GAIN:{value}")

    @property
    def dut_frequency_range(self):
        """value : str or int {Auto, 1, 2, 4, 8} divisor

        1: 10 MHz to 6 GHz
        2: 6.1 GHz to 12 GHz
        4: 12.1 GHz to 24 GHz
        8: 24.1 GHz to 26.5 GHz
        """
        LU = {
            "Divisor set to auto detect": "Auto",
            "1": "10 MHz to 6 GHz",
            "2": "6.1 GHz to 12 GHz",
            "4": "12.1 GHz to 24 GHz",
            "8": "24.1 GHz to 26.5 GHz",
        }
        resp = self._query(":SENS:PN:DIV?")
        return LU.get(resp, resp)

    @dut_frequency_range.setter
    def dut_frequency_range(self, value):
        self._set_parameter(f":SENS:PN:DIV:{value}")

    @property
    def dut_splitter(self):
        """value : str {Internal, External}"""
        return self._query(":SENS:CORR:POW:STAT?")

    @dut_splitter.setter
    def dut_splitter(self, value):
        self._set_parameter(f":SENS:CORR:POW:STAT:{value}")

    @property
    def dut_mixer(self):
        """value : str {Internal, External}"""
        LU = {
            "External mixer Not in Use": "Internal",
            "External mixer in Use": "External",
        }
        resp = self._query(":SENS:PN:MEXT?")
        return LU.get(resp, resp)

    @dut_mixer.setter
    def dut_mixer(self, value):
        LU = {"Internal": "Off", "External": "On"}
        value = LU[value]
        self._set_parameter(f":SENS:PN:MEXT:{value}")

    @property
    def phase_shifters(self):
        """value : bool {True, False} HX5100 phase shifters in use"""
        LU = {"HX5100 Not in Use": False, "HX5100 in Use": True}
        resp = self._query(":SENS:PN:HX5100?")
        return LU.get(resp, resp)

    @phase_shifters.setter
    def phase_shifters(self, value):
        value = int(value)
        self._set_parameter(f":SENS:PN:HX5100:{value}")

    @property
    def lo_configuration(self):
        """value : str {Internal, External}"""
        LU = {"Internal LO status": "Internal", "External LO status": "External"}
        resp = self._query(":SENS:PN:LO:STATUS?")
        return LU.get(resp, resp)

    @property
    def smoothing_points(self):
        """value : int, 0 or 3 to 99 points of smoothing"""
        resp = self._query(":CALC:PN:TRAC:SMO:STAT?")
        if resp == "OFF":
            return 0
        return int(self._query(":CALC:PN:TRAC:SMO:PNTS?"))

    @smoothing_points.setter
    def smoothing_points(self, value):
        if value > 0:
            self._set_parameter(f":CALC:PN:TRAC:SMO:PNTS:{value}")
            self._set_parameter(":CALC:PN:TRAC:SMO:STAT:ON")
        else:
            self._set_parameter(":CALC:PN:TRAC:SMO:STAT:OFF")

    @property
    def spur_removal(self):
        """value : str or int, {OFF, 0 to 99} dB"""
        resp = self._query(":CALC:PN:TRAC:SPUR:OMIS?")
        if resp == "OFF":
            return resp
        return int(self._query(":CALC:PN:TRAC:SPUR:THR?"))

    @spur_removal.setter
    def spur_removal(self, value):
        if value == "OFF":
            self._set_parameter(":CALC:PN:TRAC:SPUR:OMIS:OFF")
        else:
            self._set_parameter(f":CALC:PN:TRAC:SPUR:THR:{value}")
            self._set_parameter(":CALC:PN:TRAC:SPUR:OMIS:ON")
