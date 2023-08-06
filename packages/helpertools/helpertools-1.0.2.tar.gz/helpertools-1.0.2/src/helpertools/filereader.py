
import openpyxl

from openpyxl import load_workbook


def readExcel(path):
    return load_workbook(filename=path, read_only=True)


def readTxt(path):
    with open(path, 'r') as reader:
        return reader.readlines()




