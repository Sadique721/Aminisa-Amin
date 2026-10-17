import xml.etree.ElementTree as ET

tree = ET.parse("phone_full_share_ui.xml")
root = tree.getroot()

for node in root.iter("node"):
    text = node.attrib.get("text", "")
    desc = node.attrib.get("content-desc", "")
    res_id = node.attrib.get("resource-id", "")
    bounds = node.attrib.get("bounds", "")
    cls = node.attrib.get("class", "")
    if any(k in (text+desc).lower() for k in ["threads", "facebook", "ai label", "next", "share", "story", "draft"]):
        print(f"ID: {res_id} | Class: {cls} | Text: '{text}' | Desc: '{desc}' | Bounds: {bounds}")
