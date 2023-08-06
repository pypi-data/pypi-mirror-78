import argparse
import logging

from rsyslog_postgres_tools.commands.admin import attach_admin_command
from rsyslog_postgres_tools.commands.bootstrap import attach_bootstrap_command
from rsyslog_postgres_tools.commands.clean import attach_clean_command
from rsyslog_postgres_tools.commands.run_http_server import attach_run_http_server_command
from rsyslog_postgres_tools.commands.search import attach_search_command
from rsyslog_postgres_tools.commands.tail import attach_tail_command


argument_parser = argparse.ArgumentParser("rsyslog_postgres_tools")
argument_parser.add_argument(
    "postgres_connection_url", type=str,
    help="The postgres:// style connection URL to the database used for log storage."
)
argument_parser.add_argument(
    "-v", "--verbose", action="count", default=0, help="Report with increasing verbosity"
)

subparsers = argument_parser.add_subparsers(title="commands", dest="command")
subparsers.required = True
attach_admin_command(subparsers.add_parser("admin"))
attach_bootstrap_command(subparsers.add_parser("bootstrap"))
attach_clean_command(subparsers.add_parser("clean"))
attach_run_http_server_command(subparsers.add_parser("run_http_server"))
attach_search_command(subparsers.add_parser("search"))
attach_tail_command(subparsers.add_parser("tail"))

LOG_FORMAT = "[%(asctime)s] - %(levelname)s - %(message)s - " \
             "(%(name)s : %(funcName)s : %(lineno)d : Thread/PID(%(thread)d/%(process)d))"


main_logger = logging.getLogger(__name__)


def main(args=None):
    root_logger = logging.getLogger('')
    stderr_handler = logging.StreamHandler()
    stderr_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    root_logger.addHandler(stderr_handler)

    args = args or argument_parser.parse_args()

    if args.verbose == 2:
        root_logger.setLevel(logging.DEBUG)
        stderr_handler.setLevel(logging.DEBUG)
    elif args.verbose == 1:
        root_logger.setLevel(logging.INFO)
        stderr_handler.setLevel(logging.INFO)
    else:
        root_logger.setLevel(logging.WARNING)
        stderr_handler.setLevel(logging.WARNING)
    try:
        main_logger.info("Executing command: {0}".format(args.command))
        args.func(args)
    except BaseException:
        main_logger.exception("Unhandled exception executing command: {0}".format(args.command))
        raise
