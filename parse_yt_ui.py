import xml.etree.ElementTree as ET

tree = ET.parse("phone_yt_ui.xml")
root = tree.getroot()

for node in root.iter("node"):
    text = node.attrib.get("text", "")
    desc = node.attrib.get("content-desc", "")
    bounds = node.attrib.get("bounds", "")
    cls = node.attrib.get("class", "")
    clickable = node.attrib.get("clickable", "")
    if any(k in (text + desc).lower() for k in ["create", "project", "generate", "video", "add", "plus"]):
        print(f"Class: {cls} | Clickable: {clickable} | Text: '{text}' | Desc: '{desc}' | Bounds: {bounds}")
