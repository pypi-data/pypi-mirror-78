#! python3
import openpyxl
import os

from Vys.app.core.excel_core import ExcelCore


class Excel(ExcelCore):
    def __init__(self):
        super().__init__()
