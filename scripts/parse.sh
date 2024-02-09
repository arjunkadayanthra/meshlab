#!/bin/bash

set -x
set -e


src_dir="${1:-/media/arjun/Data/HSN/S2/IT Performance Analysis/project/extracted/rawdata}"
trg_dir="${2:-/media/arjun/Data/HSN/S2/IT Performance Analysis/project/extracted/data}"

mkdir "$trg_dir" || true
mkdir "$src_dir/tmp" || true

traces=$(ls -1 "$src_dir" | grep "trace_.*.pcap")

for f in $traces
do
  proto="tcp"
  if [[ $f == "trace_udp_"* ]]; then
    proto="udp"
  fi
	temp_fname=`echo $f | cut -d '_' -f2-4`
	out_fname="${temp_fname%.pcap*}.csv"
	# echo $out_fname
	# echo "Extracting : $src_dir/$f"
	echo "time,tcp,udp,icmp,bitrate" > "$trg_dir/$out_fname"
	tshark -Y "ip.src == 10.23.10.1 and ip.dst == 10.23.20.1 and $proto.port == 5201" -r "$src_dir/$f" -w "$src_dir/tmp/$temp_fname" && tcpstat -F -r "$src_dir/tmp/$temp_fname" -o "%R,%T,%U,%C,%b\n" 1 >> "$trg_dir/$out_fname" && echo "## Extracted : $src_dir/$f -> $trg_dir/$out_fname" &
	
	while [[ $(jobs | wc -l) -ge 5 ]]; do
		sleep 5s
	done
	
done

while [[ $(jobs | wc -l) -ge 2 ]]; do
	sleep 5s
done

echo "### Extraction completed. Files :"
ls -lh "$trg_dir"