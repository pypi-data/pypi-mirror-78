# (C) Copyright 2020 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#


def download_and_cache(url: str) -> str:
    """[summary]

    :param url: [description]
    :type url: str
    :return: [description]
    :rtype: str
    """
    from climetlab import load_source

    return load_source("url", url).path
