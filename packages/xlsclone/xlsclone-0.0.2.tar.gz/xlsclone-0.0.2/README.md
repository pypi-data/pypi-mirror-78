# baangt-CloneXLS

This package was mainly made to use in [baangt](https://www.baangt.org/). 

It's functionality is to Clone a ``excel file(xls/xlsx)`` and a new sheet is made inside cloned file which is used to 
store the change logs. 

This package contains two main classes. First is ``CloneXls`` & second is ``ChangeLog``.

CloneXls
========
``update_or_make_clone`` is the main method of this class. On the first run it will create a clone file and if the file 
already exist it will call ``ChangeLog`` class.

ChangeLog
=========
This class is used to check the changes between source and cloned file and update those changes inside cloned file.
Their are few helpful functionalities like ignore_headers & ignore_sheets these both parameters takes a list.
Headers and sheets present in this lists will be ignored for change log and will not be updated from source.
``xlsxChangeLog`` is the main method of this class which will trigger all the other methods like checking for changes,
updating change log sheet, updating whole clone file from source(except ignored data). AIt will write all the 
changes in ``Change Logs`` worksheet. This data will contain 
``Date & time, "Sheet Name", "Header Name", "Row Number", "Old Value", "New Value"``.