# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## Unreleased

## [1.0.0] - 2020-09-01

- Dropped support for Python 2.7 and 3.4 (#10, #12).
- Updated civisquery magic to support database names with spaces (#10).
- Better document civisquery magic (#10).
- Relaxed requirements on ``pandas`` so that any version >0.20 is also allowed (#11).

## [0.1.3] - 2017-11-28

### Fixed
- Fixed an issue where databases with spaces in their names could not be used
  the line magic splits on spaces. It now splits on semicolons. (#8)
- Relaxed requirements on ``pandas`` so that minor versions >0.20 are also allowed (#9).

## [0.1.2] - 2017-09-20

### Fixed
- Fixed an issue in requirements.txt that was causing problems with setuptools
  (#5).

## [0.1.1] - 2017-09-13

### Fixed
- Relaxed requirement markers for Python 2 packaging (#3).

## [0.1.0] - 2017-09-08

### Added
- Initial commit.
