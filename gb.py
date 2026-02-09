from enum import Enum, auto


class Gear(Enum):
    REVERSE = auto()
    NEUTRAL = auto()
    FIRST = auto()
    SECOND = auto()
    THIRD = auto()
    FOURTH = auto()
    FIFTH = auto()


class GearboxError(Exception):
    pass


class Gearbox:
    def __init__(self, automatic=False):
        self.automatic = automatic
        self.current_gear = Gear.NEUTRAL
        self.clutch_engaged = True  # True = clutch in
        self.rpm = 800  # idle RPM

        self.max_rpm = 6500
        self.idle_rpm = 800
        self.shift_up_rpm = 5500
        self.shift_down_rpm = 1500

        self.forward_gears = [
            Gear.FIRST,
            Gear.SECOND,
            Gear.THIRD,
            Gear.FOURTH,
            Gear.FIFTH,
        ]

    def engage_clutch(self):
        self.clutch_engaged = True

    def release_clutch(self):
        self.clutch_engaged = False

    def shift_to(self, gear: Gear):
        if self.automatic:
            raise GearboxError("Cannot manually shift an automatic gearbox")

        if not self.clutch_engaged:
            raise GearboxError("Clutch must be engaged to shift")

        self.current_gear = gear

    def apply_throttle(self, throttle: float):
        """
        throttle: 0.0 - 1.0
        """
        throttle = max(0.0, min(1.0, throttle))

        if self.current_gear == Gear.NEUTRAL or self.clutch_engaged:
            self.rpm += throttle * 2000
        else:
            self.rpm += throttle * 3000

        self.rpm = min(self.rpm, self.max_rpm)

        if self.automatic:
            self._auto_shift()

    def apply_brake(self, force: float):
        force = max(0.0, min(1.0, force))
        self.rpm -= force * 3000
        self.rpm = max(self.idle_rpm, self.rpm)

        if self.automatic:
            self._auto_shift()

    def _auto_shift(self):
        if self.current_gear == Gear.NEUTRAL:
            self.current_gear = Gear.FIRST
            return

        if self.current_gear in self.forward_gears:
            idx = self.forward_gears.index(self.current_gear)

            if self.rpm > self.shift_up_rpm and idx < len(self.forward_gears) - 1:
                self.current_gear = self.forward_gears[idx + 1]
                self.rpm -= 2000

            elif self.rpm < self.shift_down_rpm and idx > 0:
                self.current_gear = self.forward_gears[idx - 1]
                self.rpm += 1500

    def status(self):
        return {
            "gear": self.current_gear.name,
            "rpm": int(self.rpm),
            "clutch_engaged": self.clutch_engaged,
            "mode": "automatic" if self.automatic else "manual",
        }

gearbox = Gearbox(automatic=True)

for _ in range(5):
    gearbox.apply_throttle(0.7)
    print(gearbox.status())
