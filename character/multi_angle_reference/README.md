# 🌸 Aminsa Amin — Multi-Angle Character Reference Matrix (17 Real Positions)

> **Official 3D Spatial Turnaround & Character Reference Matrix for Aminsa Amin**  
> **Character:** Aminsa Amin (`@aminsa.official`) — 22-Year-Old Indian Virtual Tech Creator  
> **Biometric Identity Locks:** Wheatish Porcelain (`#EAD5C3`), Deep Almond Hazel-Brown Eyes (`#6B4423`) with dark limbal rings, Dark Espresso Wavy Hair (`#231709`), STRICTLY ZERO MOLES / ZERO SCARS  
> **Attire & Setting:** Modern maroon cropped scoop top, tactical olive-drab cargo pants, red scarf choker, arid desert hills with sunny blue sky  
> **Primary Identity Anchor:** `shared/identity/face_anchor.jpg` (SHA-256: `C58BBA2286E63E1FCEA3334C6244C38DCEF2459B540F9D9901FF507996176467`)

---

## 🔍 Forensic Analysis: Reference Guide vs Aminsa Amin

| Parameter | Reference Guide Base | Aminsa Amin Master Reference |
|---|---|---|
| **Grid System** | 4-Row vertical infographic poster (4+4+4+5 = 17 cells) | Identical 4-Row 17-cell master infographic poster |
| **Identity / Face** | Red-haired generic fictional character | **100% Aminsa Amin** (Wheatish porcelain `#EAD5C3`, zero moles) |
| **Eyes** | Generic grey-blue | **Almond Hazel-Brown** (`#6B4423`) with dark limbal rings |
| **Hair** | Ginger / Copper-red waves | **Dark Espresso Wavy Hair** (`#231709`) cascading naturally |
| **Attire** | Maroon ribbed crop top + cargo pants + neck scarf | Exact modern maroon scoop top + olive tactical pants |
| **Lighting & Setting** | Warm sunny desert with rocky mountain dunes | Photorealistic 8K desert panorama under clear sunny sky |
| **Camera Poses** | 17 true physical camera angles (360° + low + high + close-up) | **17 exact 3D physical camera angles & body postures** |

---

## 📸 The 17 Canonical Positions

| Slot | Code | Angle Label | Category | Azimuth ($\theta$) | Elevation ($\phi$) | Asset Path | Description |
|:---:|---|---|---|:---:|:---:|---|---|
| **01** | `front` | Front | Eye-Level 360° | $0^\circ$ | $0^\circ$ | `01_aminsa_front.jpg` | Direct frontal eye-level portrait with symmetrical gaze. |
| **02** | `front_quarter_right` | Front-Quarter Right | Eye-Level 360° | $45^\circ$ | $0^\circ$ | `02_aminsa_front_quarter_right.jpg` | 3/4 view facing slightly right, right cheek lit, eyes to camera. |
| **03** | `front_quarter_left` | Front-Quarter Left | Eye-Level 360° | $315^\circ$ | $0^\circ$ | `03_aminsa_front_quarter_left.jpg` | 3/4 view facing slightly left, left cheek lit, eyes to camera. |
| **04** | `side_profile_right` | Side Profile Right | Eye-Level 360° | $90^\circ$ | $0^\circ$ | `04_aminsa_side_profile_right.jpg` | Pure 90° right profile, sharp jawline, delicate nasal bridge. |
| **05** | `side_profile_left` | Side Profile Left | Eye-Level 360° | $270^\circ$ | $0^\circ$ | `05_aminsa_side_profile_left.jpg` | Pure 90° left profile, elegant jawline, hair cascading. |
| **06** | `three_quarter_right_back` | Three-Quarter Right Back | Eye-Level 360° | $135^\circ$ | $0^\circ$ | `06_aminsa_three_quarter_right_back.jpg` | Rear 45° angle from right, open back scoop, head turned over shoulder. |
| **07** | `three_quarter_left_back` | Three-Quarter Left Back | Eye-Level 360° | $225^\circ$ | $0^\circ$ | `07_aminsa_three_quarter_left_back.jpg` | Rear 45° angle from left, open back scoop, head turned over shoulder. |
| **08** | `back_view_direct` | Back View (Direct) | Eye-Level 360° | $180^\circ$ | $0^\circ$ | `08_aminsa_back_view_direct.jpg` | Direct 180° rear view, cascading espresso waves, open back scoop top. |
| **09** | `low_angle_front` | Low Angle Front | Low Angle (Worm's Eye) | $0^\circ$ | $+35^\circ$ | `09_aminsa_low_angle_front.jpg` | Worm's eye view from ground looking up at front torso and chin. |
| **10** | `low_angle_right` | Low Angle Right | Low Angle (Worm's Eye) | $45^\circ$ | $+35^\circ$ | `10_aminsa_low_angle_right.jpg` | Low angle from 45° right looking up at right hip, waist, and jaw. |
| **11** | `low_angle_left` | Low Angle Left | Low Angle (Worm's Eye) | $315^\circ$ | $+35^\circ$ | `11_aminsa_low_angle_left.jpg` | Low angle from 45° left looking up at left hip, waist, and torso. |
| **12** | `low_angle_back` | Low Angle Back | Low Angle (Worm's Eye) | $180^\circ$ | $+35^\circ$ | `12_aminsa_low_angle_back.jpg` | Low angle rear view looking up at cargo pants, open back, and hair. |
| **13** | `high_angle_front` | High Angle Front | High Angle (Bird's Eye) | $0^\circ$ | $-35^\circ$ | `13_aminsa_high_angle_front.jpg` | Bird's eye view looking down at head crown, forehead, hazel eyes. |
| **14** | `high_angle_right` | High Angle Right | High Angle (Bird's Eye) | $45^\circ$ | $-35^\circ$ | `14_aminsa_high_angle_right.jpg` | High angle from 45° right looking down at right cheek, shoulder. |
| **15** | `high_angle_left` | High Angle Left | High Angle (Bird's Eye) | $315^\circ$ | $-35^\circ$ | `15_aminsa_high_angle_left.jpg` | High angle from 45° left looking down at left cheek, shoulder. |
| **16** | `high_angle_back` | High Angle Back | High Angle (Bird's Eye) | $180^\circ$ | $-35^\circ$ | `16_aminsa_high_angle_back.jpg` | High angle rear shot looking down at crown of head and open back. |
| **17** | `close_up_portrait` | Close-Up Portrait | Close-Up Detail | $0^\circ$ | $0^\circ$ | `17_aminsa_close_up_portrait.jpg` | Extreme 85mm close-up, hazel eyes, dark limbal rings, zero moles. |

---

## 🛠️ Programmatic Usage in Pipeline

Har future generation me specific camera angle provide karne ke liye `multi_angle_engine` call karein:

```python
from engines.aminsa_multi_angle_engine import multi_angle_engine

# Example: Get static reference and prompt snippet for 'Low Angle Front'
ref_data = multi_angle_engine.get_angle_reference("09")
print(ref_data["image_path"])      # character/multi_angle_reference/09_aminsa_low_angle_front.jpg
print(ref_data["prompt_snippet"])  # Prompt injection snippet for diffusion/ControlNet
print(ref_data["biometric_locks"]) # {'skin': '#EAD5C3', 'eyes': '#6B4423', 'hair': '#231709', 'moles': 0}
```

---

*Verified and locked by Aminsa Amin Multi-Angle Reference Pipeline.*
