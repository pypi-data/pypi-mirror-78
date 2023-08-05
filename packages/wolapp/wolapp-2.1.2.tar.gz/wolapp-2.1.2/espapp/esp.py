import socket, os, sys, requests, json
import uuid, re
import subprocess
from crontab import CronTab
from getpass import getpass
import time

import urllib3
urllib3.disable_warnings(urllib3.exceptions.SecurityWarning)

host_ip = ''
host_name = ''
host_mac = ''
names = []
macs = []
ips = []
all_jsons = {}
check_version = 0
dirname = os.path.dirname(__file__)


def test():
    global dirname
    path = dirname + "/data/file.txt"
    f = open(path, "w")
    f.write("ok")
    print("doneit")
    f.close()


def ethtool_x_cp():
    global dirname

    # **************************************************************************************************************
    path = dirname + "/data/ether.data"
    f = open(path, "w")
    p = subprocess.check_output(["nmcli", "connection", "show"]).decode("utf-8")
    f.write(p)
    f.close()
    p = subprocess.check_output(["sudo", "awk", "/ethernet/ {print $NF}", path]).decode("utf-8")
    p = p.split()
    # **************************************************************************************************************

    if p == '--':
        print("****************** WARNING: WOL MAY NOT WORK FOR WIFI CONNECTED SYSTEMS ************************")

    subprocess.call(['sudo', 'ethtool', '-s', p[0], 'wol', 'g'])

    # ***********************************************************************************************************
    path = dirname + "/data/ethtoolpyth.py"
    f = open(path, "w")
    f.write("import subprocess\n\r")
    f.write("import time\n\r")
    f.write("print('Running ethtool command')\n\r")
    s = "subprocess.call(['sudo', 'ethtool', '-s', '"
    s += p[0]
    s += "' , 'wol','g' ])\n\r"
    f.write(s)
    f.write("time.sleep(10)\n\r")
    f.write(s)
    f.close()

    try:
        subprocess.call(["sudo", "chmod", "a+x", path])
        # print("Adding ethtoolpyth.py (y/n)")
        # subprocess.call(["sudo", "cp", "-i", path, "/bin"])
        subprocess.call(["sudo", "cp", path, "/bin"])

    except:
        print(" Error while adding file to bin")


def checker(data, length=64):
    if len(data) <= 0 or len(data) > length:
        print("Not valid Input, length must be less than {0}\n\r".format(length))
        return True
    return False


def yn_checker(data):
    data = data.lower()
    if (data == 'n') or (data == 'N') or (data == 'Y') or (data == 'y'):
        return 0
    else:
        print("You enter invalid response {0}. Please enter 'y' for 'yes' and 'n' for 'no' \n\r".format(data))
        return 1


def ip_address_check(data):
    i = 0
    j = 0

    for x in data:
        if x == '.':
            i += 1
        if x == '-':
            j += 1

    if i == 6 and j == 1:
        return 0

    print("i {0} j {1} ip {2}".format(i, j, data))
    return 1


def cron_jobs():
    global check_version
    global dirname
    try:
        print("Running cron command")
        cron = CronTab(user='root')

        print("root access gained")

        for jobs in cron:
            print(jobs)
            if jobs.comment == 'run_it' or jobs.comment == 'daily_run':
                cron.remove(jobs)
                cron.write()

        # **************** knowing python version **********************************
        __knowversion = ''
        if sys.version_info[0] < 3:
            check_version = 2
            # __knowversion = 'python /bin/ethtoolpyth.py &'
            print(" Python version < 3 not supported. Please install python version > 3. Thank you!")
            return 0
        else:
            __knowversion = 'python3 /bin/ethtoolpyth.py &'
        # **************************************************************************

        # job = cron.new(command='python3 /bin/ethtoolpyth.py &', comment="run_it")
        job = cron.new(command=__knowversion, comment="run_it")
        job.every_reboot()
        cron.write()

        # cmd_run = dirname + '/daily.py &'
        # cmd_run = "python3 " + cmd_run
        # job2 = cron.new(command=cmd_run, comment='daily_run')
        # job2.minute.every(2)  # change it to hourly 888888880000000000000000000
        # cron.write()

        for jobs in cron:
            print(jobs)

    except Exception as ex:
        print("Unable to create in job{0} ----{1}".format(type(ex).__name__, ex.args))


def comp_info():
    try:
        global host_name
        global host_mac
        host_name = socket.gethostname()
        # host_ip = socket.gethostbyname(host_name)  # this give local ip
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        host_ip = ip_address  # getting ip address through socket
        print("Master computer IP address: ", host_ip)
        print("Master computer name :  ", host_name)
        #        print("IP : ", host_ip)
        # print(':'.join(re.findall('..', '%012x' % uuid.getnode())))
        host_mac = (':'.join(re.findall('..', '%012x' % uuid.getnode())))
        print("Master computer mac : {0}".format(host_mac))
        print("")
    except:
        print("Unable to get master name and IP")


def tool_run():
    global dirname
    global host_ip
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        host_ip = ip_address  # getting ip address through socket
        s.close()

        ip_address_part = ""
        i = 0
        for x in ip_address:
            if x == '.':
                i += 1
                if i == 3:
                    break
            ip_address_part += x
        # __________________________________________________
        # ip_address_part += "1-"
        # ip_address_part += ip_address[0:11]
        # ip_address_part += "255"
        temp = ip_address_part
        ip_address_part += ".1-"
        ip_address_part += temp
        ip_address_part += ".255"

         # Stage unconformed change *********************************************************
        # print("Your network subnet range :", ip_address_part)

        # correct = input("If it is correct, Enter (y) to continue and (n) to abort installation: ")
        # while yn_checker(correct):
        #     correct = input("If it is correct, Enter (y) to continue and (n) to abort installation: ")
        #
        # if correct[0].lower() == 'n':
        #     print("Aborting installation")
        #     exit()
        #     return 0
        # **************************************************************************************************


        # Uncommeting this code till "88888" series will let you to enter ip range
        print("Your network IP address range: {0}".format(ip_address_part))
        correct = input("Is it correct (y/n): ")

        while yn_checker(correct):
            correct = input("Is it correct (y/n): ")

        if correct[0].lower() == 'n':
            ip_address_part = input("Please enter correct network IP address range (Subnet). For example: (192.168.148.1-192.168.148.255): ")
            while ip_address_check(ip_address_part):
                ip_address_part = input("Please enter correct network IP address range (Subnet). For example: (192.168.148.1-192.168.148.255): ")
        # 88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

        # print("Running Nbtscan ........")
        # subprocess.call(["nbtscan", ip_address_part])
        print("Wait a minute .....")

        path = dirname + "/data/output.txt"
        f = open(path, "w")
        p = subprocess.check_output(["nbtscan", ip_address_part]).decode("utf-8")
        f.write(p)
        f.close()
    except:
        print("Nbt scan failed ( Please check internet is connected!)")

    try:
        path = dirname + "/data/output2.txt"
        f = open(path, "w")
        p2 = subprocess.check_output(["sudo", "arp-scan", ip_address_part]).decode("utf-8")
        f.write(p2)
        f.close()
    except:
        print("arp-scan failed ( Please check internet is connected!)")


def soft_install():
    try:
        print("installing ethtool")
        subprocess.call(["sudo", "apt-get", "install", "ethtool"])
        print("Ethtool installed")

    except:
        print("ethtool installation failed")

    try:
        print("Installing nbttool")
        subprocess.call(["sudo", "apt-get", "install", "nbtscan"])
        print("Nbtscan installed")

    except:
        print("ethtool installation failed")
    try:
        print("Installing arp-scan")
        subprocess.call(["sudo", "apt-get", "install", "arp-scan"])
        print("arp-scan installed")

    except:
        print("arp-scan installtion failed")


def send_data():
    global names
    global macs
    global ips
    global host_ip
    global dirname
    try:

        print("")
        print("  <---------------  Press ' ctrl + z'  to stop program --------------> \n\r")
        print(" **Note: There must be only one master computer in a network ")
        print(" Master computer: Scans all other computer in the network through which it is connected")
        master = input("Is it master computer (y/n): ")

        while yn_checker(master):
            master = input("Is it master computer (y/n): ")

        # for x in range(0, len(macs)):
        #   print("{0}---------{1} --------- {2}".format(names[x], macs[x], ips[x]))s

        jsondata = []
        for i in range(1, len(macs)):
            list = [names[i], macs[i], ips[i]]
            jsondata.append(list)

        # for x in jsondata:
        #     print(x)

        # *****clubing****************************************************

        check = input("Do you want to update this computer details on WOL device (y/n) : ")

        while yn_checker(check):
            check = input("Do you want to update this computer details on WOL device (Y/n) : ")

        if check[0].lower() == 'n':
            return 1

        print("")
        print(" - - - - - All inputs are case sensitive! - - - - - - - - - ")
        print("")

        name = input("Enter email that is registered with Kratinn dashboard: ")
        # while len(name) != 12:
        #     print("Must be of length 12")
        #     name = input("Enter Device ID  : ")

        userpass = getpass("Enter Kratinn password (Hidden Field): ")
        while checker(userpass, length=64):
            userpass = getpass("Enter Kratinn dashboard password (Hidden Field): ")

        user_repass = getpass("Re-Enter Kratinn dashboard password (Hidden Field): ")
        while checker(user_repass, length=64):
            user_repass = getpass("Re-Enter Kratinn dashboard password (Hidden Field): ")

        while user_repass != userpass:
            print("WOL device password does not match: Please try again")
            userpass = getpass("Enter Kratinn dashboard password (Hidden Field): ")
            while checker(userpass, length=64):
                userpass = getpass("Enter Kratinn dashboard password (Hidden Field): ")

            user_repass = getpass("Re-Enter Kratinn dashboard password (Hidden Field): ")
            while checker(user_repass, length=64):
                user_repass = getpass("Re-Enter Kratinn dashboard password (Hidden Field): ")

        # wifi = input("Enter WiFi name (SSID)  : ")
        # while checker(wifi, length=32):
        #     wifi = input("Enter WiFi name (SSID)  : ")
        #
        #
        # password = getpass("WiFi password (Hidden Field): ")
        # while checker(password, length=64):
        #     password = getpass("WiFi password (Hidden Field): ")
        #
        # re_password = getpass("Re-enter WiFi password (Hidden Field): ")
        # while checker(re_password, length=64):
        #     re_password = getpass("Re-enter WiFi password (Hidden Field): ")
        #
        # while re_password != password:
        #     print("WiFi password does not match: Please try again")
        #     password = getpass("WiFi password (Hidden Field): ")
        #     while checker(password, length=64):
        #         password = getpass("WiFi password (Hidden Field): ")
        #
        #     re_password = getpass("Re-enter WiFi password (Hidden Field): ")
        #     while checker(re_password, length=64):
        #         re_password = getpass("Re-enter WiFi password (Hidden Field): ")

        # *!!!!!!!!!!!!!!!!!!!!!!*************************************************************************************

        headers = {}
        send = "https://dashboard.kratinn.com/api/first_login"
        #send = "http://192.168.61.180:5001/api/first_login"

        try:
            r = requests.post('https://dashboard.kratinn.com/api-token-auth/',
                              data={'username': name, 'password': userpass})

            if r.status_code == 200:
                print(".......... . . .")
                token = eval(r.text)
                headers["Authorization"] = "Token " + token["token"]

            else:
                print("Please check internet connection or Enter correct Device ID or password")
                return 0

            r = requests.get(send, headers=headers)
            if r.status_code == 200:
                print("\n\rLogin successfully\n\r")
                WOL_devices = json.loads(r.text)

                try:
                    if len(WOL_devices['WOL_Devices']) == 0:
                        print("No device found. Please register WOl device first")
                        time.sleep(7)
                        exit()
                except IndexError:
                    print("No device found. Please register WOl device first")
                    time.sleep(7)
                    exit()

                WOL_id = []
                if len(WOL_devices['WOL_Devices']) == 1:
                    WOL_id.append(WOL_devices['WOL_Devices'][0][1])
                    option = 1
                    print("\n\r\n\r WOL device name: {0} \n\r WOL Device ID: {1} \n\r\n\r".format(
                        WOL_devices['WOL_Devices'][0][0], WOL_id[option - 1]))
                else:

                    print("\n\r\n\r Please select your WOL device \n\r")
                    i = 1
                    for x in WOL_devices['WOL_Devices']:
                        print("{0}) Device name: {1} | Device id: {2}".format(i, x[0], x[1]))
                        WOL_id.append(x[1])
                        i += 1

                    try:
                        option = int(input(" Enter number between 1 to {0} to select your device: ".format(i - 1)))
                    except ValueError:
                        print("Please enter valid number")

                    while (option < 1) and (option > (i - 1)):
                        try:
                            option = int(input(" Enter number between 1 to {0} to select your device: ".format(i - 1)))
                        except ValueError:
                            print("Please enter valid number")

                    print("Seleted option: {0}) {1} {2}".format(option, WOL_devices['WOL_Devices'][option - 1][0],
                                                                WOL_devices['WOL_Devices'][option - 1][1]))

                    new_check = input("Do you want to continue? (y/n): ")
                    while yn_checker(new_check):
                        new_check = input("Do you want to continue? (y/n): ")

                    if new_check[0].lower() == 'n':
                        return 0

                # send = send_per
                send = "https://dashboard.kratinn.com/api/network/"
                #send = "http://192.168.61.180:5001/api/network/"
                send += WOL_id[option - 1]

                device_id = WOL_id[option - 1]

                r = requests.get(send, headers=headers)
                if r.status_code == 200:
                    ssid_list = json.loads(r.text)

                # __________________________________________________________________________________

                try:
                    if len(ssid_list['SSID']) == 0:
                        pass
                except IndexError:
                    print("\n\r No router present. Please reset WOL device, go to 'wifi password setting' and enter "
                          "router name{s) and password \n\r")
                    time.sleep(7)
                    exit()

                i = 1
                option = 1
                master_mac = []

                if len(ssid_list['SSID']) == 1:
                    print("Router: {0}".format(ssid_list['SSID'][0][0]))
                    master_mac.append(ssid_list['SSID'][0][1])

                else:

                    print("\n\r ** Note: Make sure you enter correct option of router through which master computer is "
                          "connected  **\n\r")

                    print("Router List:")
                    print("")

                    for x in ssid_list['SSID']:
                        print("{0}) {1} ".format(i, x[0]))
                        master_mac.append(x[1])
                        i += 1

                    try:
                        option = int(input(" Enter number between 1 to {0} to select your router: ".format(i - 1)))
                    except ValueError:
                        print("Please enter valid number")

                    while (option < 1) and (option > (i - 1)):
                        try:
                            option = int(input(" Enter number between 1 to {0} to select your router: ".format(i - 1)))
                        except ValueError:
                            print("Please enter valid number")

                    print("Seleted option: {0}) {1}".format(option, ssid_list['SSID'][option - 1][0]))

                if master_mac[option - 1] != 'Not Provided' and master_mac[option - 1] != host_mac.upper() and master[
                    0].lower() != 'n':
                    print("\n\r** Router {0} already have master computer with mac {1}. Do you want make this "
                          "computer Master ?".format(ssid_list['SSID'][option - 1][0], master_mac[option - 1]))
                else:
                    if master_mac[option - 1] == 'Not Provided' and master[0].lower() == 'n':
                        print("\n\r\n\r\n\r ********* Please first run espapp on master computer ********** "
                              "\n\r\n\r\n\r")
                        return 0
                    if master_mac[option - 1] != 'Not Provided' and master_mac[option - 1] != host_mac.upper():
                        print("* Mac address of master computer for router '{0}': {1}".format(
                            ssid_list['SSID'][option - 1][0], master_mac[option - 1]))

                new_check = input("Do you want to continue? (y/n): ")
                while yn_checker(new_check):
                    new_check = input("Do you want to continue? (y/n): ")

                if new_check[0].lower() == 'n':
                    return 0

                wifi = ssid_list['SSID'][option - 1][0]
                password = "**********"

                # __________________________________________________________________________________
                # __________________________________________________________________________________

                # ******************************** Storing credits for daily scan ***************
                credits = [headers, wifi, device_id]
                path3 = dirname + "/data/.temp"
                #        os.chmod(path3, 0o600)
                with open(path3, 'w') as f:
                    json.dump(credits, f)

                # __________________________________________________________________________________

            else:
                print("Please check internet connection or Enter correct Device ID or password")
                return 0

        except:
            print("FAILED to connect to server, Please check internet connection ")
            return 0

        # ******************************************!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        daily_scan = 'n'
        check = 'n'

        if master[0].lower() == 'y':
            print("")
            print("List of all other computers in master computer network\n\r")
            for x in range(0, len(macs)):
                print("{0}---------{1} --------- {2}".format(names[x], macs[x], ips[x]))

            print(" Total number of computer interfacing unit scanned on this network: {0}".format(len(macs)))

            print("")
            check = input("Do you want to update all above computers details on WOL device (y/n): ")
            while yn_checker(check):
                check = input("Do you want to update all above computers details on WOL device (y/n) : ")

            daily_scan = input(
                "Do you want to run daily scan on master computer network ( !Helps to keep WOL device updated)  (y/n) : ")
            while yn_checker(daily_scan):
                daily_scan = input(
                    "Do you want to run daily scan on master computer network ( !Helps to keep WOL device updated)  (y/n) : ")

        print("")
        submit = input("Do you want to submit all above information? Sure!  (y/n): ")
        while yn_checker(submit):
            submit = input("Do you want to submit all above information? Sure!  (y/n): ")

        if submit[0].lower() == 'n':
            return 0

        # ********************************************** daily.py to cron *********************************
        if daily_scan[0].lower() == 'y':
            cron = CronTab(user='root')
            cmd_run = dirname + '/daily.py &'
            cmd_run = "python3 " + cmd_run
            job2 = cron.new(command=cmd_run, comment='daily_run')
            # job2.minute.every(15)  # change it to hourly 888888880000000000000000000
            job2.hour.every(5)  # change it to hourly 888888880000000000000000000
            job2.hour.also.on(11)
            cron.write()

            for jobs in cron:
                print(jobs)

        # ************************************************************************************
        all_jsons['wifi'] = [wifi, password]
        all_jsons['host_computer'] = [host_name, host_mac, host_ip]

        if master[0].lower() == 'y':
            all_jsons['master'] = '1'
        else:
            all_jsons['master'] = '0'

        if check[0].lower() == 'y':
            all_jsons['sub_host'] = jsondata
        else:
            all_jsons['sub_host'] = []

        collect_json_data = json.dumps(all_jsons)
        
        # print(collect_json_data)

        send = "https://dashboard.kratinn.com/api/data/"
        #send = "http://192.168.61.180:5001/api/data/"
        send += device_id

        try:
            r = requests.post(send, headers=headers, data=collect_json_data)
            if r.status_code == 200:
                print("Process completed successfully")
                return 1
            else:
                print("Please check internet connection or Enter correct Device ID and password")
                return 0

        except:
            print("FAILED to connect to server, Please check internet connection ")
            return 0
        # r = requests.post('http://username:userpass@127.0.0.1:8000/api/data', data=json.dumps(data))

        # ************************************************************************************
    except Exception as ex:
        print("ERROR Unable to create in job{0} ----{1}".format(type(ex).__name__, ex.args))


def format_data():
    global host_name
    global host_mac
    global check_version
    global dirname
    global names
    global macs
    global ips
    global host_ip

    # print("Formating the output")

    try:
        path = dirname + "/data/data.txt"
        path2 = dirname + "/data/output.txt"
        f = open(path, "w")
        p = subprocess.check_output(["sudo", "awk", "/server/ {print $2}", path2]).decode("utf-8")
        f.write(p)
        f.close()

        path = dirname + "/data/data2.txt"
        f = open(path, "w")
        p = subprocess.check_output(["sudo", "awk", "/server/ {print $NF}", path2]).decode("utf-8")
        f.write(p)
        f.close()

        path = dirname + "/data/data_ip.txt"  # fetching ip address using nbttool
        f = open(path, "w")
        p = subprocess.check_output(["sudo", "awk", "/server/ {print $1}", path2]).decode("utf-8")
        f.write(p)
        f.close()

        # sudo awk '/192/ {print $1,$2}' "output2.txt"
        path = dirname + "/data/data3.txt"
        path2 = dirname + "/data/output2.txt"  # fetching ip address using arp scan
        f = open(path, "w")

        ip_first_octet = ""
        for x in host_ip:
            if x == '.':
                break
            ip_first_octet += x
        find_string = "/"
        find_string += ip_first_octet
        find_string += "/ && NR>1 {print $1}"
        # p = subprocess.check_output(["sudo", "awk", "/192/ {print $1}", path2]).decode("utf-8")
        p = subprocess.check_output(["sudo", "awk", find_string, path2]).decode("utf-8")
        f.write(p)
        f.close()

        path = dirname + "/data/data4.txt"
        f = open(path, "w")
        find_string = "/"
        find_string += ip_first_octet
        find_string += "/ && NR>1 {print $2}"
        # p = subprocess.check_output(["sudo", "awk", "/192/ {print $2}", path2]).decode("utf-8")
        p = subprocess.check_output(["sudo", "awk", find_string, path2]).decode("utf-8")
        f.write(p)
        f.close()
        # **************************************************************************************************
        with open(dirname + '/data/data.txt') as f:
            names = f.readlines()
        f.close()
        names = [x.strip() for x in names]

        with open(dirname + '/data/data2.txt') as f:
            macs = f.readlines()
        f.close()
        macs = [x.strip() for x in macs]

        with open(dirname + '/data/data_ip.txt') as f:
            ips = f.readlines()
        f.close()
        ips = [x.strip() for x in ips]

        with open(dirname + '/data/data3.txt') as f:
            ips2 = f.readlines()
        f.close()
        ips2 = [x.strip() for x in ips2]

        with open(dirname + '/data/data4.txt') as f:
            macs2 = f.readlines()
        f.close()
        macs2 = [x.strip() for x in macs2]

        mac_tracker = []
        for m in macs2:
            n = macs2.index(m)
            if (m not in macs) and (n not in mac_tracker):
                mac_tracker.append(n)

        # print(len(mac_tracker))
        # print(mac_tracker)

        for x in mac_tracker:
            macs.append(macs2[x])
            ips.append(ips2[x])
            names.append("Not available")

        path1 = dirname + "/data/main_names.json"
        path2 = dirname + "/data/main_macs.json"
        path3 = dirname + "/data/main_ips.json"

        with open(path1, 'w') as f:
            json.dump(names, f)

        with open(path2, 'w') as f:
            json.dump(macs, f)

        with open(path3, 'w') as f:
            json.dump(ips, f)



    except:
        print("error in formatting")


def finder():
    if not os.geteuid() == 0:
        sys.exit("\nOnly root can run this script (Run with sudo on ubuntu)\n")

    comp_info()
    ethtool_x_cp()
    cron_jobs()
    soft_install()
    tool_run()
    format_data()

    while (send_data() != 1):
        print("")
        print("<<<<<<<<<Please try again, ( or Enter <ctrl+Z) to exit>>>>>>>>>>>>>>")
        print("")


def main():
    finder()
    # test()


if __name__ == '__main__':
    finder()
