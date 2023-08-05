Change log
================================================================================
0.5.9 - 29.08.2020
--------------------------------------------------------------------------------

Added


#. `pyexcel-xls#35 <https://github.com/pyexcel/pyexcel-xls/issues/35>`_, include
tests
 
0.5.8 - 22.08.2018
--------------------------------------------------------------------------------

Added


#. `pyexcel#151 <https://github.com/pyexcel/pyexcel/issues/151>`_, read cell
   error as #N/A.

0.5.7 - 15.03.2018
--------------------------------------------------------------------------------

Added


#. `pyexcel#54 <https://github.com/pyexcel/pyexcel/issues/54>`_, Book.datemode
   attribute of that workbook should be passed always.

0.5.6 - 15.03.2018
--------------------------------------------------------------------------------

Added


#. `pyexcel#120 <https://github.com/pyexcel/pyexcel/issues/120>`_, xlwt cannot
   save a book without any sheet. So, let's raise an exception in this case in
   order to warn the developers.

0.5.5 - 8.11.2017
--------------------------------------------------------------------------------

Added


#. `#25 <https://github.com/pyexcel/pyexcel-xls/issues/25>`_, detect merged cell
   in .xls

0.5.4 - 2.11.2017
--------------------------------------------------------------------------------

Added


#. `#24 <https://github.com/pyexcel/pyexcel-xls/issues/24>`_, xlsx format cannot
   use skip_hidden_row_and_column. please use pyexcel-xlsx instead.

0.5.3 - 2.11.2017
--------------------------------------------------------------------------------

Added


#. `#21 <https://github.com/pyexcel/pyexcel-xls/issues/21>`_, skip hidden rows
   and columns under 'skip_hidden_row_and_column' flag.

0.5.2 - 23.10.2017
--------------------------------------------------------------------------------

updated

#. pyexcel `pyexcel#105 <https://github.com/pyexcel/pyexcel/issues/105>`_,
   remove gease from setup_requires, introduced by 0.5.1.
#. remove python2.6 test support
#. update its dependecy on pyexcel-io to 0.5.3

0.5.1 - 20.10.2017
--------------------------------------------------------------------------------

added

#. `pyexcel#103 <https://github.com/pyexcel/pyexcel/issues/103>`_, include
   LICENSE file in MANIFEST.in, meaning LICENSE file will appear in the released
   tar ball.

0.5.0 - 30.08.2017
--------------------------------------------------------------------------------

Updated

#. `#20 <https://github.com/pyexcel/pyexcel-xls/issues/20>`_, is handled in
   pyexcel-io
#. put dependency on pyexcel-io 0.5.0, which uses cStringIO instead of StringIO.
   Hence, there will be performance boost in handling files in memory.

0.4.1 - 25.08.2017
--------------------------------------------------------------------------------

Updated

#. `#20 <https://github.com/pyexcel/pyexcel-xls/issues/20>`_, handle unseekable
   stream given by http response.

0.4.0 - 19.06.2017
--------------------------------------------------------------------------------

Updated

#. `pyexcel-xlsx#15 <https://github.com/pyexcel/pyexcel-xlsx/issues/15>`_, close
   file handle
#. pyexcel-io plugin interface now updated to use `lml
   <https://github.com/chfw/lml>`_.

0.3.3 - 30/05/2017
--------------------------------------------------------------------------------

Updated

#. `#18 <https://github.com/pyexcel/pyexcel-xls/issues/18>`_, pass on
   encoding_override and others to xlrd.

0.3.2 - 18.05.2017
--------------------------------------------------------------------------------

Updated

#. `#16 <https://github.com/pyexcel/pyexcel-xls/issues/16>`_, allow mmap to be
   passed as file content

0.3.1 - 16.01.2017
--------------------------------------------------------------------------------

Updated

#. `#14 <https://github.com/pyexcel/pyexcel-xls/issues/14>`_, Python 3.6 -
   cannot use LOCALE flag with a str pattern
#. fix its dependency on pyexcel-io 0.3.0

0.3.0 - 22.12.2016
--------------------------------------------------------------------------------

Updated

#. `#13 <https://github.com/pyexcel/pyexcel-xls/issues/13>`_, alert on empyty
   file content
#. Support pyexcel-io v0.3.0

0.2.3 - 20.09.2016
--------------------------------------------------------------------------------

Updated

#. `#10 <https://github.com/pyexcel/pyexcel-xls/issues/10>`_, To support
   generator as member of the incoming two dimensional data

