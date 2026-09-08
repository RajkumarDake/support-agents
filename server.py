"""Single entry point: python server.py"""

import logging

import uvicorn

from api import app

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    force=True)
# the raw "POST https://openrouter.ai ... 200 OK" lines say nothing useful, drop them
logging.getLogger("httpx").setLevel(logging.WARNING)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info", access_log=True)
