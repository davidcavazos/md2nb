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

import jinja2
import md2nb
import nbformat

DEFAULT_KERNEL = 'python3'


def new_notebook(
    input_file,
    variables=None,
    imports=None,
    notebook_title=None,
    lang=None,
    lang_shell=None,
    docs_url=None,
    docs_logo_url=None,
    github_ipynb_url=None,
    kernel=None,
    steps=None,
    jinja_env=None,
):

  sections = md2nb.read.sections(input_file, variables, jinja_env)
  paragraphs = md2nb.apply(sections, [
      (md2nb.steps.imports, imports, variables, jinja_env),
      md2nb.steps.flatten,
      (md2nb.steps.lang, lang, lang_shell)
  ])
  paragraphs = md2nb.apply(paragraphs, steps)
  cells = list(md2nb.apply(paragraphs, [
      md2nb.steps.paragraphs_to_cells,
      (md2nb.steps.view_the_docs, docs_url, docs_logo_url),
      (md2nb.steps.open_in_colab, github_ipynb_url),
  ]))

  for cell in cells:
    if notebook_title:
      break
    first_line = cell.source.splitlines()[0]
    if first_line.startswith('#'):
      notebook_title = first_line.strip('# ')

  # Create the notebook with all the cells.
  if not kernel:
    kernel = DEFAULT_KERNEL
  metadata = {
    'colab': {"toc_visible": True},
    'kernelspec': {'name': kernel, 'display_name': kernel},
  }
  if notebook_title:
    metadata['colab']['name'] = notebook_title

  return nbformat.v4.new_notebook(cells, metadata=metadata)