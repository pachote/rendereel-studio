"""
NSFW LoRA API Routes

This module provides API endpoints for NSFW/adult content LoRA models,
including model listing, compatibility checks, and content warnings.
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
import logging

from services.nsfw_lora_service import (
    nsfw_lora_service,
    NSFWLoRAModel,
    LoRACategory,
    ContentRating
)
from middleware.auth_middleware import get_current_user
from models.base import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/nsfw-loras", tags=["NSFW LoRAs"])

class LoRASearchRequest(BaseModel):
    """Request model for LoRA search"""
    model_id: Optional[str] = Field(None, description="Target model ID")
    category: Optional[str] = Field(None, description="LoRA category")
    rating: Optional[str] = Field(None, description="Content rating")
    use_case: Optional[str] = Field(None, description="Specific use case")

class LoRACombinationRequest(BaseModel):
    """Request model for LoRA combination suggestions"""
    primary_lora: str = Field(..., description="Primary LoRA ID")
    model_id: str = Field(..., description="Target model ID")

# Age verification middleware
async def verify_adult_access(current_user: User = Depends(get_current_user)):
    """Verify user has adult content access"""
    # Check if user is verified for adult content
    if not nsfw_lora_service.validate_age_verification(str(current_user.id)):
        raise HTTPException(
            status_code=403, 
            detail="Age verification required for adult content access"
        )
    return current_user

@router.get("/models/{model_id}/compatible")
async def get_compatible_loras(
    model_id: str,
    category: Optional[str] = Query(None, description="Filter by category"),
    rating: Optional[str] = Query(None, description="Filter by content rating"),
    current_user: User = Depends(verify_adult_access)
):
    """
    Get NSFW LoRAs compatible with a specific model
    """
    try:
        compatible_loras = nsfw_lora_service.get_loras_by_model(model_id)
        
        # Apply filters if provided
        if category:
            try:
                category_enum = LoRACategory(category)
                compatible_loras = [
                    lora for lora in compatible_loras 
                    if lora.category == category_enum
                ]
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid category: {category}")
        
        if rating:
            try:
                rating_enum = ContentRating(rating)
                compatible_loras = [
                    lora for lora in compatible_loras 
                    if lora.rating == rating_enum
                ]
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid rating: {rating}")
        
        # Convert to dict format for JSON response
        lora_data = []
        for lora in compatible_loras:
            lora_dict = {
                "id": lora.id,
                "name": lora.name,
                "description": lora.description,
                "category": lora.category.value,
                "rating": lora.rating.value,
                "recommended_strength": lora.recommended_strength,
                "strength_range": lora.strength_range,
                "trigger_words": lora.trigger_words,
                "negative_prompts": lora.negative_prompts,
                "sample_prompts": lora.sample_prompts,
                "creator": lora.creator,
                "version": lora.version,
                "file_size": lora.file_size,
                "content_warnings": nsfw_lora_service.get_content_warnings(lora.id)
            }
            lora_data.append(lora_dict)
        
        logger.info(f"Retrieved {len(lora_data)} compatible LoRAs for model {model_id}")
        
        return JSONResponse(content={
            "model_id": model_id,
            "compatible_loras": lora_data,
            "total_count": len(lora_data)
        })
        
    except Exception as e:
        logger.error(f"Failed to get compatible LoRAs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/categories")
async def get_lora_categories(
    current_user: User = Depends(verify_adult_access)
):
    """Get available LoRA categories"""
    try:
        categories = [
            {
                "value": cat.value,
                "label": cat.value.replace("_", " ").title(),
                "description": {
                    "general_nsfw": "General adult/NSFW content",
                    "realistic_adult": "Photorealistic adult content",
                    "anime_adult": "Anime/manga adult content",
                    "artistic_nude": "Artistic nude and erotic art",
                    "fetish_specific": "Fetish and kink content",
                    "body_enhancement": "Enhanced body proportions",
                    "pose_specific": "Intimate and explicit poses",
                    "style_specific": "Style-focused content"
                }.get(cat.value, "")
            }
            for cat in LoRACategory
        ]
        
        return JSONResponse(content={"categories": categories})
        
    except Exception as e:
        logger.error(f"Failed to get categories: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ratings")
async def get_content_ratings(
    current_user: User = Depends(verify_adult_access)
):
    """Get available content ratings"""
    try:
        ratings = [
            {
                "value": rating.value,
                "label": rating.value.replace("_", " ").title(),
                "description": {
                    "softcore": "Suggestive content, artistic nudity",
                    "hardcore": "Explicit adult content",
                    "extreme": "Extreme adult content, fetish themes",
                    "artistic_nude": "Artistic nude photography/art",
                    "erotic_art": "Erotic and sensual art",
                    "fetish": "Fetish and kink content"
                }.get(rating.value, "")
            }
            for rating in ContentRating
        ]
        
        return JSONResponse(content={"ratings": ratings})
        
    except Exception as e:
        logger.error(f"Failed to get ratings: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search")
async def search_loras(
    request: LoRASearchRequest,
    current_user: User = Depends(verify_adult_access)
):
    """
    Search NSFW LoRAs with multiple filters
    """
    try:
        results = []
        
        if request.model_id:
            results = nsfw_lora_service.get_loras_by_model(request.model_id)
        elif request.category:
            try:
                category_enum = LoRACategory(request.category)
                results = nsfw_lora_service.get_loras_by_category(category_enum)
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid category: {request.category}")
        elif request.rating:
            try:
                rating_enum = ContentRating(request.rating)
                results = nsfw_lora_service.get_loras_by_rating(rating_enum)
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid rating: {request.rating}")
        else:
            # Get all LoRAs if no specific filter
            all_loras = nsfw_lora_service.get_all_loras()
            results = list(all_loras.values())
        
        # Convert to dict format
        lora_data = []
        for lora in results:
            lora_dict = {
                "id": lora.id,
                "name": lora.name,
                "description": lora.description,
                "category": lora.category.value,
                "rating": lora.rating.value,
                "compatible_models": lora.compatible_models,
                "recommended_strength": lora.recommended_strength,
                "strength_range": lora.strength_range,
                "trigger_words": lora.trigger_words,
                "creator": lora.creator,
                "version": lora.version,
                "file_size": lora.file_size
            }
            lora_data.append(lora_dict)
        
        return JSONResponse(content={
            "search_criteria": request.dict(),
            "results": lora_data,
            "total_count": len(lora_data)
        })
        
    except Exception as e:
        logger.error(f"LoRA search failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recommendations/{use_case}")
async def get_lora_recommendations(
    use_case: str,
    model_type: str = Query(default="flux", description="Model type (flux, sdxl, wan)"),
    current_user: User = Depends(verify_adult_access)
):
    """
    Get recommended LoRAs for specific use cases
    """
    try:
        valid_use_cases = [
            "realistic_nude", "anime_adult", "artistic_nude", 
            "fetish_content", "intimate_couples"
        ]
        
        if use_case not in valid_use_cases:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid use case. Valid options: {', '.join(valid_use_cases)}"
            )
        
        recommendations = nsfw_lora_service.get_recommended_loras(use_case, model_type)
        
        # Convert to dict format
        lora_data = []
        for lora in recommendations:
            lora_dict = {
                "id": lora.id,
                "name": lora.name,
                "description": lora.description,
                "category": lora.category.value,
                "rating": lora.rating.value,
                "recommended_strength": lora.recommended_strength,
                "trigger_words": lora.trigger_words,
                "sample_prompts": lora.sample_prompts,
                "creator": lora.creator,
                "version": lora.version,
                "content_warnings": nsfw_lora_service.get_content_warnings(lora.id)
            }
            lora_data.append(lora_dict)
        
        return JSONResponse(content={
            "use_case": use_case,
            "model_type": model_type,
            "recommendations": lora_data,
            "total_count": len(lora_data)
        })
        
    except Exception as e:
        logger.error(f"Failed to get recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/combinations")
async def get_lora_combinations(
    request: LoRACombinationRequest,
    current_user: User = Depends(verify_adult_access)
):
    """
    Get suggestions for combining LoRAs
    """
    try:
        combinations = nsfw_lora_service.get_lora_combination_suggestions(request.primary_lora)
        
        # Validate that combinations are compatible with the target model
        compatible_combinations = []
        for combo in combinations:
            secondary_lora_id = combo["secondary"]
            all_loras = nsfw_lora_service.get_all_loras()
            
            if secondary_lora_id in all_loras:
                secondary_lora = all_loras[secondary_lora_id]
                if request.model_id in secondary_lora.compatible_models:
                    compatible_combinations.append({
                        **combo,
                        "secondary_lora_details": {
                            "name": secondary_lora.name,
                            "category": secondary_lora.category.value,
                            "rating": secondary_lora.rating.value
                        }
                    })
        
        return JSONResponse(content={
            "primary_lora": request.primary_lora,
            "target_model": request.model_id,
            "combinations": compatible_combinations,
            "total_combinations": len(compatible_combinations)
        })
        
    except Exception as e:
        logger.error(f"Failed to get LoRA combinations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/lora/{lora_id}/details")
async def get_lora_details(
    lora_id: str,
    current_user: User = Depends(verify_adult_access)
):
    """
    Get detailed information about a specific LoRA
    """
    try:
        all_loras = nsfw_lora_service.get_all_loras()
        
        if lora_id not in all_loras:
            raise HTTPException(status_code=404, detail="LoRA not found")
        
        lora = all_loras[lora_id]
        content_warnings = nsfw_lora_service.get_content_warnings(lora_id)
        combinations = nsfw_lora_service.get_lora_combination_suggestions(lora_id)
        
        lora_details = {
            "id": lora.id,
            "name": lora.name,
            "description": lora.description,
            "category": lora.category.value,
            "rating": lora.rating.value,
            "compatible_models": lora.compatible_models,
            "strength_range": lora.strength_range,
            "recommended_strength": lora.recommended_strength,
            "trigger_words": lora.trigger_words,
            "negative_prompts": lora.negative_prompts,
            "sample_prompts": lora.sample_prompts,
            "creator": lora.creator,
            "version": lora.version,
            "file_size": lora.file_size,
            "content_warnings": content_warnings,
            "combination_suggestions": combinations
        }
        
        return JSONResponse(content=lora_details)
        
    except Exception as e:
        logger.error(f"Failed to get LoRA details: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
async def get_lora_statistics(
    current_user: User = Depends(verify_adult_access)
):
    """
    Get statistics about available NSFW LoRAs
    """
    try:
        all_loras = nsfw_lora_service.get_all_loras()
        
        stats = {
            "total_loras": len(all_loras),
            "by_category": {},
            "by_rating": {},
            "by_model_type": {
                "flux": len(nsfw_lora_service.flux_loras),
                "sdxl": len(nsfw_lora_service.sdxl_loras),
                "wan": len(nsfw_lora_service.wan_loras)
            }
        }
        
        # Count by category
        for category in LoRACategory:
            category_loras = nsfw_lora_service.get_loras_by_category(category)
            stats["by_category"][category.value] = len(category_loras)
        
        # Count by rating
        for rating in ContentRating:
            rating_loras = nsfw_lora_service.get_loras_by_rating(rating)
            stats["by_rating"][rating.value] = len(rating_loras)
        
        return JSONResponse(content={"statistics": stats})
        
    except Exception as e:
        logger.error(f"Failed to get statistics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check for NSFW LoRA service"""
    try:
        all_loras = nsfw_lora_service.get_all_loras()
        
        return JSONResponse(content={
            "service": "NSFW LoRA Service",
            "status": "healthy",
            "total_loras": len(all_loras),
            "flux_loras": len(nsfw_lora_service.flux_loras),
            "sdxl_loras": len(nsfw_lora_service.sdxl_loras),
            "wan_loras": len(nsfw_lora_service.wan_loras),
            "categories": len(LoRACategory),
            "ratings": len(ContentRating)
        })
        
    except Exception as e:
        logger.error(f"NSFW LoRA service health check failed: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={"service": "NSFW LoRA Service", "status": "unhealthy", "error": str(e)}
        )
