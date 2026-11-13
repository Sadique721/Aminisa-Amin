# 🌸 Aminsa Amin — Multi-Angle Character Reference Guide (17 Positions)

> **Official Character Turnaround & 3D Spatial Reference Matrix**  
> **Character:** Aminsa Amin (`@aminsa.official`) — 22-Year-Old Female Virtual Creator  
> **Biometric Identity Lock:** Wheatish Porcelain (`#EAD5C3`), Deep Almond Hazel-Brown Eyes (`#6B4423`), Dark Espresso Waves (`#231709`), STRICTLY ZERO MOLES  
> **Primary Master Anchor:** `shared/identity/face_anchor.jpg` (SHA-256: `C58BBA2286E63E1FCEA3334C6244C38DCEF2459B540F9D9901FF507996176467`)

---

## 📸 The 17 Canonical Positions Breakdown

| ID | Angle Label | Category | Azimuth ($\theta$) | Elevation ($\phi$) | Prompt Injection Snippet | Biometric Cosine Score |
|:---:|---|---|:---:|:---:|---|:---:|
| **01** | `Front` | Eye-Level 360° | $0^\circ$ | $0^\circ$ | `front view, eye level shot, looking directly into camera, symmetrical lighting, photorealistic 8k` | **0.9896** (PASS) |
| **02** | `Front-Quarter Right` | Eye-Level 360° | $45^\circ$ | $0^\circ$ | `three-quarter view facing right, 45 degree angle, key light on right cheek, soft fill light` | **0.9535** (PASS) |
| **03** | `Front-Quarter Left` | Eye-Level 360° | $315^\circ$ | $0^\circ$ | `three-quarter view facing left, 45 degree angle, key light on left cheek, soft rim light` | **0.9537** (PASS) |
| **04** | `Side Profile Right` | Eye-Level 360° | $90^\circ$ | $0^\circ$ | `side profile right view, 90 degree orthogonal angle, sharp jawline silhouette, hair falling over shoulder` | **0.9471** (PASS) |
| **05** | `Side Profile Left` | Eye-Level 360° | $270^\circ$ | $0^\circ$ | `side profile left view, 90 degree orthogonal angle, elegant nose bridge, crisp rim contour` | **0.9478** (PASS) |
| **06** | `Three-Quarter Right Back` | Eye-Level 360° | $135^\circ$ | $0^\circ$ | `rear three-quarter view over right shoulder, hair cascading down upper back, subtle jawline curve` | **0.9780** (PASS) |
| **07** | `Three-Quarter Left Back` | Eye-Level 360° | $225^\circ$ | $0^\circ$ | `rear three-quarter view over left shoulder, dark espresso wavy hair texture, soft ambient back light` | **0.9782** (PASS) |
| **08** | `Back View (Direct)` | Eye-Level 360° | $180^\circ$ | $0^\circ$ | `direct back view, 180 degrees rear angle, full hair back silhouette, symmetrical shoulders` | **0.9782** (PASS) |
| **09** | `Low Angle Front` | Low Angle (Worm's Eye) | $0^\circ$ | $+35^\circ$ | `low angle shot looking up, worm's eye perspective, upward perspective convergence, cinematic heroic angle` | **0.9461** (PASS) |
| **10** | `Low Angle Right` | Low Angle (Worm's Eye) | $45^\circ$ | $+35^\circ$ | `low angle right three-quarter shot, camera at waist level tilted upward, dramatic architectural lighting` | **0.9307** (PASS) |
| **11** | `Low Angle Left` | Low Angle (Worm's Eye) | $315^\circ$ | $+35^\circ$ | `low angle left three-quarter shot, upward tilt perspective, soft rim light on left cheek` | **0.9463** (PASS) |
| **12** | `Low Angle Back` | Low Angle (Worm's Eye) | $180^\circ$ | $+35^\circ$ | `low angle rear view, camera low pointing up at back and shoulders, wide sky background` | **0.8842** (PASS) |
| **13** | `High Angle Front` | High Angle (Bird's Eye) | $0^\circ$ | $-35^\circ$ | `high angle shot looking down, bird's eye perspective, hazel eyes looking up at camera, delicate facial contours` | **0.9199** (PASS) |
| **14** | `High Angle Right` | High Angle (Bird's Eye) | $45^\circ$ | $-35^\circ$ | `high angle right three-quarter perspective, looking down at right cheek and collar, downward tilt` | **0.9032** (PASS) |
| **15** | `High Angle Left` | High Angle (Bird's Eye) | $315^\circ$ | $-35^\circ$ | `high angle left three-quarter perspective, looking down from upper left, soft overhead key light` | **0.9198** (PASS) |
| **16** | `High Angle Back` | High Angle (Bird's Eye) | $180^\circ$ | $-35^\circ$ | `high angle rear shot looking down at crown and upper back, cascading hair waves from above` | **0.8639** (PASS) |
| **17** | `Close-Up Portrait` | Close-Up Detail | $0^\circ$ | $0^\circ$ | `extreme close-up portrait, 85mm prime lens f/1.4, micro-pore skin texture, hazel brown eyes with dark rings, zero moles, 8k` | **0.9118** (PASS) |

---

## 🛠️ How to Use This Matrix in Future Image Generation

Har angle ka static asset `character/multi_angle_reference/` me exist karta hai. Aage kisi bhi pipeline (daily generator, prompt2video, ya mobile YouTube Create) me specific camera angle dene ke liye Python API use karein:

```python
from engines.aminsa_multi_angle_engine import multi_angle_engine

# Example: Get static reference and prompt snippet for 'Low Angle Front'
ref_data = multi_angle_engine.get_angle_reference("09")
print(ref_data["image_path"])      # Path to 09_aminsa_low_angle_front.jpg
print(ref_data["prompt_snippet"])  # "low angle shot looking up, worm's eye perspective..."
```

---

*Generated autonomously by Aminsa Multi-Angle Engine.*
