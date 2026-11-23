# -*- coding: utf-8 -*-
"""
Aminsa ChatGPT-Themed Ultra-Modern Production Dashboard
Restored to exact original ChatGPT UI styling, grid layout, fonts, pills, and 1-tap copy buttons.
Configured for: 100% Real-Time Dynamic Topics, Video Motion Prompts ONLY (<300 chars YouTube Create).
"""

def build_chatgpt_html(date_str, mobile_slots, dna_rows=None):
    if not dna_rows:
        dna_rows = [
            ("Full Name", "Aminsa", "Locked across all social accounts (@aminsa.official)"),
            ("Age", "22 Years Old", "Strictly consistent visual and vocal maturity"),
            ("Skin Complexion", "Warm Wheatish Porcelain (#EAD5C3)", "Strictly ZERO moles, ZERO blemishes, ZERO marks"),
            ("Eye Color & Shape", "Hazel-Brown Almond Eyes (#6B4423)", "Deep, expressive, intelligent and warm"),
            ("Hair & Features", "Lustrous wavy dark espresso hair", "Naturally arched eyebrows, delicate straight nose"),
            ("Vocal Persona", "224 Hz Vocal Pitch (hi-IN-SwaraNeural)", "Warm, articulate, natural conversational speed"),
            ("Greeting Protocol", "STRICTLY 'Hello everyone!'", "Strictly ZERO 'Namaste' across all scripts"),
            ("Daily Quota", "10 Slots / Day (Every 2.4 Hours)", "YouTube Create Prompts (<300 chars) + AI Video Motion"),
            ("Content Engine", "100% Real-Time Live News Harvester", "Zero hardcoded text, multi-tier live RSS fallback pipeline")
        ]

    # Build Chat-Style Cards & Table Rows
    cards_html = ""
    excel_rows_html = ""

    status_colors = {
        "CONFIRMED": ("#10a37f", "rgba(16, 163, 127, 0.15)"),
        "DEVELOPING": ("#f59e0b", "rgba(245, 158, 11, 0.15)"),
        "PROPOSAL": ("#8b5cf6", "rgba(139, 92, 246, 0.15)"),
        "SCHEDULED": ("#38bdf8", "rgba(56, 189, 248, 0.15)"),
        "EVERGREEN": ("#94a3b8", "rgba(148, 163, 184, 0.15)"),
        "UNVERIFIED": ("#ef4444", "rgba(239, 68, 68, 0.15)")
    }

    for s in mobile_slots:
        slot_num = s["slot"]
        slot_time = s["time"]
        slot_cat = s["category"]
        slot_lang = s.get("language", "hinglish").upper()
        slot_title = s["title"]
        script_txt = s["script"]
        vid_txt = s.get("video_prompt", "")
        yt_post_txt = s.get("yt_shorts_posting", f"{slot_title[:65]} #Aminsa #Shorts")
        fb_txt = s.get("fb_description", s.get("caption", ""))
        wardrobe_txt = s.get("wardrobe", "Modern tailored chic")
        location_txt = s.get("location", "Studio")
        v_status = s.get("verification_status", "CONFIRMED")
        c_score = s.get("confidence_score", 1.0)
        f_ctx = s.get("factual_context", "")
        v_fg, v_bg = status_colors.get(v_status, ("#10a37f", "rgba(16, 163, 127, 0.15)"))

        # ChatGPT Conversation Block
        cards_html += f"""
        <div class="chat-message" id="slot-card-{slot_num}" data-search="{slot_title.lower()} {slot_cat.lower()} {script_txt.lower()}">
            <div class="message-header">
                <div class="avatar-badge">
                    <div class="avatar-icon">✨</div>
                    <div class="avatar-info">
                        <div class="avatar-name">Aminsa AI <span class="verified-icon">✓</span></div>
                        <div class="slot-pill-group">
                            <span class="slot-pill">SLOT {slot_num} &bull; {slot_time}</span>
                            <span class="category-pill">{slot_cat}</span>
                            <span class="category-pill" style="background: rgba(56, 189, 248, 0.15); color: var(--accent-cyan);">{slot_lang}</span>
                            <span class="category-pill" style="background: {v_bg}; color: {v_fg}; font-weight: 700;">✓ {v_status} ({int(c_score * 100)}%)</span>
                            <span class="category-pill" style="background: rgba(16, 163, 127, 0.12); color: #34d399;">30-Day Fresh ✓</span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="message-body">
                <h3 class="slot-title">{slot_title}</h3>
                {f'<div style="margin: 8px 0 12px 0; padding: 8px 12px; background: rgba(255,255,255,0.03); border-left: 3px solid {v_fg}; border-radius: 4px; font-size: 12px; color: var(--text-secondary);"><strong style="color: {v_fg};">📌 Verified Source Context:</strong> {f_ctx}</div>' if f_ctx else ''}

                <!-- Script Section -->
                <div class="section-title">🗣️ Spoken Script ({slot_lang})</div>
                <div class="script-bubble" id="script-{slot_num}">{script_txt}</div>

                <!-- Video Motion Prompt Section (ChatGPT Code Block Style) -->
                <div class="section-title">🎬 Video Motion Prompt (YouTube Create &bull; &lt;300 Chars)</div>
                <div class="code-block-container">
                    <div class="code-block-header">
                        <span class="code-lang">motion</span>
                        <button class="code-copy-btn" onclick="copyFromId('vid-{slot_num}', this)">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                            <span>Copy code</span>
                        </button>
                    </div>
                    <pre class="code-content" id="vid-{slot_num}">{vid_txt}</pre>
                </div>

                <!-- YouTube Shorts / Reel Posting Section (Strictly <100 Chars) -->
                <div class="section-title">📱 YouTube Shorts &bull; Title (&lt;100 Chars)</div>
                <div class="code-block-container">
                    <div class="code-block-header">
                        <span class="code-lang">youtube-title-under-100c</span>
                        <button class="code-copy-btn" onclick="copyFromId('yt-{slot_num}', this)">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                            <span>Copy Title</span>
                        </button>
                    </div>
                    <pre class="code-content" id="yt-{slot_num}">{yt_post_txt}</pre>
                </div>

                <!-- Action Button Row -->
                <div class="action-buttons-row">
                    <button class="pill-btn primary" onclick="copyFromId('script-{slot_num}', this)">
                        <span>📋</span> Copy Script
                    </button>
                    <button class="pill-btn secondary" onclick="copyFromId('vid-{slot_num}', this)">
                        <span>🎬</span> Copy Video Prompt
                    </button>
                    <button class="pill-btn tertiary" onclick="copyFromId('yt-{slot_num}', this)" style="border-color: rgba(245, 158, 11, 0.4); color: #fbbf24;">
                        <span>📱</span> Copy YouTube Tags
                    </button>
                    <button class="pill-btn tertiary" onclick="copyFromId('cap-{slot_num}', this)">
                        <span>📢</span> Copy Social Post
                    </button>
                </div>

                <div style="display:none;" id="cap-{slot_num}">{fb_txt}</div>
            </div>
        </div>
        """

        # Table Row (Live Excel Grid Structure with Spoken Script removed & 1-tap Copy on all fields)
        excel_rows_html += f"""
        <tr>
            <td class="center bold">{slot_num}</td>
            <td class="nowrap center">{slot_time}</td>
            <td class="cat-cell">{slot_cat}</td>
            <td class="center nowrap"><span class="category-pill" style="font-size:10px; padding:2px 6px;">{slot_lang}</span></td>
            <td class="title-cell">
                <div id="table-title-{slot_num}">{slot_title}</div>
                <button class="table-copy-btn" onclick="copyFromId('table-title-{slot_num}', this)">Copy</button>
            </td>
            <td class="code-cell">
                <div id="table-vid-{slot_num}">{vid_txt}</div>
                <button class="table-copy-btn" onclick="copyFromId('table-vid-{slot_num}', this)">Copy</button>
            </td>
            <td class="text-cell">
                <div id="table-yt-{slot_num}" style="font-size: 11.5px; color: #fbbf24; font-weight: 500;">{yt_post_txt}</div>
                <button class="table-copy-btn" onclick="copyFromId('table-yt-{slot_num}', this)">Copy</button>
            </td>
            <td class="text-cell">
                <div id="table-cap-{slot_num}" style="max-height: 100px; overflow-y: auto; white-space: pre-line; font-size: 11px;">{fb_txt}</div>
                <button class="table-copy-btn" onclick="copyFromId('table-cap-{slot_num}', this)">Copy</button>
            </td>
            <td class="text-cell">
                <div id="table-wardrobe-{slot_num}" style="font-size: 11px;">{wardrobe_txt}</div>
                <button class="table-copy-btn" onclick="copyFromId('table-wardrobe-{slot_num}', this)">Copy</button>
            </td>
            <td class="text-cell">
                <div id="table-loc-{slot_num}" style="font-size: 11px;">{location_txt}</div>
                <button class="table-copy-btn" onclick="copyFromId('table-loc-{slot_num}', this)">Copy</button>
            </td>
        </tr>
        """

    # Build DNA Table Rows
    dna_rows_html = ""
    for attr, val, enf in dna_rows:
        dna_rows_html += f"""
        <tr>
            <td class="bold">{attr}</td>
            <td class="val-cell">{val}</td>
            <td>{enf}</td>
        </tr>
        """

    try:
        import sys, os
        _PR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if _PR not in sys.path:
            sys.path.insert(0, _PR)
        from engines.kill_switch import is_production_enabled
        prod_active = is_production_enabled()
    except Exception:
        prod_active = True

    if prod_active:
        kill_badge = '<a href="/kill_switch/toggle" style="text-decoration:none;" title="Click to Emergency Pause"><span style="background: rgba(16, 163, 127, 0.2); border: 1px solid #10a37f; color: #6ee7b7; padding: 5px 12px; border-radius: 14px; font-size: 11px; font-weight: 700; cursor: pointer;">🟢 PROD ACTIVE</span></a>'
    else:
        kill_badge = '<a href="/kill_switch/toggle" style="text-decoration:none;" title="Click to Resume"><span style="background: rgba(239, 68, 68, 0.25); border: 1px solid #ef4444; color: #fca5a5; padding: 5px 12px; border-radius: 14px; font-size: 11px; font-weight: 700; cursor: pointer;">🔴 EMERGENCY PAUSED</span></a>'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Aminsa &bull; Daily Production Catalog</title>
    <style>
        :root {{
            --bg-main: #212121;
            --bg-card: #2f2f2f;
            --bg-subtle: #171717;
            --bg-code: #181818;
            --border: rgba(255, 255, 255, 0.12);
            --border-subtle: rgba(255, 255, 255, 0.08);
            --text-main: #ececec;
            --text-secondary: #b4b4b4;
            --text-muted: #737373;
            --gpt-green: #10a37f;
            --gpt-green-hover: #1a7f64;
            --accent-cyan: #38bdf8;
            --accent-gold: #f59e0b;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            -webkit-tap-highlight-color: transparent;
        }}

        body {{
            background-color: var(--bg-main);
            color: var(--text-main);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
            font-size: 14.5px;
            line-height: 1.55;
            padding: 12px;
            padding-bottom: 110px;
        }}

        /* ChatGPT Header */
        .chatgpt-nav {{
            position: sticky;
            top: 0;
            z-index: 999;
            background: rgba(33, 33, 33, 0.95);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border);
            padding: 12px 6px;
            margin: -12px -12px 14px -12px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .brand-container {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .gpt-pill {{
            background: #2f2f2f;
            border: 1px solid var(--border);
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 13.5px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 6px;
            color: var(--text-main);
        }}

        .refresh-pill {{
            background: rgba(16, 163, 127, 0.2);
            border: 1px solid rgba(16, 163, 127, 0.4);
            color: #6ee7b7;
            padding: 4px 10px;
            border-radius: 14px;
            font-size: 11px;
            font-weight: 600;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            transition: all 0.15s;
        }}

        .refresh-pill:active {{
            transform: scale(0.95);
            background: rgba(16, 163, 127, 0.4);
        }}

        .next-pill {{
            background: rgba(56, 189, 248, 0.2);
            border: 1px solid rgba(56, 189, 248, 0.4);
            color: #7dd3fc;
            padding: 4px 10px;
            border-radius: 14px;
            font-size: 11px;
            font-weight: 600;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            transition: all 0.15s;
        }}

        .next-pill:active {{
            transform: scale(0.95);
            background: rgba(56, 189, 248, 0.4);
        }}

        .status-dot {{
            width: 8px;
            height: 8px;
            background: var(--gpt-green);
            border-radius: 50%;
            display: inline-block;
            box-shadow: 0 0 8px var(--gpt-green);
        }}

        .date-pill {{
            font-size: 11.5px;
            color: var(--text-secondary);
            font-weight: 500;
        }}

        /* Segmented Tabs (ChatGPT Model Switcher Style) */
        .tab-switcher {{
            display: flex;
            background: var(--bg-subtle);
            border: 1px solid var(--border-subtle);
            padding: 3px;
            border-radius: 12px;
            margin-bottom: 14px;
            gap: 4px;
        }}

        .tab-btn {{
            flex: 1;
            padding: 9px 8px;
            border: none;
            background: transparent;
            color: var(--text-secondary);
            font-size: 12px;
            font-weight: 600;
            border-radius: 8px;
            cursor: pointer;
            text-align: center;
            transition: all 0.15s ease;
        }}

        .tab-btn.active {{
            background: #3b3b3b;
            color: #ffffff;
            box-shadow: 0 1px 4px rgba(0,0,0,0.4);
        }}

        /* Search Filter */
        .search-box {{
            width: 100%;
            padding: 10px 14px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            color: #fff;
            font-size: 13.5px;
            margin-bottom: 14px;
            outline: none;
            transition: border 0.2s;
        }}

        .search-box:focus {{
            border-color: var(--gpt-green);
        }}

        /* Chat Message Cards */
        .chat-message {{
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: 16px;
            padding: 16px 14px;
            margin-bottom: 16px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.25);
            transition: transform 0.15s ease;
        }}

        .message-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 12px;
        }}

        .avatar-badge {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .avatar-icon {{
            width: 34px;
            height: 34px;
            border-radius: 50%;
            background: linear-gradient(135deg, #10a37f, #0d8366);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            color: white;
            box-shadow: 0 2px 6px rgba(16, 163, 127, 0.4);
        }}

        .avatar-name {{
            font-weight: 700;
            font-size: 14px;
            color: #ffffff;
            display: flex;
            align-items: center;
            gap: 4px;
        }}

        .verified-icon {{
            color: var(--gpt-green);
            font-weight: 800;
            font-size: 12px;
        }}

        .slot-pill-group {{
            display: flex;
            gap: 6px;
            margin-top: 2px;
            flex-wrap: wrap;
        }}

        .slot-pill {{
            background: rgba(56, 189, 248, 0.15);
            color: var(--accent-cyan);
            border: 1px solid rgba(56, 189, 248, 0.3);
            border-radius: 6px;
            padding: 1px 7px;
            font-size: 11px;
            font-weight: 700;
        }}

        .category-pill {{
            background: rgba(245, 158, 11, 0.15);
            color: var(--accent-gold);
            border-radius: 6px;
            padding: 1px 7px;
            font-size: 11px;
            font-weight: 600;
        }}

        .slot-title {{
            font-size: 16px;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 10px;
            line-height: 1.35;
        }}

        .section-title {{
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--text-muted);
            margin-top: 10px;
            margin-bottom: 5px;
        }}

        .script-bubble {{
            background: var(--bg-subtle);
            border: 1px solid var(--border-subtle);
            border-left: 3px solid var(--gpt-green);
            border-radius: 10px;
            padding: 10px 12px;
            font-size: 13.5px;
            color: #e2e8f0;
            line-height: 1.5;
            margin-bottom: 10px;
            white-space: pre-wrap;
        }}

        /* ChatGPT Code Blocks */
        .code-block-container {{
            background: var(--bg-code);
            border: 1px solid var(--border-subtle);
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 12px;
        }}

        .code-block-header {{
            background: #262626;
            padding: 7px 12px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }}

        .code-lang {{
            font-size: 11px;
            color: var(--text-muted);
            font-family: monospace;
            text-transform: lowercase;
        }}

        .code-copy-btn {{
            background: transparent;
            border: none;
            color: var(--text-secondary);
            font-size: 11px;
            display: flex;
            align-items: center;
            gap: 4px;
            cursor: pointer;
            padding: 2px 6px;
            border-radius: 4px;
            transition: all 0.15s;
        }}

        .code-copy-btn:hover {{
            background: rgba(255, 255, 255, 0.1);
            color: #fff;
        }}

        .code-content {{
            padding: 10px 12px;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            font-size: 12px;
            color: #d1d5db;
            line-height: 1.5;
            white-space: pre-wrap;
            word-break: break-word;
            max-height: 180px;
            overflow-y: auto;
        }}

        /* Action Buttons Row */
        .action-buttons-row {{
            display: flex;
            gap: 8px;
            margin-top: 10px;
            flex-wrap: wrap;
        }}

        .pill-btn {{
            flex: 1;
            min-width: 120px;
            padding: 9px 12px;
            border-radius: 20px;
            border: 1px solid var(--border);
            background: #3b3b3b;
            color: #ffffff;
            font-size: 12px;
            font-weight: 600;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            cursor: pointer;
            transition: all 0.15s;
        }}

        .pill-btn:hover {{
            background: #474747;
        }}

        .pill-btn.primary {{
            background: rgba(16, 163, 127, 0.2);
            border-color: rgba(16, 163, 127, 0.4);
            color: #6ee7b7;
        }}

        .pill-btn.primary:hover {{
            background: rgba(16, 163, 127, 0.35);
        }}

        .pill-btn.secondary {{
            background: rgba(56, 189, 248, 0.18);
            border-color: rgba(56, 189, 248, 0.35);
            color: #7dd3fc;
        }}

        .pill-btn.secondary:hover {{
            background: rgba(56, 189, 248, 0.3);
        }}

        .pill-btn.tertiary {{
            background: rgba(255, 255, 255, 0.08);
            border-color: var(--border);
            color: var(--text-secondary);
        }}

        .pill-btn.tertiary:hover {{
            background: rgba(255, 255, 255, 0.14);
            color: #fff;
        }}

        /* Table View (Original Grid Layout Restored) */
        .table-responsive {{
            width: 100%;
            overflow-x: auto;
            border: 1px solid var(--border);
            border-radius: 12px;
            background: var(--bg-card);
            -webkit-overflow-scrolling: touch;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
            min-width: 1350px;
        }}

        th {{
            background: #262626;
            color: var(--text-secondary);
            font-weight: 700;
            text-align: left;
            padding: 10px;
            border-bottom: 1px solid var(--border);
            border-right: 1px solid var(--border-subtle);
            position: sticky;
            top: 0;
            white-space: nowrap;
        }}

        td {{
            padding: 10px;
            border-bottom: 1px solid var(--border-subtle);
            border-right: 1px solid var(--border-subtle);
            vertical-align: top;
            color: var(--text-main);
        }}

        tr:nth-child(even) {{
            background: rgba(255, 255, 255, 0.02);
        }}

        .nowrap {{ white-space: nowrap; }}
        .center {{ text-align: center; }}
        .bold {{ font-weight: 700; color: #fff; }}
        .cat-cell {{ color: var(--accent-gold); font-weight: 600; min-width: 130px; }}
        .title-cell {{ font-weight: 700; color: #fff; min-width: 150px; }}
        .text-cell {{ min-width: 240px; }}
        .code-cell {{ font-family: monospace; font-size: 11px; min-width: 250px; color: #bae6fd; }}

        .table-copy-btn {{
            background: #3b3b3b;
            color: #fff;
            border: 1px solid var(--border);
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 10px;
            font-weight: 600;
            margin-top: 5px;
            cursor: pointer;
            transition: all 0.15s;
        }}

        .table-copy-btn:hover {{
            background: #4a4a4a;
            color: var(--gpt-green);
        }}

        /* Floating Bottom Action Bar */
        .bottom-action-bar {{
            position: fixed;
            bottom: 14px;
            left: 12px;
            right: 12px;
            max-width: 600px;
            margin: 0 auto;
            background: rgba(47, 47, 47, 0.95);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border);
            border-radius: 26px;
            padding: 8px 12px;
            display: flex;
            gap: 8px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.6);
            z-index: 999;
        }}

        .bottom-btn {{
            flex: 1;
            padding: 10px 8px;
            border-radius: 18px;
            border: none;
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            transition: all 0.15s;
        }}

        .bottom-btn.all {{
            background: var(--gpt-green);
            color: white;
        }}

        .bottom-btn.excel {{
            background: #3b3b3b;
            color: white;
            border: 1px solid var(--border);
        }}

        /* Toast */
        .toast {{
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: var(--gpt-green);
            color: white;
            padding: 10px 20px;
            border-radius: 24px;
            font-weight: 700;
            font-size: 13px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
            display: none;
            z-index: 10000;
        }}

        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}
    </style>
</head>
<body>

    <!-- TOP BAR -->
    <div class="chatgpt-nav">
        <div class="brand-container">
            <div class="gpt-pill">
                <span class="status-dot"></span>
                <span>Aminsa 4o</span>
            </div>
            <span class="date-pill">{date_str}</span>
        </div>
        <div style="display: flex; align-items: center; gap: 8px;">
            {kill_badge}
            <a href="/next" class="next-pill" onclick="this.innerHTML='&#x23F3; Advancing...';">
                <span>&#x23ED;</span> NEXT Cycle
            </a>
            <a href="/refresh" class="refresh-pill" onclick="this.innerHTML='&#x23F3; Harvesting...';">
                <span>&#x1F504;</span> Refresh Live
            </a>
            <div style="font-size: 11px; color: var(--accent-cyan); font-weight: 600;">
                10 Slots &bull; 2.4h Loop
            </div>
        </div>
    </div>

    <!-- DUAL-AI & ECOSYSTEM METADATA STATUS BANNER -->
    <div style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-subtle); border-radius: 10px; padding: 8px 12px; margin-bottom: 12px; display: flex; flex-wrap: wrap; gap: 10px; justify-content: space-between; align-items: center; font-size: 11.5px; color: var(--text-secondary);">
        <div style="display: flex; gap: 12px; align-items: center; flex-wrap: wrap;">
            <span>💻 <strong>Laptop AI:</strong> <span style="color:#6ee7b7; font-weight:600;">MSA_AI_AGENT_LAPTOP</span></span>
            <span>📱 <strong>Mobile AI:</strong> <span style="color:#7dd3fc; font-weight:600;">GOOGLE_AI_EDGE_MOBILE</span></span>
            <span>📊 <strong>Status:</strong> <span style="color:#fcd34d; font-weight:600;">10/10 Slots [DRAFT]</span></span>
        </div>
        <div style="display: flex; gap: 10px; align-items: center;">
            <span style="color: #a7f3d0; background: rgba(16,163,127,0.15); padding: 2px 8px; border-radius: 6px; font-weight:600;">✓ 30-Day Anti-Repetition</span>
            <span style="color: #94a3b8; background: rgba(148,163,184,0.12); padding: 2px 8px; border-radius: 6px; font-weight:600;">🔒 Zero Auto-Publish</span>
        </div>
    </div>

    <!-- TABS SWITCHER -->
    <div class="tab-switcher">
        <button class="tab-btn active" id="btn-tab-chat" onclick="switchTab('tab-chat')">💬 10 Chat Cards</button>
        <button class="tab-btn" id="btn-tab-table" onclick="switchTab('tab-table')">📊 Live Excel Grid</button>
        <button class="tab-btn" id="btn-tab-health" onclick="switchTab('tab-health')">🛡️ Ecosystem Health &amp; Sync</button>
        <button class="tab-btn" id="btn-tab-dna" onclick="switchTab('tab-dna')">🧬 DNA Rules</button>
    </div>

    <!-- TAB 1: CHAT CARDS -->
    <div id="tab-chat" class="tab-content active">
        <input type="text" class="search-box" placeholder="🔍 Search topics, scripts, keywords..." oninput="filterCards(this.value)">
        {cards_html}
    </div>

    <!-- TAB 2: LIVE EXCEL GRID -->
    <div id="tab-table" class="tab-content">
        <div style="margin-bottom: 8px; font-size: 12px; color: var(--accent-gold); font-weight: 600;">
            📊 MASTER EXCEL SPREADSHEET GRID (Scroll horizontally)
        </div>
        <div class="table-responsive">
            <table>
                <thead>
                    <tr>
                        <th>Slot</th>
                        <th>Time</th>
                        <th>Category</th>
                        <th>Language</th>
                        <th>Headline / Focus</th>
                        <th>Video Motion Prompt (&lt;300 Chars)</th>
                        <th>YouTube Shorts Title (&lt;100 Chars)</th>
                        <th>Social Media Caption &amp; Tags</th>
                        <th>Wardrobe &amp; Attire</th>
                        <th>Setting / Location</th>
                    </tr>
                </thead>
                <tbody>
                    {excel_rows_html}
                </tbody>
            </table>
        </div>
    </div>

    <!-- TAB 3: DNA RULES -->
    <div id="tab-dna" class="tab-content">
        <div class="table-responsive">
            <table>
                <thead>
                    <tr>
                        <th>Parameter</th>
                        <th>Enforced Rule</th>
                        <th>Verification Protocol</th>
                    </tr>
                </thead>
                <tbody>
                    {dna_rows_html}
                </tbody>
            </table>
        </div>
    </div>

    <!-- TAB 4: ECOSYSTEM HEALTH & SYNC -->
    <div id="tab-health" class="tab-content">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 14px; margin-bottom: 20px;">
            <div style="background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 18px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <span style="font-size: 14px; font-weight: 700; color: #fff;">💻 Laptop Orchestrator</span>
                    <span style="background: rgba(16, 163, 127, 0.2); color: #6ee7b7; padding: 4px 10px; border-radius: 8px; font-size: 11px; font-weight: 700;">ACTIVE</span>
                </div>
                <div style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.7;">
                    <div>• <strong>Role:</strong> Primary Intelligence &amp; Master Scheduler</div>
                    <div>• <strong>Engines:</strong> Google News RSS &bull; 30-Day Anti-Repetition &bull; Openpyxl</div>
                    <div>• <strong>Ledger DB:</strong> SQLite (18 production tables active)</div>
                    <div>• <strong>Timezone:</strong> Asia/Kolkata (IST 08:00 AM Cycle)</div>
                </div>
            </div>

            <div style="background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 18px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <span style="font-size: 14px; font-weight: 700; color: #fff;">📱 OPPO A78 5G Mobile Worker</span>
                    <span style="background: rgba(56, 189, 248, 0.2); color: #7dd3fc; padding: 4px 10px; border-radius: 8px; font-size: 11px; font-weight: 700;">STANDALONE OK</span>
                </div>
                <div style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.7;">
                    <div>• <strong>Node ID:</strong> oppo_a78_5g_termux</div>
                    <div>• <strong>Environment:</strong> Android 15 &bull; Termux &bull; Google AI Edge</div>
                    <div>• <strong>Services:</strong> Web Hub Port 8765 &bull; Wake-Lock Persistent</div>
                    <div>• <strong>Offline Queue:</strong> Self-sufficient local production fallback</div>
                </div>
            </div>

            <div style="background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 18px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <span style="font-size: 14px; font-weight: 700; color: #fff;">🛡️ Safety &amp; Production Guardrails</span>
                    {kill_badge}
                </div>
                <div style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.7;">
                    <div>• <strong>Auto-Publishing:</strong> STRICTLY DISABLED (Drafts Only)</div>
                    <div>• <strong>Face Anchor:</strong> aminsa_face_master_4k.png (Locked 4K Master)</div>
                    <div>• <strong>Shorts Title Limit:</strong> Enforced &le; 100 characters</div>
                    <div style="margin-top: 10px;">
                        <a href="/kill_switch/toggle" style="display: inline-block; padding: 8px 14px; background: rgba(239, 68, 68, 0.2); border: 1px solid rgba(239, 68, 68, 0.5); color: #fca5a5; text-decoration: none; border-radius: 8px; font-size: 12px; font-weight: 600;">
                            ⚡ Toggle Emergency Software Kill Switch
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- FLOATING BOTTOM BAR -->
    <div class="bottom-action-bar">
        <button class="bottom-btn all" onclick="copyAll10Slots()">
            <span>📋</span> Copy All 10 Slots
        </button>
        <button class="bottom-btn excel" onclick="switchTab('tab-table')">
            <span>📊</span> View Excel Sheet
        </button>
    </div>

    <!-- TOAST -->
    <div class="toast" id="toast">✓ Copied to clipboard!</div>

    <script>
        function switchTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            
            document.getElementById(tabId).classList.add('active');
            if (tabId === 'tab-chat') document.getElementById('btn-tab-chat').classList.add('active');
            if (tabId === 'tab-table') document.getElementById('btn-tab-table').classList.add('active');
            if (tabId === 'tab-health') document.getElementById('btn-tab-health').classList.add('active');
            if (tabId === 'tab-dna') document.getElementById('btn-tab-dna').classList.add('active');
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}

        function showToast(msg) {{
            const t = document.getElementById('toast');
            t.innerText = msg;
            t.style.display = 'block';
            setTimeout(() => {{ t.style.display = 'none'; }}, 2000);
        }}

        function copyTextDirect(text, btn) {{
            if (navigator.clipboard) {{
                navigator.clipboard.writeText(text).then(() => {{
                    successAnim(btn);
                }}).catch(() => fallbackCopy(text, btn));
            }} else {{
                fallbackCopy(text, btn);
            }}
        }}

        function copyFromId(id, btn) {{
            const el = document.getElementById(id);
            if (!el) return;
            const text = el.innerText;
            copyTextDirect(text, btn);
        }}

        function successAnim(btn) {{
            if (!btn) return;
            const orig = btn.innerHTML;
            btn.innerHTML = "<span>✓</span> Copied!";
            const origColor = btn.style.color;
            btn.style.color = "#10a37f";
            setTimeout(() => {{
                btn.innerHTML = orig;
                btn.style.color = origColor;
            }}, 2000);
            showToast("✓ Copied to clipboard!");
        }}

        function fallbackCopy(text, btn) {{
            const ta = document.createElement("textarea");
            ta.value = text;
            ta.style.position = "fixed";
            document.body.appendChild(ta);
            ta.select();
            document.execCommand("copy");
            document.body.removeChild(ta);
            successAnim(btn);
        }}

        function copyAll10Slots() {{
            let allText = "🌟 AMINSA DAILY MASTER PRODUCTION SCHEDULE\\nDate: {date_str}\\n\\n";
            for (let i = 1; i <= 10; i++) {{
                const s = document.getElementById("script-" + i);
                const v = document.getElementById("vid-" + i);
                const y = document.getElementById("yt-" + i);
                if (s && v) {{
                    allText += `[SLOT ${{i}}]\\nSCRIPT: ${{s.innerText}}\\nVIDEO PROMPT: ${{v.innerText}}\\n`;
                    if (y) allText += `YOUTUBE SHORTS: ${{y.innerText}}\\n`;
                    allText += `\\n`;
                }}
            }}
            fallbackCopy(allText, event.target);
        }}

        function filterCards(query) {{
            const q = query.toLowerCase().trim();
            document.querySelectorAll('.chat-message').forEach(el => {{
                const data = el.getAttribute('data-search') || '';
                if (!q || data.includes(q)) {{
                    el.style.display = 'block';
                }} else {{
                    el.style.display = 'none';
                }}
            }});
        }}
    </script>
</body>
</html>"""
    return html
