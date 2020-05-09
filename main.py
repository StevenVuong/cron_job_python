import sys

from src.cronjob import CronJob
from src.parse_args import parse_cron_args
import time
import datetime


def main(raw_args=None):

    args = parse_cron_args(raw_args)

    # Run until keyboard interrupt
    # TODO: Improve runtime -> Assumes instantaneous, not so great
    # TODO: Run in container where we limit resources? Requires very little..
    while True:
        if datetime.datetime.now().second == 0:  
            CronJob(args)
            time.sleep(59.5) # Run once a minute


if __name__=="__main__":

    try:

        main()

    except KeyboardInterrupt:

        print ("Killed by user")
        sys.exit(0)
