#!/usr/bin/env python
"""A script version of Dropbox

Provides utilities to work with Dropbox just like the official dropbox cli
(http://www.dropboxwiki.com/tips-and-tricks/using-the-official-dropbox-command-line-interface-cli),
but in a script instead of a REPL way. sorno_dropbox also has higher level
features like copying directories recursively. Before you use this script, you
need to export the environment variables DROPBOX_APP_KEY and
DROPBOX_APP_SECRET for the app key and app secret of Dropbox. You can find
these at http://www.dropbox.com/developers/apps. For simplicity sake, just
give the app key "Full Dropbox" permission.


    Copyright 2014 Heung Ming Tai

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import argparse
import humanize
import logging
import os
import pprint
import re
import sys

from dropbox import files as dbfiles
from dropbox import oauth, rest, session, dropbox
import six
from sorno import loggingutil


# Fill in your consumer key and secret below or set the corresponding
# environment variables.
# You can find these at http://www.dropbox.com/developers/apps
DROPBOX_APP_KEY = None  # Full Dropbox permission
DROPBOX_APP_SECRET = None
DROPBOX_TOKEN_FILE = "/tmp/dropbox_token"

_LOG = logging.getLogger(__name__)
_PLAIN_LOGGER = None  # will be created in main()


def command(login_required=True):
    """a decorator for handling authentication and exceptions"""
    def decorate(f):
        def wrapper(self, *args):
            if login_required and self.api_client is None:
                _PLAIN_LOGGER.info("Need to login first")
                self.login()
                if self.api_client is None:
                    _PLAIN_LOGGER.error("Fail to login")
                    return

            try:
                return f(self, *args)
            except rest.ErrorResponse as e:
                msg = e.user_error_msg or str(e)
                _LOG.exception(msg)

        wrapper.__doc__ = f.__doc__
        return wrapper
    return decorate


class DropboxApp(object):
    def __init__(
        self,
        app_key,
        app_secret,
    ):
        self.app_key = app_key
        self.app_secret = app_secret

        self.api_client = None
        try:
            serialized_token = open(DROPBOX_TOKEN_FILE).read()
            if serialized_token.startswith('oauth2:'):
                access_token = serialized_token[len('oauth2:'):]
                self.api_client = dropbox.Dropbox(access_token)
                _LOG.debug("[loaded OAuth 2 access token]")
            else:
                _LOG.warn("Malformed access token in %r.", DROPBOX_TOKEN_FILE)
        except IOError:
            pass # don't worry if it's not there

    @command(login_required=True)
    def do_ls(self, args):
        dirpath = "" if not args.dirpath else args.dirpath
        if dirpath == "/":
            dirpath = ""
        cursor = None
        while True:
            entries, cursor = self.ls(dirpath, recursive=args.recursive, cursor=cursor)
            for entry in entries:
                if isinstance(entry, dropbox.files.DeletedMetadata):
                    continue
                self.print_result(entry, args)

            if cursor is None:
                break

        return 0

    def ls(self, dirpath, recursive=False, cursor=None):
        """List files in current remote directory

        Returns:
            A list of file/directory names in strings under the given dirpath.
            Return None if dirpath does not exist.
        """
        if cursor:
            resp = self.api_client.files_list_folder_continue(cursor)
        else:
            resp = self.api_client.files_list_folder(dirpath, recursive=recursive)

        _LOG.debug(resp)

        if resp.has_more:
            cursor = resp.cursor
        else:
            cursor = None

        return resp.entries, cursor

    def is_exists(self, filepath):
      try:
          resp = self.api_client.metadata(filepath)
          _LOG.debug(resp)
          return not resp.get('is_deleted')
      except rest.ErrorResponse as e:
          if e.status == 404:
              return False
          raise

    @command(login_required=False)
    def do_login(self):
        self.login()

    def login(self):
        """log in to a Dropbox account"""
        flow = oauth.DropboxOAuth2FlowNoRedirect(self.app_key, self.app_secret)
        authorize_url = flow.start()
        _PLAIN_LOGGER.info("1. Go to: " + authorize_url + "\n")
        _PLAIN_LOGGER.info("2. Click \"Allow\" (you might have to log in first).\n")
        _PLAIN_LOGGER.info("3. Copy the authorization code.\n")
        code = six.moves.input("Enter the authorization code here: ").strip()

        try:
            oauth_result = flow.finish(code)
            access_token, user_id = oauth_result.access_token, oauth_result.user_id
            _LOG.debug("User id is %s", user_id)
        except rest.ErrorResponse, e:
            _PLAIN_LOGGER.error('Error: %s', e)
            return

        with open(DROPBOX_TOKEN_FILE, 'w') as f:
            f.write('oauth2:' + access_token)
        _LOG.info(
            "The access token is written to the file %s",
            DROPBOX_TOKEN_FILE,
        )
        self.api_client = dropbox.Dropbox(access_token)
        _LOG.debug("Client info: %s", self.api_client.users_get_current_account())

    @command(login_required=True)
    def do_copydir(self, args):
        try:
            self.copydir(args.from_path, args.to_path)
            return 0
        except IOError as e:
            _PLAIN_LOGGER.error("%s", e)
            return 1

    def copydir(self, src_dir, dest_dir):
      # create dest dir
      src_dir = src_dir.rstrip('/')

      if not self.is_exists(dest_dir):
          raise IOError("Dest dir [%s] does not exist!" % dest_dir)
          return

      dest_dir = os.path.join(dest_dir, os.path.basename(src_dir))
      sys.stdout.write("dest: " + dest_dir + "\n")

      if not self.is_exists(dest_dir):
        self.prompt("Do you want to create directory [%s]?" % dest_dir)
        self.mkdir(dest_dir)

      # do the copying
      for root, dirs, files in os.walk(src_dir):
        for f in files:
          src_filepath = os.path.join(root, f)
          dest_filepath = os.path.join(dest_dir, src_filepath[len(src_dir):].lstrip('/'))
          sys.stdout.write("put %s to %s\n" % (src_filepath, dest_filepath))
          self.put(src_filepath, dest_filepath)
        for d in dirs:
          src_filepath = os.path.join(root, d)
          dest_filepath = os.path.join(dest_dir, src_filepath[len(src_dir):].lstrip('/'))
          sys.stdout.write("mkdir %s\n" % dest_filepath)
          self.mkdir(dest_filepath)

    @command()
    def do_get(self, args):
        if args.to_path:
            to_path = args.to_path
        else:
            to_path = os.path.join('.', os.path.basename(args.from_path))

        self.get(args.from_path, to_path)
        return 0

    def get(self, from_path, to_path):
        """
        Copy file from Dropbox to local file and print out the metadata.

        Examples:
        sorno_dropbox.py get file.txt ~/dropbox-file.txt
        """
        metadata = self.api_client.files_download_to_file(
            to_path,
            from_path,
        )

        _PLAIN_LOGGER.info(
            'Metadata: %s',
            pprint.pformat(self.metadata_to_dict(metadata)))

    @command()
    def do_mkdir(self, args):
        self.mkdir(args.dirpath)
        return 0

    def mkdir(self, dirpath):
        """create a new directory"""
        self.api_client.file_create_folder(dirpath)

    @command()
    def do_put(self, args):
        self.put(args.from_path, args.to_path, overwrite=args.overwrite)
        return 0

    def put(self, from_path, to_path, overwrite=False):
        """Copy local file to Dropbox

        Examples:
        sorno_dropbox.py put ~/test.txt dropbox-copy-test.txt
        """
        with open(from_path, "rb") as from_file:
            if overwrite:
                writemode = dbfiles.WriteMode.overwrite
            else:
                writemode = dbfiles.WriteMode.add
            self.api_client.files_upload(
                from_file,
                to_path,
                mode=writemode,
            )

    @command(login_required=True)
    def do_search(self, args):
        dirpath = "" if not args.dirpath else args.dirpath
        start = 0
        while True:
            results, start = self.search(dirpath, args.query, start=start)
            for r in results:
                metadata = r.metadata
                self.print_result(r.metadata, args)

            if not start:
                break

        return 0

    def search(self, dirpath, query, start=None):
        if start is not None:
            result = self.api_client.files_search(dirpath, query, start=start)
        else:
            result = self.api_client.files_search(dirpath, query)

        start = None
        if result.more:
            start = result.start
        return result.matches, start

    def prompt(self, msg):
        ans = six.moves.input(msg)
        if ans.lower() in ('y', 'yes'):
            return
        else:
            raise Exception("aborted!")

    def metadata_to_dict(self, metadata):
        return {n: getattr(metadata, n) for n in metadata._all_field_names_}

    def print_result(self, metadata, args):
        s = ""
        if args.detail:
            s += pprint.pformat(self.metadata_to_dict(metadata))
        if args.print_full_path:
            if s:
                s += "\n"
            s += metadata.path_display
        if not s:
            s = metadata.name
        if args.print_size and not args.detail and isinstance(metadata, dropbox.files.FileMetadata):
            s += "\t" + humanize.naturalsize(metadata.size)
        if args.output_buffer:
            # the following comes from the StreamHandler.emit method in the
            # logging module
            if isinstance(s, unicode):
                try:
                    if sys.stdout.encoding:
                        print(s.encode(sys.stdout.encoding))
                    else:
                        print(s)
                except UnicodeEncodeError:
                    print(s.encode("utf8"))
            else:
                print(s)
        else:
            _PLAIN_LOGGER.info(s)


def parse_args(app_obj, cmd_args):
    description = __doc__.split("Copyright 2014")[0].rstrip()
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--debug",
        action="store_true",
    )

    subparsers = parser.add_subparsers(
        title="Commands",
    )

    #
    # parser_ls
    #

    ls_help = "List the content of a directory"
    parser_ls = subparsers.add_parser(
        "ls",
        help=ls_help,
        description=ls_help,
    )
    parser_ls.add_argument(
        "dirpath",
        nargs="?",
        help="The path of the directory in dropbox. For the root directory,"
        " use an empty string",
    )
    parser_ls.add_argument(
        "--detail",
        help="If true, the whole details of the results are printed out",
        action="store_true",
    )
    parser_ls.add_argument(
        "--recursive",
        help="If true, recursively list all content",
        action="store_true",
    )
    parser_ls.add_argument(
        "--print-full-path",
        help="If true, print the full path of each content",
        action="store_true",
    )
    parser_ls.add_argument(
        "--print-size",
        help="Print the full path of the result",
        action="store_true",
    )
    parser_ls.add_argument(
        "--buffer",
        help="Buffer the output",
        action="store_true",
        dest="output_buffer",
    )
    parser_ls.set_defaults(func=app_obj.do_ls)

    #
    # parser_copydir
    #

    copydir_help = "Copy a directory to dropbox recursively"
    parser_copydir = subparsers.add_parser(
        "copydir",
        help=copydir_help,
        description=copydir_help,
    )
    parser_copydir.add_argument(
        "from_path",
    )
    parser_copydir.add_argument(
        "to_path",
    )
    parser_copydir.set_defaults(func=app_obj.do_copydir)

    #
    # parser_get
    #

    get_help = (
        """
        Copy file from Dropbox to local file and print out the metadata.

        Examples:
        get file.txt ~/dropbox-file.txt
        """
    )
    parser_get = subparsers.add_parser(
        "get",
        help=get_help,
        description=get_help,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser_get.add_argument(
        "from_path",
        help="The location in dropbox",
    )
    parser_get.add_argument(
        "to_path",
        nargs="?",
        help=re.sub(
            r"\s+",
            " ",
            """
            The local path. If if you skip this, the filename of the from_path
            is used instead and will be downloaded to your current directory.
            """,
        ).strip(),
    )

    parser_get.set_defaults(func=app_obj.do_get)

    #
    # parser_put
    #

    put_help = (
        "Copy. Examples: put ~/test.txt dropbox-copy-test.txt"
    )
    parser_put = subparsers.add_parser(
        "put",
        help=put_help,
        description=put_help,
    )
    parser_put.add_argument(
        "from_path",
        help="The local path",
    )
    parser_put.add_argument(
        "to_path",
        help="The location in dropbox",
    )
    parser_put.add_argument(
        "--overwrite",
        help="Overwrite the existing file or not. If false, a file"
        " with a new name is created instead of the specified name"
        " in to_path",
        action="store_true",
    )
    parser_put.set_defaults(func=app_obj.do_put)

    #
    # parser_search
    #

    search_help = "Search in dropbox"
    parser_search = subparsers.add_parser(
        "search",
        help=search_help,
        description=search_help,
    )
    parser_search.add_argument(
        "--dirpath",
        help="The directory to e searched from. By default it searches from"
            + " the root."
    )
    parser_search.add_argument(
        "--detail",
        help="If true, the whole details of the results are printed out",
        action="store_true",
    )
    parser_search.add_argument(
        "--print-full-path",
        help="Print the full path of the result",
        action="store_true",
    )
    parser_search.add_argument(
        "--print-size",
        help="Print the full path of the result",
        action="store_true",
    )
    parser_search.add_argument("query")
    parser_search.set_defaults(func=app_obj.do_search)

    args = parser.parse_args(cmd_args)
    return args


def main():
    global _PLAIN_LOGGER

    app = DropboxApp(
        DROPBOX_APP_KEY or os.getenv('DROPBOX_APP_KEY'),
        DROPBOX_APP_SECRET or os.getenv('DROPBOX_APP_SECRET'),
    )
    args = parse_args(app, sys.argv[1:])

    loggingutil.setup_logger(_LOG, debug=args.debug)
    _PLAIN_LOGGER = loggingutil.create_plain_logger(
        "PLAIN",
        debug=args.debug,
    )
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
