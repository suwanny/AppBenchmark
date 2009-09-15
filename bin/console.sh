#!/bin/bash
# Start Console
#
#cd ..; export GRINDERPATH=${PWD}
export GRINDERPATH=~/AppBenchmark

CLASSPATH="."
for file in $GRINDERPATH/lib/*.jar; do
  CLASSPATH=$CLASSPATH:$file
done

#java -cp $CLASSPATH net.grinder.Console -headless
run="java -cp $CLASSPATH net.grinder.Console -thriftui"

APP=net.grinder.Console
PID=`ps -ef | grep $APP | grep -v grep | awk '{print $2}'`

# Start up the service
case "$1" in
  start)
    echo "start ${APP}"
    if [ "$PID" = "" ]; then
      $run & 
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

  
