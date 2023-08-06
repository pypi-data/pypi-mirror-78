This is a utility package to interact with an
Orange and Rockland Utility smart energy meter

Oru calls the API of the Orange and Rockland Utility
smart energy meter to return the current energy usage.

It requires a meter number.
You can find your meter number fon your Orange and Rockland Utility bill.

Example usage::

    from oru import Meter

    meter = Meter("701138804")
    energy_usage_kWh = meter.last_read()

