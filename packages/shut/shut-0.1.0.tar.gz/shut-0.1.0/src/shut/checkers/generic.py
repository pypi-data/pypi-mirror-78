# -*- coding: utf8 -*-
# Copyright (c) 2020 Niklas Rosenstein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

from .core import CheckResult, CheckStatus, Checker, check, register_checker
from shut.model import AbstractProjectModel, Project
from typing import Iterable, Optional, Union


class GenericChecker(Checker):

  @check('unknown-config')
  def _check_unknown_keys(
    self,
    project: 'Project',
    obj: Union['MonorepoModel', 'PackageModel'],
  ) -> Iterable[CheckResult]:
    yield CheckResult(
      CheckStatus.WARNING if obj.unknown_keys else CheckStatus.PASSED,
      ', '.join(map(str, obj.unknown_keys)) if obj.unknown_keys else None)


register_checker(AbstractProjectModel, GenericChecker)

