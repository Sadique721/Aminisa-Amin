import xml.etree.ElementTree as ET

tree = ET.parse("phone_ig_ui.xml")
root = tree.getroot()

for node in root.iter("node"):
    text = node.attrib.get("text", "")
    desc = node.attrib.get("content-desc", "")
    res_id = node.attrib.get("resource-id", "")
    bounds = node.attrib.get("bounds", "")
    if any(k in res_id.lower() for k in ["title", "user", "name", "account", "header"]) or any(k in (text+desc).lower() for k in ["post", "edit", "share", "md_sadique_amin", "profile"]):
        print(f"ID: {res_id} | Text: '{text}' | Desc: '{desc}' | Bounds: {bounds}")
