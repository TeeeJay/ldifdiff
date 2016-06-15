#!/usr/bin/env python2

"""
    ldiffsearch truncates and wraps lines that exceeds 78 characters from LDAP/AD, and proceeds on next line prefixed with a space " ".
    This tool fixes lines back to how they should be, without truncation for correct parsing by ldiff afterwards.
"""

import argparse

def postprocess(ldif_file):
    with open(ldif_file+".postprocessed", 'w') as output:
        write_previous = False
        previous_line = ""
        with open(ldif_file, 'r') as ldif:
            for line in ldif:
                line = line.strip("\n")

                # between each entity there is an empty line
                if (line.strip() == ""):
                    previous_line += "\n"
                    write_previous = True
                elif line.startswith(" "):
                    line = line[1:]
                    write_previous = False
                else:
                    write_previous = True

                if previous_line and write_previous:
                    output.write(previous_line + "\n")
                    previous_line = ""
                    write_previous = False

                previous_line += line

            output.write(previous_line + "\n")

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Post process LDIF-files that has been capped at 78 chars. Takes one input and creates a postprocessed file with .postprocessed file extension")
    parser.add_argument('-i', '--input-file', default=None, dest='input_file', required=True, help="Will create a new file with postfix _postprocessed")
    args = parser.parse_args()

    postprocess(args.input_file)
