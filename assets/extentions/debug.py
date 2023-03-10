import inspect
import os
import datetime

def report(content, display_location=True):
    local = os.path.abspath(__file__)
    resources_dir = os.path.dirname(local)
    resources_dir = os.path.join(*resources_dir.split(os.sep)[:-2])
    caller_frame = inspect.stack()[1]
    filename, line_number, function_name, code_line, code_index = inspect.getframeinfo(caller_frame[0])
    calling_script = os.path.basename(filename)
    timestamp = datetime.datetime.now()
    year = timestamp.strftime("%y"[-2:])
    timestamp = timestamp.strftime("%m%d%H%M%S")
    timestamp = year + timestamp
    log_file = "/" + resources_dir + "/debug.txt"
    x = open(str(log_file), "a+")
    x.write(str(timestamp))
    x.write(" from ")
    x.write(calling_script)
    if display_location is True:
        x.write(" around line ")
        x.write(str(line_number))
    x.write(": ")
    x.write(str(content))
    x.write("\n")
    x.close()
    if display_location is True:
        print("WARNING: potential issue caught, check debug.txt for more details...")

def newline():
    local = os.path.abspath(__file__)
    resources_dir = os.path.dirname(local)
    resources_dir = os.path.join(*resources_dir.split(os.sep)[:-2])
    log_file = "/" + resources_dir + "/debug.txt"
    x = open(str(log_file), "a+")
    x.write("\n")
    x.close()



