"""Utilities to deal with Git
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import git

def get_config_reader(filepath):
  """Gets an instance of GitConfigParser

  https://github.com/gitpython-developers/GitPython/blob/77e47bc313e42f9636e37ec94f2e0b366b492836/git/config.py#L194
  """
  return git.Repo(filepath).config_reader()

def get_sections(filepath):
  """Gets the sections from git config."""
  reader = get_config_reader(filepath)
  sections = {}
  for sec_name in reader.sections():
    sections[sec_name] = reader.items_all(sec_name)

  return sections

def get_remote_urls(filepath):
  sections = get_sections(filepath)

  urls = []
  for sec, section in sections.items():
    if sec.startswith("remote"):
      for option, values in section:
        if option == 'url':
          urls.extend(values)

  return urls

def get_remote_urls_safe(filepath):
  """Safe version of get_remote_urls

  Just like get_remote_urls but returns an empty list of
  urls instead ot throwing an error if the file path is not a git repo.

  Let's say "~/py-ws/sorno-py-scripts" is a legit git repo:

  print(get_remote_urls_safe(os.path.expanduser('~/py-ws/sorno-py-scripts')))
  print(get_remote_urls_safe(os.path.expanduser('~/py-ws')))
  print(get_remote_urls_safe(os.path.expanduser('~/blah')))

  Output:
  ['https://github.com/hermantai/sorno-py-scripts.git']
  []
  []
  """

  try:
    return get_remote_urls(filepath)
  except git.exc.InvalidGitRepositoryError:
    return []
  except git.exc.NoSuchPathError:
    return []
