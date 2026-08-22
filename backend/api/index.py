"""
Vercel Python serverless entrypoint. Vercel looks for a variable named
`app` (ASGI application) in this file when using the @vercel/python
runtime. This just re-exports the FastAPI app defined in main.py.

IMPORTANT CAVEAT (read before relying on this):
Vercel's Hobby plan serverless functions time out at 10 seconds.
This pipeline makes 3 sequential Tavily searches + 1 Groq call, which
can easily take 10-20+ seconds combined - so /api/plan may time out
on Hobby. Options:
  1. Upgrade to Vercel Pro (60s function timeout), or
  2. Deploy this backend on a platform built for longer-running
     processes instead - Render, Railway, or Fly.io all have free
     tiers well suited to this (see README.md "Deploying the backend").
Either way, only the frontend needs to live on Vercel for a smooth
experience; point VITE_API_URL at wherever the backend actually runs.
"""

import sys
import os
from main import app

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app  # noqa: E402
