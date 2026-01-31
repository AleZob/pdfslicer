#!/usr/bin/env python3

import subprocess
import argparse
from pathlib import Path


def run_zathura(file: str):
    runned = subprocess.run(
        ["zathura", file], capture_output=True, text=True, check=True
    )
    return runned.stdout


def run_qpdf(in_file: str, pages: str, out_file: str):
    command = ["qpdf", "--empty", "--pages", in_file, pages, "--", out_file]
    print("About to execute the following comand:")
    print(*command)
    approval = input("Continue? [Y, n]").capitalize()
    if approval == "N":
        return
    else:
        pass
    subprocess.run(command, check=True)


def arg_parse():
    parser = argparse.ArgumentParser(
        prog="slicer",
        description="Runs zathura and keeps the marked pages",
        epilog="I am not sorry for writing this",
    )
    parser.add_argument("file_in")
    parser.add_argument("file_out")

    args = parser.parse_args()

    file_in = Path(args.file_in)
    file_out = Path(args.file_out)
    if file_in.exists():
        pass
    else:
        raise ValueError(f"Input file {file_in} does not exist")

    if file_out.suffix == ".pdf":
        pass
    else:
        raise ValueError(f"Output file {file_in} is not a .pdf")

    return file_in, file_out


def zathura_out_parse(stdin_zathura):
    data = stdin_zathura.strip().split("\n")
    data = [int(page) for page in data]

    proccessed_data = []
    for page in data:
        if page in proccessed_data:
            continue
        elif -page in proccessed_data:
            proccessed_data.remove(-page)
        elif page < 0:
            continue
        else:
            proccessed_data.append(page)
    proccessed_data.sort()
    out_string = ",".join([str(page) for page in proccessed_data])
    # out_string = proccessed_data.join("")
    return out_string


def main():
    file_in, file_out = arg_parse()
    zathura_out = run_zathura(file_in)
    pages_to_keep = zathura_out_parse(zathura_out)
    run_qpdf(file_in, pages_to_keep, file_out)


if __name__ == "__main__":
    main()
