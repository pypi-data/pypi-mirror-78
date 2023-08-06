import paramiko
from netmiko import ConnectHandler
from netmiko import ssh_exception
import os
import shlex
import subprocess
import re

error_tuple = (
    ssh_exception.SSHException,
    ssh_exception.NetMikoTimeoutException,
    ssh_exception.NetMikoAuthenticationException,
    ssh_exception.AuthenticationException,
)

default_pattern = re.compile('.*')


def handle_huawei_port_ip(port_name):
    return "dis ip int {} | in Address".format(port_name)


def sftp_exec_command(command='\n', **kwargs):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(**kwargs, timeout=20)
        # chan = ssh_client.invoke_shell()
        # chan.send(command)
        # recv = chan.recv(100)
        stdin, stdout, stderr = ssh_client.exec_command(command)
        # print(stdout.read())
        # for line in std_out:
        #     print(line.strip("\n"))
        ssh_client.close()
    except Exception as e:
        pass
        # print(str(e))


class DeviceConn():

    DEV_TYPE_DICT = {
        # "CISCO": "cisco",
        "CISCO_IOS": "cisco_ios",
        # "CISCO_XR": "cisco_xr",
        "JUNIPER": "juniper",
        # "JUNIPER_JUNOS": "juniper_junos",
        "HUAWEI": "huawei",
        "HUAWEI_VRPV8": "huawei_vrpv8"
    }

    DEV_TYPE_CMD_SHOW_INTERFACE = {
        # "CISCO": "cisco",
        "cisco_ios": "show interfaces ",
        # "CISCO_XR": "cisco_xr",
        "juniper": "show interfaces ",
        # "JUNIPER_JUNOS": "juniper_junos",
        # "huawei": "display cu interface ",
        "huawei": handle_huawei_port_ip,
        # "HUAWEI_VRPV8": "huawei_vrpv8"
    }

    DEV_TYPE_CMD_SHOW_ARP = {
        # "CISCO": "cisco",
        "cisco_ios": "show arp ",
        # "CISCO_XR": "cisco_xr",
        "juniper": "show arp interface ",
        # "JUNIPER_JUNOS": "juniper_junos",
        "huawei": "display arp interface ",
        # "HUAWEI_VRPV8": "huawei_vrpv8"
    }

    RE_PATTERN = {
        'ip_pattern_raw': '(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)',
        'ip_pattern': re.compile(
            '(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)'),
        'ip_pattern_like': re.compile(
            '.*(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d).*'),
        'port_pattern': re.compile('interface .*')
    }

    def __init__(self, *args, **kwargs):
        self.conn = None
        self._device_info = kwargs

    @property
    def device_info(self):
        """
        para:
        return:
        """
        return self._device_info

    def connect(self, strip=True, **kwargs):
        try:
            self.conn = ConnectHandler(**self.device_info)
        except error_tuple as e:
            # print("--->", str(e))
            raise Exception(e)
        try:
            self.conn.enable()
        except Exception as e:
            # print(str(e))
            raise Exception(e)
        if strip:
            return self._strip_sep(self.conn.find_prompt())
        return self.conn.find_prompt()

    def exec_cmd(self, cmd, _filter=False, pattern=default_pattern):
        """
        param :
        return:
        """
        res_raw = self.conn.send_command(cmd)
        if _filter:
            return pattern.search(res_raw).group()
            # return re.findall(pattern, res_raw, re.M)
        return res_raw

    def disconnect(self):
        self.conn.disconnect()

    def _strip_sep(self, prompt):
        if self.device_info.get("device_type") == self.DEV_TYPE_DICT.get("CISCO_IOS"):
            prompt = prompt.strip("#")
            try:
                return prompt.split(":")[1]
            except Exception as e:
                # print(str(e))
                return prompt
        elif self.device_info.get("device_type") == self.DEV_TYPE_DICT.get("JUNIPER"):
            prompt = prompt.strip(">").strip("<")
            try:
                return prompt.split("@")[1]
            except Exception as e:
                # print(str(e))
                return prompt
        elif self.device_info.get("device_type") == self.DEV_TYPE_DICT.get("HUAWEI"):
            prompt = prompt.strip(">").strip("<")
            # try:
            #     prompt.split("@")[1]
            # except Exception as e:
            #     print(str(e))
            #     return prompt
            return prompt
        return prompt


class DeviceHandler:

    def handler_local_and_remote_addr(self, *args, **kwargs):
        """
        param :
        return:
        """
        raise NotImplementedError(
            "handler_local_and_remote_addr must be implement in subclass")

    def get_vendor(self, *args, **kwargs):
        raise NotImplementedError(
            "get_vendor must be implement in subclass")

    def get_os(self, *args, **kwargs):
        raise NotImplementedError(
            "get_os must be implement in subclass")

    def get_version(self, *args, **kwargs):
        raise NotImplementedError(
            "get_version must be implement in subclass")

    def get_interfaces_brief(self, *args, **kwargs):
        raise NotImplementedError(
            "get_interfaces_brief must be implement in subclass")


class CiscoDevConn(DeviceConn,
                   DeviceHandler):

    # def __init__():
    #     super.__init__()

    def handler_local_and_remote_addr(self, device_type, ap_phyical_port, pattern, *args, **kwargs):
        """
        param :
        return:
        """
        # print("handle cisco device addr")
        # self.conn.enable()
        # local_addr
        device_type_cmd_show_int = self.DEV_TYPE_CMD_SHOW_INTERFACE.get(
            device_type)
        cmd = device_type_cmd_show_int + ap_phyical_port
        local_addr = self.exec_cmd(cmd, _filter=True, pattern=pattern)
        # remote_addr
        device_type_cmd_show_arp_int = self.DEV_TYPE_CMD_SHOW_ARP.get(
            device_type)
        cmd = device_type_cmd_show_arp_int + ap_phyical_port
        arp_raw = self.exec_cmd(cmd, _filter=False)
        addr_raw = re.findall(pattern, arp_raw)
        if len(addr_raw) == 2:
            # print(".".join(addr_raw[0]), ".".join(addr_raw[1]))
            result = {
                "local_addr": local_addr,
                "remote_addr": ".".join(addr_raw[1]) if local_addr == ".".join(addr_raw[0]) else ".".join(addr_raw[0])
            }
            return result
        else:
            raise Exception("get cisco address fail: <{}>".format(cmd))

    def get_interfaces_brief(self, pattern, *args, **kwargs):
        if pattern:
            res_raw = self.exec_cmd("show ipv4 interface brief")
        else:
            res_raw = self.exec_cmd("show ipv4 interface brief", _filter=False)


class JuniperDevConn(DeviceConn,
                     DeviceHandler):

    def handler_local_and_remote_addr(self, device_type, ap_phyical_port, pattern, *args, **kwargs):
        """
        param :
        return:
        """
        # handle cisco device addr
        # self.conn.enable()
        # local_addr
        device_type_cmd_show_int = self.DEV_TYPE_CMD_SHOW_INTERFACE.get(
            device_type)
        cmd = device_type_cmd_show_int + ap_phyical_port
        local_addr = self.exec_cmd(cmd, _filter=True, pattern=pattern)
        # remote_addr
        device_type_cmd_show_arp_int = self.DEV_TYPE_CMD_SHOW_ARP.get(
            device_type)
        cmd = device_type_cmd_show_arp_int + ap_phyical_port
        arp_raw = self.exec_cmd(cmd, _filter=False)
        addr_raw = re.findall(pattern, arp_raw)
        if len(addr_raw) == 2:
            # print(".".join(addr_raw[0]), ".".join(addr_raw[1]))
            result = {
                "local_addr": local_addr,
                "remote_addr": ".".join(addr_raw[0])
            }
            return result
        else:
            raise Exception("get juniper address fail: <{}>".format(cmd))


class HuaweiDevConn(DeviceConn,
                    DeviceHandler):

    def handler_local_and_remote_addr(self, device_type, ap_phyical_port, pattern, *args, **kwargs):
        """
        param :
        return:
        """
        # handle cisco device addr
        device_type_cmd_show_int = self.DEV_TYPE_CMD_SHOW_INTERFACE.get(
            device_type)
        if callable(device_type_cmd_show_int):
            # cmd = "dis ip int GigabitEthernet2/1/1 | in Address"
            cmd = device_type_cmd_show_int(ap_phyical_port)
        else:
            cmd = device_type_cmd_show_int + ap_phyical_port

        local_addr = self.exec_cmd(
            cmd, _filter=True, pattern=pattern)
        # print(local_addr)
        # remote_addr
        device_type_cmd_show_arp_int = self.DEV_TYPE_CMD_SHOW_ARP.get(
            device_type)
        cmd = device_type_cmd_show_arp_int + ap_phyical_port
        arp_raw = self.exec_cmd(cmd, _filter=False)
        addr_raw = re.findall(pattern, arp_raw)
        if len(addr_raw) == 2:
            # print(".".join(addr_raw[0]), ".".join(addr_raw[1]))
            result = {
                "local_addr": local_addr,
                "remote_addr": ".".join(addr_raw[1]) if local_addr == ".".join(addr_raw[0]) else ".".join(addr_raw[0])
            }
            return result
        else:
            raise Exception("get huawei address fail: <{}>".format(cmd))


class DevType():
    CISCO = "cisco"
    CISCO_IOS = "cisco_ios"
    CISCO_XR = "cisco_xr"
    JUNIPER = "juniper"
    JUNIPER_JUNOS = "juniper_junos"
    HUAWEI = "huawei"
    HUAWEI_VRPV8 = "huawei_vrpv8"


DEV_TYPE_CLASS_MAP = {
    "cisco_ios": CiscoDevConn,
    "juniper": JuniperDevConn,
    "huawei": HuaweiDevConn,
}


def test_cisco():

    validated_data = {
        "device_type": "cisco_ios",
        "ip": "172.17.17.8",
        "port": 22,
        "username": "noc",
        "password": "xc(%v+1@&&ASDF+",
    }
    device_type = validated_data.get("device_type")
    ap_phyical_port = "tenGigE0/1/1/2"
    try:
        dev_type_class = DEV_TYPE_CLASS_MAP.get("cisco_ios")
        dev_conn = dev_type_class(**validated_data)
        pattern = dev_conn.RE_PATTERN.get("ip_pattern")
        dev_conn.connect(strip=False)
        result = dev_conn.handler_local_and_remote_addr(
            device_type, ap_phyical_port, pattern)
        # dev_conn.get_interfaces_brief()
        dev_conn.disconnect()
    except Exception as e:
        # print(str(e))
        dev_conn.disconnect()
        # return response.DefaultResponse(code=False, msg=str(e))
    # print(result)
    # return response.DefaultResponse(result, status=status.HTTP_200_OK)


def test_junper():
    validated_data = {
        "device_type": "juniper",
        "ip": "10.44.0.254",
        "port": 22,
        "username": "ne40_noc",
        "password": "+9*fAD-\\7djnJGjH"
    }
    device_type = validated_data.get("device_type")
    ap_phyical_port = "et-0/2/1.0"
    try:
        dev_type_class = DEV_TYPE_CLASS_MAP.get(device_type)
        dev_conn = dev_type_class(**validated_data)
        pattern = dev_conn.RE_PATTERN.get("ip_pattern")
        dev_conn.connect(strip=False)
        result = dev_conn.handler_local_and_remote_addr(
            device_type, ap_phyical_port, pattern)
        dev_conn.disconnect()
    except Exception as e:
        # print(str(e))
        dev_conn.disconnect()
        # return response.DefaultResponse(code=False, msg=str(e))
    # print(result)
    # return response.DefaultResponse(result, status=status.HTTP_200_OK)

    # juniper = {
    #     "device_type": DevType.JUNIPER,
    #     "ip": "10.44.0.254",
    #     "port": 22,
    #     "username": "ne40_noc",
    #     "password": "+9*fAD-\\7djnJGjH"
    # }
    # # +9*fAD-\7djnJGjH
    # dc = DeviceConn(**juniper)
    # p = dc.connect()
    # print(p)
    # dc.conn.enable()  # 相当于进入特权模式
    # cmd = 'show interfaces et-0/2/1.0'
    # pattern = dc.RE_PATTERN.get("ip_pattern")
    # res = dc.exec_cmd(cmd, _filter=True, pattern=pattern)
    # print(res)
    # cmd = 'show arp interface et-0/2/1.0'
    # res = dc.exec_cmd(cmd, _filter=False)
    # res = re.findall(pattern, res)
    # print(res)


def test_huawei():
    """
    param :
    return:
    """
    validated_data = {
        "device_type": "huawei",
        "ip": "10.40.0.8",
        "port": 22,
        "username": "ikglobal_l0",
        "password": "AQToUAKFr^KXCC*B"
    }
    device_type = validated_data.get("device_type")
    ap_phyical_port = "GigabitEthernet2/1/1"
    try:
        dev_type_class = DEV_TYPE_CLASS_MAP.get(device_type)
        dev_conn = dev_type_class(**validated_data)
        pattern = dev_conn.RE_PATTERN.get("ip_pattern")
        dev_conn.connect(strip=False)
        result = dev_conn.handler_local_and_remote_addr(
            device_type, ap_phyical_port, pattern)
        dev_conn.disconnect()
    except Exception as e:
        print(str(e))
        dev_conn.disconnect()
        # return response.DefaultResponse(code=False, msg=str(e))
    print(result)


def test_junper():
    validated_data = {
        "device_type": "juniper",
        "ip": "10.44.0.254",
        "port": 22,
        "username": "ne40_noc",
        "password": "+9*fAD-\\7djnJGjH"
    }
    device_type = validated_data.get("device_type")
    ap_phyical_port = "et-0/2/1.0"
    try:
        dev_type_class = DEV_TYPE_CLASS_MAP.get(device_type)
        dev_conn = dev_type_class(**validated_data)
        pattern = dev_conn.RE_PATTERN.get("ip_pattern")
        dev_conn.connect(strip=False)
        result = dev_conn.handler_local_and_remote_addr(
            device_type, ap_phyical_port, pattern)
        dev_conn.disconnect()
    except Exception as e:
        print(str(e))
        dev_conn.disconnect()
        # return response.DefaultResponse(code=False, msg=str(e))
    print(result)



def test():
    c = """ 
    RP/0/RSP0/CPU0:USLA-C201-A9K-3#show arp tenGigE0/1/1/2
Thu Dec 19 02:25:17.251 PST

-------------------------------------------------------------------------------
0/1/CPU0
-------------------------------------------------------------------------------
Address         Age        Hardware Addr   State      Type  Interface
218.30.48.137   03:02:19   b026.807b.09c7  Dynamic    ARPA  TenGigE0/1/1/2
218.30.48.138   -          10f3.113d.701e  Interface  ARPA  TenGigE0/1/1/2
    """
    ip_pattern = DeviceConn.RE_PATTERN.get("ip_pattern")
    ip_pattern = '(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)'
    result = re.findall(ip_pattern, c, re.M)
    # result = re.split(" ", result)
    # # for i in result:
    # #     print(type(i),len(i))
    # #     if i != '' or i != ' ': print(i)
    # result = [i for i in result if len(i) != 0 or i != '-']
    print(result)
    # print(len(result))
    print(".".join(result[0]), ".".join(result[1]))


if __name__ == "__main__":
    test_junper()
    # test_cisco()
    # test_huawei()
    # test()
