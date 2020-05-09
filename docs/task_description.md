# BigPay Coding Challenge: Cron Job

## Context:

### Background:
Cron is a linux software utility which implements a time-based job scheduler. Cron is most suitable for scheduling repetitive tasks. 
Cron is driven by a crontab (i.e. cron table) file, a configuration file that specifies shell commands to run periodically on a given schedule. 
The syntax of each line in a crontab file expects a cron expression: A cron expression comprises of five fields, followed by a shell command to execute. 

### Challenge:
You are required to implement a cron-style service in python. 
A solution should comprise of the following: <br>
-   a full copy of your source code 
-   instructions on how to use a working demo 
-   a report on your solution, including documentation on 
-   any assumptions you have made for your code implementation – any limitations in your implementation 

### Additional Comments:
-  Design Implentation and thoughts
-  Minimal impact on system as possible

## Inital Thoughts (self):

-  We may have to make several assumptions, note these
-  Perhaps we can approach this like a research implementation task, tackling the primary bulk of the task
and leave a section in the report for further investigation to be taken if so desired
-  Minimal Impact on System, this could mean multiple things?
    -  Fast and able to run without interfering with mainline processes
        - Fast: CPU Optimisation (and GPU?) with storing as little information in memory as effectively possible.
        - Little interference: Portable -> Either this means we can run with Python 2, Python 3 and able to run without
        having to install other libraries. If we do install other packages, this may interefere with the system. One
        way around this is by utilising virtual environments or docker containers. Likely to go with the latter.

## Requirements:
python3
