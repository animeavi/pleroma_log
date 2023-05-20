import re
import time
import select
import subprocess
import sys

word_filter = [
    "ssl_handshake",
    "LRDD",
    "user is deactivated",
    "DBConnection.ConnectionError",
    "Updating metadata",
    "constraint: :unique, constraint_name",
    "Error while fetching",
    "Couldn't fetch reply@",
    "Could not decode user",
    "Error while processing object",
    "emoji pack",
    "[notice] Application",
    "JOINED chat:public",
    "Parameters: %{}",
    "Transport: :websocket",
    "ONNECTED TO Pleroma.Web.UserSocket",
    ", \"vsn\" => ",
    "Serializer: Phoenix.Socket.V2.JSONSerializer",
    "fetching rich media",
    "Internal server error",
    "<no file>"
]

time_regex = r"^\d+:\d+:\d+\.\d\d\d "
log_path = "/var/log/pleroma.log"


def print_filtered(line, tail=False):
    if not any(word in line for word in word_filter):
        if not tail:
            if not line.isspace():
                if len(re.findall(time_regex, line)) > 0:
                    print("")

                print(line.rstrip())
        else:
            print(line)


if len(sys.argv) < 2:
    print("No argument provided!")
    exit(1)

if sys.argv[1] == "tail":
    with subprocess.Popen(["tail", "-n0", "-f", log_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as pro:
        for line in pro.stdout:
            print_filtered(str(line.decode('utf-8')), True)
else:
    log_file = open(log_path, 'r')
    lines = log_file.readlines()
    log_file.close()

    for line in lines:
        print_filtered(line)
