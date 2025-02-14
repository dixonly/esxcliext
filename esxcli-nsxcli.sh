#!/bin/sh
# nsxdp-cli
echo "<?xml version=\"1.0\" ?>"
echo "<output xmlns=\"http://www.vmware.com/Products/ESX/5.0/esxcli/\">"
echo -n "<string><![CDATA["
/bin/nsxcli --cmd  "$@"
echo "]]></string>"
echo "</output>"


