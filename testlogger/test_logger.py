import os

import datetime
import re

ROOT_DIR = os.path.abspath(os.pardir)
logfile = r"\logfile\test.log"
infile = ROOT_DIR+logfile
entry_list = []
exit_list = []
final_list = []
REPORT_list= []

with open(infile) as f:
    f = f.readlines()
    for line in f:
        if "entry with" in line:
            match_date = re.search(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2},\d{3}', line)
            date = datetime.datetime.strptime(match_date.group(), '%Y-%m-%dT%H:%M:%S,%f')
            string_date = str(date)
            spl_word = "entry with ("
            serviceName = str(line.partition(spl_word)[2])
            entry_service_name =  serviceName.split(':')[0]
            request_name =  serviceName.split(':')[1]
            entry_request_ID = request_name.replace(')', "").strip()
            entry_date = string_date
            entry_list_object = (entry_request_ID, entry_service_name, entry_date)
            entry_list.append(entry_list_object)

        if "exit with" in line:
            match_date = re.search(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2},\d{3}', line)
            date = datetime.datetime.strptime(match_date.group(), '%Y-%m-%dT%H:%M:%S,%f')
            string_date = str(date)
            spl_word = "exit with ("
            serviceName = str(line.partition(spl_word)[2])
            exit_service_name = serviceName.split(':')[0]
            request_name = serviceName.split(':')[1]
            exit_request_ID = request_name.replace(')', "").strip()
            exit_date = string_date
            exit_list_object = (exit_request_ID, exit_service_name, exit_date)
            exit_list.append(exit_list_object)
#instead of this list , need to use Hashmap ,for python so can add same in and out event for same request id.
#current implementation takes much time to provide results.

if len(entry_list) == len(set(entry_list)):
    print("NO duplicate ENTRY logs ")
else:
    print("There are duplicate ENTRY logs ")

if len(exit_list) == len(set(exit_list)):
    print("NO duplicate EXIT logs ")
else:
    print("There are duplicate EXIT logs ")

set_entryList = set(entry_list)
set_exitList = set(exit_list)

for entry_val in set_entryList:
    ENTRY_REQ_ID = entry_val[0]
    ENTRY_SERVICE = entry_val[1]
    ENTRY_TIME = entry_val[2]
    for exit_val in set_exitList:
        EXIT_REQ_ID = exit_val[0]
        EXIT_SERVICE = exit_val[1]
        EXIT_TIME = exit_val[2]
        if EXIT_REQ_ID == ENTRY_REQ_ID and EXIT_SERVICE == ENTRY_SERVICE:
            list_object = (EXIT_REQ_ID, EXIT_SERVICE, ENTRY_TIME, EXIT_TIME)
            final_list.append(list_object)

for service in final_list:
    FINAL_REQ_ID = service[0]
    FINAL_SERVICE_NAME = service[1]
    FINAL_ENTRY_TIME = service[2]
    FINAL_EXIT_TIME = service[3]
    date_format = '%Y-%m-%d %H:%M:%S.%f'
    inTime = datetime.datetime.strptime(FINAL_ENTRY_TIME, date_format)
    outTime = datetime.datetime.strptime(FINAL_EXIT_TIME, date_format)
    time_diff = (outTime-inTime).total_seconds()
    REPORT_list_object = (time_diff, FINAL_REQ_ID, FINAL_SERVICE_NAME)
    REPORT_list.append(REPORT_list_object)
    #print("request id: " +FINAL_REQ_ID+ " - service name: "+ FINAL_SERVICE_NAME+" time_diff: " + str(time_diff))

print(REPORT_list)
print("----------------------------")
REPORT_list.reverse()
print(REPORT_list)

FINAL_SERVICE_NAME = REPORT_list[0][2]
FINAL_MAX_TIME = REPORT_list[0][0]
print(" - service name: " + FINAL_SERVICE_NAME + " MAX TIME For this service: " + str(FINAL_MAX_TIME))

list_serviceName= []
for service in REPORT_list:
    list_serviceName.append(service[2])

service_count = {i:list_serviceName.count(i) for i in list_serviceName}
print(service_count)



