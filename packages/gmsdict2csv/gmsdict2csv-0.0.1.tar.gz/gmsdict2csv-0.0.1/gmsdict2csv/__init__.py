"""
Given a dictionary, output dictionary data as a csv file.
"""
import os
import csv


def list_csv(datalist=None, path=None, file=None):
    """
    Convert a data list to a csv file

    example input lists: [
        ['datalist01', 'item11', 'item12', 'item13'],
        ['datalist02', '0', 'itemN', '20'],
        ['datalist03', 'Git', 'Repo', 'Data']
    ]

    :param datalist: the data list to output as a csv file. ['item1', 'item2', 'itemN']
    :param path: The address of the folder in which to create the output csv file
    :param file: output file name with extension
    :return: output a [{path}/{file}.csv] file
    """
    log = f"Convert((datalist), {path}, {file})"

    path = path if path is not None else '.'
    file = file if file is not None else "dict2csvOutput.csv"

    if datalist:
        # Creating a file at specified location
        outpath = f"{os.path.expanduser('~')}/{path}" if path is not None else f"{os.path.expanduser('~')}/Downloads"
        with open(os.path.join(outpath, f"{file}.csv"), 'w', newline='') as csvfile:
            csvfile.write('')
            csvwriter = csv.writer(csvfile, delimiter=' ')
            csvwriter.writerow(datalist)
    return True