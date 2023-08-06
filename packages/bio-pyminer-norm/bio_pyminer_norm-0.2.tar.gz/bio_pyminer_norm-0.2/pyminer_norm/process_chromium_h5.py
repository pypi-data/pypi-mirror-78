import argparse
import csv
from pyminer_norm.common_functions import run_cmd
from pyminer_norm.col_sums import calculate_col_sum


def parse_arguments(parser=None):
    """ Define the arguments available on the command line."""
    if not parser:

        parser = argparse.ArgumentParser()

    parser.add_argument("--input_file", "-i",
                        help="the input matrix which needs to be normalized", required=True)

    parser.add_argument("--cellranger_cmd", "-cell_ranger_cmd","-cellranger_cmd","-cellranger",
                        default="~/bin/cellranger-2.1.1/cellranger")
    args = parser.parse_args()
    return args


def prepend_string_to_file(filename, firstline):
    with open(filename, 'r+') as file_handle:
        content = file_handle.read()
        file_handle.seek(0, 0)
        file_handle.write(firstline.rstrip('\r\n') + content)


def print_head(filename):
    with open(filename, "r") as file_handle:
        file_handle.readline()
        return


def csv_to_tsv(csv_file, tsv_file):
    with open(csv_file, "r") as csv_f, open(tsv_file, "w") as tsv_f:
        csv.writer(tsv_f, delimiter='\t').writerows(csv.reader(csv_f))


def main():
    """ Run the code in this file from the command line."""
    args = parse_arguments()

    base_file_name = args.input_file[:-3]

    # convert to csv
    cmd_string = [args.cellranger_cmd,
                  "mat2csv",
                  args.input_file,
                  base_file_name + ".csv"]

    run_cmd(cmd_string)

    # add the 'gene' to the header
    prepend_string_to_file(base_file_name + ".csv", "gene")

    # print the head
    print_head(base_file_name + ".csv")

    # convert to tsv
    csv_to_tsv(base_file_name + ".csv", base_file_name + ".tsv")

    # look at the distribution of transcript counts in the cells
    calculate_col_sum(input_file=base_file_name + ".tsv")

    # look at the distribution of transcript counts in the cells
    calculate_col_sum(input_file=base_file_name + ".tsv", type_of_analysis='count')


if __name__ == "__main__":
    main()
