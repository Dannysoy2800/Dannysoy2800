"""Run the OmniRouter AI FastAPI application locally."""

import uvicorn


if __name__ == "__main__":
    uvicorn.run("omnirouter_ai.app:app", host="0.0.0.0", port=8000, reload=True)
