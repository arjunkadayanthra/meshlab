#!/bin/bash

#set -x
set -e

source secrets.sh

function usage() {
    echo "Usage: collect.sh [-n <num> -d <seconds> -s <size> -u] mode"
    echo "Defaults: -n 10 -d 60 -s 256"
    echo "Options:"
    echo "-n : number of iterations"
    echo "-d : duration for traffic generation (per iteration). Translates to : iperf3 -t <seconds>"
    echo "-s : size of data bytes to be stored from each packet. Translates to : tcpdump -s <size>"
    echo "-u : use UDP rather than TCP for iperf3. Note that -u option doesn't take any params and sets the target bandwidth to 1Gbps. Translates to : iperf3 -ub 1000000000"
    exit 1
}

# Defaults
iterations=10
duration=60
udp_opts=""
size=256

while getopts "n:d:s:uh" opt ; do
 case $opt in
 n)
  iterations=$OPTARG
   ;;
 d)
   duration=$OPTARG
   ;;
 u)
    udp_opts=" -ub 1000000000"
    ;;
 s)
   size=$OPTARG
   ;;
 h | *)
  usage
  ;;
 esac
done

shift $((OPTIND -1))

if [[ -z "$1" ]]; then
    echo "Error: mode is not specified" >&2
    usage
fi

mode="$1"
dir="/home/team5/udp"
filename="$dir/trace_$mode"

echo "### Configuration:"
echo "Mode: $mode"
if [ -n "$udp_opts" ]; then
    echo "## Using UDP"
fi
echo "Iterations: $iterations"
echo "Duration: $duration"
echo "Dir: $dir"

mkdir "$dir" || true

for i in $(seq "$iterations");
do
	echo "#### Iteration $i starting......"
	suffix="$(date +%y%m%d_%H%M%S).pcap"
	timeout $((duration+5)) sudo ip netns exec itsys-d3-sink sudo tcpdump -nei ul-sink -s "$size" -w "$filename-$suffix" &
	sudo ip netns exec itsys-d3-source iperf3 -c "$IP_SINK" -t "$duration" $udp_opts
	sleep 10s
done

echo "#### Trace collection completed for mode : $mode"
echo "#### Files : "
ls $dir -lah | grep "$mode"
