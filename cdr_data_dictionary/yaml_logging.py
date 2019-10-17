"""
Set up logging for the modules involved in yaml file geneation.
"""
# Python imports
import logging
import os

# Third party imports

# Project imports

def setup_logging(args):
    """
    Logging setup for the cdr_data_dictionary package.

    :param args:  The command line arguments.  Of interest are the desired
        log file path and whether to add a console logging handler.
    """
    try:
        os.makedirs(os.path.dirname(args.log_path))
    except OSError:
        # path already exists.  moving on.
        pass

    format_string = '%(levelname) - 10s %(asctime)s - %(name)s - %(message)s'
    logging.basicConfig(level=logging.INFO,
                        filename=args.log_path,
                        format=format_string,
                        datefmt='%Y-%m-%d %H:%M',
                        filemode='a')

    if args.console_log:
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console_format = '%(levelname) - 10s %(name)s - %(message)s'
        formatter = logging.Formatter(console_format)
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
