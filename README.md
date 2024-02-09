##  IT Performance Analysis - Team 5 (Arjun Vishnu Prakash , Eldhose Paul)

###  Table of Contents
1.  [Problem definition](#problemdefinition)
2.  [Environment Setup](#envirsetup)
3.  [Error Discussion](#errdiscuss)
4.  [Confidence Analysis](#confianalysis)
5.  [Experiment Specification](#expspecifi)
6.  [Data Analysis](#dataanalysis)
7.  [Plottting results](#plotresults)
8.  [Results](#results)
9.  [Conclusions](#conclusion)


### 1. Problem Definition <a id="problemdefinition"></a>

  * The objective of this project is to measure and analyze the performance of different network packet processing and forwarding techniques through the router [TP-Link WDR4900 v1](https://static.tp-link.com/resources/document/TL-WDR4900_V1.0_Datasheet.zip) access point (hereafter referenced as `device`).

  * Four packet processing and forwarding techniques are considered in our experiment:-

   ####  a. IP forwarding:

   magine you’re a postman (the router) and you’ve got a bunch of letters (data packets) to deliver. Each letter has an address (the destination IP). Your job is to make sure each letter gets to the right address. That’s essentially what Internet Protocol (IP) forwarding is - it’s the process of sending data from one network to another based on the destination IP.

   ####  b. IP forwarding with software offloading:

Now, imagine if you, the postman, had a helper who could sort the letters for you while you’re out delivering. That would make your job a lot easier, right? This is what happens in IP forwarding with software offloading. Some of the data forwarding tasks are handed off (or “offloaded”) from the Central Processing Unit (CPU) to another part of the system that can handle these tasks more efficiently.
        
   ####  c. IP forwarding with hardware offloading:

Taking the postman analogy further, what if you had a super-fast bike that could get you to each address more quickly? That’s the idea behind IP forwarding with hardware offloading. Certain data forwarding tasks are offloaded from the software to the hardware, which can process these tasks faster, leading to quicker packet routing.
      
   ####  d. eBPF (TC):

Extended Berkeley Packet Filter (eBPF) used with Traffic Control (TC) is like having a super-smart sorting machine that not only sorts the letters but also decides the best route for delivery. eBPF allows for the execution of sandboxed programs in the Linux kernel without changing the kernel source code or loading kernel modules. When used with TC, it can classify and take action on network traffic, providing fine-grained control over network packets.

### 2.  Environment Setup <a id="envirsetup"></a>

* The `controller` (named as `one-to-rule-them-all` or Muxer) for the whole setup is a regular x86_64-based Desktop-PC (with a Intel i5 750 (4) @ 2.661GHz CPU) , running  on OpenWrt linux distribution ( SNAPSHOT, r24403+283-c23b509d72) and  also as a point of access. The controller has a 10-Gigabit connection to the switch.<br>

* The `device` is connected with two cables to the same switch to which the controller is also connected, thus they are in a network. To separate all the other devices and it's networks from each other, they are grouped into VLANs. The controller has access to all of these VLANs, and thus has a connection to the `device` (using a virtual interface). Every connection between a `device` and the controller gets its own unique set of IP addresses, and there’s a list that shows which of these addresses are used by the devices and the controller’s virtual interfaces.<br>

* Our team(team5) has a unique ssh key that it can use to access the `device`. This key is used along with the device’s IP address and the username ‘root’ to connect to the device. An SSH config entry has also been set up  in the `controller` to make this process easier. <br>

* In network performance experiments, it’s crucial to avoid any unwanted side-effects that could distort measurements. One such side-effect can occur when the device generating traffic is also the one being tested. This is because traffic generation is a resource-intensive task and can overload the device, leading to inaccurate results. To avoid this, traffic generation and reception are outsourced to a separate, more powerful device, known as the `controller`. However, if the `controller` detects that the source and destination of the traffic are the same device, it may bypass the device being tested and forward the traffic internally, resulting in unrealistically high throughput.To prevent this, we use a feature of the Linux kernel called `namespaces`. Namespaces allow us to create multiple network interfaces on the controller that are isolated from each other. This enables us to generate and receive traffic on the same device without the operating system recognizing it as such, ensuring accurate and reliable measurements.<br>
 
* The two connections between your device and the controller use two different subnets for better distinction. They are called the source subnet and the sink subnet, within each there is an own IP address space. We (team5) would need to use 10.23.10.1 as traffic source IP and 10.23.20.1 as traffic sink IP.<br>
 
* iperf3 is a tool that uses a client-server model to generate and transmit data, representing traffic source and sink respectively. It’s started with iperf3 on the server side and  on the client side. For this setupiperf3 is started in separate namespaces for the source and sink. The server listens on all interfaces, and the client connects to the server, transmits data, and both print throughput statistics every second.<br>

* Next step is to collect the trace. For this we are using the `tcpdump` tool that hooks onto a network interface and captures all incoming and outgoing packets, and can print that on the screen or write in into a pcap file.<br>

* Inorder to switch between the software and hardware offloading forwarding techniques , change the firewall configuration file (/etc/config/firewall) and for the eBPF (TC) forwarding, we load the prewritten eBPF [program](https://github.com/tk154/eBPF-Tests/blob/main/programs/kernel/router_map.c).<br>
 
* The setup is depicted in the following diagram.<br>

  <p align="center">
  <img src="IT.drawio2.png" alt="GitHub Image">
  
### 3. Error Discussion <a id="errdiscuss"></a>

The following are the possible errors during this setup and and operation

#### Systematic Errors: 

  * Setup Mistakes: If the network devices or tools aren’t set up right, they might give  wrong data.<br>
  * Wrong Normal: If don’t correctly define what’s “normal” for the network, then it might miss problems or see problems where there aren’t any.<br>
  * Configuration changes: Two teams are sharing the same device. So If any changes to the firewall configuration during the experiment may affect the output.
     
#### Random Errors:<br>

  * Sampling Slip-ups: If we only looking at a sample of our network traffic, we might get a skewed picture if our sample isn’t a good representation of the whole.<br>
  * Time Troubles: The time when we collect data can affect what we see. Network traffic can change a lot throughout the day.<br>
  * Measurement Mix-ups: Problems with our hardware or software can lead to errors in our data.
     
#### Other Potential Errors:<br>

  * Bad Data: If the data we are analyzing is missing information, has duplicates, or is recorded wrong, then our analysis won’t be accurate.<br>
  * Changing Threats: Cyber threats are always changing, and our analysis tools might not be able to keep up.<br>
  * Encryption Issues: As more network traffic gets encrypted, it’s harder to analyze for potential threats.
     
### 4.  Confidence Analysis <a id="confianalysis"></a>
* Hardware Configuration: The TP-Link WDR4900 v1 router is equipped with an 800MHz Freescale PPC P1014 CPU and supports both 2.4 GHz and 5 GHz bands. The `controller`is known for its flexibility and performance optimization capabilities.
* Bandwidth Estimation: Bandwidth is a critical factor in network performance. It’s the maximum rate of data transfer across a given path. Monitor the bandwidth usage over time to understand the capacity of this network setup.
* Network Traffic Analysis: Analyze the type and amount of traffic passing through the router. High network traffic can lead to congestion and reduced bandwidth..
* Quality of Service (QoS): If your network handles various types of traffic, consider configuring QoS rules on your router. QoS can prioritize certain types of traffic and optimize the bandwidth usage.
* External Factors: Consider external factors such as the physical placement of the router and potential interference sources. These factors can impact the signal strength and thus the network performance.
* Offload States: Offloading can improve performance by allowing the network device to bypass the kernel when sending packets. However, it’s important to note that not all processes can be offloaded.
* Testing and Validation: Conduct regular performance tests under different conditions to validate the network setup. Tools like iperf can help with this.

### 5.  Experiment Specification <a id="expspecifi"></a>

  We have planned to conduct each forwarding techniques 10 iterations with a duration of 60 seconds and by using TCP and UDP data transmission protocol. So in total the number of `tcpdump` output files are 40 numbers in each protocol. You can access the collected `tcpdump` output files [here](https://zenodo.org/uploads/new)
  
### 6.  Data Analysis <a id="dataanalysis"></a>

   For performance analysis we use python scripting. Mean, median and standard deviations are the numerical measurements that we have used. <br>
   The script that we used are displayed below and also access those files with this link. [Python Scripts](https://www.example.com)
   
### 7.  Plottting results <a id="plotresults"></a>

   For plotting the results, first we have extracted the necessary fields such as timestamp and bitrate from the individual trace files and filter it using the tools such as [tshark](https://tshark.dev/) and [tcpstat](https://linux.die.net/man/1/tcpstat) .After that we converted those trace files into .csv files. With the help of [python](https://docs.python.org/3/tutorial/index.html) scripting and [matplotlib](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html) libraries, we have plotted the individual iterations into line graphs and calculated the mean, meadian and standard deviations for each packet forwarding techniques for both protocols (TCP and UDP). Based on the calculated numerical measures, we then plotted the aggregated statistical measures into a box plot for performance comparison.

### 8.  Results <a id="results"></a>
  The results of our experiment including all the line graphs and box plots for comparison are available here. [Results]()
### 9.  Conclusions <a id="conclusion"></a>

Let's summarize the performance of the four packet processing and forwarding mechanisms:
- IP Forwarding
    - TCP: 214.5 Mbps
    - UDP: 560.1 Mbps
- IP Forwarding with Software Offloading
    - TCP: 281.6 Mbps (an increase of about 31.2% from IP Forwarding)
    - UDP: 924.7 Mbps (an growth of approximately 65.1% from IP Forwarding)
- IP Forwarding with Hardware Offloading
    - TCP: 293.2 Mbps (an increase of approximately 4.1% from IP Forwarding with Software Offloading)
    - UDP: 936.6 Mbps (an growth of about 1.Three% from IP Forwarding with Software Offloading)
- eBPF (TC)
    - TCP: 284.9 Mbps (a lower of approximately 2.8% from IP Forwarding with Hardware Offloading)
    - UDP: 965.Eight Mbps (an growth of approximately 3.1% from IP Forwarding with Hardware Offloading)

From those effects, we will finish that for each TCP and UDP, IP Forwarding with Hardware Offloading and eBPF (TC) provide the very best performance. However, the precise desire between these two would rely upon different factors including the unique necessities of the network and the talents of hardware. It’s additionally crucial to notice that whilst UDP gives higher bandwidth, it does not have the equal reliability and ordering ensures as TCP. Therefore, the selection between TCP and UDP might also depend upon the precise wishes of your application.

In phrases of development from one mechanism to the next, the maximum sizable leap in performance for both TCP and UDP is seen when transferring from IP Forwarding to IP Forwarding with Software Offloading. The next upgrades whilst shifting to IP Forwarding with Hardware Offloading and eBPF (TC) are much less said. This shows that at the same time as offloading (both software program and hardware) and eBPF (TC) can offer overall performance advantages, the most substantial improvement is received from the preliminary pass to software program offloading.

It’s also well worth noting that the performance decrease determined whilst moving from IP Forwarding with Hardware Offloading to eBPF (TC) in the case of TCP isn't always discovered in UDP. This may want to advocate that eBPF (TC) is particularly nicely-acceptable to UDP visitors.



