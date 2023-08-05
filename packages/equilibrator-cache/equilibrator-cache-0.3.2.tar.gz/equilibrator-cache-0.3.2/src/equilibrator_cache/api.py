"""An API module for initializing the cache."""
# The MIT License (MIT)
#
# Copyright (c) 2013 Weizmann Institute of Science.
# Copyright (c) 2018 Institute for Molecular Systems Biology, ETH Zurich.
# Copyright (c) 2018, 2019 Novo Nordisk Foundation Center for Biosustainability,
# Technical University of Denmark
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import logging
from typing import Optional

import quilt
from requests.exceptions import ConnectionError
from sqlalchemy import create_engine

from .compound_cache import CompoundCache


__all__ = ("create_compound_cache_from_quilt", "DEFAULT_QUILT_PKG")


logger = logging.getLogger(__name__)

DEFAULT_QUILT_PKG = "equilibrator/cache"
DEFAULT_QUILT_VERSION = "0.2.10"


def create_compound_cache_from_quilt(
    package: str = DEFAULT_QUILT_PKG,
    hash: Optional[str] = None,
    tag: Optional[str] = None,
    version: Optional[str] = DEFAULT_QUILT_VERSION,
    force: bool = True,
) -> CompoundCache:
    """
    Initialize a compound cache from a quilt data package.

    Parameters
    ----------
    package : str, optional
        The quilt package used to initialize the compound cache
        (Default value = `equilibrator/cache`)
    hash : str, optional
        quilt hash (Default value = None)
    version : str, optional
        quilt version (Default value = DEFAULT_QUILT_VERSION)
    tag : str, optional
        quilt tag (Default value = None)
    force : bool, optional
        Re-download the quilt data if a newer version exists
        (Default value = `True`).

    Returns
    -------
    CompoundCache
        a compound cache object.

    """
    try:
        logger.info("Fetching eQuilibrator compound cache...")
        quilt.install(
            package=package, hash=hash, tag=tag, version=version, force=force
        )
    except ConnectionError:
        logger.error(
            "No internet connection available. Attempting to use existing "
            "compound cache."
        )
    except PermissionError:
        logger.error(
            "You do not have the necessary filesystem permissions to download "
            "an update to the quilt data. Attempting to use existing "
            "compound cache."
        )
    cache = quilt.load(package)
    return CompoundCache(create_engine(f"sqlite:///{cache.compounds()}"))


def create_compound_cache_from_sqlite_file(path: str) -> CompoundCache:
    """
    Initialize a compound cache from a local SQLite file.

    Parameters
    ----------
    path : str
        The path to the SQLite file.

    """
    return CompoundCache(create_engine(f"sqlite:///{path}"))
