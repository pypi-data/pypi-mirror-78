deploy = '''
from setux.targets import Local

host = Local(name='remote')
host.deploy('{module}'{kwargs})
'''

script = '''
#!/bin/bash

export PYTHONPATH={path}:$PYTHONPATH
cd {path}
python3 {name}
'''
