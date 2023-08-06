def check_config_value(data={},match=""):
    if not isinstance(data,dict): 
        return "check data type is not dict,but {}".format((type(data)))
    if not data: return "data is null obj"
    for k,v in data.items():
        if isinstance(v,list):
            for i in v:
                if isinstance(i,dict):
                    if check_config_value(v,match) == "ok": break
                    break
                if i == match:
                    # print(v)
                    # print("matched ",i,match)
                    break
                if check_config_value(v,match) == "ok": break
            continue
        # for i in match:
        # print(v)
        if v == match: 
            # print("matched ",v,match)
            return "ok"
        if check_config_value(v,match) == "ok": break
            # return True
    return False


if __name__ == "__main__":
    data = {
        "config": {
            "dst": {"ip_type": "step", "dst_ip": {"start_ip":"","max_ip":"1.1.1.10","min_ip":"1.1.1.1","inc":"1"},"port_type": "scatter","dst_port":[4444,3333,2222]},
            "method": "ssdp",
            "pkt_args":{"ssdp_pkt_type":"reply","ssdp_ip":"8.8.8.8"},
            "setting": {"tag_id": "12", "tag_pri": "7"},
            "src": {"ip_type": "scatter", "src_ip":["1.1.1.1", "11.1.1.2", "1.1.51.3"],"port_type": "scatter","src_port":[5555,6666,7777]},
            "test_args": {"total": "1000", "speed": "100", "timer": "60", "sustain": True},
            "arp_attr": {"is_arp": True, "gw_ip": "192.168.11.2", "if_ip": "192.168.11.1"}
        }
    }
    res = check_config_value(data)
    # print(res)
