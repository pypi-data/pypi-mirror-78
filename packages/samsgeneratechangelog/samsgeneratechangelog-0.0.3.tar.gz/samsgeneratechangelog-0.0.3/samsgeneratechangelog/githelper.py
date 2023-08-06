"""
A series of helper classes for dealing with pygit
"""
import os
import re
import logging
import time
import json
import git
from datetime import datetime
from .decorators import DebugOutput


class FileCommit():
    """ A single file changed by a commit

    Parameters:
        commit (Commit): The :class:`~git.objects.commit.Commit` that this file was changed in
        file_path (str): The path of the file that was changed relative to the root of the repo
        change_type (str): The single character change type
        repo (Repo): The :class:`~git.repo.base.Repo` that the commit is from
        custom_attributes (dict): A dictionary of custom attributes with the attribute name as the key, and subkeys of `pattern` and `derived_from`

    Attributes:
        commit (Commit): The :class:`~git.objects.commit.Commit` object for this commit
        author (Actor): The :class:`~git.util.Actor` object that authored the commit. Contains :attr:`email` and :attr:`name` attributes
        author_date (datetime): Date authored
        committer (str): Committer
        hexsha (str): Long form commit sha
        message (str): The commit message
        file_path (str): The path to the file which was changed (relative to the root of the repo)
        friendly_change_type (str): The type of change that happend to this file.
    """

    def __init__(self, commit, file_path, change_type, repo, custom_attributes=None):
        change_types = {'A': 'Added', 'M': 'Modified',
                        'D': 'Deleted', 'R': 'Renamed', 'T': 'Type Change'}
        self.commit = commit
        self.file_path = file_path
        self.change_type = change_type
        self._generate_custom_attributes(custom_attributes or {})
        self.friendly_change_type = change_types.get(
            change_type,
            'Unknown change type'
        )
        self._hexsha_short = None

    @property
    def hexsha_short(self):
        """ Short version of the commit sha 
        
        Returns: 
            str
        """
        if not self._hexsha_short:
            self._hexsha_sort = self.repo.git.rev_parse(self.hexsha, short=7)
        return self._hexsha_sort

    @property
    def committed_date(self):
        """ Get a python datetime object of the committed date 
        
        Returns: 
            datetime
        """
        return datetime.fromtimestamp(self.commit.committed_date)

    def __getattr__(self, attr):
        """ Return the value from the commit object if the attribute
        was one of FileCommit's directly """
        return getattr(self.commit, attr)

    def _generate_custom_attributes(self, custom_attributes):
        for attr, attribute_spec in custom_attributes.items():
            logging.debug(f"Getting custom attribute {attr} from commit"
                        f"using {attribute_spec['pattern']} against {attribute_spec['derived_from']}")
            derived_from = getattr(self, attribute_spec['derived_from'])
            derived_from = derived_from or getattr(self.commit, attribute_spec['derived_from'])
            match = re.search(
                attribute_spec['pattern'],
                derived_from,
                re.IGNORECASE
            )
            setattr(self, attr, match[0] if match else '')

    def __repr__(self):
        return f"FileCommit({self.commit}, {self.file_path}, {self.change_type})"


class GitHelper:
    """
    Helper class to facilitate in diffing and organising commits

    Parameters:
        path (string): Path to the folder containing the git repo
        custom_attributes (dict): A dictionary of custom attributes with the attribute name as the key, and subkeys of `pattern` and `derived_from`

    """

    def __init__(self, path, custom_attributes=None):
        logging.debug(f'Using git repo {path}')
        self.repo = git.Repo(path or os.path.dirname(
            os.path.realpath(__file__)
        ))
        self.git = self.repo.git
        self.custom_attributes = custom_attributes

    def commit_log(self, rev_a, rev_b):
        """ Get commit objects for every commit between
        rev_a and rev_b """
        commit_ids = self.git.log(
            '--pretty=%H', f"{rev_a}...{rev_b}").split('\n')
        for commit_id in commit_ids:
            commit = self.repo.commit(commit_id)
            for file_commit in self.generate_file_commits_from_commit(commit):
                yield file_commit

    def generate_file_commits_from_commit(self, commit):
        """ Returns a list of FileCommit objects that represent a file changed
        by the commit as well as the change type and all other commit metadata """
        # TODO: Support generating list of files added from first commit (i.e. commit without parents)
        diff_to_parent = commit.parents[0].diff(commit)
        for change_type in diff_to_parent.change_type:
            for change in diff_to_parent.iter_change_type(change_type):
                yield FileCommit(
                    commit,
                    change.b_path,
                    change_type,
                    self.repo,
                    self.custom_attributes
                )
