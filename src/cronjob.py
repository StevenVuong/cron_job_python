import subprocess
import datetime
import argparse
from copy import deepcopy


class CronJob():
    """Initialise cron job class object.

    Note:
        - Reboot is not handled right now.
        - Erroneous values are not handled in input, assumes user entered correctly.

    TODO: Be able to execute in background and kill when we want.
    TODO: Handle different timezones
    TODO: Comments
    TODO: Refactor
    TODO: Handle special case where day of month and day of week is specified 
    """
    def __init__(self, args: argparse.Namespace):

        self.args = deepcopy(args)

        # TODO: Check how fast this runs; assumes instantaneous right now
        self.datetime_now = datetime.datetime.now()

        # TODO: Handle reboot bool -> This at the moment does nothing
        self.reboot = self.args.reboot

        self.crontime_dict = self._parse_crontime_str_to_dict()

        # TODO: Put the checks into one function
        self.is_minute_match = self._check_minute_match()
        self.is_hour_match = self._check_hour_match()
        self.is_month_match = self._check_month_match()
        # We want to run at beginning of each second.
        self.is_seconds_zero = self.datetime_now.second == 0
        self.is_day_of_week_month = self._check_day_of_week_month()

        if all([
            self.is_minute_match,
            self.is_hour_match,
            self.is_month_match,
            self.is_seconds_zero,
            self.is_day_of_week_month
        ]):
            self.shell_cmds = self.args.shell_cmd
            self._run_shell_command()

    # TODO: Error handling for mis entered strings.
    # TODO: Docstring
    def _parse_crontime_str_to_dict(self):
        """
        """
        crontimes = self.args.cron_time.split()

        if len(crontimes) != 5:
            raise ValueError("Input crontimes is erroneous!")

        crontime_dict = {
            "minute": crontimes[0],
            "hour": crontimes[1],
            "day_of_month": crontimes[2],
            "month": crontimes[3],
            "day_of_week": crontimes[4],
        }

        return crontime_dict

    # TODO: Docstring
    # TODO: Refactor
    # TODO: Test exceptions
    def _check_minute_match(self):

        minute = self.crontime_dict["minute"]
        minute_now = self.datetime_now.minute

        if minute[0] == "*":

            if minute[0:2] == "*/" and len(minute)>1:
                minute_delta = int(minute[2:]) # TODO, cast as int. Better to apply round()?

                if minute_delta < 0 or minute_delta > 59: # 
                    raise ValueError("Minute denominator must be in range [0,59]!")
                
                if minute_now % minute_delta == 0: # Minute matches n for */n
                    return True

            else:
                return True # Every minute match, *

        else:
            # Single value int
            if minute.isdigit():
                minute = int(minute)
                if minute < 0 or minute > 59:
                    raise ValueError("Minutes must be within range [0, 59]!")

                if minute_now == minute: # minute matches minute npw
                    return True

            # Multiple ints for minute
            else:
                try:
                    minutes = [int(m.strip()) for m in minute.split(",")]
                    if minute_now in minutes:
                        return True # if minutes in list of minutes
                except:
                    raise ValueError("Minutes input is erroneous!")
        return False

    # TODO: Same as minute match
    def _check_hour_match(self):

        hour = self.crontime_dict["hour"]
        hour_now = self.datetime_now.hour

        if hour[0] == "*":

            if hour[0:2] == "*/" and len(hour)>1:
                hour_delta = int(hour[2:])

                if  hour_delta < 0 or hour_delta > 23: # 
                    raise ValueError("Hour denominator must be [0, 23]!")
                
                if hour_now % hour_delta == 0: # hour matches n for */n
                    return True

            else:
                return True # True for every hour

        else:
            # Multiple values for hour
            if hour.isdigit():
                hour = int(hour)
                if hour < 0 or hour > 23:
                    raise ValueError("Hour must be within range [0, 23]!")

                if hour_now == hour: # hour matches hour now
                    return True

            # Single value int
            else:
                try:
                    hours = [int(h.strip()) for h in hour.split(",")]
                    if hour_now in hours:
                        return True # if hour in list of hours
                except:
                    raise ValueError("Hours input is erroneous!")
        return False

    # TODO: Same as minute match -> Make base template and use that instead
    def _check_month_match(self):
        month = self.crontime_dict["month"]
        month_now = self.datetime_now.month

        if month[0] == "*":

            if month[0:2] == "*/" and len(month)>1:
                month_delta = int(month[2:])

                if month_delta > 12 or month_delta < 1: # 
                    raise ValueError("Month denominator must be [1, 12]!")
                
                if month_now % month_delta == 0: # month matches n for */n
                    return True

            else:
                return True # True for every month

        else:
            # Multiple values for month
            if month.isdigit():
                month = int(month)
                if month > 12 or month < 1:
                    raise ValueError("Month denominator must be [1, 12]!")

                if month_now == month: # month matches monh now
                    return True

            # Single value int
            else:
                try:
                    months = [int(m.strip()) for m in month.split(",")]
                    if month_now in months:
                        return True # if month in list of months
                except:
                    raise ValueError("Months input is erroneous!")
        return False

    # TODO: Docstring
    # TODO: Big refactor, could be so much better in terms of handling (running out of time)
    # TODO: tests! Error handling & checking too. Faulty where parse several numbers
    def _check_day_of_week_month(self):
        """
        """
        day_of_month = self.crontime_dict["day_of_month"]
        day_of_week = self.crontime_dict["day_of_week"]

        day_now_num = self.datetime_now.day

        # Monday is 0 for datetime and sunday is 6. Alter so it matches
        # cron day of week
        day_now_of_week = self.datetime_now.today().weekday()
        day_now_of_week += 1
        if day_now_of_week == 7: day_now_of_week = 0

        is_month_day_match = None
        is_week_day_match = None

        if day_of_month == "*" and day_of_week == "*":
            return True

        if day_of_month == "*":
            is_month_day_match = True

        if day_of_month != "*":

            ## Logic to handle
            if day_of_month[0:2] == "*/" and len(day_of_month)>1:
                dom_delta = int(day_of_month[2:])

                if dom_delta > 31 or dom_delta < 1: # 
                    raise ValueError("Day of Month denominator must be [1, 31]!")
                
                if day_now_num % day_of_month == 0:
                    is_month_day_match = True
                else: is_month_day_match = False

            # Multiple values for day of month
            if day_of_month.isdigit():
                day_of_month = int(day_of_month)
                if day_of_month > 31 or day_of_month < 1:
                    raise ValueError("Day of Month denominator must be [1, 31]!")

                if day_of_month == day_now_num:
                    is_month_day_match = True
                else: is_month_day_match = False

            # Single value int
            else:
                try:
                    days_of_month = [int(dom.strip()) for dom in day_of_month.split(",")]
                    if day_now_num in days_of_month:
                        is_month_day_match = True #
                    else: is_month_day_match = False
                except:
                    raise ValueError("Months input is erroneous!")
        

        if day_of_week == "*":
            is_week_day_match = True
            
        # Handles wheer day of week is specified
        if day_of_week != "*":
            ## Logic to handle
            if day_of_week[0:2] == "*/" and len(day_of_week)>1:
                dow_delta = int(day_of_week[2:])

                if dow_delta > 6 or dow_delta < 0: # 
                    raise ValueError("Day of Week denominator must be [0, 6]!")
                
                if day_now_of_week % day_of_week == 0:
                    is_week_day_match = True
                else: is_week_day_match = False

            # Multiple values for day of week
            if day_of_week.isdigit():
                day_of_week = int(day_of_week)
                if day_of_week > 6 or day_of_week < 0:
                    raise ValueError("Day of Week denominator must be [0, 6]!")

                if day_of_week == day_now_of_week: 
                    is_week_day_match = True
                else: is_week_day_match = False

            else:
                try:
                    days_of_week = [int(dow.strip()) for dow in day_of_week.split(",")]
                    if day_now_of_week in days_of_week:
                        return True # if month in list of months
                    else: is_week_day_match = False

                except:
                    raise ValueError("Day of Week input is erroneous!")

        # If both true, return true
        # TODO: Testing for this! Need to run scenarious through to idea check.
        if all([is_month_day_match, is_week_day_match]): return True
        else:
            return False
            #Specified Day of month and day of week do not align!
            # TODO: Raise error if this iss the case?

 # TODO: Time! Need a timer

    def _run_shell_command(self):

        try:
            subprocess.run(self.shell_cmds.split())

        except subprocess.SubprocessError as err:
            print(str(err), "Exception occured when running subprocess shell script")
