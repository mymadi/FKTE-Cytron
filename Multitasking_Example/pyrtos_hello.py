'''
RTOS Module
Exercise 3: Hello World using 'pyRTOS'
'''

import pyRTOS
import time

# This is our first "task" defined as a generator function
def hello_task(self):
    print("Hello from pyRTOS task!")
    yield # The first yield gives control back to the scheduler

    # After the first yield, this code runs when the task resumes
    while True:
        print("Still running 'hello_task'...")
        yield [pyRTOS.timeout(1)] # Yield control, and ask to be resumed after 1 second

# This is our first "task" defined as a generator function
def hello_longtask(self):
    print("Hello from pyRTOS LONGtask!")
    yield # The first yield gives control back to the scheduler

    # After the first yield, this code runs when the task resumes
    while True:
        print("Still running 'hello_LONGtask'...")
        yield [pyRTOS.timeout(10)] # Yield control, and ask to be resumed after 10 second
        
# Create an instance of our task
# pyRTOS.Task(task_function, name, priority).
task1 = pyRTOS.Task(hello_task, name="HelloTask", priority=2)
task2 = pyRTOS.Task(hello_longtask, name="HelloLongTask", priority=1)

# Start the RTOS scheduler with our task(s)
pyRTOS.add_task(task1)
pyRTOS.add_task(task2)

print("Starting pyRTOS scheduler...")
# 3. Start the pyRTOS scheduler.
pyRTOS.start()

# This code will generally not be reached if the tasks run indefinitely
print("Scheduler stopped.")
