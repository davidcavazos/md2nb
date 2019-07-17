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

import unittest

from . import imports


class ImportsTest(unittest.TestCase):
  def test_imports_at_start(self):
    actual = list(imports(
        sections=[['# section 1'], ['# section 2']],
        imports={
            0: [['# title', 'start', '# subtitle']],
            1: [['# section 1.1']],
        },
    ))
    expected = [
        ['# title', 'start'],
        ['# subtitle'],
        ['# section 1'],
        ['# section 1.1'],
        ['# section 2'],
    ]
    self.assertEqual(actual, expected)

  def test_imports_at_end(self):
    actual = list(imports(
        sections=[['# section 1'], ['# section 2']],
        imports={
            -1: [['# pre-end', ':)', '# end']],
            -2: [['# section 1.1']],
        },
    ))
    expected = [
        ['# section 1'],
        ['# section 1.1'],
        ['# section 2'],
        ['# pre-end', ':)'],
        ['# end'],
    ]
    self.assertEqual(actual, expected)

  def test_imports_file(self):
    actual = list(imports(
        sections=[['# section 1'], ['# section 2']],
        imports={
            0: ['examples/templates/title.md'],
            -1: ['examples/templates/cleanup.md'],
        },
        variables={'title': 'Title'},
    ))
    expected = [
        ['# Title'],
        ['# section 1'],
        ['# section 2'],
        ['## Clean up', "You're all done 🎉🎉"]
    ]
    self.assertEqual(actual, expected)