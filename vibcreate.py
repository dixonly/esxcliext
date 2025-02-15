#!/usr/bin/env python3
from xml.etree import ElementTree as ET
import datetime
import os
import shutil
import netstats
import nsxcli
import nsxdpcli
import vsipioctl
import tarfile
import hashlib
import gzip
import subprocess

def SubElement(parent, tag, text=None, attributes={}):
    e = ET.SubElement(parent, tag, attrib=attributes)
    e.text = text
    return e

def main():
    version="1.0.0-0.0.0"
    vibname = "esxcli-nsx-ext"
    vibfile = vibname + ".vib"
    sigfile = "sig.pkcs7"
    descriptor = "descriptor.xml"
    scripts = ["esxcli-netstats.sh", "esxcli-nsxcli.sh", "esxcli-nsxdpcli.sh", "esxcli-summarize-dvfilters.sh", "esxcli-vsipioctl.sh"]
    vib_bin_dir = "opt/esxcliext/bin"
    vib_ext_dir = "usr/lib/vmware/esxcli/ext"

    files = {}
    files["netstats"]  = {"script": "esxcli-netstats.sh", "ext": "nsx-netstats.xml"}
    files["nsxcli"] = {"script": "esxcli-nsxcli.sh", "ext": "nsx-nsxcli.xml"}
    files["nsxdpcli"] = {"script": "esxcli-nsxdpcli.sh", "ext":"nsx-nsxdpcli.xml"}
    files["dvfilters"] = {"script": "esxcli-summarize-dvfilters.sh", "ext":""}
    files["vsipioctl"] = {"script": "esxcli-vsipioctl.sh", "ext": "nsx-vsipioctl.xml"}

    print("Removing existing output files and directories...")
    if os.path.exists(vib_bin_dir):
        shutil.rmtree(vib_bin_dir)
    if os.path.exists(vib_ext_dir):
        shutil.rmtree(vib_ext_dir)
    if os.path.exists(descriptor):
        os.remove(descriptor)
    if os.path.exists(sigfile):
        os.remove(sigfile)
    if os.path.exists(vibfile):
        os.remove(vibfile)

    print("Creating output directories: %s, %s" %(vib_bin_dir, vib_ext_dir))
    os.makedirs(vib_bin_dir)
    os.makedirs(vib_ext_dir)

    print("Generating esxcli extensions")
    for f in files.keys():
        if f == "netstats":
            netstats.createNetstatsExt(vib_ext_dir + "/" + files[f]["ext"])
            os.chmod(vib_ext_dir + "/" + files[f]["ext"], 0o444)
        elif f == "nsxcli":
            nsxcli.createNsxcliExt(vib_ext_dir + "/" + files[f]["ext"])
            os.chmod(vib_ext_dir + "/" + files[f]["ext"], 0o444)
        elif f == "nsxdpcli":
            nsxdpcli.createNsxdpcliExt(vib_ext_dir + "/" + files[f]["ext"])
            os.chmod(vib_ext_dir + "/" + files[f]["ext"], 0o444)
        elif f == "vsipioctl":
            vsipioctl.createVsipExt(vib_ext_dir + "/" + files[f]["ext"])
            os.chmod(vib_ext_dir + "/" + files[f]["ext"], 0o444)
        shutil.copy(files[f]["script"], vib_bin_dir)
        os.chmod(files[f]["script"], 0o555)

    # Create the tar bundle
    # for whatever reason, using tarfile to create the tar file
    # results in vib tail fails to install
    '''
    tar = tarfile.open(vibname + ".tar", "w:")
    tar.add(vib_bin_dir)
    tar.add(vib_ext_dir)
    '''
    print("Creating tar bundle for VIB payload")
    r = subprocess.run(["tar", "cf", vibname+".tar", vib_bin_dir, vib_ext_dir])
    #print(r.stdout)


    tar = tarfile.open(vibname+".tar", "r:")
    vib_payload = []
    for tf in tar.getmembers():
        if tf.isfile():
            vib_payload.append(tf.name)
    tar.close()

    # Get sha256 and sha1 chksums of the tar fil
    vibtar = open(vibname + ".tar", "rb")
    data = vibtar.read()
    h256 = hashlib.sha256(data).hexdigest()
    h1 = hashlib.sha1(data).hexdigest()
    #print("sha256- "+ h256)
    #print("sha1- " + h1)
    vibtar.seek(0)
    print("Creating gzip file of tar bundle for VIB payload")

    # gz compress the tar file
    vibgz = gzip.open(vibname, "wb")
    vibgz.writelines(vibtar)
    vibtar.close()
    vibgz.close()

    # get sha256 chksum of the gz file
    total = os.path.getsize(vibname)
    #print("vib size is %d" %total)
    vibgz = open(vibname, "rb")
    vibdata = vibgz.read()
    gzhash = hashlib.sha256(vibdata).hexdigest()
    #print("gz sha256 - " + gzhash)

    print("Creating descriptor.xml for VIB")
    #create the vib descriptor file
    vibdesc = ET.Element("vib", attrib={"version": "5.0"})
    SubElement(vibdesc, tag="type", text="bootbank")
    SubElement(vibdesc, tag="name", text=vibname)
    SubElement(vibdesc, tag="version", text=version)
    SubElement(vibdesc, tag="vendor", text="esxcliext")
    SubElement(vibdesc, tag="summary", text="esxcli extensions for NSX networking & security")
    SubElement(vibdesc, tag="description", text="esxcli extensions for nsxcli, nsxdp-cli, summarize-dvfilter, vsipioctl")
    SubElement(vibdesc, tag="release-date", text=str(datetime.datetime.now()))
    url = SubElement(vibdesc, tag="urls")
    SubElement(url, tag="url", attributes={"key": "website"}, text="https://github.com/dixonly")
    rel = SubElement(vibdesc, tag="relationships")
    SubElement(rel, tag="depends")
    SubElement(rel, tag="conflicts")
    SubElement(rel, tag="replaces")
    SubElement(rel, tag="provides")
    SubElement(rel, tag="compatbileWith")
    SubElement(vibdesc,tag="software-tags")
    req = SubElement(vibdesc, tag="system-requires")
    SubElement(req, tag="maintenance-mode", text="false")
    files = SubElement(vibdesc, "file-list")
    for f in vib_payload:
        SubElement(files, tag="file", text=f)
    SubElement(vibdesc, tag="acceptance-level", text="community")
    SubElement(vibdesc, tag="live-install-allowed", text="true")
    SubElement(vibdesc, tag="live-remove-allowed", text="true")
    SubElement(vibdesc, tag="cimom-restart", text="false")
    SubElement(vibdesc, tag="stateless-ready", text="true")
    SubElement(vibdesc, tag="overlay", text="false")
    p = SubElement(vibdesc, tag="payloads")
    pname = SubElement(p, tag="payload",
                       attributes={"name":vibname, "type":"tgz", "size":str(total)})
    SubElement(pname, tag="checksum",
               attributes={"checksum-type":"sha-256"},
               text=gzhash)
    SubElement(pname, tag="checksum",
               attributes={"checksum-type": "sha-256", "verify-process": "gunzip"},
               text=h256)
    SubElement(pname, tag="checksum",
               attributes={"checksum-type": "sha-1", "verify-process": "gunzip"},
               text=h1)

    tree = ET.ElementTree(vibdesc)
    ET.indent(tree, '    ')
    with open(descriptor, "wb") as f:
        tree.write(f)

    open(sigfile, "a").close()

    print("Creating the vib: %s" % vibname + ".vib")
    r = subprocess.run(["ar","r", vibname + ".vib", descriptor, sigfile, vibname],
                       capture_output=True, text=True)
    print(r.stdout)
                       
    
if __name__ == '__main__':
    main()

    


