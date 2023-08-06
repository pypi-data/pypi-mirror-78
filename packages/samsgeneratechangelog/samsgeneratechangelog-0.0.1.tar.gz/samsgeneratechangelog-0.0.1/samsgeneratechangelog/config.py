import os
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
        choices=['print'],
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
        default='author_all_commits',
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
        '--log-level',
        required=False,
        default='WARN',
        choices=['ERROR', 'WARN', 'INFO', 'DEBUG'],
        help='Log level'
    )
    return parser
