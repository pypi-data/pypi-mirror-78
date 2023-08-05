# MqTLS client for python
This repository contains the client of Message Queuing Telemetry over SSL/TLS for python. You can read more at: <https://github.com/efrenbg1/gobroker>

## Install
```bash
$ pip3 install mqtls
or
$ pip install mqtls
```
PyPI link: <https://pypi.org/project/mqtls/>

## Usage
Basic usage in master mode:
```python
from mqtls import mqtls

broker = mqtls()

if broker.mpublish('mytopic', 0, 'hello from python'):
    print("Message sent!")

print(broker.mretrieve('mytopic', 0))
```
You may also use it as a normal client:
```python
from mqtls import mqtls

broker = mqtls(host='127.0.0.1', port=2443, user='myuser', pw='secret!')

if broker.publish('mytopic', 0, 'hello from python'):
    print("Message sent!")

print(broker.retrieve('mytopic', 0))
```

## License
Copyright © 2020 Efrén Boyarizo <efren@boyarizo.es><br>
This work is free. You can redistribute it and/or modify it under the
terms of the Do What The Fuck You Want To Public License, Version 2,
as published by Sam Hocevar. See http://www.wtfpl.net/ for more details.