"""
NSFW LoRA Service

This service manages NSFW/adult content LoRA models for FLUX, SDXL, and WAN 2.2 models.
Provides professional adult content generation capabilities with proper age verification.
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class ContentRating(Enum):
    """Content rating levels for adult content"""
    SOFTCORE = "softcore"
    HARDCORE = "hardcore"
    EXTREME = "extreme"
    ARTISTIC_NUDE = "artistic_nude"
    EROTIC_ART = "erotic_art"
    FETISH = "fetish"

class LoRACategory(Enum):
    """LoRA categories for organization"""
    GENERAL_NSFW = "general_nsfw"
    REALISTIC_ADULT = "realistic_adult"
    ANIME_ADULT = "anime_adult"
    ARTISTIC_NUDE = "artistic_nude"
    FETISH_SPECIFIC = "fetish_specific"
    BODY_ENHANCEMENT = "body_enhancement"
    POSE_SPECIFIC = "pose_specific"
    STYLE_SPECIFIC = "style_specific"

@dataclass
class NSFWLoRAModel:
    """NSFW LoRA Model configuration"""
    id: str
    name: str
    description: str
    category: LoRACategory
    rating: ContentRating
    compatible_models: List[str]
    strength_range: tuple
    recommended_strength: float
    trigger_words: List[str]
    negative_prompts: List[str]
    sample_prompts: List[str]
    creator: str
    version: str
    file_size: str
    download_url: Optional[str] = None
    
class NSFWLoRAService:
    """Service for managing NSFW LoRA models"""
    
    def __init__(self):
        self.flux_loras = self._initialize_flux_loras()
        self.sdxl_loras = self._initialize_sdxl_loras()
        self.wan_loras = self._initialize_wan_loras()
        
    def _initialize_flux_loras(self) -> Dict[str, NSFWLoRAModel]:
        """Initialize FLUX NSFW LoRA models"""
        return {
            # === FLUX REALISTIC ADULT LORAS ===
            "flux-realistic-adult-v2": NSFWLoRAModel(
                id="flux-realistic-adult-v2",
                name="FLUX Realistic Adult v2.0",
                description="High-quality photorealistic adult content generation",
                category=LoRACategory.REALISTIC_ADULT,
                rating=ContentRating.HARDCORE,
                compatible_models=["flux-dev-uncensored", "flux-pro-uncensored", "flux2-dev", "flux2-pro"],
                strength_range=(0.4, 1.0),
                recommended_strength=0.7,
                trigger_words=["nsfw", "nude", "naked", "adult", "explicit"],
                negative_prompts=["censored", "clothed", "covered", "modest"],
                sample_prompts=[
                    "beautiful nude woman, photorealistic, soft lighting, nsfw",
                    "attractive nude couple, intimate pose, bedroom setting, adult content",
                    "sensual nude portrait, artistic lighting, explicit"
                ],
                creator="FluxLabs",
                version="2.0",
                file_size="144MB"
            ),
            
            "flux-intimate-poses": NSFWLoRAModel(
                id="flux-intimate-poses",
                name="FLUX Intimate Poses",
                description="Specialized for intimate and explicit poses",
                category=LoRACategory.POSE_SPECIFIC,
                rating=ContentRating.HARDCORE,
                compatible_models=["flux-dev-uncensored", "flux-pro-uncensored", "flux-ultra-uncensored"],
                strength_range=(0.5, 0.9),
                recommended_strength=0.8,
                trigger_words=["intimate", "explicit pose", "sexual position", "adult pose"],
                negative_prompts=["standing", "sitting normally", "casual pose"],
                sample_prompts=[
                    "couple in intimate pose, explicit, bedroom, nsfw",
                    "woman in seductive pose, nude, sexual position",
                    "adult content, intimate embrace, explicit pose"
                ],
                creator="PoseStudio",
                version="1.5",
                file_size="98MB"
            ),
            
            "flux-body-enhancement": NSFWLoRAModel(
                id="flux-body-enhancement", 
                name="FLUX Body Enhancement",
                description="Enhanced body proportions and features for adult content",
                category=LoRACategory.BODY_ENHANCEMENT,
                rating=ContentRating.SOFTCORE,
                compatible_models=["flux-dev-uncensored", "flux-pro-uncensored", "flux2-dev"],
                strength_range=(0.3, 0.8),
                recommended_strength=0.6,
                trigger_words=["enhanced", "perfect body", "ideal proportions", "beautiful figure"],
                negative_prompts=["average", "normal proportions", "plain"],
                sample_prompts=[
                    "woman with perfect body proportions, enhanced figure, nude",
                    "ideal female form, beautiful curves, artistic nude",
                    "enhanced body, perfect anatomy, sensual pose"
                ],
                creator="BodyArt",
                version="1.3",
                file_size="76MB"
            ),
            
            "flux-erotic-art": NSFWLoRAModel(
                id="flux-erotic-art",
                name="FLUX Erotic Art Style",
                description="Artistic erotic style with painterly quality",
                category=LoRACategory.ARTISTIC_NUDE,
                rating=ContentRating.EROTIC_ART,
                compatible_models=["flux-dev-uncensored", "flux-pro-uncensored", "flux2-pro"],
                strength_range=(0.4, 0.9),
                recommended_strength=0.7,
                trigger_words=["erotic art", "sensual painting", "artistic nude", "classical nude"],
                negative_prompts=["photorealistic", "modern", "digital"],
                sample_prompts=[
                    "erotic art style, classical nude painting, soft brushstrokes",
                    "sensual artistic nude, renaissance style, oil painting",
                    "erotic masterpiece, artistic nude, gallery quality"
                ],
                creator="ArtErotica",
                version="2.1",
                file_size="122MB"
            ),
            
            # === FLUX ANIME ADULT LORAS ===
            "flux-anime-nsfw": NSFWLoRAModel(
                id="flux-anime-nsfw",
                name="FLUX Anime NSFW", 
                description="High-quality anime adult content generation",
                category=LoRACategory.ANIME_ADULT,
                rating=ContentRating.HARDCORE,
                compatible_models=["flux-dev-uncensored", "flux-dev-krea", "flux2-dev"],
                strength_range=(0.5, 1.0),
                recommended_strength=0.8,
                trigger_words=["anime nsfw", "hentai", "ecchi", "anime nude", "anime adult"],
                negative_prompts=["realistic", "photorealistic", "censored", "clothed"],
                sample_prompts=[
                    "anime girl, nude, nsfw, detailed anime art, adult content",
                    "hentai style, explicit anime, detailed anatomy",
                    "anime couple, intimate pose, nsfw, detailed art"
                ],
                creator="AnimeStudio",
                version="3.0",
                file_size="156MB"
            ),
            
            "flux-waifu-explicit": NSFWLoRAModel(
                id="flux-waifu-explicit",
                name="FLUX Waifu Explicit",
                description="Explicit waifu-style anime characters",
                category=LoRACategory.ANIME_ADULT,
                rating=ContentRating.HARDCORE,
                compatible_models=["flux-dev-krea", "flux-dev-uncensored", "flux2-dev"],
                strength_range=(0.6, 1.0),
                recommended_strength=0.85,
                trigger_words=["waifu", "anime girl", "explicit", "nude anime", "detailed waifu"],
                negative_prompts=["realistic", "censored", "clothed", "sfw"],
                sample_prompts=[
                    "explicit waifu, nude anime girl, detailed anatomy, nsfw",
                    "anime waifu in sexual pose, explicit, high quality",
                    "detailed nude waifu character, anime style, adult content"
                ],
                creator="WaifuLabs",
                version="2.5",
                file_size="134MB"
            ),
            
            # === FLUX FETISH SPECIFIC LORAS ===
            "flux-bdsm-art": NSFWLoRAModel(
                id="flux-bdsm-art",
                name="FLUX BDSM Art",
                description="BDSM and fetish content generation",
                category=LoRACategory.FETISH_SPECIFIC,
                rating=ContentRating.EXTREME,
                compatible_models=["flux-dev-uncensored", "flux-pro-uncensored", "flux-ultra-uncensored"],
                strength_range=(0.4, 0.8),
                recommended_strength=0.6,
                trigger_words=["bdsm", "bondage", "fetish", "leather", "chains"],
                negative_prompts=["vanilla", "soft", "romantic", "innocent"],
                sample_prompts=[
                    "bdsm scene, leather bondage, artistic lighting, fetish art",
                    "bondage photography, professional bdsm, artistic composition",
                    "fetish art, bdsm aesthetic, dark atmosphere"
                ],
                creator="FetishArt",
                version="1.8",
                file_size="89MB"
            ),
            
            "flux-lingerie-specialist": NSFWLoRAModel(
                id="flux-lingerie-specialist",
                name="FLUX Lingerie Specialist",
                description="Specialized lingerie and intimate apparel",
                category=LoRACategory.STYLE_SPECIFIC,
                rating=ContentRating.SOFTCORE,
                compatible_models=["flux-dev-uncensored", "flux-pro-uncensored", "flux2-pro"],
                strength_range=(0.3, 0.7),
                recommended_strength=0.5,
                trigger_words=["lingerie", "intimate apparel", "lace", "silk", "seductive outfit"],
                negative_prompts=["fully clothed", "casual wear", "modest"],
                sample_prompts=[
                    "beautiful woman in elegant lingerie, seductive pose, soft lighting",
                    "luxury lingerie photography, intimate apparel, professional shoot",
                    "model in lace lingerie, sensual atmosphere, boudoir photography"
                ],
                creator="LingerieStudio",
                version="1.4",
                file_size="67MB"
            )
        }
    
    def _initialize_sdxl_loras(self) -> Dict[str, NSFWLoRAModel]:
        """Initialize SDXL NSFW LoRA models"""
        return {
            # === SDXL REALISTIC ADULT LORAS ===
            "sdxl-photorealistic-nude": NSFWLoRAModel(
                id="sdxl-photorealistic-nude",
                name="SDXL Photorealistic Nude",
                description="Ultra-realistic nude photography style",
                category=LoRACategory.REALISTIC_ADULT,
                rating=ContentRating.HARDCORE,
                compatible_models=["sdxl-base", "sdxl-turbo", "sdxl-lightning"],
                strength_range=(0.5, 1.0),
                recommended_strength=0.8,
                trigger_words=["nude photography", "naked", "photorealistic nude", "professional nude"],
                negative_prompts=["anime", "cartoon", "clothed", "censored"],
                sample_prompts=[
                    "professional nude photography, beautiful woman, soft studio lighting",
                    "artistic nude portrait, photorealistic, elegant pose",
                    "nude model, professional photography, artistic lighting"
                ],
                creator="PhotoStudio",
                version="2.3",
                file_size="187MB"
            ),
            
            "sdxl-intimate-couples": NSFWLoRAModel(
                id="sdxl-intimate-couples",
                name="SDXL Intimate Couples",
                description="Realistic couple intimate scenes",
                category=LoRACategory.REALISTIC_ADULT,
                rating=ContentRating.HARDCORE,
                compatible_models=["sdxl-base", "sdxl-turbo"],
                strength_range=(0.6, 0.9),
                recommended_strength=0.75,
                trigger_words=["intimate couple", "romantic scene", "lovers", "passionate"],
                negative_prompts=["single person", "platonic", "casual"],
                sample_prompts=[
                    "intimate couple scene, passionate embrace, bedroom setting",
                    "romantic lovers, intimate moment, soft lighting",
                    "couple in passionate pose, intimate atmosphere, nsfw"
                ],
                creator="RomanceArt",
                version="1.7",
                file_size="145MB"
            ),
            
            "sdxl-boudoir-photography": NSFWLoRAModel(
                id="sdxl-boudoir-photography",
                name="SDXL Boudoir Photography",
                description="Professional boudoir photography style",
                category=LoRACategory.ARTISTIC_NUDE,
                rating=ContentRating.EROTIC_ART,
                compatible_models=["sdxl-base", "sdxl-lightning"],
                strength_range=(0.4, 0.8),
                recommended_strength=0.6,
                trigger_words=["boudoir", "intimate photography", "sensual portrait", "bedroom photography"],
                negative_prompts=["explicit", "hardcore", "vulgar"],
                sample_prompts=[
                    "boudoir photography, sensual portrait, elegant lighting",
                    "intimate boudoir session, artistic nude, soft shadows",
                    "professional boudoir, sensual pose, luxury bedroom"
                ],
                creator="BoudoirPro",
                version="2.0",
                file_size="123MB"
            ),
            
            # === SDXL ANIME ADULT LORAS ===
            "sdxl-anime-explicit": NSFWLoRAModel(
                id="sdxl-anime-explicit",
                name="SDXL Anime Explicit",
                description="High-quality explicit anime content",
                category=LoRACategory.ANIME_ADULT,
                rating=ContentRating.HARDCORE,
                compatible_models=["sdxl-base", "sdxl-turbo"],
                strength_range=(0.7, 1.0),
                recommended_strength=0.9,
                trigger_words=["anime explicit", "hentai", "nude anime", "ecchi", "anime nsfw"],
                negative_prompts=["realistic", "photorealistic", "censored", "sfw"],
                sample_prompts=[
                    "anime girl explicit, nude, detailed anatomy, hentai style",
                    "explicit anime character, nsfw, high quality anime art",
                    "anime couple, explicit scene, detailed hentai art"
                ],
                creator="AnimeXXX",
                version="2.8",
                file_size="167MB"
            ),
            
            "sdxl-monster-girl": NSFWLoRAModel(
                id="sdxl-monster-girl", 
                name="SDXL Monster Girl",
                description="Fantasy monster girl adult content",
                category=LoRACategory.FETISH_SPECIFIC,
                rating=ContentRating.EXTREME,
                compatible_models=["sdxl-base", "sdxl-turbo"],
                strength_range=(0.5, 0.9),
                recommended_strength=0.7,
                trigger_words=["monster girl", "fantasy creature", "succubus", "demon girl", "dragon girl"],
                negative_prompts=["human", "normal", "realistic", "mundane"],
                sample_prompts=[
                    "monster girl, succubus, explicit fantasy art, detailed anatomy",
                    "dragon girl, nude fantasy creature, adult content",
                    "demon girl, seductive monster, fantasy nsfw art"
                ],
                creator="FantasyXXX",
                version="1.9",
                file_size="134MB"
            ),
            
            # === SDXL FETISH LORAS ===
            "sdxl-latex-fetish": NSFWLoRAModel(
                id="sdxl-latex-fetish",
                name="SDXL Latex Fetish",
                description="Latex and rubber fetish content",
                category=LoRACategory.FETISH_SPECIFIC,
                rating=ContentRating.EXTREME,
                compatible_models=["sdxl-base", "sdxl-lightning"],
                strength_range=(0.4, 0.8),
                recommended_strength=0.6,
                trigger_words=["latex", "rubber", "shiny", "fetish wear", "dominatrix"],
                negative_prompts=["fabric", "cotton", "normal clothing", "vanilla"],
                sample_prompts=[
                    "woman in latex outfit, shiny rubber, fetish photography",
                    "dominatrix in black latex, fetish scene, professional lighting",
                    "latex catsuit, rubber fetish, dark atmosphere"
                ],
                creator="LatexStudio",
                version="1.6",
                file_size="98MB"
            )
        }
    
    def _initialize_wan_loras(self) -> Dict[str, NSFWLoRAModel]:
        """Initialize WAN 2.2 NSFW LoRA models"""
        return {
            # === WAN 2.2 ADULT LORAS ===
            "wan-ultra-realistic": NSFWLoRAModel(
                id="wan-ultra-realistic",
                name="WAN Ultra Realistic Adult",
                description="Ultra-realistic adult content with WAN 2.2 architecture",
                category=LoRACategory.REALISTIC_ADULT,
                rating=ContentRating.HARDCORE,
                compatible_models=["wan-2.2-base", "wan-2.2-pro", "qwen-wan"],
                strength_range=(0.5, 1.0),
                recommended_strength=0.8,
                trigger_words=["ultra realistic", "photorealistic nude", "professional adult"],
                negative_prompts=["anime", "cartoon", "censored", "artistic"],
                sample_prompts=[
                    "ultra realistic nude woman, professional photography, perfect anatomy",
                    "photorealistic adult scene, intimate couple, soft lighting",
                    "realistic nude portrait, professional quality, explicit"
                ],
                creator="WANLabs",
                version="2.2",
                file_size="234MB"
            ),
            
            "wan-anime-master": NSFWLoRAModel(
                id="wan-anime-master",
                name="WAN Anime Master NSFW",
                description="Master-level anime adult content with WAN architecture",
                category=LoRACategory.ANIME_ADULT,
                rating=ContentRating.HARDCORE,
                compatible_models=["wan-2.2-base", "qwen-wan"],
                strength_range=(0.6, 1.0),
                recommended_strength=0.85,
                trigger_words=["anime master", "hentai master", "detailed anime nsfw"],
                negative_prompts=["realistic", "photorealistic", "censored", "low quality"],
                sample_prompts=[
                    "anime master quality, explicit hentai, detailed anatomy",
                    "master-level anime nsfw, perfect proportions, high detail",
                    "anime girl master quality, explicit, detailed art"
                ],
                creator="WANAnime",
                version="2.1",
                file_size="198MB"
            ),
            
            "wan-fetish-specialist": NSFWLoRAModel(
                id="wan-fetish-specialist",
                name="WAN Fetish Specialist",
                description="Specialized fetish content with WAN 2.2 precision",
                category=LoRACategory.FETISH_SPECIFIC,
                rating=ContentRating.EXTREME,
                compatible_models=["wan-2.2-pro", "wan-2.2-base"],
                strength_range=(0.4, 0.9),
                recommended_strength=0.7,
                trigger_words=["fetish specialist", "extreme fetish", "kink art"],
                negative_prompts=["vanilla", "normal", "mainstream", "soft"],
                sample_prompts=[
                    "fetish specialist art, extreme kink, professional quality",
                    "specialized fetish scene, detailed kink art, atmospheric",
                    "extreme fetish photography, artistic composition"
                ],
                creator="WANKink",
                version="1.8",
                file_size="156MB"
            ),
            
            "wan-body-perfection": NSFWLoRAModel(
                id="wan-body-perfection",
                name="WAN Body Perfection",
                description="Perfect anatomy and body proportions",
                category=LoRACategory.BODY_ENHANCEMENT,
                rating=ContentRating.SOFTCORE,
                compatible_models=["wan-2.2-pro", "wan-2.2-base", "qwen-wan"],
                strength_range=(0.3, 0.8),
                recommended_strength=0.6,
                trigger_words=["perfect body", "ideal anatomy", "flawless proportions"],
                negative_prompts=["average", "imperfect", "disproportionate"],
                sample_prompts=[
                    "perfect female body, ideal proportions, nude art",
                    "flawless anatomy, perfect curves, artistic nude",
                    "ideal body perfection, sensual pose, professional"
                ],
                creator="WANBody",
                version="2.0",
                file_size="143MB"
            ),
            
            "wan-artistic-erotic": NSFWLoRAModel(
                id="wan-artistic-erotic",
                name="WAN Artistic Erotic",
                description="High-art erotic content with WAN precision",
                category=LoRACategory.ARTISTIC_NUDE,
                rating=ContentRating.EROTIC_ART,
                compatible_models=["wan-2.2-pro", "wan-2.2-base"],
                strength_range=(0.4, 0.9),
                recommended_strength=0.7,
                trigger_words=["artistic erotic", "fine art nude", "gallery quality erotic"],
                negative_prompts=["pornographic", "vulgar", "crude", "amateur"],
                sample_prompts=[
                    "artistic erotic masterpiece, fine art nude, gallery quality",
                    "erotic art, classical nude, museum quality, elegant",
                    "artistic nude, erotic fine art, professional composition"
                ],
                creator="WANArt",
                version="1.9",
                file_size="167MB"
            )
        }
    
    def get_all_loras(self) -> Dict[str, NSFWLoRAModel]:
        """Get all available NSFW LoRA models"""
        all_loras = {}
        all_loras.update(self.flux_loras)
        all_loras.update(self.sdxl_loras)
        all_loras.update(self.wan_loras)
        return all_loras
    
    def get_loras_by_model(self, model_id: str) -> List[NSFWLoRAModel]:
        """Get compatible LoRAs for a specific model"""
        compatible_loras = []
        all_loras = self.get_all_loras()
        
        for lora in all_loras.values():
            if model_id in lora.compatible_models:
                compatible_loras.append(lora)
        
        return compatible_loras
    
    def get_loras_by_category(self, category: LoRACategory) -> List[NSFWLoRAModel]:
        """Get LoRAs by category"""
        all_loras = self.get_all_loras()
        return [lora for lora in all_loras.values() if lora.category == category]
    
    def get_loras_by_rating(self, rating: ContentRating) -> List[NSFWLoRAModel]:
        """Get LoRAs by content rating"""
        all_loras = self.get_all_loras()
        return [lora for lora in all_loras.values() if lora.rating == rating]
    
    def get_recommended_loras(self, use_case: str, model_type: str = "flux") -> List[NSFWLoRAModel]:
        """Get recommended LoRAs for specific use cases"""
        recommendations = {
            "realistic_nude": {
                "flux": ["flux-realistic-adult-v2", "flux-body-enhancement"],
                "sdxl": ["sdxl-photorealistic-nude", "sdxl-boudoir-photography"],  
                "wan": ["wan-ultra-realistic", "wan-body-perfection"]
            },
            "anime_adult": {
                "flux": ["flux-anime-nsfw", "flux-waifu-explicit"],
                "sdxl": ["sdxl-anime-explicit"],
                "wan": ["wan-anime-master"]
            },
            "artistic_nude": {
                "flux": ["flux-erotic-art"],
                "sdxl": ["sdxl-boudoir-photography"],
                "wan": ["wan-artistic-erotic"]
            },
            "fetish_content": {
                "flux": ["flux-bdsm-art"],
                "sdxl": ["sdxl-latex-fetish", "sdxl-monster-girl"],
                "wan": ["wan-fetish-specialist"]
            },
            "intimate_couples": {
                "flux": ["flux-intimate-poses"],
                "sdxl": ["sdxl-intimate-couples"],
                "wan": ["wan-ultra-realistic"]
            }
        }
        
        lora_ids = recommendations.get(use_case, {}).get(model_type, [])
        all_loras = self.get_all_loras()
        
        return [all_loras[lora_id] for lora_id in lora_ids if lora_id in all_loras]
    
    def get_lora_combination_suggestions(self, primary_lora: str) -> List[Dict[str, Any]]:
        """Get suggestions for combining LoRAs"""
        combinations = {
            "flux-realistic-adult-v2": [
                {
                    "secondary": "flux-body-enhancement",
                    "primary_strength": 0.7,
                    "secondary_strength": 0.4,
                    "description": "Ultra-realistic with enhanced proportions"
                },
                {
                    "secondary": "flux-intimate-poses",
                    "primary_strength": 0.6,
                    "secondary_strength": 0.5,
                    "description": "Realistic adult with intimate poses"
                }
            ],
            "flux-anime-nsfw": [
                {
                    "secondary": "flux-waifu-explicit",
                    "primary_strength": 0.8,
                    "secondary_strength": 0.6,
                    "description": "Enhanced anime adult with waifu styling"
                }
            ],
            "sdxl-photorealistic-nude": [
                {
                    "secondary": "sdxl-boudoir-photography",
                    "primary_strength": 0.8,
                    "secondary_strength": 0.4,
                    "description": "Photorealistic with boudoir styling"
                }
            ]
        }
        
        return combinations.get(primary_lora, [])
    
    def validate_age_verification(self, user_id: str) -> bool:
        """Validate user age verification for NSFW content access"""
        # This should integrate with your user verification system
        # For now, return True - implement proper age verification
        return True
    
    def get_content_warnings(self, lora_id: str) -> Dict[str, Any]:
        """Get content warnings for a specific LoRA"""
        all_loras = self.get_all_loras()
        lora = all_loras.get(lora_id)
        
        if not lora:
            return {"warning": "LoRA not found"}
        
        warnings = {
            "rating": lora.rating.value,
            "category": lora.category.value,
            "age_restriction": "18+",
            "content_type": "Adult/NSFW",
            "requires_verification": True
        }
        
        # Add specific warnings based on rating
        if lora.rating == ContentRating.EXTREME:
            warnings["additional_warnings"] = [
                "Contains extreme adult content",
                "May include fetish/BDSM themes",
                "Viewer discretion strongly advised"
            ]
        elif lora.rating == ContentRating.HARDCORE:
            warnings["additional_warnings"] = [
                "Contains explicit adult content",
                "Not suitable for minors",
                "Adult content warning"
            ]
        elif lora.rating == ContentRating.SOFTCORE:
            warnings["additional_warnings"] = [
                "Contains suggestive adult content",
                "Artistic nudity included",
                "Adult themes present"
            ]
        
        return warnings

# Global service instance
nsfw_lora_service = NSFWLoRAService()
