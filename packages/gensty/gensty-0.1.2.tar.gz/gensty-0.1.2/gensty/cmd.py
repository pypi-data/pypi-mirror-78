#!/usr/bin/env python
import gensty
import argparse

def main():
    parser = argparse.ArgumentParser(
        prog='genSty', description="LaTeX Style file generator for fonts")
    parser.add_argument('--version', '-v', action='version',
                        version='%(prog)s ' + gensty.__version__)
    parser.add_argument('path',
                        help='Font(s) path. It can be either a directory in case of multiple fonts or file path.')
    parser.add_argument('--all', '-a', action="store_true",
                        help='If choosed %(prog)s will generate LaTeX Styles for all fonts in directory')
    parser.add_argument('--smufl', '-s', type=str,
                        help='If choosed %(prog)s will generate LaTeX Styles for all fonts in directory based on glyphnames provided.')
    parser.add_argument('--name', '-n', type=str,
                        help='In case of single font provided forces specified name. Otherwise %(prog)s detects the name from file.')
    parser.add_argument('--description', type=str,
                        help='LaTeX Style package description. It is ignored in case of --all flag.')
    parser.add_argument('--author', type=str, help='Author\'s name.')
    parser.add_argument('--ver', type=str, help='LaTeX package version.')
    args = parser.parse_args()

    if isdir(args.path) == False and isfile(args.path) == False:
        raise Exception("Error! First argument must be file or directory.")

    # Normalize and validate optional values
    optionals = gensty.validateNormalize(args)

    # Handles different cases of command.
    # In case of "all" flag we create styles for every font in folder. For both
    # "all" true/false createPackage handles the package creation and
    # createStyleFile the LaTeX style content.
    if args.all == True and isdir(args.path) == False:
        raise Exception(
            "Error! flag --all must be defined along with directory only!")

    if args.all == True and isdir(args.path) == True:
        fontfiles, result = gensty.handleFolder(args.path, optionals["author"],
                                         optionals["description"], optionals["version"],
                                         args.smufl)
    if args.all == False and isfile(args.path) == True:
        fontfiles, result = gensty.createStyleFile(args.path, optionals["author"],
                                            optionals["description"], optionals["version"],
                                            args.smufl)
    # Create LaTeX package(s).
    gensty.createPackage(fontfiles, result)
if __name__ == "__main__":
    main()
