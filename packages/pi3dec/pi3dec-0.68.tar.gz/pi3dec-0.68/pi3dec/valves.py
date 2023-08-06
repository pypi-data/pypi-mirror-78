from pi3dec import pm
import time


class Valves:
    def __init__(self, pe):
        self.pe = pe
        self.dev = pe.dev

    def _set_pwm(self, tube, pwm):
        """
        Sets the pwm signal that controls the rotor position of the servo valves.
        :param tube: tube index between 0 and 6
        :param pwm: Pulse Width Modulation period in microseconds
        """
        servo_remapping = {3: 0,
                           4: 1,
                           5: 2,
                           6: 3,
                           2: 4,
                           1: 5,
                           0: 6}
        tube = servo_remapping[tube]

        if tube == 0:
            self.dev.request(pm.dev_msg.SetServoStateRequest(servo0=pwm))
        elif tube == 1:
            self.dev.request(pm.dev_msg.SetServoStateRequest(servo1=pwm))
        elif tube == 2:
            self.dev.request(pm.dev_msg.SetServoStateRequest(servo2=pwm))
        elif tube == 3:
            self.dev.request(pm.dev_msg.SetServoStateRequest(servo3=pwm))
        elif tube == 4:
            self.dev.request(pm.dev_msg.SetServoStateRequest(servo4=pwm))
        elif tube == 5:
            self.dev.request(pm.dev_msg.SetServoStateRequest(servo5=pwm))
        elif tube == 6:
            self.dev.request(pm.dev_msg.SetServoStateRequest(servo6=pwm))

        time.sleep(0.3)  # wait for valve to move in desired position

        # cut power to all 7 valves
        self.dev.request(pm.dev_msg.SetServoStateRequest(servo0=0, servo1=0, servo2=0, servo3=0,
                                                         servo4=0, servo5=0, servo6=0))

    def open_valve(self, tube):
        self._set_pwm(tube, pwm=2300)

    def close_valve(self, tube):
        self._set_pwm(tube, pwm=500)

    def close_all_valves(self):
        for t in range(7):
            self.close_valve(tube=t)
            time.sleep(0.05)

    def open_all_valves(self):
        for t in range(7):
            self.open_valve(tube=t)

