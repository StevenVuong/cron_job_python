import argparse


def parse_cron_args(raw_args):
    """Parse command line args for cron_job.py, attempts to replicate cron-style
    time argument inputs.

    Args:
        - raw_args: list of command line arguments that specify
        desired schedule times to run and the shell command to run
    Returns:
        - parser.parseargs object

    Ref: https://crontab.guru/ is quite a useful tool to help idealise cron time args
        
    Todo:
        - Be able to also handle non-strings, currently all inputs must be
        of string type
        - Have an actual use case for reboot
        - Constraint of ranges of values able to be parsed"""

    parser = argparse.ArgumentParser(
        description='Parse speicified inputs for cron job'
        )

    parser.add_argument(
        "-r",
        "--reboot",
        default=False,
        type=bool,
        help="If passed, executes shell command upon reboot (bool)",
        required=False
    )

    parser.add_argument(
        "-ct",
        "--cron_time",
        type=str,
        default="* * * * *",
        help="Entire cron time to be parsed",
        required=True
    )

    parser.add_argument(
        "-sc",
        "--shell_cmd",
        type=str,
        help="Shell command to be run.",
        required=True
    )

    return parser.parse_args(raw_args)
