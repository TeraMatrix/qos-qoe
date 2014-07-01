#! /usr/bin/python
import time, sys, getopt
from sys import argv

TIMEFORMAT = "%m/%d/%y %H:%M:%S"
INTERVAL = 1
OK=0
WARNING=1
CRITICAL=2
UNKNOWN=3
usage = 'Usage:\t./check_cpu.py -w/--warn <integer> -c/--crit <integer>'

def printHelp():
    print "\n--------------------------------------------------------------------------\n"
    print "Title:\tPlugin to find CPU usage\n"
    print "Author:\tGaurav Singh\n"
    print "Help: \tpython <script_name>.py -h\" or \"python <script_name>.py --help\n"
    print usage
    print "\t 1. Critical Threshold should be greater than Warning Threshold\n\t 2. Both the values must be between 0 and 100 inclusive\n"
    print "Any other number of or any other format of arguments will not be accepted\n"
    print "---------------------------------------------------------------------------\n"

#validates command line argumnets
def command_line_validate(argv):
    try:
        opts, args = getopt.getopt(argv, 'w:c:o:', ['warn=' ,'crit='])
    except getopt.GetoptError:
        print usage
    try:
        for opt, arg in opts:
            if opt in ('-w', '--warn'):
                try:
                  warn = int(arg)
                except:
                  print '***warn value must be an integer***'
                  sys.exit(CRITICAL)
            elif opt in ('-c', '--crit'):
                try:
                  crit = int(arg)
                except:
                  print '***crit value must be an integer***'
                  sys.exit(CRITICAL)
            else:
                print usage
        try:
            isinstance(warn, int)
            #print 'warn level:', warn
        except:
            print '***warn level is required***'
            print usage
            sys.exit(CRITICAL)
        try:
            isinstance(crit, int)
            #print 'crit level:', crit
        except:
            print '***crit level is required***'
            print usage
            sys.exit(CRITICAL)
    except:
        sys.exit(CRITICAL)
        # confirm that warning level is less than critical level, alert and exit if check fails
    if warn > crit:
        print '***warning level must be less than critical level***'
        sys.exit(CRITICAL)
    return warn, crit

#reads proc file and get time list
def getTimeList():
    statFile = file("/proc/stat", "r")
    timeList = statFile.readline().split(" ")[2:6]
    statFile.close()
    for i in range(len(timeList))  :
        timeList[i] = int(timeList[i])
    return timeList

#calculates difference between two time intervals from time lists
def deltaTime(interval)  :
    x = getTimeList()
    time.sleep(interval)
    y = getTimeList()
    for i in range(len(x))  :
        y[i] -= x[i]
    return y

#calculate cpu usage from time difference
def get_cpu_usage():
    dt = deltaTime(INTERVAL)
    timeStamp = time.strftime(TIMEFORMAT)
    total_cpu_use = 100 - (dt[len(dt) - 1] * 100.00 / sum(dt))
    return total_cpu_use

#gets the status of cpu as per nagios
def get_status(total_cpu_use, threshold_warning, threshhold_critical):
    
    if total_cpu_use < threshold_warning and total_cpu_use>=0:
        Status=[OK,"Okay"]
    elif total_cpu_use <threshhold_critical:
        Status=[WARNING,"Warning"]
    elif total_cpu_use <= 100:
        Status=[CRITICAL,"Critical"]
    else:
        Status=[UNKNOWN,"Unknown"]
        
    return Status

#performance data for nagios
def performance_data(total_cpu_use, warn, crit):
    total_data = str('Total'), '=',  str('%.2f' %total_cpu_use), str('%;'), str(warn), ';', str(crit), ';', str('0'), ';', str('100')
    total_cpu_data = "".join(total_data)
    #print total_cpu_data
    performance_data =  total_cpu_data
    return performance_data

#main function
def main():
    argv = sys.argv[1:]  
    if len(argv)==1:
        if argv[0]=="--help" or argv[0]=="-h":
            printHelp()
            sys.exit()
        else:
            print "Invalid argument.For Help type -h or --help in argument"
            sys.exit(UNKNOWN)

    threshold_warning, threshhold_critical = command_line_validate(argv)
    total_cpu_use=get_cpu_usage()
    Status=get_status(total_cpu_use, threshold_warning, threshhold_critical)
    perf_data=performance_data(total_cpu_use, threshold_warning, threshhold_critical)
    timeStamp = time.strftime(TIMEFORMAT)
    print timeStamp+': ', Status[1],' - ', str('%.2f' %total_cpu_use), '% |', perf_data
    

if __name__ == "__main__"  :
    main()
