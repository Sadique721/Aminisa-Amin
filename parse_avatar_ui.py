import xml.etree.ElementTree as ET

tree = ET.parse("phone_avatar_ui.xml")
root = tree.getroot()

for node in root.iter("node"):
    text = node.attrib.get("text", "")
    desc = node.attrib.get("content-desc", "")
    bounds = node.attrib.get("bounds", "")
    cls = node.attrib.get("class", "")
    if any(k in (text + desc).lower() for k in ["agree", "no thanks", "close", "cancel", "x"]):
        print(f"{cls} | Text: '{text}' | Desc: '{desc}' | Bounds: {bounds}")
