import xml.etree.ElementTree as ET

tree = ET.parse("phone_ig_ui.xml")
root = tree.getroot()

for node in root.iter("node"):
    desc = node.attrib.get("content-desc", "")
    res_id = node.attrib.get("resource-id", "")
    bounds = node.attrib.get("bounds", "")
    cls = node.attrib.get("class", "")
    if any(k in desc.lower() for k in ["create", "new", "camera", "add", "post", "reel"]) or "action_bar" in res_id.lower() or "button" in cls.lower():
        print(f"ID: {res_id} | Class: {cls} | Desc: '{desc}' | Bounds: {bounds}")
