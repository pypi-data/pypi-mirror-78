from sys import argv
from time import strftime
from getopt import getopt, GetoptError
from urllib.request import Request, urlopen
from codecs import getreader
from json import load

try:
    from scapy.all import Ether, ARP, srp1

except (ImportError) as e:
    print(e)
    
    exit(1)


def version():

    print("+-----------------------------------------------------------------------------------+")
    print("| Pylocalnet. Copyright (C) 2020 BrainDisassembly, Contact: braindisassm@gmail.com    |")
    print("| Version: 1.0.0                                                                    |")
    print("|                                                                                   |")
    print("| This program comes with ABSOLUTELY NO WARRANTY; for details type `show w`.        |")
    print("| This is free software, and you are welcome to redistribute it                     |")
    print("| under certain conditions; type `show c` for details.                              |")
    print("+-----------------------------------------------------------------------------------+")


def usage():

    print("Pylocalnet 1.0.0 [ARP reconnaissance tool POC]")
    print("Written by: BrainDisassembly <braindisassm@gmail.com>\n")

    print("Usage: {0} --ip 192.168.1. --rng 255 --device eth0".format(argv[0]))

    print("\nOptions:")
    print("  -h: --help                           Print usage and exit.")
    print("  -V: --version                        Print version information and exit.")
    print("  -i: --ip                             Enter an IP.")
    print("  -r: --rng                            Scan a given range.")
    print("  -d: --device                         Your network device.")
    print("  -w: --write                          Write results to a file.")


def pylocalnet():

    print("--------------------------------------------------------------------------------")
    print("-- Starting at: ({0})".format(strftime("%c")))
    print("--------------------------------------------------------------------------------")
    print("-- Currently scanning: {0}   |   Screen View: Unique Hosts".format(ip + "/" + str(rng)))

    count_hosts = []
    count_responses = []

    count_total_size = 0

    for num in range(0, rng):
        i = ip + (str(num))

        arpRequest = Ether(dst="ff:ff:ff:ff:ff:ff:ff")/ARP(pdst=i, hwdst="ff:ff:ff:ff:ff:ff")

        try:
            arpResponse = srp1(arpRequest, timeout=0.1, verbose=0, iface=device)

        except (OSError) as e:
            print(e)

        finally:
            if arpResponse:

                url = "http://macvendors.co/api/"

                request = Request(url+arpResponse.hwsrc, headers={"User-Agent": "API Browser"})
                response = urlopen(request)

                reader = getreader("utf-8")
                obj = load(reader(response))

                count_hosts.append(len(i))
                count_responses.append(len(arpResponse))
                count_total_size += len(arpResponse)

                print("--------------------------------------------------------------------------------")
                print("-- IP: ({0})".format(arpResponse.psrc))
                print("-- At MAC Address: ({0})".format(arpResponse.hwsrc))
                print("-- Count: (1)")
                print("-- Len: ({0})".format(len(arpResponse)))
                print("-- Company: ({0})".format(obj["result"]["company"]))
                print("-- Address: ({0})".format(obj["result"]["address"]))
                print("--------------------------------------------------------------------------------")

                if write:
                    with open(write, "a") as file:
                        file.write("--------------------------------------------------------------------------------")
                        file.write("\n-- IP: ({0})".format(arpResponse.psrc))
                        file.write("\n-- At MAC Address: ({0})".format(arpResponse.hwsrc))
                        file.write("\n-- Count: (1)")
                        file.write("\n-- Len: ({0})".format(len(arpResponse)))
                        file.write("\n-- Company: ({0})".format(obj["result"]["company"]))
                        file.write("\n-- Address: ({0})".format(obj["result"]["address"]))
                        file.write("\n--------------------------------------------------------------------------------\n")

    print("--------------------------------------------------------------------------------")
    print("-- ({0}) Captured ARP Req/Rep packets, from ({1}) hosts.   Total size: ({2})".format(len(count_responses), len(count_hosts), count_total_size))
    print("-- Finished at: ({0})".format(strftime("%c")))
    print("--------------------------------------------------------------------------------")


def main():

    global ip
    ip = ""

    global rng
    rng = ""

    global device
    device = ""

    global write
    write = ""

    try:
        opts, args = getopt(argv[1:], "hVi:r:d:w:", ["help", "version", "ip=", "rng=", "device=", "write="])

    except GetoptError: usage()

    else:
        try:
            for opt, arg in opts:
                if opt in ("-h", "--help"): usage(); exit(1)
                if opt in ("-V", "--version"): version(); exit(1)
                if opt in ("-i", "--ip"): ip = arg
                if opt in ("-r", "--rng"): rng = int(arg)
                if opt in ("-d", "--device"): device = arg
                if opt in ("-w", "--write"): write = arg

            if ip and rng and device: pylocalnet()

            else:
                usage()

        except (UnboundLocalError):
            pass

        except (TypeError):
            pass

if __name__ == "__main__":
        main()
