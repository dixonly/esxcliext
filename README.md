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

