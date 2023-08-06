# schedule_filter

This repository allows to create advanced [dbader/schedule](https://github.com/dbader/schedule) job scheduling

## Features
* doing a job at/in the:
    * nth day of the year
    * nth month of the year
    * nth day of a month
    * nth week of a month

## Examples

* basic:
    * monthly:
        * doing a job on every second sunday of a month ```schedule.every().sunday.do(nth_week_monthly(2, job_func))```
        * doing a job on every last monday of a month ```schedule.every().monday.do(nth_week_monthly(-1, job_func))```
        * doing a job on every last day of a month ```schedule.every().monday.do(nth_day_monthly(-1, job_func))```
        * doing a job on every 15th of a month ```schedule.every().monday.do(nth_day_monthly(15, job_func))```
    * yearly:
        * doing a job on every first day of a year ```schedule.every().day.do(nth_day_yearly(1, job_func))```
        * doing a job on every New Year's Eve ```schedule.every().day.do(nth_day_yearly(-1, job_func))```
        * doing a job every day in april ```schedule.every().day.do(nth_month_yearly(4, job_func))```
* advanced:
    * doing a job on every Christmas Eve ```schedule.every().day.do(nth_month_yearly(12, nth_day_monthly(24, job_func)))```