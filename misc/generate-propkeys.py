import os, sys
import re

TEMPLATE = re.compile("DEFINE_PROPERTYKEY\(PKEY_(\w+), ([0-9A-Fx, ]+)\)")

source = r"C:\Program Files\Microsoft SDKs\Windows\v7.0\Include\propkey.h"
for a, b in TEMPLATE.findall(open(source).read()):
    print [i.strip() for i in b.split(",")]