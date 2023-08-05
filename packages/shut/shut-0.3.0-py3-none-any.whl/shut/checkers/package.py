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

import os
from typing import Iterable, Optional

from shut.model import MonorepoModel, PackageModel, Project
from shut.utils.external.classifiers import get_classifiers
from .core import CheckResult, CheckStatus, Checker, SkipCheck, check, register_checker


class PackageChecker(Checker[PackageModel]):

  @check('readme')
  def _check_readme(self, project: Project, package: PackageModel) -> Iterable[CheckResult]:
    if not package.get_readme_file():
      yield CheckResult(CheckStatus.WARNING, 'No README file found.')

  @check('license')
  def _check_license(self, project: Project, package: PackageModel) -> Iterable[CheckResult]:
    if not package.license:
      yield CheckResult(CheckStatus.WARNING, 'not specified')

    elif package.license and not package.get_license_file():
      yield CheckResult(CheckStatus.WARNING, 'No LICENSE file found.')

    monorepo = project.monorepo
    if package.license and monorepo and monorepo.license \
        and monorepo.license != package.license:
      yield CheckResult(CheckStatus.ERROR,
        'License is not consistent with parent mono repository (package: {}, monorepo: {}).'
          .format(package.license, monorepo.license))

  @check('classifiers')
  def _check_classifiers(self, project: Project, package: PackageModel) -> Iterable[CheckResult]:
    classifiers = get_classifiers()
    unknown_classifiers = [x for x in package.classifiers if x not in classifiers]
    if unknown_classifiers:
      yield CheckResult(
        CheckStatus.WARNING,
        'Unknown classifiers: ' + ', '.join(unknown_classifiers))

  @check('author')
  def _check_author(self, project: Project, package: PackageModel) -> Iterable[CheckResult]:
    if not package.author:
      yield CheckResult(CheckStatus.WARNING, 'missing')

  @check('url')
  def _check_author(self, project: Project, package: PackageModel) -> Iterable[CheckResult]:
    if not package.url:
      yield CheckResult(CheckStatus.WARNING, 'missing')

  @check('consistent-author')
  def _check_consistent_author(self, project: Project, package: PackageModel) -> Iterable[CheckResult]:
    metadata = package.get_python_package_metadata()
    if package.author and metadata.author != str(package.author):
      yield CheckResult(
        CheckStatus.ERROR,
        'Inconsistent package author (package.yaml: {!r} != {}: {!r})'.format(
          str(package.author), metadata.filename, metadata.author))

  @check('consistent-version')
  def _check_consistent_version(self, project: Project, package: PackageModel) -> Iterable[CheckResult]:
    metadata = package.get_python_package_metadata()
    if package.version and metadata.version != str(package.version):
      yield CheckResult(
        CheckStatus.ERROR,
        '{!r} ({}) != {!r} ({})'.format(
          str(package.version),
          os.path.basename(package.filename),
          metadata.version,
          os.path.relpath(metadata.filename)))

  @check('typed')
  def _check_typed(self, project: Project, package: PackageModel) -> Iterable[CheckResult]:
    metadata = package.get_python_package_metadata()
    try:
      py_typed_file = os.path.join(metadata.package_directory, 'py.typed')
    except ValueError:
      if package.typed:
        yield CheckResult(
          CheckStatus.WARNING,
          '$.package.typed only works with packages, but this is a module')
    else:
      if os.path.isfile(py_typed_file) and not package.typed:
        yield CheckResult(
          CheckStatus.WARNING,
          'file "py.typed" exists but $.typed is not set')
    yield SkipCheck()


register_checker(PackageModel, PackageChecker)
