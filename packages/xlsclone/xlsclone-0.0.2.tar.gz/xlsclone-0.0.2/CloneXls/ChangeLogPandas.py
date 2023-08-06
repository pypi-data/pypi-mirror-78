import pandas as pd
from datetime import datetime
import logging
import numpy as np

logger = logging.getLogger("pyC")

class ChangeLog:
    def __init__(
            self, source_file, clone_file, log_sheet_name="Change Logs", ignore_headers=[], ignore_sheets=[],
            case_sensitive_ignore=False
    ):
        """

        :param source_file: Path of excel file.
        :param clone_file: Path of clone version of source file.
        :param log_sheet_name: (optional) (default="Change Logs") Name of sheet containing change logs
        :param ignore_headers: (optional) list of headers to be ignored for change log
        :param ignore_sheets: (optional) list of sheet names to be ignored for change log
        :param case_sensitive_ignore: (default=False) If True, ignore sheets & headers list's data will be matched with same case.
        """
        self.source_file = source_file
        self.clone_file = clone_file
        self.log_sheet_name = log_sheet_name
        self.ignore_headers = ignore_headers
        self.ignore_sheets = ignore_sheets
        self.ignore_sheets.append(self.log_sheet_name)
        self.case_senstive_ignore = case_sensitive_ignore
        self.update_ignore_list()
        self.headers_column = {}

    def update_ignore_list(self):
        # Making data inside igonre lists in lower only if case_sensitive_ignore is false, so that it will be later
        # used at the time of comparision
        logger.debug("Updating ignore lists")
        if self.case_senstive_ignore:
            return None
        if self.ignore_headers:
            self.ignore_headers = [header.lower() for header in self.ignore_headers]
            logger.debug("Headers ignore list updated.")
        if self.ignore_sheets:
            self.ignore_sheets = [sheet.lower() for sheet in self.ignore_sheets]
            logger.debug("Sheets ignore list updated.")

    def xlsxChangeLog(self):
        """
        Method to trigger all functionalities including checking changes and updating clone file
        :return:
        """
        # Main method which will do all things including check and updating logs
        source = pd.ExcelFile(self.source_file)
        clone = pd.ExcelFile(self.clone_file)
        source_sheets = source.sheet_names
        clone_sheets = clone.sheet_names
        sheets = self.get_sheets(source_sheets, clone_sheets)
        logs = self.get_change_logs(source, clone, sheets)
        self.update_change_logs(logs, clone)
        self.update_clone_file(source, source_sheets)

    def get_sheets(self, source_sheets, clone_sheets):
        # method is used to get sheets which are not inside ignore list, also deals with case_sensitive functionality
        sheets = []
        for sheet in source_sheets:  # looping through sheets in source file
            if sheet in clone_sheets:  # if sheet is not already present in clone file than change log is skipped
                if self.ignore_sheets:  # if ignore_sheets doesn't have any values than sheet name is directly added in list
                    if self.case_senstive_ignore:  # if the name is case_sensitive then check for exact value
                        if sheet not in self.ignore_sheets:
                            sheets.append(sheet)
                    elif sheet.lower() not in self.ignore_sheets:  # if checking is not case sensitive than checking value
                        sheets.append(sheet)                       # in lower as ignore list is also converted to lower
                else:
                    sheets.append(sheet)
        logger.debug("Sheets Gathered after filtering ignored sheets.")
        return sheets

    def get_str_sheet(self, excel, sheet):
        columns = excel.parse(sheet).columns
        converters = {column: str for column in columns}
        data = excel.parse(sheet, converters=converters)
        return data

    def get_change_logs(self, source, clone, sheets):
        # method returns a list of change log with all data in correct column position
        logs = []
        for sheet in sheets:
            source_sht = self.get_str_sheet(source, sheet)
            clone_sht = self.get_str_sheet(clone, sheet)
            headers, new_headers, removed_headers = self.get_headers(source_sht, clone_sht, sheet)
            for header in new_headers:
                # adding new headers in change log list with appropriate values
                logs.append([
                    datetime.now().strftime("%d-%m-%Y %H:%M"),
                    sheet,
                    header,
                    1,
                    "-",
                    "(new header)"
                ])
            for header in removed_headers:
                # adding removed headers in change log list with appropriate values
                logs.append([
                    datetime.now().strftime("%d-%m-%Y %H:%M"),
                    sheet,
                    header,
                    1,
                    "(removed header)",
                    "-"
                ])
            for header in source_sht.columns.values.tolist():
                if header not in headers or header in new_headers or header in removed_headers:
                    source_sht = source_sht.drop(header, 1)
            for header in clone_sht.columns.values.tolist():
                if header not in headers or header in new_headers or header in removed_headers:
                    clone_sht = clone_sht.drop(header, 1)
            logs += self.find_changes(source_sht, clone_sht, sheet)
        logger.debug("Change logs gathered")
        return logs

    def get_headers(self, source_sht, clone_sht, sheetname):
        # return a list of headers which are to be considered for change log, along with it return 2 others list with
        # new headers and removed headers so the change log contain directly entry of changes headers instead of whole
        # columns. Logic is same like get_sheets method
        source_headers = source_sht.columns.values.tolist()
        clone_headers = clone_sht.columns.values.tolist()
        self.headers_column[sheetname] = {}
        headers = []
        temp_headers = []
        new_headers = []
        removed_headers = []
        for header in source_headers:
            if not header:
                continue
            if self.ignore_headers:
                if self.case_senstive_ignore:
                    if header not in self.ignore_headers:
                        temp_headers.append(header)
                    else:
                        self.headers_column[sheetname][source_headers.index(header)] = header
                elif header.lower() not in self.ignore_headers:
                    temp_headers.append(header)
                else:
                    self.headers_column[sheetname][source_headers.index(header)] = header
            else:
                temp_headers.append(header)

        for header in temp_headers:
            if header not in clone_headers:
                new_headers.append(header)
            headers.append(header)

        for header in clone_headers:
            if not header:
                continue
            if self.ignore_headers:
                if self.case_senstive_ignore:
                    if header not in self.ignore_headers:
                        if header not in source_headers:
                            removed_headers.append(header)
                elif header.lower() not in self.ignore_headers:
                    if header not in source_headers:
                        removed_headers.append(header)
            else:
                if header not in source_headers:
                    removed_headers.append(header)
        logger.debug(f"Headers gathered after filtering ignored headers for sheet: {sheetname}")
        return headers, new_headers, removed_headers

    def find_changes(self, source_sht, clone_sht, sheetname):
        # finding changes for a column(header) from source to clone
        changes = []
        while len(source_sht) < len(clone_sht):
            source_sht = source_sht.append(pd.Series(), ignore_index=True)
        while len(clone_sht) < len(source_sht):
            clone_sht = clone_sht.append(pd.Series(), ignore_index=True)
        source_sht.fillna("", inplace=True)
        clone_sht.fillna("", inplace=True)
        source_sht = source_sht.reindex(sorted(source_sht.columns), axis=1)
        clone_sht = clone_sht.reindex(sorted(clone_sht.columns), axis=1)
        comparison_values = source_sht.values == clone_sht.values
        rows, cols = np.where(comparison_values == False)
        for item in zip(rows, cols):
            source_value = source_sht.iloc[item[0], item[1]]
            clone_value = clone_sht.iloc[item[0], item[1]]
            if repr(source_value) == repr(clone_value):
                continue
            # if clone and source value didn't matched then creating a list with appropriate data in correct position
            changes.append([
                datetime.now().strftime("%d-%m-%Y %H:%M"),
                sheetname,
                source_sht.columns[item[1]],
                item[0] + 2,
                clone_value,
                source_value
            ])
        return changes

    def update_change_logs(self, logs, clone):
        # Updates Chane Log sheet in log file
        df = clone.parse(self.log_sheet_name)
        for log in logs:  # looping through logs list which contains a lists of log with data inside in perfect order
            df.loc[len(df), :] = log
        self.changeLogDf = df
        logger.debug("Change logs sheet updated")

    def update_clone_file(self, source, source_sheets):
        df_dic = {}
        for sheet in source_sheets:
            df = self.get_str_sheet(source, sheet)
            df_dic[sheet] = df
        df_dic[self.log_sheet_name] = self.changeLogDf
        with pd.ExcelWriter(self.clone_file) as writer:
            for sheetname in df_dic:
                df_dic[sheetname].to_excel(writer, sheetname, index=False)
            writer.save()

