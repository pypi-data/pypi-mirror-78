#
# remt - reMarkable tablet command-line tools
#
# Copyright (C) 2018-2020 by Artur Wroblewski <wrobell@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Read and parse reMarkable tablet metadata.
"""

import getmac
import glob
import json
import logging
import operator
import os
from cytoolz.dicttoolz import assoc
from cytoolz.functoolz import compose
from datetime import datetime
from functools import partial

from remt.error import *

logger = logging.getLogger(__name__)

BASE_DIR = '/home/root/.local/share/remarkable/xochitl'

fn_local = os.path.join

def fn_path(data, base=BASE_DIR, ext='.*'):
    """
    Having metadata object create UUID based path of a file created by
    reMarkable tablet.

    :param data: Metadata object.
    """
    return '{}/{}{}'.format(base, data['uuid'], ext)

def fn_remote(fn: str) -> str:
    """
    Return path to a file on reMarkable tablet.
    """
    return os.path.join(BASE_DIR, fn)

def create_metadata(is_dir, parent_uuid, name):
    now = datetime.utcnow()
    tstamp = int(now.timestamp() * 1000)
    type = 'CollectionType' if is_dir else 'DocumentType'
    data = {
        'deleted': False,
        'lastModified': str(tstamp),
        'metadatamodified': True,
        'modified': True,
        'parent': parent_uuid,
        'pinned': False,
        'synced': False,
        'type': type,
        'version': 0,
        'visibleName': name,
    }
    return data

def to_path(data, meta):
    parent = data.get('parent')
    name = data['visibleName']
    if parent:
        return to_path(meta[parent], meta) + '/' + name
    else:
        return name

def resolve_uuid(meta):
    meta = {
        k: assoc(v, 'uuid', k) for k, v in meta.items()
        if v.get('parent') != 'trash'
    }
    return {to_path(data, meta): data for data in meta.values()}

def fn_metadata(meta, path):
    """
    Get reMarkable tablet file metadata or raise file not found error if no
    metadata for path is found.

    :param meta: reMarkable tablet metadata.
    :param path: Path of reMarkable tablet file.
    """
    data = meta.get(path)
    if not data:
        raise FileError('File or directory not found: {}'.format(path))
    return data

def is_meta(fn: str) -> bool:
    """
    Check if a filename is reMarkable tablet meta file.

    :param fn: Filename to be checked.
    """
    return fn.endswith('.content') or fn.endswith('.metadata')

async def ls_remote(sftp):
    """
    List reMarkable tablet meta files.
    """
    items = await sftp.readdir(BASE_DIR)
    items = (f for f in items if is_meta(f.filename))
    return {f.filename: f.attrs.mtime for f in items}

def ls_local(dir_meta: str):
    """
    List reMarkable tablet meta files in local cache.
    """
    files = glob.glob(fn_local(dir_meta, '*'))
    return {os.path.basename(fn): os.stat(fn).st_mtime for fn in files}

def find_meta_update(files_remote, files_local):
    """
    Find reMarkable tablet meta files, which need to be updated in local
    cache.
    """
    items = (f for f, t in files_remote.items() if t > files_local.get(f, 0))
    yield from items

def find_meta_delete(files_remote, files_local):
    """
    Find reMarkable tablet meta files, which need to be removed from local
    cache.
    """
    yield from (f for f in files_local if f not in files_remote)

async def sync_meta(sftp, dir_meta):
    """
    Synchronize metadata from reMarkable tablet to local cache.

    :param sftp: SFTP connection object.
    :param dir_meta: Local cache directory with reMarkable tablet metadata.
    """
    files_remote = await ls_remote(sftp)
    files_local = ls_local(dir_meta)

    # update new and out-of-date meta files
    files = find_meta_update(files_remote, files_local)
    files = [fn_remote(f) for f in files]
    await sftp.mget(files, dir_meta, preserve=True)
    logger.info('fetched {} files into local cache'.format(len(files)))

    # remove metadata, which does not exist on reMarkable tablet anymore
    files = list(find_meta_delete(files_remote, files_local))
    for fn in files:
        assert fn.endswith('.content') or fn.endswith('.metadata')
        os.unlink(fn_local(dir_meta, fn))
    logger.info('removed {} files from local cache'.format(len(files)))

def read_meta(dir_meta):
    """
    Read metadata from a reMarkable tablet.
    """
    to_uuid = compose(
        operator.itemgetter(0),
        os.path.splitext,
        os.path.basename,
    )
    load_json = compose(json.load, open)
    list_files = compose(glob.glob, partial(fn_local, dir_meta))

    files_content = list_files('*.content')
    files_content = {to_uuid(fn): fn for fn in files_content}

    files = list_files('*.metadata')
    files = ((fn, to_uuid(fn)) for fn in files)
    files = ((fn, u) for fn, u in files if u in files_content)

    # load metadata file and content file
    data = (
        (u, load_json(fn), load_json(files_content[u]))
        for fn, u in files
    )
    meta = {u: assoc(m, 'content', c) for u, m, c in data}
    return resolve_uuid(meta)

def cache_dir(host: str) -> str:
    """
    Generate directory for reMarkable tablet metadata cache.

    :param host: reMarkable tablet hostname.
    """
    mac = getmac.get_mac_address(hostname=host)
    base = os.path.expanduser('~')
    return os.path.join(base, '.cache/remt', mac)

# vim: sw=4:et:ai
