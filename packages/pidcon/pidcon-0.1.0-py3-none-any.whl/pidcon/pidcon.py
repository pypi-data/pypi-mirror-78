import threading
import time

from events import Events


class PID(Events):
    def __init__(self, sample_rate, kp=0.0, ki=0.0, kd=0.0, n=1.0, output_upper_limit=None, output_lower_limit=None):
        super().__init__("on_new_output")

        self._output_timer = threading.Timer(sample_rate, self.calculate_output)
        self._output_timer.daemon = True

        self._kp = kp
        self._ki = ki
        self._kd = kd
        self._n = n
        self._is_enabled = False
        self._input_error = 0.0
        self._sample_rate = sample_rate

        self._output_upper_limit = output_upper_limit
        self._output_lower_limit = output_lower_limit

        self._proportional = 0.0
        self._integral = 0.0
        self._derivative = 0.0
        self._last_output = 0.0
        self._last_time = self._get_current_time_ms()
        self._output_timer.start()

    def calculate_output(self):
        if not self._is_enabled:
            output = self._last_output
        else:
            dt = self._get_current_time_ms() - self._last_time

            # Todo: Check other PID methods and implement them
            self._proportional = self._kp * self._input_error
            self._integral += self._ki * self._input_error * dt
            self._derivative = (self._kd * self._input_error) / dt

            output = self._trim_output(self._n * (self._proportional + self._integral + self._derivative))

        self.on_new_output(output)
        self._last_output = output
        self._output_timer = threading.Timer(self._sample_rate, self.calculate_output)
        self._output_timer.daemon = True
        self._output_timer.start()

    def _trim_output(self, output):
        if self._output_upper_limit is not None and output > self._output_upper_limit:
            return self._output_upper_limit
        elif self._output_lower_limit is not None and output < self._output_lower_limit:
            return self._output_lower_limit
        else:
            return output

    def enable_pid(self):
        self._is_enabled = True

    def disable_pid(self):
        self._is_enabled = False

    def reset_pid(self):
        self._proportional = 0.0
        self._integral = 0.0
        self._derivative = 0.0
        self._last_output = 0.0
        self._last_time = self._get_current_time_ms()

    @staticmethod
    def _get_current_time_ms():
        return time.monotonic_ns() / 1000000

    @property
    def is_enabled(self):
        return self._is_enabled

    @property
    def output_upper_limit(self):
        return self._output_upper_limit

    @output_upper_limit.setter
    def output_upper_limit(self, value):
        self._output_upper_limit = float(value)

    @property
    def output_lower_limit(self):
        return self._output_lower_limit

    @output_lower_limit.setter
    def output_lower_limit(self, value):
        self._output_lower_limit = float(value)

    @property
    def kp(self):
        return self._kp

    @kp.setter
    def kp(self, value):
        self._kp = float(value)

    @property
    def ki(self):
        return self._ki

    @ki.setter
    def ki(self, value):
        self._ki = float(value)

    @property
    def kd(self):
        return self._kd

    @kd.setter
    def kd(self, value):
        self._kd = float(value)

    @property
    def n(self):
        return self._n

    @n.setter
    def n(self, value):
        self._n = float(value)

    @property
    def input_error(self):
        return self._input_error

    @input_error.setter
    def input_error(self, value):
        self._input_error = value

    @property
    def sample_rate(self):
        return self._sample_rate

    @sample_rate.setter
    def sample_rate(self, value):
        self._sample_rate = value
