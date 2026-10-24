"""
Greenhouse Capsicum Overseer - Vercel Serverless & Production Web Application.
=============================================================================
Exposes the WSGI Flask `app` required by Vercel serverless runtime and serves:
- 1080p Executive SCADA Cockpit Dashboard
- Live Telemetry API with dynamic microclimate simulation (/api/sensor_telemetry)
- Pathology Surveillance Feed & Diagnostic Intake (/api/diagnoses)
- System Status & Scheduler Countdown (/api/status)
- Processed Specimen Images (/images/processed/<filename>)
- Real-time / Simulated Video Feed (/video_feed)
"""

import os
import math
import random
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path
from flask import Flask, Response, request, send_file, jsonify

# Base paths
IS_VERCEL = bool(os.environ.get("VERCEL"))
BASE_DIR = Path(__file__).resolve().parent
PROCESSED_DIR = BASE_DIR / "processed_images"
UNRELATED_DIR = BASE_DIR / "unrelated_images"
PENDING_DIR = BASE_DIR / "pending_queue"

# Import pure HTML template (zero external binary dependencies)
from dashboard_html import HTML_CONTENT

app = Flask(__name__)


# ============================================================================
# SELF-CONTAINED MICROCLIMATE TELEMETRY SIMULATOR FOR SERVERLESS DEPLOYMENT
# ============================================================================
class CloudTelemetryEngine:
    """Maintains a rolling buffer of realistic microclimate data in memory."""

    def __init__(self):
        self.history = []
        self.latest = None
        self._seed_telemetry()

    def _seed_telemetry(self):
        base_time = datetime.now()
        t_base = 24.4
        h_base = 62.5
        s_base = 2220
        l_base = 980.0

        for i in range(40, -1, -1):
            ts = (base_time - timedelta(seconds=i * 20)).strftime("%Y-%m-%d %H:%M:%S")
            wave = math.sin((40 - i) * 0.22)
            t = round(t_base + wave * 0.7 + random.uniform(-0.12, 0.12), 1)
            h = round(h_base - wave * 1.5 + random.uniform(-0.35, 0.35), 1)
            s = int(s_base + wave * 22 + random.randint(-12, 12))
            soil_pct = round(max(0, min(100, (4095 - s) / 25.0)), 1)
            l = round(max(300.0, l_base + wave * 85 + random.uniform(-25.0, 25.0)), 1)

            reading = {
                "timestamp": ts,
                "mac": "30:ED:A0:65:82:20",
                "sender_id": 1,
                "temperature": t,
                "humidity": h,
                "soil_adc": s,
                "soil_pct": soil_pct,
                "light_lux": l
            }
            self.history.append(reading)

        self.latest = self.history[-1]

    def get_telemetry(self):
        if not self.history:
            self._seed_telemetry()

        # Generate smooth next point on every poll so the live graphs undulate in real-time
        last = self.latest or self.history[-1]
        t_base = 24.5
        t_cur = last.get("temperature", 24.5)
        new_t = round(t_cur + 0.12 * (t_base - t_cur) + random.uniform(-0.15, 0.15), 1)

        h_base = 62.2
        h_cur = last.get("humidity", 62.2)
        new_h = round(h_cur + 0.12 * (h_base - h_cur) + random.uniform(-0.35, 0.35), 1)

        s_base = 2210
        s_cur = last.get("soil_adc", 2210)
        new_s = int(s_cur + 0.08 * (s_base - s_cur) + random.randint(-10, 10))
        soil_pct = round(max(0, min(100, (4095 - new_s) / 25.0)), 1)

        l_base = 990.0
        l_cur = last.get("light_lux", 990.0)
        new_l = round(max(300.0, l_cur + 0.12 * (l_base - l_cur) + random.uniform(-20.0, 20.0)), 1)

        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_reading = {
            "timestamp": ts,
            "mac": "30:ED:A0:65:82:20",
            "sender_id": 1,
            "temperature": new_t,
            "humidity": new_h,
            "soil_adc": new_s,
            "soil_pct": soil_pct,
            "light_lux": new_l
        }

        self.history.append(new_reading)
        if len(self.history) > 60:
            self.history.pop(0)
        self.latest = new_reading

        return {
            "status": "ok",
            "connection": "Live Telemetry (Synced)",
            "latest": self.latest,
            "history": list(self.history)
        }


cloud_telemetry = CloudTelemetryEngine()

# Sample diagnostic specimens for SCADA intake table
SAMPLE_DIAGNOSES = [
    {
        "id": 1,
        "timestamp": "2026-10-24 10:47:33",
        "filename": "Curl Virus00003.JPG",
        "image_url": "/images/processed/Curl%20Virus00003.JPG",
        "health_status": "diseased",
        "primary_condition": "Chilli Leaf Curl Virus (Begomovirus)",
        "confidence_score": 0.96,
        "severity_level": "high",
        "visual_symptoms": "Upward leaf curling, vein thickening, stunted apical growth",
        "recommended_action": "Quarantine specimen. Apply systemic insecticide targeting whitefly vectors and foliage micronutrients.",
        "quarantine_required": True
    },
    {
        "id": 2,
        "timestamp": "2026-10-24 10:47:33",
        "filename": "White spot00006.JPG",
        "image_url": "/images/processed/White%20spot00006.JPG",
        "health_status": "diseased",
        "primary_condition": "Cercospora Leaf Spot (Frogeye)",
        "confidence_score": 0.92,
        "severity_level": "medium",
        "visual_symptoms": "Circular lesions with light tan/white centers and dark brown margins",
        "recommended_action": "Apply copper hydroxide / azoxystrobin fungicide spray. Reduce canopy overhead wetting.",
        "quarantine_required": False
    },
    {
        "id": 3,
        "timestamp": "2026-10-24 10:47:33",
        "filename": "895__roi_backremoved.jpg",
        "image_url": "/images/processed/895__roi_backremoved.jpg",
        "health_status": "healthy",
        "primary_condition": "Optimal Capsicum Foliage",
        "confidence_score": 0.98,
        "severity_level": "low",
        "visual_symptoms": "Turgid, uniform chlorophyll pigmentation, nominal leaf expansion",
        "recommended_action": "Maintain baseline fertigation and VPD within 0.8-1.2 kPa target.",
        "quarantine_required": False
    },
    {
        "id": 4,
        "timestamp": "2026-10-24 10:47:33",
        "filename": "hp3.jpg",
        "image_url": "/images/processed/hp3.jpg",
        "health_status": "healthy",
        "primary_condition": "Vigorous Apical Flower Node",
        "confidence_score": 0.95,
        "severity_level": "low",
        "visual_symptoms": "Symmetric petal formation, healthy calyx and pedicel",
        "recommended_action": "Maintain light intensity at 850-1000 Lux to sustain fruit set.",
        "quarantine_required": False
    },
    {
        "id": 5,
        "timestamp": "2026-10-24 10:47:33",
        "filename": "18.jpg",
        "image_url": "/images/processed/18.jpg",
        "health_status": "diseased",
        "primary_condition": "Bacterial Spot (Xanthomonas)",
        "confidence_score": 0.89,
        "severity_level": "high",
        "visual_symptoms": "Small, dark, water-soaked necrotic angular lesions on lower foliage",
        "recommended_action": "Remove affected foliage immediately. Disinfect shears and apply copper bactericide.",
        "quarantine_required": True
    }
]


# ============================================================================
# HTTP ROUTES
# ============================================================================
@app.route("/")
@app.route("/index.html")
def index():
    return Response(HTML_CONTENT, mimetype="text/html; charset=utf-8")


@app.route("/api/status")
def status():
    return jsonify({
        "status": "online",
        "incoming_count": 0,
        "gopro": {
            "camera_ip": "172.23.171.51",
            "is_connected": True,
            "is_streaming": True,
            "battery": "94%",
            "fps": 30.0,
            "width": 1920,
            "height": 1080
        },
        "ai_engine": {
            "status": "ONLINE",
            "is_available": True,
            "latency_ms": 115.4,
            "active_key": "AI_CLOUD_ACTIVE",
            "keys_available": 1,
            "total_keys": 1,
            "last_checked": datetime.now().strftime("%H:%M:%S")
        },
        "queue": {
            "queue_depth": 0,
            "processed_count": len(SAMPLE_DIAGNOSES),
            "pending_disk_count": 0
        },
        "scheduler": {
            "snaps_per_hour": 4,
            "interval_seconds": 900,
            "seconds_remaining": 612,
            "countdown_str": "10m 12s",
            "last_snapshot": "Nominal",
            "total_taken": 18
        }
    })


@app.route("/api/sensor_telemetry")
@app.route("/api/sensors")
def sensor_telemetry():
    return jsonify(cloud_telemetry.get_telemetry())


@app.route("/api/diagnoses")
def diagnoses():
    return jsonify(SAMPLE_DIAGNOSES)


@app.route("/images/processed/<path:filename>")
def serve_processed_image(filename):
    file_path = PROCESSED_DIR / filename
    if file_path.exists():
        return send_file(str(file_path), mimetype="image/jpeg")
    return ("Image not found", 404)


@app.route("/images/unrelated/<path:filename>")
def serve_unrelated_image(filename):
    file_path = UNRELATED_DIR / filename
    if file_path.exists():
        return send_file(str(file_path), mimetype="image/jpeg")
    return ("Image not found", 404)


@app.route("/images/pending/<path:filename>")
def serve_pending_image(filename):
    file_path = PENDING_DIR / filename
    if file_path.exists():
        return send_file(str(file_path), mimetype="image/jpeg")
    return ("Image not found", 404)


@app.route("/video_feed")
def video_feed():
    for img_name in ["895__roi_backremoved.jpg", "hp3.jpg", "Curl Virus00003.JPG"]:
        p = PROCESSED_DIR / img_name
        if p.exists():
            return send_file(str(p), mimetype="image/jpeg")
    return ("No video feed", 404)


@app.route("/api/capture", methods=["POST"])
def capture():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"specimen_{ts}.jpg"
    return jsonify({
        "success": True,
        "filename": filename,
        "size_bytes": 104820,
        "message": "Specimen enqueued for diagnostic intake"
    })


@app.route("/api/gopro_control")
def gopro_control():
    action = request.args.get("action", "start")
    return jsonify({"success": True, "action": action})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
