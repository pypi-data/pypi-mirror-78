import sys
import json
import configargparse
from .generatechangelog import GenerateChangelog


def arg_parser():
    parser = configargparse.ArgParser(
        default_config_files=['sgc.conf'],
        description="Generate change log in Markdown"
    )
    parser.add(
        'verb',
        choices=['print', 'save'],
        default='print'
    )
    parser.add(
        '--config-file',
        required=False,
        env_var='SGC_config_file',
        help='The path to an sgc.conf file'
    )
    parser.add(
        '--start-ref',
        env_var='SGC_start_ref',
        required=True,
        help='The commit sha or git ref (tag/head/etc) that the comparison will start from'
    )
    parser.add(
        '--end-ref',
        env_var='SGC_end_ref',
        required=True,
        help='The commit sha or git ref (tag/head/etc) that the comparison will end at'
    )
    parser.add(
        '--header-text',
        env_var='SGC_header_text',
        required=True,
        help='The text that appears in the header of the template'
    )
    parser.add(
        '--git-path',
        required=False,
        default='.',
        env_var='SGC_git_path',
        help='The path (relative to the cwd or absolute) that contains the `.git` folder'
    )
    parser.add(
        '--template-file',
        required=False,
        default=None,
        help='The path (relative to the cwd or absolute) to a custom jinja2 template file'
    )
    parser.add(
        '--template-name',
        required=False,
        default='author_by_change_type',
        env_var='SGC_template_name',
        help='The name of one of the templates bundled with the SamsGenerateChangelog package',
        choices=GenerateChangelog.get_template_names(),
    )
    parser.add(
        '--custom-attributes',
        required=False,
        env_var='SGC_custom_attributes',
        help='A JSON dictionary of of custom attributes to make available under each file object in the template',
        type=json.loads
    )
    parser.add(
        '--output-file',
        required='save' in sys.argv,
        env_var='SGC_output_file',
        help='The path to a changelog file to update',
    )
    parser.add(
        '--entry-id',
        required='save' in sys.argv,
        env_var='SGC_entry_id',
        help='An ID unique to this changelog entry that can be used to '
        'update it in future if required (normally the semantic version)',
    )

    parser.add(
        '--log-level',
        required=False,
        default='WARN',
        choices=['ERROR', 'WARN', 'INFO', 'DEBUG'],
        help='Log level'
    )
    return parser
