#!/bin/bash
# Start Agent 
#
export GRINDERPATH=~/AppBenchmark
CLASSPATH="."
for file in $GRINDERPATH/lib/*.jar;
do
  CLASSPATH=$CLASSPATH:$file
done

if [ $# -lt 1 ]; then 
	echo "usage: ./agent.sh [start|stop|status] [testname]"
	exit;
fi

if [ "$1" = "start" ]; then 
  if [ $# -lt 2 ]; then
    echo "usage: ./agent.sh start [testname]"
    exit;
  fi

  TEST=$2
  GRINDERPROPERTIES=${GRINDERPATH}/etc/${TEST}.properties
fi


#cd ..; export GRINDERPATH=${PWD}
# before starting, remove old logs
cmd1="rm -rf ${GRINDERPATH}/logs/*.log"
cmd2="java -cp $CLASSPATH net.grinder.Grinder $GRINDERPROPERTIES"

APP=net.grinder.Grinder
PID=`ps -ef | grep $APP | grep -v grep | awk '{print $2}'`

# Start up the service
case "$1" in
  start)
    echo "start ${APP}"
    if [ "$PID" = "" ]; then
      $cmd1 
      $cmd2 &
    else
      echo "${APP} is already running"
    fi
    ;;
  stop)
    echo "stop ${APP}"
    echo $PID | xargs kill -9
    ;;
  restart)
    $0 stop
    sleep 1
    $0 start
    ;;
  status)
    if [ "$PID" = "" ]; then
      echo "${APP} isn't running!!!!!!!!!"
    else
      echo "${APP} is running"
    fi
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|status}"
    exit 1
esac
exit $?


