#!/usr/bin/env python3

# Parse a Log file for interesting tokens 
#
# Supported Search Tokens:
#   token,token2|token3=NUM or -NUM
#   where token: "string (eg. state or m1234)" or "expression (eg. m\d{4})" 
# Support Output Formats:
#   JSON, Pretty Print, Table, None, Tokens
#
# Author: Jagmeet Singh Hanspal

import argparse
import re
import json
import pprint

def parse_tokens(filename, tokens):

    #print(f"Parsing Tokens: {tokens} from File: {filename}")

    # Data store
    data = {}

    # Date/Time expression
    # YYYY-MM-DDTHH:MM:SS.MS
    exp_date = re.compile("(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2}.\d+)")

    # Token Expression 
    # token|x|y,z=NUM OR -NUM
    # where token= "string" or "m\d{4}" expression
    exp_token = re.compile(f"({tokens})=" + "(-{0,1}\d+)")        

    log = open(filename, "r")
    for line in log:

        source = line

        d = exp_date.search(source) 
        s = exp_token.search(source)  

        while d and s:
            key = s.group(1)
            value = s.group(2)

            year = d.group(1)
            month = d.group(2)
            day = d.group(3)

            hour = d.group(4)
            minute = d.group(5)
            second = d.group(6)
            #print(f"{minute}:{second} {key}: {value}")

            if not key in data:
                data[key] = []

            data[key].append({
                "date": f"{year}/{month}/{day}",
                "time": f"{hour}:{minute}:{second}",
                "value": f"{value}"
            })

            # Check for any more matches 
            end = s.end(2)
            source = source[end:]
            s = exp_token.search(source)  
 
    log.close()
    return data

def display(data, format):
    if format == "json":
        json_data = json.dumps(data)
        print(json_data)
    elif format == "table":
        for key in data:
            header = " Token: " + key + " "
            print(f"\n{header:_^45}")
            i = 0
            colHeader = 1
            while i < len(data[key]):
                if colHeader:
                    colHeader = 0
                    for d in data[key][i]:
                        print(f"{d:20}", end=" ")
                    print("")

                for d in data[key][i]:
                    print(f"{data[key][i][d]:20}", end=" ")
                print("")
                i = i + 1
    elif format == "pretty":
        pprint.pprint(data)
    elif format == "none":
        return
    elif format == "tokens":
        for key in data:
            print(key, end=" ")
    else:
        print(f"Unsupported Format: {format}")

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--filename", help = "Path of the Log File", required=True)
    parser.add_argument("-t", "--tokens", help = "List of search token(s) or expression(s)")
    parser.add_argument("-o", "--output", help = "json OR table (default) OR pretty OR none OR tokens", default="table")

    args = parser.parse_args()

    if args.filename:
        filename = args.filename
    else:
        print("Missing name of Logfile")
        exit()

    if args.tokens:
        tokens = args.tokens.split(",")
        tokens = '|'.join(tokens)
        data = parse_tokens(filename, tokens)
    else:
        print("Missing some search Tokens")
        exit() 

    display(data, args.output)

main()
