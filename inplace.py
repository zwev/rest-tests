import glob
import argparse

# Allows user to pass arguments in when running tests from cmd.

parser = argparse.ArgumentParser(description="Replace an IP and Serial Number")

parser.add_argument("IP1", metavar="Old IP Address", type=str, help="Provide an IP Address to find in tesst files")
parser.add_argument("IP2", metavar="New IP Address", type=str, help="Provide an IP Address to insert in test files")

parser.add_argument("Serial1", metavar="Old Serial Number", type=str, help="Provide a Serial Number to find in test files")
parser.add_argument("Serial2", metavar="New Serial Number", type=str, help="Provide a Serial Number to insert in test files")


args = parser.parse_args()
for f in glob.glob("./**/*.py", recursive=True):
    with open(f, "r") as inputfile:
        newText = inputfile.read().replace(args.IP1, args.IP2).replace(args.Serial1, args.Serial2)

    with open(f, "w") as outputfile:
        outputfile.write(newText)

