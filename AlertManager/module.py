from functools import wraps
from datetime import datetime, timedelta
import time



# The Job class represents a scheduled job that will be executed at specified intervals.
class Job:
    def __init__(self):
        # Initialize the job with default values.
        self.interval = None  # Interval between executions (e.g., every 5 seconds, every 2 days).
        self.unit = None  # The time unit of the interval (e.g., 'second', 'minute', 'hour', 'day').
        self.time_at = None  # Specific time of day the job should run (only used for day/week/month/year intervals).
        self.repeat_count = None  # How many times the job should be repeated.
        self.end_date = None  # The date and time after which the job should stop running.
        self.job_func = None  # The function that will be executed when the job runs.
        self.args = ()  # Positional arguments to pass to the job function.
        self.kwargs = {}  # Keyword arguments to pass to the job function.
        self.next_run = None  # The next scheduled run time of the job.
        self.executed_count = 0  # Counter to keep track of how many times the job has run.
        self.completed = False  # Flag to indicate whether the job has completed and should not run anymore.
        self.use_threading = False  # Flag to determine if threading should be used to run the job.

    def every(self, interval):
        # Set the interval for the job's execution.
        self.interval = interval  # Assign the interval value.
        return self  # Return the Job instance for method chaining.

    @property
    def second(self):
        # Set the time unit to 'second' for the job.
        self.unit = 'second'  # Assign 'second' as the time unit.
        return self  # Return the Job instance for method chaining.

    @property
    def minute(self):
        # Set the time unit to 'minute' for the job.
        self.unit = 'minute'  # Assign 'minute' as the time unit.
        return self  # Return the Job instance for method chaining.

    @property
    def hour(self):
        # Set the time unit to 'hour' for the job.
        self.unit = 'hour'  # Assign 'hour' as the time unit.
        return self  # Return the Job instance for method chaining.

    @property
    def day(self):
        # Set the time unit to 'day' for the job.
        self.unit = 'day'  # Assign 'day' as the time unit.
        return self  # Return the Job instance for method chaining.

    def week(self, weekday, time_at=None):
        # Set the time unit to 'week' and specify the day of the week the job should run.
        self.unit = 'week'  # Assign 'week' as the time unit.
        self.weekday = weekday  # Assign the day of the week (0 = Monday, 6 = Sunday).
        if time_at:
            self.time_at = datetime.strptime(time_at, '%H:%M').time()  # Parse and set the specific time of day.
        return self  # Return the Job instance for method chaining.

    def month(self, day, time_at=None):
        # Set the time unit to 'month' and specify the day of the month the job should run.
        self.unit = 'month'  # Assign 'month' as the time unit.
        self.month_day = day  # Assign the specific day of the month.
        if time_at:
            self.time_at = datetime.strptime(time_at, '%H:%M').time()  # Parse and set the specific time of day.
        return self  # Return the Job instance for method chaining.

    def year(self, month, day, time_at=None):
        # Set the time unit to 'year' and specify the month and day the job should run.
        self.unit = 'year'  # Assign 'year' as the time unit.
        self.year_month = month  # Assign the specific month.
        self.year_day = day  # Assign the specific day of the month.
        if time_at:
            self.time_at = datetime.strptime(time_at, '%H:%M').time()  # Parse and set the specific time of day.
        return self  # Return the Job instance for method chaining.

    def at(self, time_at):
        # Set a specific time of day for the job to run.
        if self.unit in ['day', 'week', 'month', 'year']:
            self.time_at = datetime.strptime(time_at, '%H:%M').time()  # Parse and set the time if the time unit is day/week/month/year.
        else:
            raise ValueError("The 'at' method is only valid for daily, weekly, monthly, or yearly intervals.")
        return self  # Return the Job instance for method chaining.

    def repeat(self, repeat_count):
        # Set how many times the job should be repeated.
        self.repeat_count = repeat_count  # Assign the repeat count.
        return self  # Return the Job instance for method chaining.

    def until(self, end_date):
        # Set the end date and time after which the job should stop running.
        try:
            self.end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M')  # Parse and set the end date/time.
        except ValueError:
            raise ValueError("The 'until' method expects a date and time in the format 'YYYY-MM-DD HH:MM'.")
        return self  # Return the Job instance for method chaining.

    def do(self, job_func, *args, **kwargs):
        # Specify the function to execute when the job runs.
        self.job_func = job_func  # Assign the function to be executed.
        self.args = args  # Store positional arguments to pass to the function.
        self.kwargs = kwargs  # Store keyword arguments to pass to the function.
        self.next_run = self.calculate_next_run(datetime.now())  # Calculate and set the next run time based on the current time.
        # print(f"[DEBUG] Next run scheduled for: {self.next_run}")  # Debugging line to trace the calculated next run time.
        return self  # Return the Job instance for method chaining.

    def calculate_next_run(self, current_time):
        # Calculate the next run time based on the job's schedule.
        if self.unit == 'second':
            next_run_time = current_time + timedelta(seconds=self.interval)  # Calculate next run time by adding seconds to current time.
        elif self.unit == 'minute':
            next_run_time = current_time + timedelta(minutes=self.interval)  # Calculate next run time by adding minutes to current time.
        elif self.unit == 'hour':
            next_run_time = current_time + timedelta(hours=self.interval)  # Calculate next run time by adding hours to current time.
        elif self.unit == 'day':
            next_run_date = current_time.date()  # Get the current date.
            if self.time_at:
                if current_time.time() >= self.time_at:
                    next_run_date += timedelta(days=self.interval)  # If the current time has passed the time_at, move to the next interval day.
                next_run_time = datetime.combine(next_run_date, self.time_at)  # Combine the next date with the specific time.
            else:
                next_run_time = current_time + timedelta(days=self.interval)  # If no specific time, just add days to the current time.
        elif self.unit == 'week':
            days_ahead = (self.weekday - current_time.weekday() + 7 * self.interval) % 7  # Calculate the next weekday to run.
            next_run_date = current_time.date() + timedelta(days=days_ahead)  # Add the calculated days to get the next run date.
            next_run_time = datetime.combine(next_run_date, self.time_at)  # Combine the next date with the specific time.
        elif self.unit == 'month':
            next_month = current_time.month + self.interval  # Calculate the next month to run.
            year = current_time.year + (next_month - 1) // 12  # Adjust the year if the month calculation overflows to the next year.
            month = (next_month - 1) % 12 + 1  # Calculate the correct month in the year.
            next_run_date = datetime(year, month, self.month_day)  # Create the next run date with the specified day.
            if current_time > next_run_date:
                next_run_date = datetime(year, month + self.interval, self.month_day)  # If the calculated date is in the past, move to the next interval.
            next_run_time = datetime.combine(next_run_date, self.time_at)  # Combine the next date with the specific time.
        elif self.unit == 'year':
            next_run_date = datetime(current_time.year, self.year_month, self.year_day)  # Create the next run date for the year.
            if current_time > next_run_date:
                next_run_date = datetime(current_time.year + self.interval, self.year_month, self.year_day)  # If the date is in the past, move to the next year.
            next_run_time = datetime.combine(next_run_date, self.time_at)  # Combine the next date with the specific time.
        else:
            raise ValueError(f"Unsupported time unit: {self.unit}")  # Raise an error if the time unit is not supported.

        # print(f"[DEBUG] Calculated next run time: {next_run_time}")  # Debugging line to trace the calculated next run time.
        return next_run_time  # Return the calculated next run time.

    def should_run(self):
        # Determine whether the job should run at the current time.
        if self.end_date and datetime.now() > self.end_date:
            self.completed = True  # If the current date is past the end date, mark the job as completed.
            return False  # Return False since the job should not run anymore.

        if self.repeat_count is not None and self.executed_count >= self.repeat_count:
            self.completed = True  # If the job has been executed the specified number of times, mark it as completed.
            return False  # Return False since the job should not run anymore.

        return datetime.now() >= self.next_run  # Return True if the current time is equal to or after the next scheduled run time.

    def run(self):
        # Execute the job if it is scheduled to run.
        if self.should_run() and not self.completed:
            # print(f"[DEBUG] Running job: {self.job_func.__name__} at {datetime.now()}")  # Debugging line to indicate the job is running.
            self.job_func(*self.args, **self.kwargs)  # Execute the job function with the provided arguments.
            self.executed_count += 1  # Increment the count of how many times the job has run.
            self.next_run = self.calculate_next_run(self.next_run)  # Recalculate and update the next run time after the job has run.
            # print(f"[DEBUG] Next run rescheduled for: {self.next_run}")  # Debugging line to trace the next scheduled run time.

# The JobScheduler class manages the scheduling and execution of multiple jobs.
class JobScheduler:
    def __init__(self, use_threading=False):
        # Initialize the job scheduler.
        self.jobs = []  # List to store all the jobs to be managed by the scheduler.
        self.use_threading = use_threading  # Flag to set the default threading behavior for all jobs.

    def add_job(self, job):
        # Add a job to the scheduler.
        if job.use_threading is None:
            job.use_threading = self.use_threading  # If the job doesn't have threading explicitly set, inherit the scheduler's threading behavior.
        self.jobs.append(job)  # Add the job to the scheduler's list of jobs.

    def run_pending(self):
        # Run all jobs that are scheduled to run at the current time.
        while self.jobs:
            for job in self.jobs:
                job.run()  # Run each job that is scheduled to run.
            self.jobs = [job for job in self.jobs if not job.completed]  # Remove completed jobs from the list.
            if not self.jobs:
                print("All jobs are completed. Scheduler is shutting down.")  # Indicate that all jobs are completed.
                break  # Exit the loop since there are no more jobs to run.
            time.sleep(1)  # Sleep for a second to avoid busy-waiting in the loop.



def jobs(interval, unit, time_at=None, until=None, repeat=None, scheduler=None):
    # The `job` function is a decorator factory that takes scheduling parameters like interval, unit, time_at, until, and repeat.
    def decorator(func):
        # The `decorator` function wraps around the target function (the job to be scheduled).
        @wraps(func)
        # The `wraps` decorator is used to preserve the original function's metadata, like its name and docstring.
        def wrapper(*args, **kwargs):
            # The `wrapper` function is the actual wrapper around the job function that adds scheduling logic.
            new_job = Job().every(interval)
            # Create a new Job instance and set the interval for the job.
            if unit == 'second':
                new_job.second
                # If the unit is 'second', set the job to run every specified number of seconds.
            elif unit == 'minute':
                new_job.minute
                # If the unit is 'minute', set the job to run every specified number of minutes.
            elif unit == 'hour':
                new_job.hour
                # If the unit is 'hour', set the job to run every specified number of hours.
            elif unit == 'day':
                new_job.day
                # If the unit is 'day', set the job to run every specified number of days.
                if time_at:
                    new_job.at(time_at)
                    # If a specific time of day is provided, set the job to run at that time.
            else:
                raise ValueError(f"Unsupported unit: {unit}")
                # Raise an error if the unit provided is not supported.
            if until:
                new_job.until(until)
                # If an end date/time is provided, set the job to stop running after that time.
            if repeat:
                new_job.repeat(repeat)
                # If a repeat count is provided, set the job to run only that many times.
            new_job.do(func, *args, **kwargs)

            # Set the function to be executed by the job, passing any provided arguments.
            scheduler.add_job(new_job)
            # Add the newly created job to the scheduler.
        return wrapper
        # Return the wrapper function, effectively replacing the original function with this wrapped version.
    return decorator
    # Return the decorator function from the `job` function.
