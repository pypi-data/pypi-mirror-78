This is a utility package to interact with an Orange and Rockland Utility smart energy meter

Oru calls the APIs of the Orange and Rockland Utility smart energy meter to return the latest meter read value and unit of measurement.

It requires the oru.com credentials (email, password, MFA answer) and the account id and meter number.
To set up your MFA aswer, log ingto oru.com, go to your profile and reset your 2FA method. When setting up 2FA again, there will be option to say you do not have texting on your phone. Select this and you should be able to use a security question instead.
The account id and meter number can be found on your Orange and Rockland Utility bill.

Example usage::

    from oru import Meter

    meter = Meter(
        email="myemail@email.com",
        password="myorupassword",
        mfa_answer="myorumfaanswer",
        account_id="cd754d65-5380-11e8-2307-2656615779bf",
        meter_id="703437804")

    value, unit_of_measurement = event_loop.run_until_complete(meter.last_read())

