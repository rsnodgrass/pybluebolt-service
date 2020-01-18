# pybluebolt - Python interface for BlueBOLT Remote Energy Management

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=WREP29UDAMB6G)

Python library for communicating with the [BlueBOLT Remote Energy Management cloud](https://www.panamax.com/power-management/bluebolt-20-ip-power-management) for remotely controlling BlueBOLT devices. This does not currently support direct control of local BlueBOLT devices via RS232 or telnet.

NOTE:

* Directly communicating with a local BlueBOLT device is almost always preferred to communicating with the cloud, as that status/changes can be instaneous and the integration can work even when offline without an Internet connection. However, there are some BlueBOLT configuration details that are only available in the cloud. This does not yet support direct interaction with a local BlueBOLT device (and may never, as that might be better as a separate package).
* This library is community supported, please submit changes and improvements.
* This is a very basic beta-quality interface that may need to be refactored in the future.

## Installation

```
pip3 install pybluebolt
```

## Examples

```python
bluebolt = PyBlueBOLT(username, password)
locations = bluebolt.locations

home = locations[0]
```

See also [example-client.py](example-client.py) for a working example.

## Supported Hardware

* [Panamax M4315-Pro 8-outlet](https://www.amazon.com/Panamax-M4315-PRO-Bluebolt-Management-Monitoring/dp/B003XEAQTU?tag=rynoshark-20)
* [Panamax M4320-Pro 8 outlet](https://www.amazon.com/Panamax-M4320-Programmable-Power-Management/dp/B007I4GLQI?tag=rynoshark-20)
* [Panamax M4000 8 outlet](https://www.amazon.com/Panamax-Outlet-BlueBOLT-Programmable-Management/dp/B00WK646I4?tag=rynoshark-20)

## See Also

* [MyBlueBOLT Portal](https://www.mybluebolt.com/)
* [BlueBOLT local device webservice proxy](https://github.com/Tenflare/bluebolt-api)
* Home Assistant integration for BlueBOLT devices [hass-bluebolt]

## Known Issues

#### Unsupported

* direct control of a BlueBOLT device via telnet or RS232 
