# Copyright 2020 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Set environment for releasing pip package.

Warning: This script will overwrite config: ~/.pypirc
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os

FILE_TEMPLATE = """
[distutils]
  index-servers =
    pypi
    tflite-model-maker

[pypi]
  username = __token__
  password = {password}

"""

RC_FILE = os.path.expanduser('~/.pypirc')
PASSWORD = '<PLACEHOLDER>'  # TODO(tianlin): replace this with kokoro keystore.


def write_rc_file(password):
  """Writes rc file."""
  with open(RC_FILE, 'w') as f:
    rc = FILE_TEMPLATE.format(password=password)
    f.write(rc)


def main():
  write_rc_file(PASSWORD)


if __name__ == '__main__':
  main()
