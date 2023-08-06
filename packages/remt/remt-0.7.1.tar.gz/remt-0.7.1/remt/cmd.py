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
Command line commands.
"""

import asyncssh
import configparser
import json
import os.path
import shutil
import typing as tp
import urllib.request
from contextlib import asynccontextmanager
from collections import namedtuple
from cytoolz.dicttoolz import get_in
from datetime import datetime
from iterfzf import iterfzf
from functools import partial
from uuid import uuid4 as uuid

import remt
from .error import *
from .indexer import ann_text, fmt_ann_text
from .meta import BASE_DIR, fn_path, cache_dir, read_meta, sync_meta, \
    fn_metadata, create_metadata
from .pdf import pdf_open
from .util import flatten

FILE_TYPE = {
    'CollectionType': 'd',
}

ERROR_CFG = """\
Configuration file {conf} not found

  Create configuration file `{conf}` with contents

    [connection]
    host=10.11.99.1
    user=root
    password=<your reMarkable tablet password>
"""


# config: remt config
# sftp: SFTP connection to a device
# dir_meta: metadata files
# meta: parsed metadata
# dir_data: directory where to fetch files from a device or where to
#   prepare files for upload
RemtContext = namedtuple(
    'RemtContext',
    ['config', 'sftp', 'dir_meta', 'meta', 'dir_data'],
)

#
# utilities
#

def read_config():
    """
    Read and return `remt` project configuration.
    """
    conf_file = os.path.expanduser('~/.config/remt.ini')
    if not os.path.exists(conf_file):
        msg = ERROR_CFG.format(conf=conf_file)
        raise ConfigError(msg)

    cp = configparser.ConfigParser()
    cp.read(conf_file)
    return cp

@asynccontextmanager
async def remt_ctx(dir_base: tp.Optional[str]=None):
    """
    Create a `remt` project context.

    The function is an asynchronous context manager.
    """
    config = read_config()
    host = config.get('connection', 'host')
    user = config.get('connection', 'user')
    password = config.get('connection', 'password')

    if dir_base is None:
        dir_base = cache_dir(host)

    mkdir = partial(os.makedirs, exist_ok=True)
    dir_meta = os.path.join(dir_base, 'metadata')
    dir_data = os.path.join(dir_base, 'data')

    mkdir(dir_meta)
    mkdir(dir_data)

    try:
        ctx_conn = asyncssh.connect(host, username=user, password=password)
        async with ctx_conn as conn:
            async with conn.start_sftp_client() as sftp:
                await sync_meta(sftp, dir_meta)
                meta = read_meta(dir_meta)
                yield RemtContext(config, sftp, dir_meta, meta, dir_data)
    except OSError as ex:
        if ex.errno == 101:
            raise ConnectionError(
                'Cannot connect to a reMarkable tablet: {}'.format(ex.strerror)
            )
        else:
            raise
    finally:
        shutil.rmtree(dir_data)

def norm_path(path):
    """
    Normalise path of a file on a reMarkable tablet.

    All leading and trailing slashes are removed. Multiple slashes are
    replaced with one.

    :param path: Path to normalise.
    """
    return os.path.normpath(path).strip('/')

def fn_interactive(ctx: RemtContext, is_dir: bool=False) -> str:
    """
    Get filename interactively using `fzf` program.

    Raise error if selection interrupted.

    :param ctx: `remt` project context.
    :param is_dir: Allow to select only directories if true.
    """
    if is_dir:
        files = (
            k for k, v in ctx.meta.items()
            if v['type'] == 'CollectionType'
        )
    else:
        files = ctx.meta.keys()

    result = iterfzf(sorted(files))
    if result is None:
        raise FileError('Interactive file selection cancelled')

    return result

#
# parsing pages from a collection of files in reMarkable lines format
#

def parse_document(ctx, data):
    get_fin = lambda p: os.path.join(ctx.dir_data, data['uuid'], p) + '.rm'
    pages = data['content'].get('pages')
    if pages is None:
        pages = [str(i) for i in range(data['content']['pageCount'])]
    items = flatten(parse_page(get_fin(p), i) for i, p in enumerate(pages))
    yield from items


def parse_page(fin, page_number):
    """
    Parse page from reMarkable lines file.

    Return empty page if file does not exist.

    .. note::
       Version 3 of the reMarkable lines format can contain only single
       page.

    :param fin: reMarkable lines file.
    :param page_number: Page number to be associated with the page.
    """
    if os.path.exists(fin):
        with open(fin, 'rb') as f:
            yield from remt.parse(f, page_number)
    else:
        yield from remt.empty_page(page_number)

#
# cmd: ls
#

def marker(cond, marker):
    return marker if cond else '-'

def ls_line(fn, data):
    """
    Create `ls` command basic output line.
    """
    return fn

def ls_line_long(fn, data):
    """
    Create `ls` command long output line.
    """
    bookmarked = marker(data['pinned'] is True, 'b')
    is_dir = marker(data['type'] == 'CollectionType', 'd')

    tstamp = int(data['lastModified']) / 1000
    tstamp = datetime.fromtimestamp(tstamp)

    line = '{}{} {:%Y-%m-%d %H:%M:%S} {}'.format(
        is_dir, bookmarked, tstamp, fn
    )
    return line

def ls_filter_path(meta, path):
    """
    Filter metadata to keep metadata starting with path name.

    The path name itself *is* filtered out.

    :param meta: reMarkable tablet metadata.
    :param path: Path name.
    """
    meta = {k: v for k, v in meta.items() if k.startswith(path) and path != k}
    return meta

def ls_filter_parent_uuid(meta, uuid):
    """
    Filter metadata to keep metadata starting, which parent is identified
    by UUID.

    :param meta: reMarkable tablet metadata.
    :param uuid: UUID of parent directory.
    """
    check = lambda v: not v if uuid is None else v == uuid
    meta = {k: v for k, v in meta.items() if check(v.get('parent'))}
    return meta

async def cmd_ls(args):
    to_line = ls_line_long if args.long else ls_line
    path = norm_path(args.path) if args.path else None

    async with remt_ctx() as ctx:
        meta = ctx.meta

        if path == '%i':
            path = fn_interactive(ctx)

        # get starting UUID while we have all metadata
        start = None
        if path:
            start = fn_metadata(meta, path)['uuid']

        if path:
            meta = ls_filter_path(meta, path)

        if not args.recursive:
            meta = ls_filter_parent_uuid(meta, start)

        lines = (to_line(k, v) for k, v in sorted(meta.items()))
        print('\n'.join(lines))

#
# cmd: mkdir
#

async def cmd_mkdir(args):
    """
    Create a directory on reMarkable tablet device.
    """
    async with remt_ctx() as ctx:
        meta = ctx.meta
        path = norm_path(args.path)

        if path in meta:
            msg = 'Cannot create directory "{}" as it exists'.format(path)
            raise FileError(msg)

        parent, name = os.path.split(path)
        if parent and parent not in meta:
            raise FileError('Parent directory not found')

        assert bool(name)

        parent_uuid = get_in([parent, 'uuid'], meta)
        data = create_metadata(True, parent_uuid, name)

        dir_fn = os.path.join(ctx.dir_data, str(uuid()))

        with open(dir_fn + '.metadata', 'w') as f:
            json.dump(data, f)

        # empty content file required to create a directory
        with open(dir_fn + '.content', 'w') as f:
            json.dump({}, f)

        await ctx.sftp.mput(dir_fn + '.*', BASE_DIR)

#
# cmd: export
#
async def cmd_export(args):
    path = norm_path(args.input)
    f_export = _export_remt if args.renderer == 'remt' else _export_rm

    async with remt_ctx() as ctx:
        if path == '%i':
            path = fn_interactive(ctx)

        output = args.output
        if os.path.isdir(output):
            output = os.path.join(output, os.path.basename(path))
            if not output.endswith('.pdf'):
                output += '.pdf'

        data = fn_metadata(ctx.meta, path)
        await f_export(ctx, data, output)

async def _export_remt(ctx, data, fout):
    """
    Export notebook or PDF document using `remt` renderer.

    :param ctx: `remt` project context.
    :param data: Metadata of input file.
    :param fout: Filename of output file.
    """
    to_copy = fn_path(data, ext='*')
    await ctx.sftp.mget(to_copy, ctx.dir_data, recurse=True)

    fin_pdf = fn_path(data, base=ctx.dir_data, ext='.pdf')
    fin_pdf = fin_pdf if os.path.exists(fin_pdf) else None

    items = parse_document(ctx, data)
    with remt.draw_context(fin_pdf, fout) as ctx:
        for item in items:
            remt.draw(item, ctx)

async def _export_rm(ctx, data, fout):
    """
    Export notebook or PDF document using reMarkable tablet device.

    :param ctx: `remt` project context.
    :param data: Metadata of input file.
    :param fout: Filename of output file.
    """
    host = ctx.config.get('connection', 'host')
    uuid = data['uuid']
    url = 'http://{}/download/{}/placeholder'.format(host, uuid)

    response = urllib.request.urlopen(url)
    with open(fout, 'wb') as f:
        read = lambda: response.read(1024 ** 2)
        for data in iter(read, b''):
            f.write(data)

#
# cmd: import
#
def _prepare_import_data(ctx, fn_in, out_uuid):
    """
    Prepare import data for a file to be uploaded onto a reMarkable
    tablet.

    :param ctx: `remt` project context.
    :param fn_in: File to be imported.
    :param out_uuid: UUID of the output directory located on a reMarkable
        tablet.
    """
    name = os.path.basename(fn_in)
    fn_base = os.path.join(ctx.dir_data, str(uuid()))
    data = create_metadata(False, out_uuid, name)

    fn_pdf = fn_base + '.pdf'
    shutil.copy(fn_in, fn_pdf)
    with open(fn_base + '.metadata', 'w') as f:
        json.dump(data, f)

    # empty content file required
    with open(fn_base + '.content', 'w') as f:
        page_count = pdf_open(fn_pdf).get_n_pages()
        content = {
            'fileType': 'pdf',
            'lastOpenedPage': 0,
            'lineHeight': -1,
            'pageCount': page_count,

        }
        json.dump(content, f)
    return fn_base + '.*'

async def cmd_import(args):
    """
    Import a number of files onto a directory on a reMarkable tablet.
    """
    output = norm_path(args.output)

    async with remt_ctx() as ctx:
        if output == '%i':
            output = fn_interactive(ctx, is_dir=True)

        out_meta = fn_metadata(ctx.meta, output)
        if out_meta['type'] != 'CollectionType':
            raise FileError('Destination path is not a directory')

        out_uuid = out_meta['uuid']
        to_import = [
            _prepare_import_data(ctx, fn, out_uuid) for fn in args.input
        ]
        await ctx.sftp.mput(to_import, BASE_DIR)

#
# cmd: index
#

async def cmd_index(args):
    path = norm_path(args.input)

    async with remt_ctx() as ctx:
        if path == '%i':
            path = fn_interactive(ctx)

        data = fn_metadata(ctx.meta, path)

        to_copy = fn_path(data, ext='*')
        await ctx.sftp.mget(to_copy, ctx.dir_data, recurse=True)

        fin_pdf = fn_path(data, base=ctx.dir_data, ext='.pdf')
        pdf_doc = pdf_open(fin_pdf)

        items = parse_document(ctx, data)
        items = ann_text(pdf_doc, items)
        items = fmt_ann_text(items)

        for header, texts in items:
            print(header)
            print(texts)

COMMANDS = {
    'ls': cmd_ls,
    'mkdir': cmd_mkdir,
    'export': cmd_export,
    'import': cmd_import,
    'index': cmd_index,
}

# vim: sw=4:et:ai
