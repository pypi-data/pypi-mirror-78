"""Container for commandline entrypoints."""
import logging
from .generatechangelog import GenerateChangelog
from .config import arg_parser, arg_variable_to_dict


def main():
    """Entry point for gcs commandline."""
    args = arg_parser().parse_args()
    logging.basicConfig(level=args.log_level.upper())
    parameters = {
        param: getattr(args, param)
        for param in [
            'start_ref',
            'end_ref',
            'git_path',
            'custom_attributes',
            'template_file',
            'template_name'
        ]
    }
    parameters['template_variables'] = arg_variable_to_dict(args.var)
    gc = GenerateChangelog(**parameters)

    if args.verb.lower() == 'print':
        print(gc.render_markdown())

    if args.verb.lower() == 'save':
        gc.render_markdown_to_file(
            file_path=args.output_file,
            entry_id=args.entry_id
        )
