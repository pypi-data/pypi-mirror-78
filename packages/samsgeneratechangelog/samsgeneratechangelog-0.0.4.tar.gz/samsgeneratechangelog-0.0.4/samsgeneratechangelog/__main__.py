import logging
from .generatechangelog import GenerateChangelog
from .config import arg_parser


def main():
    args = arg_parser().parse_args()
    logging.basicConfig(level=args.log_level.upper())
    parameters = {
        param: getattr(args, param)
        for param in [
            'start_ref',
            'end_ref',
            'header_text',
            'git_path',
            'custom_attributes',
            'template_file',
            'template_name'
        ]
    }
    gc = GenerateChangelog(**parameters)

    if args.verb.lower() == 'print':
        print(gc.render_markdown())

    if args.verb.lower() == 'save':
        gc.render_markdown_to_file(
            file_path=args.output_file,
            entry_id=args.entry_id
        )
