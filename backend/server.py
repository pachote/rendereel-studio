# AI Generation Platform - FastAPI Backend
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from database import connect_to_mongo, db
from config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import services
from services.flux_service import FluxService
from services.video_service import VideoGenerationService
from services.hybrid_service import hybrid_service
from services.lora_service import lora_service
from services.lora_training_service import lora_training_service
from services.lora_marketplace_service import lora_marketplace_service
from services.lora_community_service import lora_community_service
from services.forge_cloud_service import rendereel_generation_studio_service as forge_cloud_service
from services.kling_lipSync_service import kling_lip_sync_service
from services.content_filter import ContentFilterService
from services.admin_service import AdminService
from services.billing_service import BillingService
from services.content_service import ContentService
from services.analytics_service import AnalyticsService
from services.system_service import SystemService
from services.emergent_auth_service import EmergentAuthService
from services.payment_service import PaymentService
from services.ai_chat_service import AIChatService
from services.ai_video_editor_service import AIVideoEditorService
from services.elevenlabs_service import ElevenLabsService
from services.marketing_service import marketing_service
from services.contest_service import contest_service
from services.showcase_service import showcase_service
from services.video_upscaler_service import video_upscaler_service
from services.marketplace_service import marketplace_service
from services.artist_portfolio_service import artist_portfolio_service
from services.video_upload_service import video_upload_service
from services.character_singer_service import character_singer_service
from services.software_license_service import SoftwareLicenseService
from services.rendereel_license_service import RendereeelLicenseService
from services.hybrid_gpu_service import get_hybrid_gpu_service
from services.social_media_automation_service import RendereeelSocialMediaService

# Import routes
from routes.auth import router as auth_router
from routes.generation import router as generation_router
from routes.lora import router as lora_router
from routes.lora_training import router as lora_training_router
from routes.lora_marketplace import router as lora_marketplace_router
from routes.lora_community import router as lora_community_router
from routes.forge_cloud import router as forge_cloud_router
from routes.lip_sync import router as lip_sync_router
from routes.social import router as social_router
from routes.nsfw_filter import router as nsfw_filter_router
from routes.admin import router as admin_router
from routes.admin_billing import router as admin_billing_router
from routes.admin_content import router as admin_content_router
from routes.admin_analytics import router as admin_analytics_router
from routes.admin_system import router as admin_system_router
from routes.ai_chat import router as ai_chat_router
from routes.video_editor import router as video_editor_router
from routes.music_generation import router as music_router
from routes.marketing import router as marketing_router
from routes.contest import router as contest_router
from routes.showcase import router as showcase_router
from routes.video_upscaler import router as video_upscaler_router
from routes.marketplace import router as marketplace_router
from routes.artist_portfolio import router as artist_portfolio_router
from routes.video_upload import router as video_upload_router
from routes.character_singer import router as character_singer_router
from routes.software_license import router as software_license_router
from routes.rendereel_license import router as rendereel_license_router
from routes.hybrid_gpu import router as hybrid_gpu_router
from routes.enhanced_models import router as enhanced_models_router
from routes.enhanced_lora import router as enhanced_lora_router
from routes.ai_chatbot import router as ai_chatbot_router
from routes.user_catalog import router as user_catalog_router
from routes.social_media_automation import router as social_media_automation_router
from routes.enhanced_ai_video_editor import router as enhanced_ai_video_editor_router
from services.comfy_studio_service import rendereel_node_studio_service
from routes.advanced_video_generation import router as advanced_video_router
from routes.kling_ai_routes import router as kling_ai_router
from routes.google_ai_routes import router as google_ai_router
from routes.runway_gen3_routes import router as runway_gen3_router
from routes.nsfw_lora_routes import router as nsfw_lora_router
from routes.comfyui_studio import router as rendereel_node_studio_router

# Initialize services
flux_service = FluxService()
video_service = VideoGenerationService()
content_filter = ContentFilterService()
admin_service = AdminService()
billing_service = BillingService() 
content_service = ContentService()
analytics_service = AnalyticsService()
system_service = SystemService()
emergent_auth_service = EmergentAuthService()
payment_service = PaymentService()
ai_chat_service = AIChatService()
ai_video_editor_service = AIVideoEditorService()
elevenlabs_service = ElevenLabsService()

# Import and initialize AI chatbot service
from services.user_catalog_service import user_catalog_service
from services.ai_chatbot_service import RendereeelAIChatbotService
ai_chatbot_service = RendereeelAIChatbotService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting AI Generation Platform...")
    
    try:
        # Initialize database
        await connect_to_mongo()
        
        # Initialize services that have initialize methods
        await flux_service.initialize()
        await video_service.initialize()
        await hybrid_service.initialize()
        await lora_service.initialize()
        await lora_training_service.initialize()
        await lora_marketplace_service.initialize()
        await lora_community_service.initialize()
        await forge_cloud_service.initialize()
        await kling_lip_sync_service.initialize()
        await payment_service.initialize()
        await marketing_service.initialize()
        await contest_service.initialize()
        await showcase_service.initialize()
        await video_upscaler_service.initialize()
        await marketplace_service.initialize()
        await artist_portfolio_service.initialize()
        await video_upload_service.initialize()
        await character_singer_service.initialize()
        await user_catalog_service.initialize()
        await ai_chatbot_service.initialize()
        
        # Set the chatbot service in routes
        from routes.ai_chatbot import set_chatbot_service
        set_chatbot_service(ai_chatbot_service)
        
        # Initialize hybrid GPU service
        hybrid_gpu_service = get_hybrid_gpu_service(db.database)
        await hybrid_gpu_service.initialize()
        
        # Initialize social media automation service
        social_media_service = RendereeelSocialMediaService()
        await social_media_service.initialize()
        
        logger.info("✅ All services initialized successfully")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize services: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down AI Generation Platform...")

# Create FastAPI app with lifespan
app = FastAPI(
    title="AI Generation Platform",
    description="Professional AI Image & Video Generation Platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(generation_router)
app.include_router(lora_router)
app.include_router(lora_training_router)
app.include_router(lora_marketplace_router)
app.include_router(lora_community_router)
app.include_router(forge_cloud_router)
app.include_router(lip_sync_router)
app.include_router(social_router)
app.include_router(nsfw_filter_router)
app.include_router(admin_router)
app.include_router(admin_billing_router)
app.include_router(admin_content_router)
app.include_router(admin_analytics_router)
app.include_router(admin_system_router)
app.include_router(ai_chat_router)
app.include_router(video_editor_router)
app.include_router(music_router)
app.include_router(marketing_router, prefix="/api/marketing")
app.include_router(contest_router, prefix="/api/contest")
app.include_router(showcase_router, prefix="/api/showcase")
app.include_router(video_upscaler_router, prefix="/api/video-upscaler")
app.include_router(marketplace_router, prefix="/api/marketplace")
app.include_router(artist_portfolio_router, prefix="/api/artist-portfolio")
app.include_router(video_upload_router, prefix="/api/video-upload")
app.include_router(character_singer_router, prefix="/api/character-singer")
app.include_router(software_license_router, prefix="/api/software-license")
app.include_router(rendereel_license_router, prefix="/api/rendereel-license")
app.include_router(hybrid_gpu_router, prefix="/api/hybrid-gpu")
app.include_router(enhanced_models_router, prefix="/api/enhanced-models")
app.include_router(enhanced_lora_router, prefix="/api/enhanced-lora")
app.include_router(user_catalog_router)
app.include_router(ai_chatbot_router)
app.include_router(social_media_automation_router, prefix="/api/social-media-automation")
app.include_router(enhanced_ai_video_editor_router)
app.include_router(rendereel_node_studio_router)
app.include_router(advanced_video_router)
app.include_router(kling_ai_router)
app.include_router(google_ai_router)
app.include_router(runway_gen3_router, prefix="/api")
app.include_router(nsfw_lora_router, prefix="/api")

# Serve uploaded files
app.mount("/uploads", StaticFiles(directory="/app/uploads"), name="uploads")

# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "AI Generation Platform is running",
        "version": "1.0.0"
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to AI Generation Platform API",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "server:app", 
        host="0.0.0.0", 
        port=8001, 
        reload=True,
        log_level="info"
    )
