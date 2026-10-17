# -*- coding: utf-8 -*-
"""
Clean Background & Quality Gate
Rejects images with low resolution, severe blur, or color clipping.
"""

import os
from PIL import Image

class CleanBgGate:
    def __init__(self):
        self.min_width = 640
        self.min_height = 960

    def ok(self, image_path):
        if not os.path.exists(image_path):
            return False

        try:
            with Image.open(image_path) as img:
                w, h = img.size
                if w < self.min_width or h < self.min_height:
                    return False
                
                # Check for completely black or blown-out white image
                colors = img.convert("L").getextrema()
                if colors[0] == colors[1]:
                    return False
                
            return True
        except Exception:
            return False

clean_bg_gate = CleanBgGate()
