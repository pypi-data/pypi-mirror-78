"""Generate a changelog from git commit history."""
import os
from jinja2 import Template
from .githelper import GitHelper
from .changelogfilehelper import ChangelogFileHelper

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATES_DIR = os.path.sep.join([MODULE_DIR, 'templates'])


class GenerateChangelog:
    """Generate a changelog by rendering a simple but flexible CommitFile object using jinja2.

    Parameters:
        start_ref (string): The commit sha or git ref (tag/head/etc) that the comparison will start from
        end_ref (string): The commit sha or git ref (tag/head/etc) that the comparison will end at
        template_variables (dict): A dict of variables to pass to Jinja's Template
        git_path (string): The path (relative to the cwd or absolute) that contains the `.git` folder
        template_file (string): The path (relative to the cwd or absolute) to a custom jinja2 template file
        template_name (string): The name of one of the templates bundled with the SamsGenerateChangelog package
        custom_attributes (dict): A dictionary of of custom attributes to make available under each file object
            in the template
    """
    _templates_requiring_custom_attributes = [
        'jira_id_all_commits',
        'jira_id_by_change_type',
        'root_folder_all_commits'
    ]

    def __init__(self, start_ref, end_ref, git_path='.', template_variables=None,
                 custom_attributes=None, template_file=None,
                 template_name='author_by_change_type'):
        """Inits GenerateChangeLog.

        Attributes:
            start_ref,
            end_ref,
            template_variables,
            git_path,
            custom_attributes,
            template_file
            git_helper
        """
        self.start_ref = start_ref
        self.end_ref = end_ref
        self.template_variables = template_variables or {}
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
        """Returns a list of valid template names."""
        return [
            os.path.splitext(file_name)[0]
            for file_name in os.listdir(TEMPLATES_DIR)
            if os.path.isfile(os.path.join(TEMPLATES_DIR, file_name))
        ]

    def _get_template_file(self, template_file, template_name):
        if template_file:
            return template_file
        if template_name in self._templates_requiring_custom_attributes and not self.custom_attributes:
            raise ValueError(
                f'{template_name} requires a custom attribute specification to be provided,'
                ' please consult the documentation'
            )
        return self._get_module_template_path(template_name)

    @staticmethod
    def _get_module_template_path(template_name):
        file_path = os.path.sep.join([TEMPLATES_DIR, f'{template_name}.j2'])
        if not os.path.isfile(file_path):
            raise ValueError(
                f"{template_name} is not a template bundled with this version of Sam's Generate Changelog")
        return file_path

    def render_markdown(self):
        """Return the rendered markdown provided by the template."""
        return self._get_markdown_template().render(
            start_ref=self.start_ref,
            end_ref=self.end_ref,
            file_commits=self.git_helper.commit_log(
                self.start_ref, self.end_ref
            ),
            **self.template_variables
        )

    def render_markdown_to_file(self, file_path, entry_id):
        """Render the markdown provided by the template and prepend it to a file.

        If an entry already exists pertaining to the current entry_id it will be overwritten.
        """
        file_helper = ChangelogFileHelper(file_path=file_path)
        entry = self.render_markdown()
        file_helper.write_entry(entry, entry_id)

    def _get_markdown_template(self):
        with open(self.template_file) as reader:
            return Template(reader.read())
