#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2015-2019European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl

import glob
import logging
import operator
import os
import re
from textwrap import dedent

import pandas as pd

__commit__ = ""

log = logging.getLogger(__name__)


_xl_extensions = re.compile(r"\.xl((s[xm]?|t[xm]?)|w|m)$", re.IGNORECASE)
_xl_extensions_anywhere = re.compile(r"\.xl((s[xm]?|t[xm]?)|w|m)\b", re.IGNORECASE)


_xl_installed = None


def is_excel_file(path):
    return _xl_extensions.search(path)


def check_excell_installed():
    """Checks once and returns `True` if Excel-app is installed in the system."""
    global _xl_installed
    if _xl_installed is None:
        try:
            from win32com.client import dynamic  # @UnresolvedImport

            dynamic.Dispatch("Excel.Application")
            _xl_installed = True
        except Exception:  # pragma: no cover
            _xl_installed = False

    return _xl_installed


def _get_xl_vb_project(xl_wb):
    """
    To allow updating Excel's VBA, follow instructions at:
      https://social.msdn.microsoft.com/Forums/office/en-US/c175d0d7-7341-4b31-9699-712e5449cf78/access-to-visual-basic-project-is-not-trusted

      1. Go to Excel's Options.
      2. Click Trust Center.
      3. Click Trust Center Settings.
      4. Click Macro Settings.
      5. Click to select the `Trust access to the VBA project object model` check box.
      6. Click OK to close the Excel Options dialog box.

    or use the Excel-2010 shortcuts
      [ALT] + [t][m][s]
    and then click the above check box.
    """
    from win32com.universal import com_error
    import easygui

    def show_unlock_msg(msg):
        text = dedent(_get_xl_vb_project.__doc__)
        #        try:
        #            from tkinter import messagebox as msgbox
        #        except ImportError:
        #            import tkMessageBox as msgbox
        #        msgbox.showinfo(title="Excel Permission Denied!", message=msg)
        easygui.textbox(title="Excel Permission Denied!", msg=msg, text=text)
        return msg

    try:
        xl_vbp = xl_wb.VBProject
        if xl_vbp.Protection == 1:
            msg = "The VBA-code in Excel is protected!"
            msg = show_unlock_msg(msg)
            raise Exception(msg)
        return xl_vbp
    except com_error as ex:  # @UndefinedVariable
        if ex.hresult == -2147352567:
            msg = "Excel complained: \n  %s" % ex.excepinfo[2]
            msg = show_unlock_msg(msg)
            raise Exception(msg)
        raise


def _gather_files(fpaths_wildcard):
    """
    :param str fpaths_wildcard: 'some/foo*bar.py'
    :return: a map {ext-less_basename --> full_path}.
    """

    def basename(fname):
        b, _ = os.path.splitext(os.path.basename(fname))
        return b

    return {basename(f): f for f in glob.glob(fpaths_wildcard)}


#############################
# Update VBA
#############################

XL_TYPE_MODULE = 1
XL_TYPE_SHEET = 100


def _remove_vba_modules(xl_vbcs, *mod_names_to_del):
    """
    :param VBProject.VBComponents xl_vbcs:
    :param str-list mod_names_to_del: which modules to remove, assumed *all* if missing
    """

    # Comparisons are case-insensitive.
    if mod_names_to_del:
        mod_names_to_del = map(str.lower, mod_names_to_del)

    # Gather all workbook vba-modules.
    xl_mods = [xl_vbc for xl_vbc in xl_vbcs if xl_vbc.Type == XL_TYPE_MODULE]

    # Remove those matching.
    #
    for m in xl_mods:
        if not mod_names_to_del or m.Name.lower() in mod_names_to_del:
            log.debug("Removing vba_module(%s)...", m.Name)
            xl_vbcs.Remove(m)


def _import_vba_files(xl_vbcs, vba_file_map):
    """
    :param VBProject.VBComponents xl_vbcs:
    :param dict vba_file_map: a map {module_name --> full_path}.

    """
    from win32com.universal import com_error

    cwd = os.getcwd()
    for vba_modname, vba_fpath in vba_file_map.items():
        try:
            log.debug("Removing vba_module(%s)...", vba_modname)
            old_xl_mod = xl_vbcs.Item(vba_modname)
            xl_vbcs.Remove(old_xl_mod)
            log.info("Removed vba_module(%s).", vba_modname)
        except com_error as ex:
            log.debug(
                "Probably vba_module(%s) did not exist, because: \n  %s",
                vba_modname,
                ex,
            )
        log.debug("Importing vba_module(%s) from file(%s)...", vba_modname, vba_fpath)
        xl_vbc = xl_vbcs.Import(os.path.join(cwd, vba_fpath))
        log.info(
            "Imported %i LoC for vba_module(%s) from file(%s).",
            xl_vbc.CodeModule.CountOfLines,
            vba_modname,
            vba_fpath,
        )
        xl_vbc.Name = vba_modname


def _save_workbook(xl_workbook, path):
    # TODO: Remove when xlwings updated to latest.
    # From
    # http://stackoverflow.com/questions/21306275/pywin32-saving-as-xlsm-file-instead-of-xlsx
    xlOpenXMLWorkbookMacroEnabled = 52

    saved_path = xl_workbook.Path
    if (saved_path != "") and (path is None):
        # Previously saved: Save under existing name
        xl_workbook.Save()
    elif (saved_path == "") and (path is None):
        # Previously unsaved: Save under current name in current working
        # directory
        path = os.path.join(os.getcwd(), xl_workbook.Name)
        xl_workbook.Application.DisplayAlerts = False
        xl_workbook.SaveAs(path, FileFormat=xlOpenXMLWorkbookMacroEnabled)
        xl_workbook.Application.DisplayAlerts = True
    elif path:
        # Save under new name/location
        xl_workbook.Application.DisplayAlerts = False
        xl_workbook.SaveAs(path, FileFormat=xlOpenXMLWorkbookMacroEnabled)
        xl_workbook.Application.DisplayAlerts = True


def _save_excel_as_macro_enabled(xl_wb, new_fname=None):
    DEFAULT_XLS_MACRO_FORMAT = ".xlsm"

    if not new_fname:
        _, e = os.path.splitext(xl_wb.FullName)
        if e.lower()[-1:] != "m":
            new_fname = xl_wb.FullName + DEFAULT_XLS_MACRO_FORMAT
            log.info(
                "Cloning as MACRO-enabled the Input-workbook(%s) --> Output-workbook(%s)",
                xl_wb.FullName,
                new_fname,
            )
    _save_workbook(xl_wb, new_fname)

    return new_fname


def import_vba_into_excel_workbook(infiles_wildcard, wrkb_fname=None, new_fname=None):
    """
    Add or update *xmlwings* VBA-code of a Workbook.

    :param str infiles_wildcard: 'some/foo*bar.vba'
    :param str wrkb_fname: filepath to update, active-workbook assumed if missing
    :param str new_fname: a macro-enabled (`.xlsm`, `.xltm`) filepath for updated workbook,
                            `.xlsm` gets appended if current not a macro-enabled excel-format
    """
    import xlwings as xw

    wb = wrkb_fname and xw.Book(wrkb_fname) or xw.books.active
    if not wb:
        raise ValueError("No active workbook found!")
    xl_wb = wb.api
    xl_vbp = _get_xl_vb_project(xl_wb)
    xl_vbcs = xl_vbp.VBComponents

    infiles_map = _gather_files(infiles_wildcard)
    log.info("Modules to import into Workbook(%s): %s", wb, infiles_map)

    if infiles_map:
        # TODO: _remove_vba_modules(xl_vbcs)

        # if xl_wb.FullName.lower()[-1:] != 'm':
        #    new_fname = _save_excel_as_macro_enabled(xl_wb, new_fname=new_fname)

        _import_vba_files(xl_vbcs, infiles_map)

        _save_excel_as_macro_enabled(xl_wb, new_fname=new_fname)

    return wb


def normalize_local_url(self, urlparts):
    """As fetched from :func:`urllib.parse.urlsplit()`."""
    if "file" == urlparts.scheme:
        urlparts = urlparts._replace(path=os.path.abspath(urlparts.path))
    return urlparts.geturl()


def main(*argv):
    """
    Updates the vba code on excel workbooks.

    Usage::

        {cmd}  *.vbas                       # Add modules into active excel-workbook.
        {cmd}  *.vbas  in_file.xlsm         # Specify input workbook to add/update.
        {cmd}  *.vbas  foo.xlsx  bar.xlsm   # Specify input & output workbooks.
        {cmd}  *.vbas  foo.xls              # A `foo.xls.xlsm` will be created.
        {cmd}  *.vbas  foo.xls   bar        # A `bar.xlm` will be created.
        {cmd}  --pandalone inp.xls [out]    # Add 'pandalone-xlwings' modules.
    """

    cmd = os.path.basename(argv[0])
    if len(argv) < 2:
        exit("Too few arguments! \n%s" % dedent(main.__doc__.format(cmd=cmd)))
    else:
        if argv[1] == "--pandalone":
            mydir = os.path.dirname(__file__)
            argv = list(argv)
            argv[1] = os.path.join(mydir, "*.vba")
        elif argv[1].startswith("--"):
            exit(
                "Unknown option(%s)! \n%s"
                % (argv[1], dedent(main.__doc__.format(cmd=cmd)))
            )

        import_vba_into_excel_workbook(*argv[1:])


if __name__ == "__main__":
    import sys

    main(*sys.argv)
