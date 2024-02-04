##  IT Performance Analysis


###  Table of Contents
1.  Problem definition
2.  Environment Setup
3.  Experiment Specification
4.  Data Analysis
5.  Plottting results
6.  Results
7.  Conclusions


###  1.  Problem Definition
  * The objective of this project is to measure and analyze the performance of different network packet forwarding techniques on a TP-Link WDR4900 v1 access point (hereafter referenced as `device`).
  * There are four packet forwarding techniques
    - IP forwarding
      This is a basic method where a system (usually a router) sends incoming packets to another network based on the destination IP address.
    - IP forwarding with software offloading
        This technique enhances performance by offloading some data forwarding tasks from the CPU to a more efficient part of the system.
    - IP forwarding with hardware offloading
      This method improves transmission performance by offloading certain data forwarding tasks from the software to the hardware, allowing for faster packet routing.
    - eBPF (TC)
      eBPF, when used with Traffic Control (TC) provides a flexible platform for executing programs in the kernel space, allowing for fast packet processing and forwarding.
###  2.  Environment Setup
   * The controller(named as `one-to-rule-them-all`) for the whole setup is a regular x86_64-based Desktop-PC (with a Intel i5 750 (4) @ 2.661GHz CPU) , running  on OpenWrt linux distribution ( SNAPSHOT, r24403+283-c23b509d72) and  also as a point of access. The controller has a 10-Gigabit connection to the switch.
   * The `device` is connected with two cables to the same switch to which the controller is also connected, thus they are in a network. To separate all the other devices and it's networks from each other, they are grouped into VLANs. The controller has access to all of these VLANs, and thus has a connection to the `device` (using a virtual interface). Every connection between a `device` and the controller gets its own unique set of IP addresses, and there’s a list that shows which of these addresses are used by the devices and the controller’s virtual interfaces.
   * Our team(team5) has a unique ssh key that it can use to access the `device`. This key is used along with the device’s IP address and the username ‘root’ to connect to the device. An SSH config entry has also been set up  in the `controller` to make this process easier.
   * In network performance experiments, it’s crucial to avoid any unwanted side-effects that could distort measurements. One such side-effect can occur when the device generating traffic is also the one being tested. This is because traffic generation is a resource-intensive task and can overload the device, leading to inaccurate results. To avoid this, traffic generation and reception are outsourced to a separate, more powerful device, known as the `controller`. However, if the `controller` detects that the source and destination of the traffic are the same device, it may bypass the device being tested and forward the traffic internally, resulting in unrealistically high throughput.To prevent this, we use a feature of the Linux kernel called `namespaces`. Namespaces allow us to create multiple network interfaces on the controller that are isolated from each other. This enables us to generate and receive traffic on the same device without the operating system recognizing it as such, ensuring accurate and reliable measurements.
   * The two connections between your device and the controller use two different subnets for better distinction. They are called the source subnet and the sink subnet, within each there is an own IP address space. We (team5) would need to use 10.23.10.1 as traffic source IP and 10.23.20.1 as traffic sink IP.
   * iperf3 is a tool that uses a client-server model to generate and transmit data, representing traffic source and sink respectively. It’s started with iperf3 on the server side and  on the client side. For this setupiperf3 is started in separate namespaces for the source and sink. The server listens on all interfaces, and the client connects to the server, transmits data, and both print throughput statistics every second.
   * Next step is to collect the trace. For this we are using the `tcpdump` tool that hooks onto a network interface and captures all incoming and outgoing packets, and can print that on the screen or write in into a pcap file.
   * Inorder to switch between the software and hardware offloading forwarding techniques , change the firewall configuration file (/etc/config/firewall) and for the eBPF (TC) forwarding, we load the prewritten eBPF program. 
###  3.  Experiment Specification
  We have planned to conduct each forwarding techniques 10 iterations.
###  4.  Data Analysis
   For performance analysis we use python script. Mean, median and standard deviations are the numerical measurements we used.
###  5.  Plottting results
   For plotting the results, first we have extracted the necessary fields such as timestamp and bitrate from the individual trace files and convert it into .csv files. With the help of python script and matpolib libraries, we have plotted the individual iterations into line graphs and calculated the mean, meadian and standard deviations for each packet forwarding techniques. Based on the calculated numerical measures, we then plot the aggregated statistical measures into a box plot for performance comparison.
###  6.  Results
  
###  7.  Conclusions
   * Justification

|x1|c1|c2|c3|
|-|-|-|-|
|1. |r1|r1|r1|
|3. |r2|r2|r2|
|1. |r1|r1|r1|

