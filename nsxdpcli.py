#!/usr/bin/env python3
from xml.etree import ElementTree as ET
from datetime import datetime


def SubElement(parent, tag, text=None, attributes={}):
    e = ET.SubElement(parent, tag, attrib=attributes)
    e.text = text
    return e

def createDescription(parent):
    root = SubElement(parent, tag="vib", attrib={"version": "5.0"})
    SubElement(root, tag="type", text="bootbank")
    SubElement(root, tag="name", text="esxcli-nsx")
    SubElement(root, tag="version", text="0.0.0.1")
    SubElement(root, tag="vendor", text="Dixon Ly")
    SubElement(root, tag="summary", text="ESXCLI extensions for NSX networking and security")
    SubElement(root, tag="description", text="ESXCLI extensions for NSX networking and security")
    SubElement(root, tag="release-date", text=str(datetime.now()))
    SubElement(root, tag="urls", text="https://github.com/dixonly")
    r = SubElement(root, tag="relationships")
    SubElement(r, tag="depends")
    SubElement(r, tag="conflicts")
    SubElement(r, tag="replaces")
    SubElement(r, tag="provides")
    SubElement(r, tag="compatibleWith")
    SubElement(root, tag="software-tags")
    q = SubElement(root, tag="system-requires")
    SubElement(q, tag="maintenance-mode", text="false")
    filelist = SubElement(root, "file-list")
    for f in files:
        fx = SubElement(filelist, tag="file", text=f)

    SubElement(root, tag="acceptance-level", text="community")
    SubElement(root, tag="live-install-allowed", text="true")
    SubElement(root, tag="live-remove-allowed", text="true")
    SubElement(root, tag="cimon-restart", text="false")
    SubElement(root, tag="stateless-ready", text="true")
    SubElement(root, tag="overlay", text="false")
    p = SubElement(root, tag="payloads")
    SubElement(p, tag="payload", attributes={"name":"esxcli-nsx", "type":"tgz", "size":"14411"})
    SubElement(p, tag="checksum", attributes={"checksum-type":"sha-256"}, text="asdfaskkfdjlakdfsjdaslfd")
    return root

def createNsxDpCliNs(parent):
    ns = SubElement(parent, tag="namespaces")
    n = SubElement(ns, tag="namespace", attributes = {"path":"nsxdpcli"})
    SubElement(n, tag="description", text = "nsxdp-cli commands")

    n = SubElement(ns, tag="namespace", attributes={"path":"nsxdpcli.ens"})
    SubElement(n, tag="description", text = "nsxdp-cli ENS commands")

    n = SubElement(ns, tag="namespace", attributes={"path":"nsxdpcli.ens.switch"})
    SubElement(n, tag="description", text = "nsxdp-cli ens switch subcommands")

    n = SubElement(ns, tag="namespace", attributes={"path":"nsxdpcli.ens.port"})
    SubElement(n, tag="description", text = "nsxdp-cli ens port subcommands")

    n = SubElement(ns, tag="namespace", attributes={"path":"nsxdpcli.ens.uplink"})
    SubElement(n, tag="description", text = "nsxdp-cli ens uplink subcommands")

    n = SubElement(ns, tag="namespace", attributes={"path":"nsxdpcli.bfd"})
    SubElement(n, tag="description", text = "nsxdp-cli BFD commands")
    return ns

def createNsxDpCli(parent):
    cli = SubElement(parent, tag="commands")

    c = SubElement(cli, tag="command", attributes={"path":"nsxdpcli.netdvs"})
    SubElement(c, tag="description", text="Show the ENS switches on host")
    inputspec = SubElement(c, tag="input-spec")
    outputspec = SubElement(c, tag="output-spec")
    SubElement(outputspec, tag="string")
    formatparam = SubElement(c, tag="format-parameters")
    SubElement(formatparam, tag="formatter", text="simple")
    SubElement(c, tag="execute", text="/opt/esxcliext/bin/esxcli-nsxdpcli.sh netdvs dump")
    
    c = SubElement(cli, tag="command", attributes={"path":"nsxdpcli.ens.switch.list"})
    SubElement(c, tag="description", text="Show the ENS switches on host")
    inputspec = SubElement(c, tag="input-spec")
    outputspec = SubElement(c, tag="output-spec")
    SubElement(outputspec, tag="string")
    formatparam = SubElement(c, tag="format-parameters")
    SubElement(formatparam, tag="formatter", text="simple")
    SubElement(c, tag="execute", text="/opt/esxcliext/bin/esxcli-nsxdpcli.sh ens switch list")
    
    c = SubElement(cli, tag="command", attributes={"path":"nsxdpcli.ens.port.list"})
    SubElement(c, tag="description", text="List all the uplink and vnic ports")
    inputspec = SubElement(c, tag="input-spec")
    inputparam = SubElement(inputspec, tag="parameter", attributes={"name":"swid", "type":"string", "required":"false"})
    SubElement(inputparam, tag="description", text="swId from ENS switch list")
    outputspec = SubElement(c, tag="output-spec")
    SubElement(outputspec, tag="string")
    formatparam = SubElement(c, tag="format-parameters")
    SubElement(formatparam, tag="formatter", text="simple")
    SubElement(c, tag="execute", text='/opt/esxcliext/bin/esxcli-nsxdpcli.sh ens port list $if{swid, "$val{"swid"}"}')
    
    
    c = SubElement(cli, tag="command", attributes={"path":"nsxdpcli.ens.port.stats"})
    SubElement(c, tag="description", text="Get Stats for an ensPID, get ensPID from port list")
    inputspec = SubElement(c, tag="input-spec")
    inputparam = SubElement(inputspec, tag="parameter", attributes={"name":"enspid", "type":"string", "required":"true"})
    SubElement(inputparam, tag="description", text="ensPID retrieved from port listing")
    outputspec = SubElement(c, tag="output-spec")
    SubElement(outputspec, tag="string")
    formatparam = SubElement(c, tag="format-parameters")
    SubElement(formatparam, tag="formatter", text="simple")
    SubElement(c, tag="execute", text='/opt/esxcliext/bin/esxcli-nsxdpcli.sh ens port stats get --port-id "$val{"enspid"}"')
    
    
    c = SubElement(cli, tag="command", attributes={"path":"nsxdpcli.ens.uplink.rss"})
    SubElement(c, tag="description", text="Display RSS info for an uplink")
    inputspec = SubElement(c, tag="input-spec")
    inputparam = SubElement(inputspec, tag="parameter", attributes={"name":"uplink", "type":"string", "required":"true"})
    SubElement(inputparam, tag="description", text="Uplink name, i.e. vmnic0, vmnic1, etc from port listing")
    outputspec = SubElement(c, tag="output-spec")
    SubElement(outputspec, tag="string")
    formatparam = SubElement(c, tag="format-parameters")
    SubElement(formatparam, tag="formatter", text="simple")
    SubElement(c, tag="execute", text='/opt/esxcliext/bin/esxcli-nsxdpcli.sh ens uplink rss list --uplink "$val{"uplink"}"')

    c = SubElement(cli, tag="command", attributes={"path":"nsxdpcli.bfd.stats"})
    SubElement(c, tag="description", text="Show the ENS switches on host")
    inputspec = SubElement(c, tag="input-spec")
    outputspec = SubElement(c, tag="output-spec")
    SubElement(outputspec, tag="string")
    formatparam = SubElement(c, tag="format-parameters")
    SubElement(formatparam, tag="formatter", text="simple")
    SubElement(c, tag="execute", text="/opt/esxcliext/bin/esxcli-nsxdpcli.sh bfd stats get")
    
    c = SubElement(cli, tag="command", attributes={"path":"nsxdpcli.bfd.sessions"})
    SubElement(c, tag="description", text="Show the ENS switches on host")
    inputspec = SubElement(c, tag="input-spec")
    outputspec = SubElement(c, tag="output-spec")
    SubElement(outputspec, tag="string")
    formatparam = SubElement(c, tag="format-parameters")
    SubElement(formatparam, tag="formatter", text="simple")
    SubElement(c, tag="execute", text="/opt/esxcliext/bin/esxcli-nsxdpcli.sh bfd sessions list")
    
    return cli
                            
    

def createNsxdpcliExt(filename):
    root=ET.Element("plugin", attrib={"xmlns":"http://www.vmware.com/Products/ESX/5.0/esxcil/"})
    SubElement(root, tag="version", text="1.0.0")
    createNsxDpCliNs(root)
    createNsxDpCli(root)
    tree = ET.ElementTree(root)
    ET.indent(tree, '    ')
    with open(filename, 'wb') as f:
        tree.write(f, xml_declaration=True)
    

def main():
    createNsxdpcliExt("nsx-nsxdpcli.xml")
    
if __name__ == '__main__':
    main()    
