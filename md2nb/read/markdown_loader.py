# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.

import html2md
import jinja2
import os

from . import github_samples


class MarkdownLoader(jinja2.BaseLoader):
  def __init__(self, searchpath='.'):
    self.searchpath = searchpath

  def get_source(self, env, name):
    path = os.path.join(self.searchpath, name)
    if not os.path.exists(path):
      raise jinja2.TemplateNotFound(path)

    mtime = os.path.getmtime(path)
    with open(path) as f:
      source = html2md.convert(f.read())
    source = github_samples(source)
    return source, path, lambda: mtime == os.path.getmtime(path)