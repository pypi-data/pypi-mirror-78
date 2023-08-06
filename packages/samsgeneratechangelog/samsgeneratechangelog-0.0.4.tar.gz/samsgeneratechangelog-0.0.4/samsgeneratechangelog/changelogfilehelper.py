""" Helpers to aid in the manipulation of changelog files """
import re
import logging


class ChangelogFileHelper:
    """ A class to help idempotently update changelog files """
    markdown_comment_syntax = '[//]: # ({comment_value})'

    def __init__(self, file_path):
        self.file_path = file_path

    def write_entry(self, entry, entry_id):
        """ Write the entry to the beginning of the changelog, or replace an existing
        entry if one exists with this entry id """
        if self._has_existing_entry(entry_id):
            logging.debug(f"Found existing changelog entry for {entry_id} in {self.file_path}, replacing it.")
            new_contents = self._replace_existing_entry(entry, entry_id)
        else:
            new_contents = self._prepend_entry(entry, entry_id)
        self._overwrite_file(new_contents)

    def _has_existing_entry(self, entry_id):
        """ Does a changelog entry delimited with this entry_id exist in the file already? """
        file_content = self._get_file_contents()
        pattern = self._get_pattern_to_match_existing_changelog_entry(entry_id)
        return re.search(pattern, file_content)

    def _delimit_entry(self, entry, entry_id):
        """ Wrap the entry in a markdown comment to delimit its start and end so we can
        replace it later if need be """
        entry_delimiter = self._generate_entry_delimiter(entry_id)
        return f"{entry_delimiter}\n{entry}\n{entry_delimiter}"

    def _prepend_entry(self, entry, entry_id):
        """ Add the (delimited) entry to the beginning of the existing file contents """
        file_content = self._get_file_contents()
        return f'{self._delimit_entry(entry, entry_id)}\n\n{file_content}'

    def _replace_existing_entry(self, entry, entry_id):
        """ Replace all text delimited by entry_id delimiter
        in string with repl

        Parameters:
            entry (str): The replacement entry
            entry_id (str): The ID to use as a delimiter for the changelog entry (usually semantic version number)
        """
        file_content = self._get_file_contents()
        pattern = self._get_pattern_to_match_existing_changelog_entry(entry_id)
        return re.sub(pattern, self._delimit_entry(entry, entry_id), file_content)

    def _get_pattern_to_match_existing_changelog_entry(self, entry_id):
        entry_delimiter = self._generate_entry_delimiter(entry_id)
        escaped_entry_delimiter = re.escape(entry_delimiter)
        return re.compile(f'{escaped_entry_delimiter}.*?{escaped_entry_delimiter}', re.DOTALL)

    def _generate_entry_delimiter(self, entry_id):
        """ Generate a markdown comment that will serve as a delimiter
        that denotes the start and end of a changelog entry """
        return self.markdown_comment_syntax.format(
            comment_value=f"SamsGenerateChangelog-{entry_id}"
        )

    def _get_file_contents(self):
        try:
            with open(self.file_path, 'r+') as file:
                return file.read()
        except IOError:
            return ''

    def _overwrite_file(self, contents):
        with open(self.file_path, 'w') as file:
            file.write(contents)
