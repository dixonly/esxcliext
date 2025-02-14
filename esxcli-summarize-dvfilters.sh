#!/bin/sh
# summarize-dvfilter
echo "<?xml version=\"1.0\" ?>"
echo "<output xmlns=\"http://www.vmware.com/Products/ESX/5.0/esxcli/\">"
echo -n "<string><![CDATA["
/bin/summarize-dvfilter
echo "]]></string>"
echo "</output>"


