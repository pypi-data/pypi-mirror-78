from sys import argv
from subprocess import call
from getopt import getopt, GetoptError

def version():

    print("+-----------------------------------------------------------------------------------+")
    print("| PyMac. Copyright (C) 2020 BrainDisassembly, Contact: braindisassm@gmail.com      |")
    print("| Version: 1.0.0                                                                    |")
    print("|                                                                                   |")
    print("| This program comes with ABSOLUTELY NO WARRANTY; for details type `show w`.        |")
    print("| This is free software, and you are welcome to redistribute it                     |")
    print("| under certain conditions; type `show c` for details.                              |")
    print("+-----------------------------------------------------------------------------------+")


def usage():

    print("PyMac 1.0.0 [Python MAC Adress Changer]")
    print("Written by: BrainDisassembly <braindisassm@gmail.com>\n")

    print("Usage: {0} --mac 00:11:22:33:44:55 --interface eth0".format(argv[0]))

    print("\nOptions:")
    print("  -h: --help                           Print usage and exit.")
    print("  -V: --version                        Print version information and exit.")
    print("  -m: --mac                            Change your MAC address.")
    print("  -i: --interface                      Enter your interface.")


def pymac():

    call(["ifconfig", interface, "down"])
    call(["ifconfig", interface, "hw", "ether", mac])
    call(["ifconfig", interface, "up"])


def main():

    global mac
    mac = ""

    global interface
    interface = ""

    try:
        opts, args = getopt(argv[1:], "hVm:i:", ["help", "version", "mac=", "interface="])

    except GetoptError: usage()

    else:
        try:
            for opt, arg in opts:
                if opt in ("-h", "--help"): usage(); exit(1)
                if opt in ("-V", "--version"): version(); exit(1)
                if opt in ("-m", "--mac"): mac = arg
                if opt in ("-i", "--interface"): interface = arg

            if mac and interface: pymac()

            else:
                usage()

        except (UnboundLocalError):
            pass

        except (TypeError):
            pass


if __name__ == "__main__":
        main()
