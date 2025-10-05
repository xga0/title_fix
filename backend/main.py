"""
FastAPI backend for Title Fix web application.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from title_fix import title_fix, get_supported_styles, get_supported_case_types, validate_input
except ImportError as e:
    print(f"Error importing title_fix: {e}")
    raise

app = FastAPI(
    title="Title Fix API",
    description="API for intelligent title case conversion and text formatting",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class TextConversionRequest(BaseModel):
    text: str
    case_type: str = "title"
    style: str = "apa"
    straight_quotes: bool = False
    quick_copy: bool = True

class TextConversionResponse(BaseModel):
    text: str
    word_count: int
    char_count: int
    headline_score: int
    quick_copy: bool
    case_type: str
    style: Optional[str] = None

class OptionsResponse(BaseModel):
    supported_styles: list[str]
    supported_case_types: list[str]


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Title Fix API is running"}

@app.get("/api/options", response_model=OptionsResponse)
async def get_options():
    """Get supported styles and case types."""
    try:
        return OptionsResponse(
            supported_styles=get_supported_styles(),
            supported_case_types=get_supported_case_types()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting options: {str(e)}")

@app.post("/api/convert", response_model=TextConversionResponse)
async def convert_text(request: TextConversionRequest):
    """Convert text using the title_fix package."""
    try:
        # Validate input
        validate_input(request.text, request.case_type, request.style)
        
        # Process the text
        result = title_fix(
            text=request.text,
            case_type=request.case_type,
            style=request.style,
            straight_quotes=request.straight_quotes,
            quick_copy=request.quick_copy
        )
        
        return TextConversionResponse(**result)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")


if os.path.exists("../frontend/build"):
    app.mount("/static", StaticFiles(directory="../frontend/build/static"), name="static")
    
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve the React frontend for all non-API routes."""
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="API endpoint not found")
        
        return FileResponse("../frontend/build/index.html")


@app.get("/")
async def read_root():
    """Root endpoint."""
    if os.path.exists("../frontend/build/index.html"):
        return FileResponse("../frontend/build/index.html")
    else:
        return {
            "message": "Title Fix API is running!", 
            "docs": "/docs",
            "frontend": "React app not built yet. Run 'npm run build' in the frontend directory."
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 