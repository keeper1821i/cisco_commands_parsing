import json
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
import pathlib

from textfsm import TextFSMError

dir_path = pathlib.Path.cwd()
my_textfsm = pathlib.Path( 'templates', 'cisco_ios_show_running-config.textfsm')

commands_list = ["show version",  "show startup-config", "show running-config", "show access-list", "show interfaces"]
with open('routers.json', 'r') as read_file:
    routers = json.load(read_file)


def send_show_command(device, commands):
    res = {}
    try:
        for i in device['routers']:
            res[i['host']] = {}
            with ConnectHandler(**i) as router:
                router.enable()

                for command in commands:
                    try:
                        output = router.send_command(command, use_textfsm=True)
                    except TextFSMError:
                        output = router.send_command(command, use_textfsm=True, textfsm_template=my_textfsm)

                    res[i['host']][command] = output

        return res
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)


if __name__ == "__main__":
    result = send_show_command(routers, commands_list)
    with open('result.json', 'w') as write_file:
        json.dump(result, write_file, indent=4, sort_keys=True)
