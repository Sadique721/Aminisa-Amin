from engines.reel_composer import compose_vertical_reel
import os

img = r"md_sadique_amin-images\01_md_sadique_amin_clean_portrait_kurta.jpg"
audio = r"voice_output\md_sadique_amin_grand_welcome_voice.mp3"
out = compose_vertical_reel(img, audio, "md_sadique_amin_official_grand_welcome_reel.mp4")
print("[+] Re-rendered Grand Welcome Reel successfully:", out)
