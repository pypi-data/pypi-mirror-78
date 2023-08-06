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

from textwrap import dedent

import pytest
import strictyaml
import LbAPCommon


def test_good_no_defaults():
    rendered_yaml = dedent(
        """\
    job_1:
        application: DaVinci/v45r3
        input:
            bk_query: /some/query
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
    """
    )
    data = LbAPCommon.parse_yaml(rendered_yaml)
    assert len(data) == 1
    assert data["job_1"]["application"] == "DaVinci/v45r3"
    assert data["job_1"]["input"] == {"bk_query": "/some/query"}
    assert data["job_1"]["output"] == "FILETYPE.ROOT"
    assert data["job_1"]["options"] == ["options.py", "$VAR/a.py"]
    assert data["job_1"]["wg"] == "Charm"
    assert data["job_1"]["automatically_configure"] is False
    assert data["job_1"]["inform"] == []


def test_good_with_defaults():
    rendered_yaml = dedent(
        """\
    defaults:
        wg: Charm
        automatically_configure: yes
        inform:
            - name@example.com

    job_1:
        application: DaVinci/v45r3
        input:
            bk_query: "/some/query"
        output: FILETYPE.ROOT
        options:
            - options.py

    job_2:
        application: DaVinci/v44r0
        input:
            bk_query: "/some/other/query"
        output: FILETYPE.ROOT
        options:
            - other_options.py
        wg: B2OC
        automatically_configure: false
        inform:
            - other@example.com
    """
    )
    data = LbAPCommon.parse_yaml(rendered_yaml)
    assert len(data) == 2

    assert data["job_1"]["application"] == "DaVinci/v45r3"
    assert data["job_1"]["input"] == {"bk_query": "/some/query"}
    assert data["job_1"]["output"] == "FILETYPE.ROOT"
    assert data["job_1"]["options"] == ["options.py"]
    assert data["job_1"]["wg"] == "Charm"
    assert data["job_1"]["automatically_configure"] is True
    assert data["job_1"]["inform"] == ["name@example.com"]

    assert data["job_2"]["application"] == "DaVinci/v44r0"
    assert data["job_2"]["input"] == {"bk_query": "/some/other/query"}
    assert data["job_2"]["output"] == "FILETYPE.ROOT"
    assert data["job_2"]["options"] == ["other_options.py"]
    assert data["job_2"]["wg"] == "B2OC"
    assert data["job_2"]["automatically_configure"] is False
    assert data["job_2"]["inform"] == ["other@example.com"]


@pytest.mark.parametrize("missing_key", ["application", "input", "output", "wg"])
def test_bad_missing_key(missing_key):
    data = {
        "job_1": {
            "application": "DaVinci/v45r3",
            "input": {"bk_query": "/some/query"},
            "output": "FILETYPE.ROOT",
            "options": ["options.py"],
            "wg": "Charm",
        }
    }
    del data["job_1"][missing_key]
    rendered_yaml = strictyaml.YAML(data).as_yaml()
    try:
        LbAPCommon.parse_yaml(rendered_yaml)
    except strictyaml.YAMLValidationError as e:
        assert "required key(s) '" + missing_key + "' not found" in str(e)
