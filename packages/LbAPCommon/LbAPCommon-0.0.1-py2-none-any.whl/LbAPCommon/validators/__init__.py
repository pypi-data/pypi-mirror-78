###############################################################################
# (c) Copyright 2020 CERN                                                     #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__all__ = [
    "match_output_filenames",
    "status_from_xml_summary",
    "parse_bookkeeping_xml",
    "parse_log",
]

from os.path import basename
import re

from lxml import etree

from .bookkeeping_xml import parse_bookkeeping_xml


def match_output_filenames(filenames, output_filetypes, application_name, step_index):
    """File the XML, log and output filenames from a test job

    Parameters
    ----------
    filenames : :obj:`list` of :obj:`str`
        The filenames found in the test output
    output_filetypes : :obj:`list` of :obj:`str`
        The output filetype(s) of the job
    application_name : :obj:`str`
        Name of the application being ran (e.g. DaVinci)
    step_index : :obj:`int`
        The index of this test within the job

    Returns
    -------
    xml_summary_fn : :obj:`str` or None
        The filename of the XML summary
    xml_bk_fn : :obj:`str` or None
        The filename of the Bookkeeping summary
    log_fn : :obj:`str` or None
        The filename of the application log
    output_fns : :obj:`dict`
        A mapping of output filetype to a filename or None
    """
    expected_log_fn = "%s_00012345_00006789_%s.log" % (
        application_name,
        step_index,
    )

    xml_summary_fn = None
    xml_bk_fn = None
    log_fn = None
    output_fns = {ft: None for ft in output_filetypes}
    for fn in filenames:
        fn = basename(fn)
        # Look for the XML summary
        if re.match(r"^summary.*\.xml$", fn):
            if xml_summary_fn is not None:
                raise NotImplementedError(fn, xml_summary_fn)
            xml_summary_fn = fn
        # Look for the Bookkeeping XML
        if re.match(r"^bookkeeping_.*\.xml$", fn):
            if xml_bk_fn is not None:
                raise NotImplementedError(fn, xml_bk_fn)
            xml_bk_fn = fn
        # Look for the application log file
        if expected_log_fn == fn:
            if log_fn is not None:
                raise NotImplementedError(fn, log_fn)
            log_fn = fn
        # Look for the output filenames
        for output_filetype in output_filetypes:
            if fn.upper().endswith(output_filetype):
                if output_fns[output_filetype] is not None:
                    raise NotImplementedError(fn, output_fns)
                output_fns[output_filetype] = fn

    return xml_summary_fn, xml_bk_fn, log_fn, output_fns


def status_from_xml_summary(fp):
    """Check is the job succeeded using the XML summary file

    Parameters
    ----------
    fp : file-like
        File pointer of the XML summary

    Returns
    -------
    passed : :obj:`bool`
        True to the XML summary reports the job as passed
    """
    xml_summary = etree.parse(fp, base_url="LbAnalysisProductions/data/xml")
    success_value = xml_summary.find(".//success").text.lower()
    if success_value == "true":
        return True
    elif success_value == "false":
        return False
    else:
        raise NotImplementedError(success_value)


def parse_log(log_text):
    """Parse the log text for errors and advice

    Parameters
    ----------
    text : :obj:`str`
        Contents of the log file

    Returns
    -------
    counts : :obj:`tuple` of :obj:`int`
        Tuple containing the number of WARNING/ERROR/FATAL level messages in the job log
    suggestions : :obj:`list`
        Suggestions to provide to the analysts
    errors : :obj:`list`
        Errors found in the log which need to be acted upon
    """
    # Look for how many messages of each type are found
    base_message = r"(?:# )?(?:\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \w+ )?[^\s]+\s*"
    warning_message = base_message + r"WARNING [^\n]+"
    n_warning = len(re.findall(warning_message, log_text))
    error_message = base_message + r"ERROR [^\n]+"
    n_error = len(re.findall(error_message, log_text))
    fatal_message = base_message + r"FATAL [^\n]+"
    n_fatal = len(re.findall(fatal_message, log_text))

    # TODO Implement errors and suggestions
    suggestions = []
    errors = []

    return (n_warning, n_error, n_fatal), suggestions, errors
