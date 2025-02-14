#!/usr/bin/env python3
from xml.etree import ElementTree as ET
from datetime import datetime


def SubElement(parent, tag, text=None, attributes={}):
    e = ET.SubElement(parent, tag, attrib=attributes)
    e.text = text
    return e

def createNetstatsNs(parent):
    ns = SubElement(parent, tag="namespaces")
    n = SubElement(ns, tag="namespace", attributes = {"path":"netstats"})
    SubElement(n, tag="description", text = "net-stats commands")

    return ns

def createNetstatsCli(parent):
    cli = SubElement(parent, tag="commands")

    c = SubElement(cli, tag="command", attributes={"path":"netstats.ports"})
    SubElement(c, tag="description", text="Run net-stats -l")
    inputspec = SubElement(c, tag="input-spec")
    outputspec = SubElement(c, tag="output-spec")
    SubElement(outputspec, tag="string")
    formatparam = SubElement(c, tag="format-parameters")
    SubElement(formatparam, tag="formatter", text="simple")
    SubElement(c, tag="execute", text="/opt/esxcliext/bin/esxcli-netstats.sh -l")
    
    c = SubElement(cli, tag="command", attributes={"path":"netstats.syntax"})
    SubElement(c, tag="description", text="Run net-stats -h")
    inputspec = SubElement(c, tag="input-spec")
    outputspec = SubElement(c, tag="output-spec")
    SubElement(outputspec, tag="string")
    formatparam = SubElement(c, tag="format-parameters")
    SubElement(formatparam, tag="formatter", text="simple")
    SubElement(c, tag="execute", text="/opt/esxcliext/bin/esxcli-netstats.sh -h")

    c = SubElement(cli, tag="command", attributes={"path":"netstats.stats"})
    SubElement(c, tag="description", text="Run net-stats -A -t <stats> -i <interval>")
    inputspec = SubElement(c, tag="input-spec")
    inputparam = SubElement(inputspec, tag="parameter", attributes={"name":"stats", "type":"string", "required":"false"})
    SubElement(inputparam, tag="description", text="net-stats -t options")
    inputparam = SubElement(inputspec, tag="parameter", attributes={"name":"interval", "type":"string", "required":"false"})
    SubElement(inputparam, tag="description", text="net-stats -i <interval> option")
    outputspec = SubElement(c, tag="output-spec")
    SubElement(outputspec, tag="string")
    formatparam = SubElement(c, tag="format-parameters")
    SubElement(formatparam, tag="formatter", text="simple")
    SubElement(c, tag="execute", text="/opt/esxcliext/bin/esxcli-netstats.sh -A $if{stats, -t $val{stats}} $if{interval, -i $val{interval}}")
    
    return cli
                            

def createNetstatsExt(filename):
    root=ET.Element("plugin", attrib={"xmlns":"http://www.vmware.com/Products/ESX/5.0/esxcil/"})
    SubElement(root, tag="version", text="1.0.0")
    createNetstatsNs(root)
    createNetstatsCli(root)
    tree = ET.ElementTree(root)
    ET.indent(tree, '    ')
    with open(filename, 'wb') as f:
        tree.write(f, xml_declaration=True, encoding='utf-8')
                   
def main():    
    createNetstatsExt("nsx-netstats.xml")
    
if __name__ == '__main__':
    main()    
