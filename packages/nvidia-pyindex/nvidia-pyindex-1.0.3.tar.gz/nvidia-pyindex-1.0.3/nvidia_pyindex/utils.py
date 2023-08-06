import subprocess
import shlex
import json


def get_configuration_files():

    command = 'python -c "from pip._internal.configuration import ' \
              'get_configuration_files; print(get_configuration_files())"'

    command = shlex.split(command)

    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        output = output.decode()
    except subprocess.CalledProcessError as e:
        output = e.output.decode()
        raise RuntimeError(output) from e

    output = output.replace("'", '"')
    output = json.loads(output)

    return output

