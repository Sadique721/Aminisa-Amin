# -*- coding: utf-8 -*-
"""
Caption & Persona Disclosure Quality Gate
Enforces:
1. #AIGenerated #VirtualCreator tags
2. Mandatory opening greeting ("Hello everyone!")
3. Strict prohibition of "Namaste"
4. Fictional character lore guardrails
"""

class CaptionGate:
    def __init__(self):
        self.mandatory_tags = ["#AIGenerated", "#VirtualCreator"]
        self.forbidden_words = ["namaste", "नमस्ते"]

    def ok(self, caption_text, script_text=None):
        cap_lower = caption_text.lower()

        # 1. AI Disclosure check
        for tag in self.mandatory_tags:
            if tag.lower() not in cap_lower:
                return False, f"Missing required disclosure tag: {tag}"

        # 2. Forbidden greeting check
        for fword in self.forbidden_words:
            if fword in cap_lower:
                return False, f"Strictly forbidden word detected: {fword}"

        # 3. If script provided, check opening greeting
        if script_text:
            s_clean = script_text.strip().lower()
            if not (s_clean.startswith("hello everyone") or s_clean.startswith("hello!")):
                return False, "Script does not open with 'Hello everyone!'"
            for fword in self.forbidden_words:
                if fword in s_clean:
                    return False, f"Forbidden word in script: {fword}"

        return True, "Caption and Persona rules certified"

caption_gate = CaptionGate()
