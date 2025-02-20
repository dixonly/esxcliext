## Extensions for esxcli for NSX networking and security

NSX operations and troubleshooting sometimes require root shell access to execute CLIs.  This is not always convenient as we recommend that SSH to the ESXi be disabled by default; and even when enabled, the root password should only be accessible through a secure vault.  ESXi provides the "esxcli" command and its family of sub-commands that can executed remotely; and the sessions can be authenticated through vCenter PSC credentials. 

However, not all the "useful" CLIs for NSX network and security operations are available through esxcli.  This project extends esxcli to support some of the more common CLIs.

The new sub-commands added are:
 - nsxcli - Same as running "nsxcli -c <command>"
 - nsxdpcli - Same as running nsxdp-cli
 - netstats - Same as running net-stats
 - vsip - same as running vsipioctl

Not all the options of nsxcli and nsxdp-cli are exposed.  If you need other commands or sub-commmands implemented, let me know.  I will avoid adding non-read-only support; for vsipioctl, I do allow for the command options that reset stats or counters to 0.

In order for vsipioctl to be useful, the output of summarize-dvfilter is already required.  I've added that as a sub-command under vsip.  

## Build
A pre-built copy of the esxcli-nsx-ext.vib is already included in the repository - I have only tested this VIB on ESXi8.  If you want to recreate it, run the python script vibcreate.py to generate the extensions and create the esxcli-nsx-ext.vib.  The host running vibcreate.py must have the python extensions specified in the python import list, tar, gzip, and ar. 

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
The VIB must be installed onto the ESXi host.  Copy the esxcli-nsx-ext.vib to a an accessible filesystem on the host or a URL that's reachable from the host.  Use ESXCLI to install the vib.  For example, use the following procedure to install the VIB at the ESXi root shell from a local file system.

This VIB is community supported; as such, your ESXi host's software acceptance level must be set to CommunitySupported.  If it's not set, then you'll ge this error during install:

```text
[root@vesxi-002:/tmp] esxcli software vib install -v file:/tmp/esxcli-nsx-ext.vib
 [AcceptanceConfigError]
 VIB esxcliext_bootbank_esxcli-nsx-ext_1.0.0-0.0.0's acceptance level is community, which is not compliant with the ImageProfile acceptance level partner
 To change the host acceptance level, use the 'esxcli software acceptance set' command.
 Please refer to the log file for more details.
```

Use the CLI 'esxcli software acceptance get' to find the current acceptance level.  Use 'esxcli software acceptance set --level=CommunitySupported' to change the acceptance level. Then use esxcli to install the vib.


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


## TO be resolved
I've found that the VIB that's created by vibcreate.py does not always install successfully.  For example, you could run into this error during VIB install:

```text

 Output: The old parameter format is deprecated, please switch to the new format. See secureMount.py -h for more details.
 ERROR:root:Failed to mount: [Errno 1] Operation not permitted: '/tardisks/esxcli_n.t00'
 Traceback (most recent call last):
   File "/lib64/python3.11/shutil.py", line 856, in move
 OSError: [Errno 22] Invalid argument: '/usr/lib/vmware/lifecycle/stageliveimage/data/esxcli_n.t00' -> '/tardisks/esxcli_n.t00'

 During handling of the above exception, another exception occurred:

 Traceback (most recent call last):
   File "/usr/lib/vmware/secureboot/bin/secureMount.py", line 372, in legacyParsing
     MountTardisk(True, FindVibInDB(sys.argv[1]), sys.argv[2], sys.argv[3])
   File "/usr/lib/vmware/secureboot/bin/secureMount.py", line 157, in MountTardisk
     shutil.move(tardiskPath, dest)
   File "/lib64/python3.11/shutil.py", line 876, in move
   File "/lib64/python3.11/shutil.py", line 448, in copy2
   File "/lib64/python3.11/shutil.py", line 258, in copyfile
 PermissionError: [Errno 1] Operation not permitted: '/tardisks/esxcli_n.t00'

```

I have yet been able to explain why this is happening; the most likely suspect is the usage of the gzip library in Python.  Regardless, any VIBs that I manually create can be installed successfully.  If the vib created by vibcreate.py is not working for you, try the following procedure:

1. run vibcreate.py to generate the contents of the "usr" and "opt" directories
2. Create the tar bundle: tar cvf esxcli-nsx-ext opt usr
3. Take the sha-256 and sha-1 checksums of the tar bundle
   - sha256sum esxcli-nsx-ext.tar
   - sha1sum esxcli-nsx-ext.tar
4. Compress the tar file with gzip: gzip esxcli-nsx-ext.tar
   This should create esxcli-nsx-ext.tar.gz
5. Rename esxcli-nsx-ext.tar.gz to esxcli-nsx-ext
6. Update descriptor.xml to reflect the size of your esxcli-nsx-ext file, and update the checksums in the file:

relevant section:
   - change the size
   - update the first sha-256 checksum to contain the checksum of your esxcli-nsx-ext.tar.gz
   - update the second sha-256 checksum to contain the checksum of your esxcli-nsx-ext.tar
   - update the sha-1 checksum to contain the sha1 checksum of your esxcli-nsx-ext.tar
```text
        <payload name="esxcli-nsx-ext" type="tgz" size="5454">
            <checksum checksum-type="sha-256">b6dc176972ae5e5d5e6a62a7d402a1d1d1da2c122a7b37bad7f788f6c133f890</checksum>
            <checksum checksum-type="sha-256" verify-process="gunzip">e49b46bcf9a22f674354be7cd55a3868d85108e6ea36cab15c2833d44a9683aa</checksum>
            <checksum checksum-type="sha-1" verify-process="gunzip">efff74fce3dc9f02103291ceb7928dca5fa4a810</checksum>
        </payload>
```
7. Create the vib: ar r esxcli-nsx-ext.vib descriptor.xml sig.pkcs7 esxcli-nsx-ext


   
