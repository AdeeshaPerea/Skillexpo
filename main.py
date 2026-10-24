"""
Greenhouse Capsicum Overseer - Production Main Entrypoint for Vercel & Cloud.
=============================================================================
Exposes the top-level `app` WSGI instance for Vercel serverless deployment.
"""

import os
from app import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
