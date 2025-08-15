import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from './contexts/ThemeContext';
import { NSFWProvider } from './contexts/NSFWContext';

// RENDEREEL STUDIO Components
import RendereeelHeader from './components/RendereeelHeader';
import UserGallery from './pages/UserGallery';
import PremiereLikeVideoEditor from './pages/PremiereLikeVideoEditor';
import EnhancedAIVideoEditor from './pages/EnhancedAIVideoEditor';
import AdvancedVideoStudio from './pages/AdvancedVideoStudio';

// RENDEREEL STUDIO Pages
import RendereeelHome from './pages/RendereeelHome';
import RendereeelAI from './pages/RendereeelAI';
import RendereeelPricing from './pages/RendereeelPricing';
import HybridGPUDashboard from './pages/HybridGPUDashboard';
import UltimateGenerationStudio from './pages/UltimateGenerationStudio';
import UltimateGenerationStudioPro from './pages/UltimateGenerationStudioPro';
import AIToolsHub from './pages/AIToolsHub';
import ProductsPage from './pages/ProductsPage';
import PerformanceTracker from './components/PerformanceTracker';
import PromptTemplates from './components/PromptTemplates';

// Professional Software Pages
import UltraScalePro from './pages/UltraScalePro';
import VideoEditorPro from './pages/VideoEditorPro';

// Legacy Pages (for backwards compatibility)
import Home from './pages/Home';
import Generate from './pages/Generate';
import Gallery from './pages/Gallery';
import Search from './pages/Search';
import Community from './pages/Community';
import Profile from './pages/Profile';
import EnhancedProfile from './pages/EnhancedProfile';
import ContestHub from './pages/ContestHub';
import LoRAStudio from './pages/LoRAStudio';
import VideoGeneration from './pages/VideoGeneration';
import Login from './pages/Login';
import PaymentSuccess from './pages/PaymentSuccess';
import PaymentCancel from './pages/PaymentCancel';
import AIChat from './pages/AIChat';
import VideoEditor from './pages/VideoEditor';
import MusicGeneration from './pages/MusicGeneration';
import UltraScale from './pages/UltraScale';
import Marketplace from './pages/Marketplace';
import ArtistPortfolio from './pages/ArtistPortfolio';
import VideoUpload from './pages/VideoUpload';
import CharacterSinger from './pages/CharacterSinger';
import CompleteForgeWebUI from './pages/CompleteForgeWebUI';
import EnhancedForgeStudio from './pages/EnhancedForgeStudio';

// Admin Pages
import AdminDashboard from './pages/AdminDashboard';
import AdminUsers from './pages/AdminUsers';
import AdminBilling from './pages/AdminBilling';
import AdminContent from './pages/AdminContent';
import AdminAnalytics from './pages/AdminAnalytics';
import AdminSystem from './pages/AdminSystem';
import AdminMarketing from './pages/AdminMarketing';
import SocialMediaAutomation from './pages/SocialMediaAutomation';

// Professional UI Pages
import ProfessionalHome from './pages/ProfessionalHome';
import ProfessionalGallery from './pages/ProfessionalGallery';
import ProfessionalGenerate from './pages/ProfessionalGenerate';

// UI Pages
import UltraHome from './pages/UltraHome';
import UltraAIChat from './pages/UltraAIChat';
import UltraMusicGeneration from './pages/UltraMusicGeneration';
import ForgeStudio from './pages/ForgeStudio';
import Showcase from './pages/Showcase';

// Components
import AIChatbot from './components/AIChatbot';

// Styles
import './App.css';
import './styles/rendereel-design-system.css';
import './styles/civitai-inspired.css';

function App() {
  return (
    <ThemeProvider>
      <NSFWProvider>
        <Router>
          <div className="App bg-gray-900 min-h-screen">
            <RendereeelHeader />
            
            <Routes>
              {/* RENDEREEL STUDIO - Main Routes */}
              <Route path="/" element={<RendereeelHome />} />
              <Route path="/rendereel-ai" element={<RendereeelAI />} />
              <Route path="/rendereel-upscaler" element={<UltraScalePro />} />
              <Route path="/rendereel-editor" element={<VideoEditorPro />} />
              <Route path="/rendereel-singer" element={<CharacterSinger />} />
              <Route path="/rendereel-suite" element={<RendereeelAI />} />
              <Route path="/pricing" element={<RendereeelPricing />} />
              <Route path="/ai-tools" element={<AIToolsHub />} />
              <Route path="/products" element={<ProductsPage />} />
              <Route path="/hybrid-gpu" element={<HybridGPUDashboard />} />
              <Route path="/ultimate-studio" element={<UltimateGenerationStudio />} />
              <Route path="/ultimate-studio-pro" element={<UltimateGenerationStudioPro />} />
              
              {/* Professional Software Routes */}
              <Route path="/ultra-scale-pro" element={<UltraScalePro />} />
              <Route path="/video-editor-ai" element={<EnhancedAIVideoEditor />} />
              <Route path="/video-studio-pro" element={<AdvancedVideoStudio />} />
              <Route path="/rendereel-node-studio" element={<CompleteForgeWebUI />} />
              <Route path="/rendereel-generation-studio" element={<EnhancedForgeStudio />} />
              <Route path="/video-editor-pro" element={<PremiereLikeVideoEditor />} />
              
              {/* Enhanced Forge WebUI */}
              <Route path="/complete-forge-webui" element={<CompleteForgeWebUI />} />
              <Route path="/forge" element={<CompleteForgeWebUI />} />
              
              {/* Authentication & User Management */}
              <Route path="/login" element={<Login />} />
              <Route path="/profile" element={<EnhancedProfile />} />
              
              {/* Community & Content */}
              <Route path="/gallery" element={<UserGallery />} />
              <Route path="/community" element={<Community />} />
              <Route path="/search" element={<Search />} />
              <Route path="/showcase" element={<Showcase />} />
              
              {/* Creative Tools & Features */}
              <Route path="/generate" element={<ProfessionalGenerate />} />
              <Route path="/video-generation" element={<VideoGeneration />} />
              <Route path="/ai-chat" element={<AIChat />} />
              <Route path="/music-generation" element={<MusicGeneration />} />
              <Route path="/lora-studio" element={<LoRAStudio />} />
              <Route path="/contest-hub" element={<ContestHub />} />
              
              {/* Marketplace & Commerce */}
              <Route path="/marketplace" element={<Marketplace />} />
              <Route path="/artist-portfolio" element={<ArtistPortfolio />} />
              <Route path="/video-upload" element={<VideoUpload />} />
              
              {/* Character & Animation */}
              <Route path="/character-singer" element={<CharacterSinger />} />
              
              {/* Legacy Video Tools */}
              <Route path="/video-editor" element={<VideoEditor />} />
              <Route path="/ultra-scale" element={<UltraScale />} />
              
              {/* Payment & Billing */}
              <Route path="/payment-success" element={<PaymentSuccess />} />
              <Route path="/payment-cancel" element={<PaymentCancel />} />
              
              {/* Admin Dashboard Routes */}
              <Route path="/admin" element={<AdminDashboard />} />
              <Route path="/admin/users" element={<AdminUsers />} />
              <Route path="/admin/billing" element={<AdminBilling />} />
              <Route path="/admin/content" element={<AdminContent />} />
              <Route path="/admin/analytics" element={<AdminAnalytics />} />
              <Route path="/admin/system" element={<AdminSystem />} />
              <Route path="/admin/marketing" element={<AdminMarketing />} />
              <Route path="/social-automation" element={<SocialMediaAutomation />} />
              
              {/* Alternative UI Versions */}
              <Route path="/ultra" element={<UltraHome />} />
              <Route path="/ultra/ai-chat" element={<UltraAIChat />} />
              <Route path="/ultra/music-generation" element={<UltraMusicGeneration />} />
              <Route path="/forge-studio" element={<ForgeStudio />} />
              
              {/* Legacy Routes for Backwards Compatibility */}
              <Route path="/legacy" element={<Home />} />
              <Route path="/legacy/generate" element={<Generate />} />
              <Route path="/legacy/gallery" element={<Gallery />} />
              <Route path="/legacy/profile" element={<Profile />} />
              <Route path="/professional" element={<ProfessionalHome />} />
              
              {/* Redirects for SEO and User Experience */}
              <Route path="/home" element={<Navigate to="/" replace />} />
              <Route path="/ai" element={<Navigate to="/rendereel-ai" replace />} />
              <Route path="/upscaler" element={<Navigate to="/rendereel-upscaler" replace />} />
              <Route path="/editor" element={<Navigate to="/rendereel-editor" replace />} />
              <Route path="/singer" element={<Navigate to="/rendereel-singer" replace />} />
              <Route path="/suite" element={<Navigate to="/rendereel-suite" replace />} />
              
              {/* Catch-all redirect to home */}
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
            
            {/* AI Chatbot - Available on all pages */}
            <AIChatbot />
          </div>
        </Router>
      </NSFWProvider>
    </ThemeProvider>
  );
}

export default App;
