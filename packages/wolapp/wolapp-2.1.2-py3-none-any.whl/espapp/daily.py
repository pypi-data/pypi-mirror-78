from espapp.esp import comp_info, tool_run, format_data
from espapp.esp import dirname
import json
import requests
import uuid, re

def update_new_comp():
    #    global macs
    #    global names
    #    global dirname

    with open(dirname + '/data/log', 'a') as f:
        f.write("update started")

    path1 = dirname + "/data/main_names.json"
    path2 = dirname + "/data/main_macs.json"
    path3 = dirname + "/data/main_ips.json"

    try:
        with open(path1) as f:
            name2 = json.load(f)

        with open(path2) as f:
            mac2 = json.load(f)

        with open(path3) as f:
            ip2 = json.load(f)

        f.close()

        jsondata = []
        for index in range(0, len(mac2)):
            list = [name2[index], mac2[index], ip2[index]]
            jsondata.append(list)

        #        with open(dirname + '/data/log', 'a') as f:
        #            f.write("dswdwd{0}".format(count))

        #        with open(path1, 'w') as f:
        #            json.dump(names, f)

        #        with open(path2, 'w') as f:
        #            json.dump(macs, f)

        try:
            with open(dirname + '/data/.temp') as f:
                array = json.load(f)

            master_computer_mac = (':'.join(re.findall('..', '%012x' % uuid.getnode())))   # fetching computer mac add

            data_update = {}
            data_update["wifi"] = array[1]
            data_update["sub_host"] = jsondata
            data_update["master_mac"] = master_computer_mac

            collect_json_data = json.dumps(data_update)

        except Exception as ex:
            print(" failed to fetch credit")
            with open(dirname + '/data/log', 'a') as l:
                l.write(type(ex).__name__)


        send = "https://dashboard.kratinn.com/api/update_auto/"
        #ssend = "http://192.168.61.180:5001/api/update_auto/"
        send += array[2]

        try:
            r = requests.post(send, headers=array[0], data=collect_json_data)
            if r.status_code == 200:
                print("Process completed successfully")
                return 1
            else:
                print("Please check internet connection or Enter correct Device ID and password")
                return 0

        except:
            print("FAILED to connect to server, Please check internet connection ")
            return 0



    except Exception as ex:
        print("daily scan fails")
        with open(dirname + '/data/log', 'w') as l:
            l.write(type(ex).__name__)


def daily_runner():
    try:
        comp_info()
        tool_run()
        format_data()  # updates names and macs
        update_new_comp()

    except Exception as ex:
        with open(dirname + '/data/log', 'w') as l:
            l.write(type(ex).__name__)


daily_runner()
