
# Sam's Changelog Generator

Yet another changelog generator!

Sam’s Changelog Generator focusses on making it easy to group information about your commits by `author_date`, `author`, `file_path`, `friendly_change_type`, and more importantly, custom attributes!

This makes it easy to generate a changelog that’s as simple as a list of all commits/files that changed, or as complicated as a list of Python files changed grouped by module and then grouped by author with their last changed date.

# Documentation

For full documentation go to [ReadTheDocs](https://sams-generate-changelog.readthedocs.io/en/latest/).

# Installation

```
pip install samsgeneratechangelog
```

# Usage

## Command

```
$ sgc print --start-ref HEAD~3 --end-ref HEAD --header-text 0.0.1
```

## Outputs

```
# 0.0.1

## Sam Martin's Files

- docs/Makefile - e77a106 - 2020-09-02 10:00:21 - Modified
- docs/source/class-reference.rst - e77a106 - 2020-09-02 10:00:21 - Modified
- samsgeneratechangelog/__init__.py - ecc3de1 - 2020-09-02 11:26:13 - Modified
- samsgeneratechangelog/__init__.py - e77a106 - 2020-09-02 10:00:21 - Modified
- samsgeneratechangelog/__main__.py - ecc3de1 - 2020-09-02 11:26:13 - Modified
- samsgeneratechangelog/config.py - ecc3de1 - 2020-09-02 11:26:13 - Modified
- samsgeneratechangelog/config.py - d83b45e - 2020-09-02 10:15:51 - Modified
- samsgeneratechangelog/generatechangelog.py - ecc3de1 - 2020-09-02 11:26:13 - Modified
- samsgeneratechangelog/generatechangelog.py - d83b45e - 2020-09-02 10:15:51 - Modified
- samsgeneratechangelog/generatechangelog.py - e77a106 - 2020-09-02 10:00:21 - Modified
- samsgeneratechangelog/githelper.py - e77a106 - 2020-09-02 10:00:21 - Modified
- tests/fixtures/custom_template.j2 - ecc3de1 - 2020-09-02 11:26:13 - Added
- tests/test_cmdline_arguments.py - ecc3de1 - 2020-09-02 11:26:13 - Added
- tests/test_default_templates.py - ecc3de1 - 2020-09-02 11:26:13 - Modified
- tests/test_default_templates.py - d83b45e - 2020-09-02 10:15:51 - Modified
```
