Charpe
======

.. image:: https://travis-ci.org/tracsa/charpe.svg?branch=master
   :target: https://travis-ci.org/tracsa/charpe
   :alt: Build Status

**Distributes messages using different media**

Cacahuate's message delivery is in charge of distributing the  messages among
the users of the platform

Deploy
------

* Clone
* copy settings.py to settings_<environment>.py and modify (Don't override settings with default values)
* create virtualenv
* install requirements
* export settings to environment variable BROKER_SETTINGS
* run `python main.py`
