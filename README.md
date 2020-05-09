# Python Cron-Style Implemetation
Cron is a linux software utility which implements a time-based job scheduler. Cron is most suitable for scheduling repetitive tasks. Here we introduce a Python implementation which can be run from the command line.

Note: For further notes of the thoughts behind the design and approach, as well as more information on Cron, one can have a 
read over the files in `./docs` for further details. This also includes a `cron_report.pdf` which will highlight an overview of the system design, as well as assumptions, limitations and further work.


## Quickstart:

### Requirements (Linux / MacOS):
- Python 3.6 or above
- Python 2.7 is untested, however, I believe there are no dependencies that may
prohibit this.

### Command to Run:
```
nice -n 19 python main.py -sc "<BASH COMMAND>" -ct "<CRON TIME SETTINGS>" 
```
The `nice -n 19` is optional, aiding in reducing CPU impact and may be omitted
should one wish to do so. An example to run the command is:
```
nice -n 19 python main.py -sc "echo hello world" -ct "* * * * *"
```
with the bash command and cron time settings encapsulated in speech marks. The above example will output "hello world" to the command line at the begining of every minute.

To stop the program, simply use keyboard shortcuts `ctrl + c`.
