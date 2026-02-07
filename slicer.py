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
    parser.add_argument("file_in", type=Path)
    parser.add_argument("file_out", type=Path)

    args = parser.parse_args()

    file_in = args.file_in
    file_out = args.file_out
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
    if stdin_zathura == "":
        print("No input, abort")
        exit()
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
    proccessed_data = compress_pages(proccessed_data)
    out_string = ",".join(proccessed_data)
    # out_string = proccessed_data.join("")
    return out_string


# 1,2,3,5,6,10 -> "1-3","5-6","10"
def compress_pages(pages: list[int]) -> list[str]:
    if pages == []:
        return pages
    elif len(pages) == 1:
        return [str(pages[0])]
    else:
        start = pages[0]
        end = pages[0]
        res = []
        for i in range(1, len(pages)):
            if pages[i - 1] + 1 == pages[i]:
                end = pages[i]
            else:
                if start == end:
                    res.append(str(start))
                else:
                    res.append(str(start) + "-" + str(end))
                start = end = pages[i]

        if start == end:
            res.append(str(start))
        else:
            res.append(str(start) + "-" + str(end))

        return res


def main():
    file_in, file_out = arg_parse()
    zathura_out = run_zathura(file_in)
    pages_to_keep = zathura_out_parse(zathura_out)
    run_qpdf(file_in, pages_to_keep, file_out)


if __name__ == "__main__":
    main()
