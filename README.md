## Extensions for esxcli for NSX networking and security

NSX operations and troubleshooting sometimes require root shell access to execute CLIs.  This is not always convenient as we recommend that SSH to the ESXi be disabled by default; and even when enabled, the root password should only be accessible through a secure vault.  ESXi does provide the "esxcli" command its family of sub-commands that can executed remotely; and the sessions can be authenticated through vCenter PSC credentials. 

However, not all the "useful" CLIs for NSX network and security operations are available through esxcli.  This project extends esxcli to support some of the more command CLIs.

The new sub-commands added are:
 - nsxcli - Same as running "nsxcli -c <command>"
 - nsxdpcli - Same as running nsxdp-cli
 - netstats - Same as running net-stats
 - vsip - same as running vsipioctl

Not all the options of nsxcli and nsxdpcli are exposed.  If you need other commands or sub-commmands implemented, let me know.  I will avoid adding non-read-only support; for vsipioctl, I do allow for the command options that reset stats or counters to 0.

In order for vsipioctl to be useful, the output of summarize-dvfilter is already required.  I've added that as a sub-command under vsip.

## Build
A pre-build copy of th esxcli-nsx-ext.vib is already included in the repository - I have only tested this VIB on ESXi8.  If you want to recreate it, run the python script vibcreate.py to generate the extensions and create the esxcli-nsx-ext.vib.  The host running vibcreate.py must have the python extensions specified in the python import list, tar, gzip, and ar. 

```text
$ ./vibcreate.py
Removing existing output files and directories...
Creating output directories: opt/esxcliext/bin, usr/lib/vmware/esxcli/ext
Generating esxcli extensions
Creating tar bundle for VIB payload
Creating gzip file of tar bundle for VIB payload
Creating descriptor.xml for VIB
Creating the vib: esxcli-nsx-ext.vib

```

## Install
The VIB must be installed onto the ESXi host.  Copy the esxcli-nsx-ext.vib to a an accessible filesystem on the host or a URL that's reachable from the host.  Use ESXCLI to install the vib.  For example, to install the VIB at the ESXi root shell from a local file system:

```text
[root@vesxi-001:~] esxcli software vib install -v file:/tmp/esxcli-nsx-ext.vib
Installation Result
   Message: Operation finished successfully.
   VIBs Installed: esxcliext_bootbank_esxcli-nsx-ext_1.0.0-0.0.0
   VIBs Removed:
   VIBs Skipped:
   Reboot Required: false
   DPU Results:

```

The installation of the vib can be done without entering host maintenance mode or reboot.  However, after installation, you must restart hostd on the ESXi host for the new extensions to become available.

```text

[root@vesxi-001:~] /etc/init.d/hostd restart
hostd stopped.
hostd started.
[root@vesxi-001:~]

```

After restart hostd, the nestats, nsxcli, nsxdpcli and vsip namespace commands will be available:

```text

[root@vesxi-001:~] esxcli
Usage: esxcli [options] {namespace}+ {cmd} [cmd options]

Options:
  --formatter=FORMATTER
                        Override the formatter to use for a given command. Available formatters: xml, csv, keyvalue.
  --screen-width=SCREENWIDTH
                        Use the specified screen width when formatting text.
  --debug               Enable debug or internal use options.
  --log-verbose         Enable verbose logging.
  -?, --help            Display usage information.

Available Namespaces:
  daemon                Commands for controlling daemons built with Daemon SDK (DSDK).
  device                Device manager commands
  esxcli                Commands that operate on the esxcli system itself allowing users to get additional information.
  fcoe                  VMware FCOE commands. (Deprecated)
  graphics              VMware graphics commands.
  hardware              VMKernel hardware properties and commands for configuring hardware.
  iscsi                 VMware iSCSI commands.
  netstats              net-stats commands
  network               Operations that pertain to the maintenance of networking on an ESX host. This includes a wide variety of commands to manipulate virtual networking components (vswitch,
                        portgroup, etc) as well as local host IP, DNS and general host networking settings.
  nsxcli                nsxcli commands
  nsxdpcli              nsxdp-cli commands
  nvme                  VMware NVMe driver operations.
  rdma                  Operations that pertain to remote direct memory access (RDMA) protocol stack on an ESX host.
  sched                 VMKernel system properties and commands for configuring scheduling related functionality.
  software              Manage the ESXi software image and packages
  storage               VMware storage commands.
  system                VMKernel system properties and commands for configuring properties of the kernel core system and related system services.
  vm                    A small number of operations that allow a user to Control Virtual Machine operations.
  vsan                  VMware vSAN commands
  vsip                  vsipioctl commands


[root@vesxi-001:~] esxcli netstats
Usage: esxcli netstats {cmd} [cmd options]

Available Commands:
  ports                 Run net-stats -l
  stats                 Run net-stats -A -t <stats> -i <interval>
  syntax                Run net-stats -h
  
[root@vesxi-001:~] esxcli netstats ports
PortNum          Type SubType SwitchName       MACAddress         ClientName
2214592518          4       0 DvsPortset-0     00:50:56:01:10:01  vmnic0
2214592520          4       0 DvsPortset-0     00:50:56:01:20:01  vmnic1
67108874            3       0 DvsPortset-0     00:50:56:01:10:01  vmk0
67108875            3       0 DvsPortset-0     00:50:56:63:68:04  vmk1
67108876            3       0 DvsPortset-0     00:50:56:63:f6:da  vmk10
67108877            3       0 DvsPortset-0     00:50:56:6a:15:43  vmk11
67108878            3       0 DvsPortset-0     00:50:56:67:94:82  vmk50
67108879            0       0 DvsPortset-0     02:50:56:56:44:52  vdr-vdrPort
67108880            5       9 DvsPortset-0     00:0c:29:07:d0:b6  infravisor-pod.eth0
67108881            5       9 DvsPortset-0     00:50:56:a2:ec:46  vedge3.eth4
67108882            5       9 DvsPortset-0     00:50:56:a2:26:57  vedge3.eth3
67108883            5       9 DvsPortset-0     00:50:56:a2:38:94  vedge3.eth2
67108884            5       9 DvsPortset-0     00:50:56:a2:c7:1e  vedge3.eth1
67108885            5       9 DvsPortset-0     00:50:56:a2:f9:3d  vedge3.eth0


```

There should be plenty of documents and how-tos on executng esxcli remotely or via PowerCLI.

