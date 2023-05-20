import re
import tailer
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
    "Error while processing object"
]

time_regex = r"^\d+:\d+:\d+\.\d\d\d "
log_path = "/var/log/pleroma.log"


def print_filtered(line):
    if not any(word in line for word in word_filter) and not line.isspace():
        if len(re.findall(time_regex, line)) > 0:
            print("")

        print(line.rstrip())


if len(sys.argv) < 2:
    print("No argument provided!")
    exit(1)

if sys.argv[1] == "tail":
    for line in tailer.follow(open(log_path)):
        print_filtered(line)
else:
    log_file = open(log_path, 'r')
    lines = log_file.readlines()
    log_file.close()

    for line in lines:
        print_filtered(line)
