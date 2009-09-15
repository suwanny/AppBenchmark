#!/bin/bash
# Start Proxy
#
ADDRESS=twolves.cs.ucsb.edu
PORT=8008
SCRIPT_DIR=scripts/proxy

cd ..; export GRINDERPATH=${PWD}

CLASSPATH=.
for file in $GRINDERPATH/lib/*.jar; do
  CLASSPATH=$CLASSPATH:$file
done

SCRIPT_NAME="from_proxy" 
if [ "$1" != "" ]; then 
	SCRIPT_NAME=$1
fi

PROXY_OPTION="-http"
#PROXY_OPTION=${PROXY_OPTION}" -console"
PROXY_OPTION=${PROXY_OPTION}" -localhost ${ADDRESS} -localport ${PORT}"

java -cp ${CLASSPATH} net.grinder.TCPProxy ${PROXY_OPTION} > ${SCRIPT_DIR}/${SCRIPT_NAME}.py


