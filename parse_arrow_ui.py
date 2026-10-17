import xml.etree.ElementTree as ET

tree = ET.parse("phone_arrow_ui.xml")
root = tree.getroot()

for node in root.iter("node"):
    text = node.attrib.get("text", "")
    desc = node.attrib.get("content-desc", "")
    bounds = node.attrib.get("bounds", "")
    cls = node.attrib.get("class", "")
    if any(k in (text + desc).lower() for k in ["generate", "submit", "next", "arrow", "send"]) or cls == "android.widget.ImageButton" or "button" in cls.lower():
        print(f"{cls} | Text: '{text}' | Desc: '{desc}' | Bounds: {bounds}")
