import lxml.etree as ET
dom=ET.parse('a-wolf-lying-in-wait.xml')

xslt=ET.parse('stylesheet.xsl')

transform=ET.XSLT(xslt)

newdom=transform(dom)

print(ET.tostring(newdom, pretty_print=True))

with open("a-wolf-lying-in-wait.html", "wb") as f:
    f.write(ET.tostring(newdom, pretty_print=True))