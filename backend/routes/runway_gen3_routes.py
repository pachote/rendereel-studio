"""
Runway Gen-3 API Routes

This module provides API endpoints for Runway Gen-3 Alpha Turbo video generation,
including text-to-video, image-to-video, task status tracking, and model management.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends, BackgroundTasks
from fastapi.responses import StreamingResponse, JSONResponse
from typing import Optional, List, Dict, Any
import logging
import aiofiles
import tempfile
import asyncio
from pathlib import Path
import httpx

from services.runway_gen3_service import (
    runway_gen3_service,
    RunwayVideoRequest,
    TaskStatusResponse,
    RunwayVideoResponse
)
from middleware.auth_middleware import get_current_user
from models.base import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/runway-gen3", tags=["Runway Gen-3"])

@router.get("/health")
async def health_check():
    """Get Runway Gen-3 service health status"""
    try:
        health_data = await runway_gen3_service.health_check()
        return JSONResponse(content=health_data)
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={"error": "Service unavailable", "details": str(e)}
        )

@router.get("/models")
async def list_models():
    """List available Runway models"""
    try:
        models = await runway_gen3_service.list_models()
        return JSONResponse(content={"models": models})
    except Exception as e:
        logger.error(f"Failed to list models: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/estimate-cost")
async def estimate_cost(
    duration: int = Form(..., ge=5, le=10),
    model: str = Form(default="gen3a_turbo")
):
    """Estimate the cost for video generation"""
    try:
        cost_data = await runway_gen3_service.estimate_cost(duration, model)
        return JSONResponse(content=cost_data)
    except Exception as e:
        logger.error(f"Cost estimation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-text-to-video", response_model=RunwayVideoResponse)
async def generate_text_to_video(
    background_tasks: BackgroundTasks,
    prompt_text: str = Form(...),
    duration: int = Form(default=5, ge=5, le=10),
    ratio: str = Form(default="16:9"),
    seed: Optional[int] = Form(None),
    model: str = Form(default="gen3a_turbo"),
    current_user: User = Depends(get_current_user)
):
    """
    Generate video from text prompt using Runway Gen-3
    """
    try:
        # Validate ratio
        if ratio not in ["16:9", "9:16", "1:1"]:
            raise HTTPException(status_code=400, detail="Invalid aspect ratio")
        
        # Create request object
        request = RunwayVideoRequest(
            prompt_text=prompt_text,
            duration=duration,
            ratio=ratio,
            seed=seed,
            model=model
        )
        
        # Estimate cost and check user credits
        cost_estimate = await runway_gen3_service.estimate_cost(duration, model)
        if current_user.credits < cost_estimate["cost_credits"]:
            raise HTTPException(
                status_code=400, 
                detail=f"Insufficient credits. Required: {cost_estimate['cost_credits']}, Available: {current_user.credits}"
            )
        
        # Create generation task
        response = await runway_gen3_service.create_video_generation_task(
            request=request,
            user_id=str(current_user.id)
        )
        
        # Deduct credits (you'll need to implement credit deduction)
        # await deduct_user_credits(current_user.id, cost_estimate["cost_credits"])
        
        logger.info(f"Created text-to-video task {response.task_id} for user {current_user.id}")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Text-to-video generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-image-to-video", response_model=RunwayVideoResponse)
async def generate_image_to_video(
    background_tasks: BackgroundTasks,
    prompt_text: str = Form(...),
    image_file: UploadFile = File(...),
    duration: int = Form(default=5, ge=5, le=10),
    ratio: str = Form(default="16:9"),
    seed: Optional[int] = Form(None),
    model: str = Form(default="gen3a_turbo"),
    current_user: User = Depends(get_current_user)
):
    """
    Generate video from image and text prompt using Runway Gen-3
    """
    try:
        # Validate image file
        if not image_file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        if image_file.size and image_file.size > 16 * 1024 * 1024:  # 16MB limit
            raise HTTPException(status_code=400, detail="Image file too large (max 16MB)")
        
        # Validate ratio
        if ratio not in ["16:9", "9:16", "1:1"]:
            raise HTTPException(status_code=400, detail="Invalid aspect ratio")
        
        # Save uploaded image temporarily
        temp_dir = Path("/tmp/runway_uploads")
        temp_dir.mkdir(exist_ok=True)
        
        file_extension = Path(image_file.filename or "image.jpg").suffix
        temp_filename = f"runway_{current_user.id}_{int(asyncio.get_event_loop().time())}{file_extension}"
        temp_file_path = temp_dir / temp_filename
        
        try:
            async with aiofiles.open(temp_file_path, 'wb') as f:
                content = await image_file.read()
                await f.write(content)
            
            # Create request object
            request = RunwayVideoRequest(
                prompt_text=prompt_text,
                duration=duration,
                ratio=ratio,
                seed=seed,
                model=model
            )
            
            # Estimate cost and check user credits
            cost_estimate = await runway_gen3_service.estimate_cost(duration, model)
            if current_user.credits < cost_estimate["cost_credits"]:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Insufficient credits. Required: {cost_estimate['cost_credits']}, Available: {current_user.credits}"
                )
            
            # Create generation task
            response = await runway_gen3_service.create_video_generation_task(
                request=request,
                user_id=str(current_user.id),
                image_path=str(temp_file_path)
            )
            
            # Deduct credits (you'll need to implement credit deduction)
            # await deduct_user_credits(current_user.id, cost_estimate["cost_credits"])
            
            logger.info(f"Created image-to-video task {response.task_id} for user {current_user.id}")
            
            return response
            
        except Exception as e:
            # Clean up temp file on error
            if temp_file_path.exists():
                temp_file_path.unlink()
            raise
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Image-to-video generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/task-status/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(
    task_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get the status of a video generation task
    """
    try:
        task_status = await runway_gen3_service.get_task_status(task_id)
        
        # Verify task belongs to current user (basic security)
        # You might want to add this check to the service layer
        
        return task_status
        
    except Exception as e:
        if "Task not found" in str(e):
            raise HTTPException(status_code=404, detail="Task not found")
        
        logger.error(f"Failed to get task status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tasks")
async def list_user_tasks(
    current_user: User = Depends(get_current_user),
    status: Optional[str] = None,
    limit: int = 20
):
    """
    List user's video generation tasks
    """
    try:
        # Filter tasks by user and optionally by status
        user_tasks = []
        for task_id, task_data in runway_gen3_service.active_tasks.items():
            if task_data.get("user_id") == str(current_user.id):
                if status is None or task_data.get("status") == status:
                    task_info = {
                        "task_id": task_id,
                        "status": task_data.get("status"),
                        "created_at": task_data.get("created_at"),
                        "progress": task_data.get("progress", 0),
                        "cost_credits": task_data.get("cost_credits"),
                        "video_url": task_data.get("video_url"),
                        "error_message": task_data.get("error_message")
                    }
                    user_tasks.append(task_info)
        
        # Sort by creation time (newest first) and limit
        user_tasks.sort(key=lambda x: x.get("created_at", 0), reverse=True)
        user_tasks = user_tasks[:limit]
        
        return JSONResponse(content={"tasks": user_tasks, "total": len(user_tasks)})
        
    except Exception as e:
        logger.error(f"Failed to list user tasks: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/video/{task_id}")
async def stream_video(
    task_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Stream generated video content directly to the client
    """
    try:
        task_status = await runway_gen3_service.get_task_status(task_id)
        
        if task_status.status != "completed" or not task_status.video_url:
            raise HTTPException(
                status_code=404, 
                detail="Video not ready or failed to generate"
            )
        
        video_url = task_status.video_url
        
        # Stream video from Runway's URL
        async def video_streamer():
            async with httpx.AsyncClient() as client:
                async with client.stream('GET', video_url) as response:
                    async for chunk in response.aiter_bytes():
                        yield chunk
        
        return StreamingResponse(
            video_streamer(),
            media_type="video/mp4",
            headers={
                "Content-Disposition": f"inline; filename=runway_video_{task_id}.mp4",
                "Cache-Control": "public, max-age=3600"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Video streaming failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/task/{task_id}")
async def cancel_task(
    task_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Cancel a video generation task
    """
    try:
        if task_id not in runway_gen3_service.active_tasks:
            raise HTTPException(status_code=404, detail="Task not found")
        
        task_data = runway_gen3_service.active_tasks[task_id]
        
        # Verify task belongs to current user
        if task_data.get("user_id") != str(current_user.id):
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Only allow cancellation of non-completed tasks
        if task_data.get("status") in ["completed", "failed", "error", "timeout"]:
            raise HTTPException(
                status_code=400, 
                detail="Cannot cancel completed or failed task"
            )
        
        # Update task status
        runway_gen3_service.active_tasks[task_id]["status"] = "cancelled"
        runway_gen3_service.active_tasks[task_id]["error_message"] = "Task cancelled by user"
        
        logger.info(f"Task {task_id} cancelled by user {current_user.id}")
        
        return JSONResponse(content={"message": "Task cancelled successfully"})
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Task cancellation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/cleanup")
async def cleanup_old_tasks(
    hours_old: int = 24,
    current_user: User = Depends(get_current_user)
):
    """
    Clean up old completed tasks (admin or user's own tasks)
    """
    try:
        # For now, allow users to clean their own old tasks
        # In production, you might want admin-only access
        
        cleaned_count = await runway_gen3_service.cleanup_completed_tasks(hours_old)
        
        return JSONResponse(content={
            "message": f"Cleaned up {cleaned_count} old tasks",
            "cleaned_count": cleaned_count
        })
        
    except Exception as e:
        logger.error(f"Task cleanup failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Serve public files for image uploads
@router.get("/public/{filename}")
async def serve_public_file(filename: str):
    """Serve publicly accessible files for API consumption"""
    try:
        file_path = Path("/tmp/public") / filename
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        # Basic security check - prevent directory traversal
        if not str(file_path.resolve()).startswith("/tmp/public"):
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Determine content type based on file extension
        content_type = "application/octet-stream"
        if filename.lower().endswith(('.jpg', '.jpeg')):
            content_type = "image/jpeg"
        elif filename.lower().endswith('.png'):
            content_type = "image/png"
        elif filename.lower().endswith('.webp'):
            content_type = "image/webp"
        
        async def file_streamer():
            async with aiofiles.open(file_path, 'rb') as f:
                while chunk := await f.read(8192):
                    yield chunk
        
        return StreamingResponse(
            file_streamer(),
            media_type=content_type,
            headers={"Cache-Control": "public, max-age=3600"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"File serving failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
