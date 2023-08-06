""" A module for saving and retrieving data. """

import os
import pathlib
import pickle
import subprocess
import zipfile

import numpy as np
import pandas as pd
import rapidjson

from pyhelpers.ops import confirmed


def get_specific_filepath_info(path_to_file, verbose=False, vb_end=" ... ", ret_info=False):
    """
    Get information about the path of a file.

    :param path_to_file: path where a file is saved
    :type path_to_file: str
    :param verbose: whether to print relevant information in console as the function runs, defaults to ``False``
    :type verbose: bool, int
    :param vb_end: a string passed to ``end`` for ``print``, defaults to ``" ... "``
    :type vb_end: str
    :param ret_info: whether to return the file path information, defaults to ``False``
    :type ret_info: bool
    :return: a relative path and a filename
    :rtype: tuple

    **Examples**::

        from pyhelpers.store import get_specific_filepath_info

        verbose = True
        vb_end = " ... "
        ret_info = False

        from pyhelpers.dir import cd

        path_to_file = cd()
        try:
            get_specific_filepath_info(path_to_file, verbose, vb_end, ret_info)
        except AssertionError as e:
            print(e)
        # `path_to_file` may not be a file path.

        path_to_file = cd(cd("test_store.py"))
        get_specific_filepath_info(path_to_file, verbose, vb_end, ret_info)
        print("Pass.")
        # Saving "test_store.py" to "<cwd>" ... Pass.

        path_to_file = cd("tests", "test_store.py")
        get_specific_filepath_info(path_to_file, verbose, vb_end, ret_info)
        print("Pass.")
        # Updating "test_store.py" at "..\\tests" ... Pass.
    """

    abs_path_to_file = pathlib.Path(path_to_file).absolute()
    assert not abs_path_to_file.is_dir(), "`path_to_file` may not be a file path."

    filename = pathlib.Path(abs_path_to_file).name if abs_path_to_file.suffix else ""
    try:
        rel_path = abs_path_to_file.parent.relative_to(abs_path_to_file.cwd())

        if rel_path == rel_path.parent:
            rel_path = abs_path_to_file.parent
            msg_fmt = "{} \"{}\" {} \"{}\""

        else:
            msg_fmt = "{} \"{}\" {} \"..\\{}\""
            # The specified path exists?
            os.makedirs(abs_path_to_file.parent, exist_ok=True)

    except ValueError:
        if verbose == 2:
            print("Warning: \"{}\" is outside the current working directory".format(str(abs_path_to_file.parent)))

        rel_path = abs_path_to_file.parent
        msg_fmt = "{} \"{}\" {} \"{}\""

    if verbose:
        status, prep = ("Updating", "at") if os.path.isfile(abs_path_to_file) else ("Saving", "to")
        print(msg_fmt.format(status, filename, prep, rel_path), end=vb_end if vb_end else "\n")

    if ret_info:
        return rel_path, filename


def save_pickle(pickle_data, path_to_pickle, mode='wb', verbose=False, **kwargs):
    """
    Save data as a pickle file.

    :param pickle_data: data that could be dumped by `pickle`_
    :type pickle_data: any
    :param path_to_pickle: path where a pickle file is saved
    :type path_to_pickle: str
    :param mode: mode to `open`_ file, defaults to ``'wb'``
    :type mode: str
    :param verbose: whether to print relevant information in console as the function runs, defaults to ``False``
    :type verbose: bool, int
    :param kwargs: optional parameters of `open`_

    .. _`pickle`: https://docs.python.org/3/library/pickle.html
    .. _`open`: https://docs.python.org/3/library/functions.html#open

    **Example**::

        from pyhelpers.store import save_pickle

        from pyhelpers.dir import cd

        pickle_data = 1
        path_to_pickle = cd("tests\\data", "dat.pickle")
        mode = 'wb'
        verbose = True

        save_pickle(pickle_data, path_to_pickle, mode, verbose)
        # Saving "dat.pickle" to "..\\tests\\data" ... Done.
    """

    get_specific_filepath_info(path_to_pickle, verbose=verbose, ret_info=False)

    try:
        pickle_out = open(path_to_pickle, mode=mode, **kwargs)
        pickle.dump(pickle_data, pickle_out)
        pickle_out.close()
        print("Done.") if verbose else ""

    except Exception as e:
        print("Failed. {}.".format(e))


def load_pickle(path_to_pickle, mode='rb', verbose=False, **kwargs):
    """
    Load data from a pickle file.

    :param path_to_pickle: path where a pickle file is saved
    :type path_to_pickle: str
    :param mode: mode to `open`_ file, defaults to ``'rb'``
    :type mode: str
    :param verbose: whether to print relevant information in console as the function runs, defaults to ``False``
    :type verbose: bool, int
    :param kwargs: optional parameters of `open`_
    :return: data retrieved from the specified path ``path_to_pickle``
    :rtype: any

    .. _`open`: https://docs.python.org/3/library/functions.html#open

    Example::

        from pyhelpers.store import load_pickle

        from pyhelpers.dir import cd

        path_to_pickle = cd("tests\\data", "dat.pickle")
        mode = 'rb'
        verbose = True

        pickle_data = load_pickle(path_to_pickle, mode, verbose)
        # Loading "..\\tests\\data\\dat.pickle" ... Done.
        print(pickle_data)
        # 1
    """

    print("Loading \"..\\{}\"".format(os.path.relpath(path_to_pickle)), end=" ... ") if verbose else ""

    try:
        pickle_in = open(path_to_pickle, mode=mode, **kwargs)
        pickle_data = pickle.load(pickle_in)
        pickle_in.close()
        print("Done.") if verbose else ""
        return pickle_data

    except Exception as e:
        print("Failed. {}".format(e)) if verbose else ""


def save_json(json_data, path_to_json, mode='w', verbose=False, **kwargs):
    """
    Save data as a json file

    :param json_data: data that could be dumped by `python-rapidjson`_
    :type json_data: any json data
    :param path_to_json: path where a json file is saved
    :type path_to_json: str
    :param mode: mode to `open`_ file, defaults to ``'w'``
    :type mode: str
    :param verbose: whether to print relevant information in console as the function runs, defaults to ``False``
    :type verbose: bool, int
    :param kwargs: optional parameters of `open`_

    .. _`python-rapidjson`: https://pypi.org/project/python-rapidjson
    .. _`open`: https://docs.python.org/3/library/functions.html#open

    **Example**::

        from pyhelpers.store import save_json

        from pyhelpers.dir import cd

        json_data = {'a': 1, 'b': 2, 'c': 3}
        path_to_json = cd("tests\\data", "dat.json")
        mode = 'w'
        verbose = True

        save_json(json_data, path_to_json, mode, verbose)
        # Saving "dat.json" to "..\\tests\\data" ... Done.
    """

    get_specific_filepath_info(path_to_json, verbose=verbose, ret_info=False)

    try:
        json_out = open(path_to_json, mode=mode, **kwargs)
        rapidjson.dump(json_data, json_out)
        json_out.close()
        print("Done.") if verbose else ""

    except Exception as e:
        print("Failed. {}.".format(e))


def load_json(path_to_json, mode='r', verbose=False, **kwargs):
    """
    Load data from a json file.

    :param path_to_json: path where a json file is saved
    :type path_to_json: str
    :param mode: mode to `open`_ file, defaults to ``'r'``
    :type mode: str
    :param verbose: whether to print relevant information in console as the function runs, defaults to ``False``
    :type verbose: bool, int
    :param kwargs: optional parameters of `open`_
    :return: data retrieved from the specified path ``path_to_json``
    :rtype: dict

    .. _`open`: https://docs.python.org/3/library/functions.html#open

    **Example**::

        from pyhelpers.store import load_json

        from pyhelpers.dir import cd

        path_to_json = cd("tests\\data", "dat.json")
        mode = 'r'
        verbose = True

        json_data = load_json(path_to_json, mode, verbose)
        # Loading "..\\tests\\data\\dat.json" ... Done.
        print(json_data)
        # {'a': 1, 'b': 2, 'c': 3}
    """

    print("Loading \"..\\{}\"".format(os.path.relpath(path_to_json)), end=" ... ") if verbose else ""

    try:
        json_in = open(path_to_json, mode=mode, **kwargs)
        json_data = rapidjson.load(json_in)
        json_in.close()
        print("Done.") if verbose else ""
        return json_data

    except Exception as e:
        print("Failed. {}".format(e)) if verbose else ""


def save_feather(feather_data, path_to_feather, verbose=False):
    """
    Save data frame as a feather file.

    :param feather_data: a data frame to be saved as a feather-formatted file
    :type feather_data: pandas.DataFrame
    :param path_to_feather: path where a feather file is saved
    :type path_to_feather: str
    :param verbose: whether to print relevant information in console as the function runs, defaults to ``False``
    :type verbose: bool, int

    **Example**::

        from pyhelpers.store import save_feather

        from pyhelpers.dir import cd

        feather_data = pd.DataFrame({'Col1': 1, 'Col2': 2}, index=[0])
        path_to_feather = cd("tests\\data", "dat.feather")
        verbose = True

        save_feather(feather_data, path_to_feather, verbose)
        # Saving "dat.feather" to "..\\tests\\data" ... Done.
    """

    assert isinstance(feather_data, pd.DataFrame)

    get_specific_filepath_info(path_to_feather, verbose=verbose, ret_info=False)

    try:
        feather_data.to_feather(path_to_feather)
        print("Done.") if verbose else ""

    except Exception as e:
        print("Failed. {}.".format(e)) if verbose else ""


def load_feather(path_to_feather, verbose=False, **kwargs):
    """
    Load data frame from a feather file

    :param path_to_feather: path where a feather file is saved
    :type path_to_feather: str
    :param verbose: whether to print relevant information in console as the function runs, defaults to ``False``
    :type verbose: bool, int
    :param kwargs: optional parameters of `pandas.read_feather`_

        * columns: (sequence, None) a sequence of column names, if ``None``, all columns
        * use_threads: (bool) whether to parallelize reading using multiple threads, defaults to ``True``

    :return: data retrieved from the specified path ``path_to_feather``
    :rtype: pandas.DataFrame

    .. _`pandas.read_feather`: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_feather.html

    **Example**::

        from pyhelpers.store import load_feather

        from pyhelpers.dir import cd

        feather_data = load_feather(path_to_feather, verbose)
        # Loading "..\\tests\\data\\dat.feather" ... Done.
        print(feather_data)
        #    Col1  Col2
        # 0     1     2
    """

    print("Loading \"..\\{}\"".format(os.path.relpath(path_to_feather)), end=" ... ") if verbose else ""

    try:
        feather_data = pd.read_feather(path_to_feather, **kwargs)
        print("Done.") if verbose else ""
        return feather_data

    except Exception as e:
        print("Failed. {}".format(e)) if verbose else ""


def save_spreadsheet(spreadsheet_data, path_to_spreadsheet, index=False, delimiter=',', verbose=False, **kwargs):
    """
    Save spreadsheet as a CSV or an MS Excel file.

    The file extension can include `".txt"`, `".csv"`, `".xlsx"` or `".xls"`.

    Engines can include: `xlsxwriter`_ for `".xlsx"`; `openpyxl`_ for `".xlsx"` / `".xlsm"`; `xlwt`_ for `".xls"`

    .. _`xlsxwriter`: https://xlsxwriter.readthedocs.io/
    .. _`openpyxl`: https://openpyxl.readthedocs.io/en/stable/
    .. _`xlwt`: https://pypi.org/project/xlwt/

    :param spreadsheet_data: data that could be saved as a spreadsheet, e.g. .xlsx, .csv
    :type spreadsheet_data: pandas.DataFrame
    :param path_to_spreadsheet: path where a spreadsheet is saved
    :type path_to_spreadsheet: str
    :param index: whether to include the index as a column, defaults to ``False``
    :type index: bool
    :param delimiter: separator for saving a `".xlsx"` (or `".xls"`) file as a `".csv"` file, defaults to ``','``
    :type delimiter: str
    :param verbose: whether to print relevant information in console as the function runs, defaults to ``False``
    :type verbose: bool, int
    :param kwargs: optional parameters of `pandas.DataFrame.to_excel`_ or `pandas.DataFrame.to_csv`_

    .. _`pandas.DataFrame.to_excel`:
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_excel.html
    .. _`pandas.DataFrame.to_csv`:
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html

    **Examples**::

        from pyhelpers.dir import cd
        from pyhelpers.store import save_spreadsheet

        import pandas as pd
        from pyhelpers.dir import cd

        spreadsheet_data = pd.DataFrame({'Col1': 1, 'Col2': 2}, index=['data'])
        index = False
        delimiter = ','
        verbose = True

        path_to_spreadsheet = cd("tests\\data", "dat.csv")
        # path_to_spreadsheet = cd("tests\\data", "dat.txt")
        save_spreadsheet(spreadsheet_data, path_to_spreadsheet, index, delimiter, verbose)
        # Saving "dat.csv" to "..\\tests\\data" ... Done.

        path_to_spreadsheet = cd("tests\\data", "dat.xls")
        save_spreadsheet(spreadsheet_data, path_to_spreadsheet, index, delimiter, verbose)
        # Saving "dat.xls" to "..\\tests\\data" ... Done.

        path_to_spreadsheet = cd("tests\\data", "dat.xlsx")
        save_spreadsheet(spreadsheet_data, path_to_spreadsheet, index, delimiter, verbose)
        # Saving "dat.xlsx" to "..\\tests\\data" ... Done.
    """

    _, spreadsheet_filename = get_specific_filepath_info(path_to_spreadsheet, verbose=verbose, ret_info=True)

    try:  # to save the data
        if spreadsheet_filename.endswith(".xlsx"):  # a .xlsx file
            spreadsheet_data.to_excel(path_to_spreadsheet, index=index, engine='openpyxl', **kwargs)

        elif spreadsheet_filename.endswith(".xls"):  # a .xls file
            spreadsheet_data.to_excel(path_to_spreadsheet, index=index, engine='xlwt', **kwargs)

        elif spreadsheet_filename.endswith((".csv", ".txt")):  # a .csv file
            spreadsheet_data.to_csv(path_to_spreadsheet, index=index, sep=delimiter, **kwargs)

        else:
            raise AssertionError('File extension must be ".txt", ".csv", ".xlsx" or ".xls"')

        print("Done.") if verbose else ""

    except Exception as e:
        print("Failed. {}.".format(e.args[0])) if verbose else ""


def save_multiple_spreadsheets(spreadsheets_data, sheet_names, path_to_spreadsheet, mode='w', index=False,
                               confirmation_required=True, verbose=False, **kwargs):
    """
    Save multiple spreadsheets to an MS Excel workbook.

    :param spreadsheets_data: a sequence of pandas.DataFrame
    :type spreadsheets_data: iterable
    :param sheet_names: all sheet names of an Excel workbook
    :type sheet_names: iterable
    :param path_to_spreadsheet: path where a spreadsheet is saved
    :type path_to_spreadsheet: str
    :param mode: mode to write to excel file, incl. ``'w'`` (default) for 'write' and ``'a'`` for 'append'
    :type mode: str
    :param index: whether to include the index as a column, defaults to ``False``
    :type index: bool
    :param confirmation_required: whether to prompt a message for confirmation to proceed, defaults to ``True``
    :type confirmation_required: bool
    :param verbose: whether to print relevant information in console as the function runs, defaults to ``False``
    :type verbose: bool, int
    :param kwargs: optional parameters of `pandas.ExcelWriter`_

    .. _`pandas.ExcelWriter`: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.ExcelWriter.html

    **Examples**::

        from pyhelpers.store import save_multiple_spreadsheets

        import numpy as np
        import pandas as pd
        from pyhelpers.dir import cd

        xy_array = np.array([(530034, 180381),   # London
                             (406689, 286822),   # Birmingham
                             (383819, 398052),   # Manchester
                             (582044, 152953)])  # Leeds

        dat1 = pd.DataFrame(xy_array,
                            index=['London', 'Birmingham', 'Manchester', 'Leeds'],
                            columns=['Easting', 'Northing'])

        dat2 = dat1.T

        spreadsheets_data = [dat1, dat2]
        sheet_names = ['TestSheet1', 'TestSheet2']
        path_to_spreadsheet = cd("tests\\data", "dat.xlsx")
        index = True
        verbose = True

        mode = 'w'
        save_multiple_spreadsheets(spreadsheets_data, sheet_names, path_to_spreadsheet, mode, index, verbose=verbose)
        # Updating "dat.xlsx" at "..\\tests\\data" ...
        #   'TestSheet1' ... Done.
        #   'TestSheet2' ... Done.

        mode = 'a'
        save_multiple_spreadsheets(spreadsheets_data, sheet_names, path_to_spreadsheet, mode, index, verbose=verbose)
        # Updating "dat.xlsx" at "..\\tests\\data" ...
        #   'TestSheet1' ... 'TestSheet1' already exists; adding a suffix to the sheet name? [No]|Yes: yes
        # TestSheet11 ... Done.
        #   'TestSheet2' ... 'TestSheet2' already exists; adding a suffix to the sheet name? [No]|Yes: yes
        # TestSheet21 ... Done.

        mode = 'a'
        confirmation_required = False
        save_multiple_spreadsheets(spreadsheets_data, sheet_names, path_to_spreadsheet, mode, index,
                                   confirmation_required, verbose)
        # Updating "dat.xlsx" at "..\\tests\\data" ...
        #   'TestSheet1' ... TestSheet12 ... Done.
        #   'TestSheet2' ... TestSheet22 ... Done.
    """

    assert path_to_spreadsheet.endswith(".xlsx") or path_to_spreadsheet.endswith(".xls")

    get_specific_filepath_info(path_to_spreadsheet, verbose=verbose, ret_info=False)

    if os.path.isfile(path_to_spreadsheet) and mode == 'a':
        excel_file_reader = pd.ExcelFile(path_to_spreadsheet)
        cur_sheet_names = excel_file_reader.sheet_names

    else:
        cur_sheet_names = []
        mode = 'w'

    excel_file_writer = pd.ExcelWriter(path_to_spreadsheet, engine='openpyxl', mode=mode, **kwargs)

    def write_excel(dat, name, idx, suffix_msg=None):
        try:
            dat.to_excel(excel_file_writer, sheet_name=name, index=idx, verbose=verbose)

            sheet_name_ = excel_file_writer.sheets[name].title
            msg_ = "{} ... Done. ".format(sheet_name_) if sheet_name_ not in sheet_names else "Done. "
            if suffix_msg:
                print("{} {}".format(msg_, suffix_msg)) if verbose == 2 else (print(msg_) if verbose else "")
            else:
                print(msg_) if verbose else ""

        except Exception as e:
            print("Failed. {}.".format(e)) if verbose else ""

    print("") if verbose else ""
    for sheet_dat, sheet_name in zip(spreadsheets_data, sheet_names):

        print("  '{}'".format(sheet_name), end=" ... ") if verbose else ""

        if sheet_name in cur_sheet_names:
            if confirmed("'{}' already exists; adding a suffix to the sheet name?".format(sheet_name),
                         confirmation_required=confirmation_required):
                write_excel(sheet_dat, sheet_name, index,
                            suffix_msg="(Note: A suffix has been added to the sheet name.)")

        else:
            write_excel(sheet_dat, sheet_name, index)

    excel_file_writer.close()


def load_multiple_spreadsheets(path_to_spreadsheet, as_dict=True, verbose=False, **kwargs):
    """
    Load multiple spreadsheets from an MS Excel workbook.

    :param path_to_spreadsheet: path where a spreadsheet is saved
    :type path_to_spreadsheet: str
    :param as_dict: whether to return the retrieved data as a dictionary type, defaults to ``True``
    :type as_dict: bool
    :param verbose: whether to print relevant information in console as the function runs, defaults to ``False``
    :type verbose: bool, int
    :param kwargs: optional parameters of `pandas.ExcelFile.parse`_
    :return: all worksheet in an Excel workbook from the specified file path ``path_to_spreadsheet``
    :rtype: list, dict

    .. _`pandas.ExcelFile.parse`: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.ExcelFile.parse.html

    **Examples**::

        from pyhelpers.store import load_multiple_spreadsheets

        from pyhelpers.dir import cd

        path_to_spreadsheet = cd("tests\\data", "dat.xlsx")
        verbose = True

        as_dict = True
        workbook_data = load_multiple_spreadsheets(path_to_spreadsheet, as_dict, verbose, index_col=0)
        # Loading "..\\tests\\data\\dat.xlsx" ...
        #   'TestSheet1'. ... Done.
        #   'TestSheet2'. ... Done.
        #   'TestSheet11'. ... Done.
        #   'TestSheet21'. ... Done.
        #   'TestSheet12'. ... Done.
        #   'TestSheet22'. ... Done.
        print(workbook_data.keys())
        # dict_keys(['TestSheet1', 'TestSheet2', 'TestSheet11', 'TestSheet21', 'TestSheet12', 'TestSheet22'])

        as_dict = False
        workbook_data = load_multiple_spreadsheets(path_to_spreadsheet, as_dict, verbose, index_col=0)
        # Loading "..\\tests\\data\\dat.xlsx" ...
        #   'TestSheet1'. ... Done.
        #   'TestSheet2'. ... Done.
        #   'TestSheet11'. ... Done.
        #   'TestSheet21'. ... Done.
        #   'TestSheet12'. ... Done.
        #   'TestSheet22'. ... Done.
        print(len(workbook_data))
        # 6
    """

    excel_file_reader = pd.ExcelFile(path_to_spreadsheet)

    sheet_names = excel_file_reader.sheet_names
    workbook_dat = []

    print("Loading \"..\\{}\" ... ".format(os.path.relpath(path_to_spreadsheet))) if verbose else ""

    for sheet_name in sheet_names:
        print("  '{}'.".format(sheet_name), end=" ... ") if verbose else ""

        try:
            sheet_dat = excel_file_reader.parse(sheet_name, **kwargs)
            print("Done.") if verbose else ""

        except Exception as e:
            sheet_dat = None
            print("Failed. {}.".format(e)) if verbose else ""

        workbook_dat.append(sheet_dat)

    excel_file_reader.close()

    if as_dict:
        workbook_data = dict(zip(sheet_names, workbook_dat))
    else:
        workbook_data = workbook_dat

    return workbook_data


def save(data, path_to_file, warning=False, **kwargs):
    """
    Save data to the specified file path.

    :param data: data that could be saved as CSV, MS Excel workbook, .feather, .json, or .pickle file
    :type data: any
    :param path_to_file: path where a file is saved
    :type path_to_file: str
    :param warning: whether to show a warning messages, defaults to ``False``
    :type warning: bool
    :param kwargs: optional parameters of those ``pyhelpers.store.save_*`` functions

    **Examples**::

        from pyhelpers.store import save

        import pandas as pd

        data = pd.DataFrame([(530034, 180381), (406689, 286822), (383819, 398052), (582044, 152953)],
                            index=['London', 'Birmingham', 'Manchester', 'Leeds'],
                            columns=['Easting', 'Northing'])

        path_to_file = cd("tests\\data", "dat.txt")
        save(data, path_to_file, verbose=True)
        # Updating "dat.txt" at "..\\tests\\data" ... Done.

        path_to_file = cd("tests\\data", "dat.csv")
        save(data, path_to_file, verbose=True)
        # Updating "dat.csv" at "..\\tests\\data" ... Done.

        path_to_file = cd("tests\\data", "dat.xlsx")
        save(data, path_to_file, verbose=True)
        # Updating "dat.xlsx" at "..\\tests\\data" ... Done.

        path_to_file = cd("tests\\data", "dat.pickle")
        save(data, path_to_file, verbose=True)
        # Updating "dat.pickle" at "..\\tests\\data" ... Done.

        path_to_file = cd("tests\\data", "dat.feather")
        # `save(data, path_to_file, verbose=True)` will produce an error due to the index of `data`
        save(data.reset_index(), path_to_file, verbose=True)
        # Updating "dat.feather" at "..\\tests\\data" ... Done.
    """

    # Make a copy the original data
    dat = data.copy()
    if isinstance(data, pd.DataFrame) and data.index.nlevels > 1:
        dat.reset_index(inplace=True)

    # Save the data according to the file extension
    if path_to_file.endswith((".csv", ".xlsx", ".xls", ".txt")):
        save_spreadsheet(dat, path_to_file, **kwargs)

    elif path_to_file.endswith(".feather"):
        save_feather(dat, path_to_file, **kwargs)

    elif path_to_file.endswith(".json"):
        save_json(dat, path_to_file, **kwargs)

    elif path_to_file.endswith(".pickle"):
        save_pickle(dat, path_to_file, **kwargs)

    else:
        if warning:
            print("Note that the current file extension is not recognisable by this \"save()\" function.")

        if confirmed("To save \"{}\" as a .pickle file? ".format(os.path.basename(path_to_file))):
            save_pickle(dat, path_to_file, **kwargs)


def save_fig(path_to_fig_file, dpi=None, verbose=False, conv_svg_to_emf=False, **kwargs):
    """
    Save a figure object.

    This function relies on `matplotlib.pyplot.savefig`_ (and `Inkscape <https://inkscape.org>`_).

    :param path_to_fig_file: path where a figure file is saved
    :type path_to_fig_file: str
    :param dpi: the resolution in dots per inch; if ``None`` (default), use ``rcParams["savefig.dpi"]``
    :type dpi: int, None
    :param verbose: whether to print relevant information in console as the function runs, defaults to ``False``
    :type verbose: bool, int
    :param conv_svg_to_emf: whether to convert a .svg file to a .emf file, defaults to ``False``
    :type conv_svg_to_emf: bool
    :param kwargs: optional parameters of `matplotlib.pyplot.savefig`_

    .. _`matplotlib.pyplot.savefig`: https://matplotlib.org/3.2.1/api/_as_gen/matplotlib.pyplot.savefig.html

    **Examples**::

        from pyhelpers.store import save_fig

        import matplotlib.pyplot as plt
        from pyhelpers.dir import cd

        x, y = (1, 1), (2, 2)
        plt.figure()
        plt.plot([x[0], y[0]], [x[1], y[1]])
        plt.show()

        dpi = 300

        path_to_fig_file = cd("tests\\images", "fig.png")
        save_fig(path_to_fig_file, dpi, verbose=True)
        # Saving "fig.png" to "..\\tests\\images" ... Done.

        path_to_fig_file = cd("tests\\images", "fig.svg")
        save_fig(path_to_fig_file, dpi, verbose=True, conv_svg_to_emf=True)
        # Saving "fig.svg" to "..\\tests\\images" ... Done.
        # Saving the "fig.svg" as "..\\tests\\images\\fig.emf" ... Done.
    """
    
    get_specific_filepath_info(path_to_fig_file, verbose=verbose, ret_info=False)

    file_ext = pathlib.Path(path_to_fig_file).suffix

    try:
        import matplotlib.pyplot as plt
        # assert file_ext.strip(".") in plt.gcf().canvas.get_supported_filetypes().keys()

        plt.savefig(path_to_fig_file, dpi=dpi, **kwargs)
        print("Done.") if verbose else ""

    except Exception as e:
        print("Failed. {}.".format(e)) if verbose else ""

    if file_ext == ".svg" and conv_svg_to_emf:
        # inkscape_exe = "C:\\Program Files\\Inkscape\\inkscape.exe"
        # if os.path.isfile(inkscape_exe):
        #     path_to_emf = path_to_fig_file.replace(file_ext, ".emf")
        #     get_specific_filepath_info(path_to_emf, verbose=verbose, ret_info=False)
        #     subprocess.call([inkscape_exe, '-z', path_to_fig_file, '-M', path_to_emf])
        #     print("Conversion from .svg to .emf successfully.") if verbose else ""
        save_svg_as_emf(path_to_fig_file, path_to_fig_file.replace(file_ext, ".emf"), verbose=verbose)


def save_svg_as_emf(path_to_svg, path_to_emf, verbose=False, **kwargs):
    """
    Save a .svg file as a .emf file.

    :param path_to_svg: path where a .svg file is saved
    :type path_to_svg: str
    :param path_to_emf: path where a .emf file is saved
    :type path_to_emf: str
    :param verbose: whether to print relevant information in console as the function runs, defaults to ``False``
    :type verbose: bool, int
    :param kwargs: optional parameters of `subprocess.call`_

    .. _`subprocess.call`: https://docs.python.org/3/library/subprocess.html#subprocess.call

    **Example**::

        from pyhelpers.store import save_svg_as_emf

        import matplotlib.pyplot as plt
        from pyhelpers.dir import cd

        x, y = (1, 1), (2, 2)
        plt.figure()
        plt.plot([x[0], y[0]], [x[1], y[1]])

        path_to_svg = cd("tests\\images", "fig.svg")
        path_to_emf = cd("tests\\images", "fig.emf")

        save_svg_as_emf(path_to_svg, path_to_emf, verbose=True)
        # Saving the "fig.svg" as "..\\tests\\images\\fig.emf" ... Done.
    """

    abs_svg_path, abs_emf_path = pathlib.Path(path_to_svg), pathlib.Path(path_to_emf)
    assert abs_svg_path.suffix == ".svg"

    inkscape_exe = "C:\\Program Files\\Inkscape\\inkscape.exe"

    if os.path.isfile(inkscape_exe):
        if verbose:
            print("Saving the \"{}\" as \"..\\{}\"".format(abs_svg_path.name, abs_emf_path.relative_to(os.getcwd())),
                  end=" ... ")

        try:
            abs_emf_path.parent.mkdir(exist_ok=True)
            subprocess.call([inkscape_exe, '-z', path_to_svg, '-M', path_to_emf], **kwargs)
            print("Done.") if verbose else ""

        except Exception as e:
            print("Failed. {}".format(e)) if verbose else ""

    else:
        print("\"Inkscape\" (https://inkscape.org) is required to convert a .svg file to a .emf. file "
              "It is not found on this device.") if verbose else ""


def unzip(path_to_zip_file, out_dir, mode='r', verbose=False, **kwargs):
    """
    Extract data from a zip file.

    :param path_to_zip_file: path where a zipped file is saved
    :type path_to_zip_file: str
    :param out_dir: path to a directory where the extracted data is saved
    :type out_dir: str
    :param mode: defaults to ``'r'``
    :type mode: str
    :param verbose: whether to print relevant information in console as the function runs, defaults to ``False``
    :type verbose: bool, int
    :param kwargs: optional parameters of `zipfile.ZipFile.extractall`_

    .. _`zipfile.ZipFile.extractall`: https://docs.python.org/3/library/zipfile.html#zipfile.ZipFile.extractall

    **Example**::

        from pyhelpers.store import unzip

        from pyhelpers.dir import cd

        path_to_zip_file = cd("tests\\data", "zipped.zip")
        out_dir = cd("tests\\data")
        mode = 'r'

        unzip(path_to_zip_file, out_dir, mode, verbose=True)
        # Unzipping "..\\tests\\data\\zipped.zip" ... Done.
    """

    if verbose:
        print("Unzipping \"..\\{}\"".format(os.path.relpath(path_to_zip_file)), end=" ... ")

    try:
        with zipfile.ZipFile(path_to_zip_file, mode) as zf:
            zf.extractall(out_dir, **kwargs)
        print("Done. ") if verbose else ""
        zf.close()

    except Exception as e:
        print("Failed. {}".format(e))


def seven_zip(path_to_zip_file, out_dir, mode='aoa', verbose=False, **kwargs):
    """
    Use `7-Zip <https://www.7-zip.org/>`_ to extract data from a compressed file.

    :param path_to_zip_file: path where a compressed file is saved
    :type path_to_zip_file: str
    :param out_dir: path to a directory where the extracted data is saved
    :type out_dir: str
    :param mode: defaults to ``'aoa'``
    :type mode: str
    :param verbose: whether to print relevant information in console as the function runs, defaults to ``False``
    :type verbose: bool, int
    :param kwargs: optional parameters of `subprocess.call`_

    .. _`subprocess.call`: https://docs.python.org/3/library/subprocess.html#subprocess.call

    **Examples**::

        from pyhelpers.store import seven_zip

        from pyhelpers.dir import cd

        out_dir = cd("tests/data")
        mode = 'aoa'

        path_to_zip_file = cd("tests/data", "zipped.zip")
        seven_zip(path_to_zip_file, out_dir, mode, verbose=True)
        # <Details about the file extraction>

        path_to_zip_file = cd("tests/data", "zipped.7z")
        seven_zip(path_to_zip_file, out_dir, mode, verbose=True)
        # <Details about the file extraction>
    """

    try:
        seven_zip_exe = "C:\\Program Files\\7-Zip\\7z.exe"
        subprocess.call('"{}" x "{}" -o"{}" -{}'.format(seven_zip_exe, path_to_zip_file, out_dir, mode), **kwargs)
        print("\nFile extracted successfully.")

    except FileNotFoundError:
        seven_zip_exe = "7z.exe"
        subprocess.call('"{}" x "{}" -o"{}" -{}'.format(seven_zip_exe, path_to_zip_file, out_dir, mode), **kwargs)

    except Exception as e:
        print("\nFailed to extract \"{}\". {}.".format(path_to_zip_file, e))
        print("\"7-Zip\" (https://www.7-zip.org/) is required to run this function. "
              "It is not found on this device.") if verbose else ""


def load_csr_matrix(path_to_csr, verbose=False, **kwargs):
    """
    Load in a compressed sparse row (CSR) or compressed row storage (CRS).

    :param path_to_csr: path where a CSR (e.g. .npz) file is saved
    :type path_to_csr: str
    :param verbose: whether to print relevant information in console as the function runs, defaults to ``False``
    :type verbose: bool, int
    :param kwargs: optional parameters of `numpy.load <https://numpy.org/doc/stable/reference/generated/numpy.load>`_
    :return: a compressed sparse row
    :rtype: scipy.sparse.csr.csr_matrix

    **Example**::

        from pyhelpers.store import load_csr_matrix

        import numpy as np
        import scipy.sparse
        from pyhelpers.dir import cd

        indptr = np.array([0, 2, 3, 6])
        indices = np.array([0, 2, 2, 0, 1, 2])
        data = np.array([1, 2, 3, 4, 5, 6])
        csr_m = scipy.sparse.csr_matrix((data, indices, indptr), shape=(3, 3))

        path_to_csr = cd("tests\\data", "csr_mat.npz")
        np.savez_compressed(path_to_csr,
                            indptr=csr_m.indptr,
                            indices=csr_m.indices,
                            data=csr_m.data,
                            shape=csr_m.shape)

        csr_mat = load_csr_matrix(path_to_csr, verbose=True)
        # Loading "..\\tests\\data\\csr_mat.npz" ... Done.

        # .nnz gets the count of explicitly-stored values (non-zeros)
        print((csr_mat != csr_m).count_nonzero() == 0)
        # True

        print((csr_mat != csr_m).nnz == 0)
        # True
    """

    print("Loading \"..\\{}\"".format(os.path.relpath(path_to_csr)), end=" ... ") if verbose else ""

    try:
        csr_loader = np.load(path_to_csr, **kwargs)
        data, indices, indptr = csr_loader['data'], csr_loader['indices'], csr_loader['indptr']
        shape = csr_loader['shape']

        import scipy.sparse
        csr_mat = scipy.sparse.csr_matrix((data, indices, indptr), shape)

        print("Done.") if verbose else ""

        return csr_mat

    except Exception as e:
        print("Failed. {}".format(e)) if verbose else ""
