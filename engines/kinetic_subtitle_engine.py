# -*- coding: utf-8 -*-
"""
Kinetic Subtitle Engine for Md Sadique Amin Autonomous Ecosystem
Generates dynamic, word-by-word highlighted ASS subtitles matching high-retention Instagram Reels.
Benchmark: @21.coders vertical reel format (1080x1920, yellow highlight on active word, bold outline).
"""

import os
import re
import subprocess
import imageio_ffmpeg

def format_ass_time(seconds):
    cs = int(round((seconds - int(seconds)) * 100))
    s = int(seconds) % 60
    m = (int(seconds) // 60) % 60
    h = int(seconds) // 3600
    if cs >= 100:
        cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def get_audio_duration(file_path, ffmpeg_exe=None):
    try:
        ff = ffmpeg_exe or imageio_ffmpeg.get_ffmpeg_exe()
        cmd = [ff, "-i", file_path]
        res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True, encoding="utf-8", errors="ignore")
        m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", res.stderr)
        if m:
            h, mn, s = float(m.group(1)), float(m.group(2)), float(m.group(3))
            return h * 3600 + mn * 60 + s
    except Exception as e:
        print(f"[WARN] Error extracting duration: {e}")
    return 10.0

class KineticSubtitleEngine:
    def __init__(self, font_name="Arial", font_size=50, primary_color="&H00FFFFFF", highlight_color="&H0000E6FF"):
        self.font_name = font_name
        self.font_size = font_size
        self.primary_color = primary_color       # Pure White
        self.highlight_color = highlight_color   # Radiant Golden-Yellow (&H0000E6FF)
        self.outline_color = "&H00000000"        # Solid Black
        self.back_color = "&H80000000"           # Shadow

    def generate_ass(self, script_text, audio_duration, output_ass_path):
        clean_text = re.sub(r'\s+', ' ', script_text).strip()
        words = [w for w in clean_text.split() if w]
        if not words:
            return None

        total_words = len(words)
        sec_per_word = audio_duration / max(total_words, 1)

        chunk_size = 4
        chunks = []
        for i in range(0, total_words, chunk_size):
            chunks.append(words[i:i + chunk_size])

        header_lines = [
            "[Script Info]",
            "Title: Md Sadique Amin Kinetic Subtitles",
            "ScriptType: v4.00+",
            "WrapStyle: 0",
            "ScaledBorderAndShadow: yes",
            "YCbCr Matrix: TV.601",
            "PlayResX: 1080",
            "PlayResY: 1920",
            "",
            "[V4+ Styles]",
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
            f"Style: KineticDefault,{self.font_name},{self.font_size},{self.primary_color},&H000000FF,{self.outline_color},{self.back_color},-1,0,0,0,100,100,1,0,1,4.5,2.5,2,40,40,420,1",
            "",
            "[Events]",
            "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
        ]
        header = "\n".join(header_lines) + "\n"

        events = []
        current_word_idx = 0

        for chunk in chunks:
            chunk_word_count = len(chunk)
            chunk_start_sec = current_word_idx * sec_per_word

            for local_idx in range(chunk_word_count):
                w_start = chunk_start_sec + (local_idx * sec_per_word)
                w_end = w_start + sec_per_word
                if w_end > audio_duration:
                    w_end = audio_duration

                start_str = format_ass_time(w_start)
                end_str = format_ass_time(w_end)

                styled_words = []
                for idx, w in enumerate(chunk):
                    if idx == local_idx:
                        styled_words.append("{\\c" + self.highlight_color + "&\\b1\\fscx110\\fscy110}" + w + "{\\c" + self.primary_color + "&\\b1\\fscx100\\fscy100}")
                    else:
                        styled_words.append("{\\c" + self.primary_color + "&\\b1}" + w)

                dialogue_text = " ".join(styled_words)
                events.append(f"Dialogue: 0,{start_str},{end_str},KineticDefault,,0,0,0,,{dialogue_text}")

            current_word_idx += chunk_word_count

        os.makedirs(os.path.dirname(os.path.abspath(output_ass_path)), exist_ok=True)
        with open(output_ass_path, "w", encoding="utf-8") as f:
            f.write(header + "\n".join(events) + "\n")

        return output_ass_path

subtitle_engine = KineticSubtitleEngine()
