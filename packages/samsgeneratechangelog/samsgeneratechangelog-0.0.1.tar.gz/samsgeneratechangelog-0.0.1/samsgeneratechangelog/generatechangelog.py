import os
import re
from datetime import date
import logging
from jinja2 import Template
from .githelper import GitHelper

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATES_DIR = os.path.sep.join([MODULE_DIR, 'templates'])

class GenerateChangelog:
    """
    Generate a changelog by rendering a simple but flexible CommitFile object using jinja2

    Parameters:
        start_ref (string): The commit sha or git ref (tag/head/etc) that the comparison will start from
        end_ref (string): The commit sha or git ref (tag/head/etc) that the comparison will end at
        header_text (string): The text that appears in the header of the template
        git_path (string): The path (relative to the cwd or absolute) that contains the `.git` folder
        template_file (string): The path (relative to the cwd or absolute) to a custom jinja2 template file
        template_name (string): The name of one of the templates bundled with the SamsGenerateChangelog package
        custom_attributes (dict): A dictionary of of custom attributes to make available under each file object in the template
    """
    templates_requiring_custom_attributes = [
        'jira_id_all_commits',
        'jira_id_by_change_type',
        'root_folder_all_commits'
    ]

    def __init__(self, start_ref, end_ref, header_text, git_path='.',
                 custom_attributes=None, template_file=None,
                 template_name='default'):
        self.start_ref = start_ref
        self.end_ref = end_ref
        self.header_text = header_text
        self.git_path = git_path
        self.custom_attributes = custom_attributes
        self.template_file = self._get_template_file(
            template_file, template_name)
        self.git_helper = GitHelper(
            self.git_path,
            self.custom_attributes
        )

    @classmethod
    def get_template_names(cls):
        """ Returns a list of valid template names """
        return [
            os.path.splitext(file_name)[0]
            for file_name in os.listdir(TEMPLATES_DIR) 
            if os.path.isfile(os.path.join(TEMPLATES_DIR, file_name))
        ]

    def _get_template_file(self, template_file, template_name):
        if template_file:
            return template_file
        if template_name in self.templates_requiring_custom_attributes and not self.custom_attributes:
            raise ValueError(
                f'{template_name} requires a custom attribute specification to be provided, please consult the documentation')
        return self._get_module_template_path(template_name)

    @staticmethod
    def _get_module_template_path(template_name):
        file_path = os.path.sep.join([TEMPLATES_DIR, f'{template_name}.j2'])
        if not os.path.isfile(file_path):
            raise ValueError(
                f"{template_name} is not a template bundled with this version of Sam's Generate Changelog")
        return file_path

    def render_markdown(self):
        """ Return the rendered markdown provided by the template """
        return self._get_markdown_template().render(
            start_ref=self.start_ref,
            end_ref=self.end_ref,
            header_text=self.header_text,
            file_commits=self.git_helper.commit_log(
                self.start_ref, self.end_ref)
        )

    def _get_markdown_template(self):
        with open(self.template_file) as reader:
            return Template(reader.read())
