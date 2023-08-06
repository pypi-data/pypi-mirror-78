import os
from .ChangeLogPandas import ChangeLog
import logging
import pandas as pd

logger = logging.getLogger("pyC")


class CloneXls:
    def __init__(self, source_file, clone_file_postfix="_baangt", log_sheet_name="Change Logs"):
        """
        This class is used to make a clone of an xlsx file and than maintain a change log
        :param source_file: Path to source file
        :param clone_file_postfix: (optional) (default="_baangt") Postfix to be added in the name of clone file
        """
        self.source_file = source_file
        self.source_file_name = ".".join(source_file.split(".")[:-1])
        self.source_file_extension = source_file.split(".")[-1]
        self.clone_file = self.source_file_name + clone_file_postfix + "." + self.source_file_extension
        self.log_sheet_name = log_sheet_name
        self.check_source_file()

    def check_source_file(self):
        if not os.path.exists(self.source_file):
            logger.info(f"{self.source_file} doesn't exists, please verify the path entered!")
            raise BaseException(f"{self.source_file} doesn't exists, please verify the path entered!")

    def update_or_make_clone(self, ignore_headers=[], ignore_sheets=[],
            case_sensitive_ignore=False, clone=True):
        """
        This method is used to update the clone file with the change log and if their is no clone file then make one
        :return:
        """
        if not os.path.exists(self.clone_file):
            # Will make a clone file if it doesn't exists, the cloned file will be exact copy of source
            # without formatting
            # Change log sheets are not added here
            self.make_clone()
            logger.debug(f"Clone file created: {self.clone_file}")
        elif clone:
            logger.debug(f"Updating clone file: {self.clone_file}")
            changeLog = ChangeLog(self.source_file, self.clone_file,
                                  log_sheet_name=self.log_sheet_name, ignore_headers=ignore_headers,
                                  ignore_sheets=ignore_sheets, case_sensitive_ignore=case_sensitive_ignore)
            changeLog.xlsxChangeLog()
            logger.debug(f"Clone file updated.")
        # Returning filename with absolute path of clone file
        return self.clone_file

    def make_clone(self):
        xl = pd.ExcelFile(self.source_file)
        sheetnames = xl.sheet_names
        sheet_dic = {}
        for sheetname in sheetnames:
            df = pd.read_excel(self.source_file, sheetname, dtype=str)
            sheet_dic[sheetname] = df
        self.save_xls(sheet_dic, self.clone_file)

    def save_xls(self, sheet_dic, xls_path):
        with pd.ExcelWriter(xls_path) as writer:
            for sheetname in sheet_dic:
                sheet_dic[sheetname].to_excel(writer, sheetname, index=False)
            headers = ["Date & Time", "Sheet Name", "Header Name", "Row Number", "Old Value", "New Value"]
            df = pd.DataFrame(columns=headers)
            df.to_excel(writer, self.log_sheet_name, index=False)
            writer.save()
