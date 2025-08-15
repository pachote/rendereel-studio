// API Service Layer for AI Generation Platform
const API_BASE_URL = process.env.REACT_APP_BACKEND_URL;

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  // Helper method to make authenticated requests
  async makeRequest(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const token = localStorage.getItem('auth_token');
    
    const defaultHeaders = {
      'Content-Type': 'application/json',
    };

    if (token) {
      defaultHeaders.Authorization = `Bearer ${token}`;
    }

    const config = {
      headers: defaultHeaders,
      ...options,
    };

    try {
      const response = await fetch(url, config);
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.message || `HTTP error! status: ${response.status}`);
      }
      
      return { success: true, data, status: response.status };
    } catch (error) {
      console.error(`API request failed for ${endpoint}:`, error);
      return { success: false, error: error.message, status: error.status || 500 };
    }
  }

  // Authentication APIs
  async login(email, password) {
    return this.makeRequest('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  async register(email, password, username) {
    return this.makeRequest('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, password, username }),
    });
  }

  async getProfile() {
    return this.makeRequest('/api/auth/profile');
  }

  // Generation APIs
  async getModels() {
    return this.makeRequest('/api/generation/models');
  }

  async generateImage(data) {
    return this.makeRequest('/api/generation/image', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async generateVideo(data) {
    return this.makeRequest('/api/generation/video', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getGenerationStatus(taskId) {
    return this.makeRequest(`/api/generation/status/${taskId}`);
  }

  async getGenerationResult(taskId) {
    return this.makeRequest(`/api/generation/result/${taskId}`);
  }

  // LoRA APIs
  async getPopularLoRAs() {
    return this.makeRequest('/api/lora/popular');
  }

  async getCompatibleLoRAs(modelId) {
    return this.makeRequest(`/api/lora/models/${modelId}`);
  }

  async searchLoRAs(query, modelType = null) {
    const params = new URLSearchParams({ query });
    if (modelType) {
      params.append('model_type', modelType);
    }
    return this.makeRequest(`/api/lora/search?${params.toString()}`);
  }

  async getLoRADetails(loraId) {
    return this.makeRequest(`/api/lora/details/${loraId}`);
  }

  // NSFW APIs
  async getNSFWStatus() {
    return this.makeRequest('/api/nsfw/status');
  }

  async updateNSFWPreferences(enabled) {
    return this.makeRequest('/api/nsfw/preferences', {
      method: 'POST',
      body: JSON.stringify({ nsfw_enabled: enabled }),
    });
  }

  async verifyAge(birthDate) {
    return this.makeRequest('/api/nsfw/verify-age', {
      method: 'POST',
      body: JSON.stringify({ birth_date: birthDate }),
    });
  }

  // Admin APIs
  async getAdminStats() {
    return this.makeRequest('/api/admin/stats');
  }

  async getUsers(page = 1, limit = 50) {
    return this.makeRequest(`/api/admin/users?page=${page}&limit=${limit}`);
  }

  // Lip Sync APIs
  async generateLipSync(data) {
    return this.makeRequest('/api/lip-sync/generate', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getLipSyncVoices() {
    return this.makeRequest('/api/lip-sync/voices');
  }

  // Runway Gen-3 API methods
  async getRunwayModels() {
    return this.makeRequest('/api/runway-gen3/models');
  }

  async generateRunwayVideo(formData) {
    return this.makeRequest('/api/runway-gen3/generate-text-to-video', {
      method: 'POST',
      body: formData,
      headers: {} // Let browser set Content-Type for FormData
    });
  }

  async generateRunwayImageToVideo(formData) {
    return this.makeRequest('/api/runway-gen3/generate-image-to-video', {
      method: 'POST',
      body: formData,
      headers: {} // Let browser set Content-Type for FormData
    });
  }

  async getRunwayTaskStatus(taskId) {
    return this.makeRequest(`/api/runway-gen3/task-status/${taskId}`);
  }

  async getRunwayTasks() {
    return this.makeRequest('/api/runway-gen3/tasks');
  }

  async estimateRunwayCost(duration, model = 'gen3a_turbo') {
    const formData = new FormData();
    formData.append('duration', duration);
    formData.append('model', model);
    
    return this.makeRequest('/api/runway-gen3/estimate-cost', {
      method: 'POST',
      body: formData,
      headers: {} // Let browser set Content-Type for FormData
    });
  }

  // NSFW LoRA methods
  async getNSFWLoRAs(modelId = null) {
    const url = modelId 
      ? `/api/nsfw-loras/models/${modelId}/compatible`
      : '/api/nsfw-loras/search';
    return this.makeRequest(url, {
      method: modelId ? 'GET' : 'POST',
      body: modelId ? undefined : JSON.stringify({})
    });
  }

  async getNSFWLoRACategories() {
    return this.makeRequest('/api/nsfw-loras/categories');
  }

  async getNSFWLoRARecommendations(useCase, modelType = 'flux') {
    return this.makeRequest(`/api/nsfw-loras/recommendations/${useCase}?model_type=${modelType}`);
  }

  async getNSFWLoRADetails(loraId) {
    return this.makeRequest(`/api/nsfw-loras/lora/${loraId}/details`);
  }

  async getNSFWLoRAStats() {
    return this.makeRequest('/api/nsfw-loras/stats');
  }

  async searchNSFWLoRAs(searchParams) {
    return this.makeRequest('/api/nsfw-loras/search', {
      method: 'POST',
      body: JSON.stringify(searchParams)
    });
  }

  // AI Video Editor methods
  async processConversationalEdit(formData) {
    return this.makeRequest('/api/ai-video-editor/conversational-edit', {
      method: 'POST',
      body: formData,
      headers: {} // Let browser set Content-Type for FormData
    });
  }

  async analyzeVideoContent(formData) {
    return this.makeRequest('/api/ai-video-editor/analyze-content', {
      method: 'POST',
      body: formData,
      headers: {} // Let browser set Content-Type for FormData
    });
  }

  async generateKeyframes(formData) {
    return this.makeRequest('/api/ai-video-editor/generate-keyframes', {
      method: 'POST',
      body: formData,
      headers: {} // Let browser set Content-Type for FormData
    });
  }

  // Enhanced video generation methods
  async getVideoModels() {
    return this.makeRequest('/api/video/models');
  }

  async generateAdvancedVideo(data) {
    return this.makeRequest('/api/video/generate-advanced', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  // Kling AI methods
  async getKlingModels() {
    return this.makeRequest('/api/kling/models');
  }

  async generateKlingVideo(data) {
    return this.makeRequest('/api/kling/generate', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  // Google AI methods
  async getGoogleVeoModels() {
    return this.makeRequest('/api/google/models');
  }

  async generateVeoVideo(data) {
    return this.makeRequest('/api/google/generate', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  // Social Media Automation
  async getSocialPlatforms() {
    return this.makeRequest('/api/social-media-automation/platforms');
  }

  async generateSocialContent(data) {
    return this.makeRequest('/api/social-media-automation/generate', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  async scheduleSocialPost(data) {
    return this.makeRequest('/api/social-media-automation/schedule', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  // Enhanced AI Models
  async getEnhancedModels() {
    return this.makeRequest('/api/enhanced-models/list');
  }

  async getModelCapabilities(modelId) {
    return this.makeRequest(`/api/enhanced-models/${modelId}/capabilities`);
  }

  // User Catalog
  async getUserGenerations(userId = null) {
    const endpoint = userId 
      ? `/api/user-catalog/generations/${userId}` 
      : '/api/user-catalog/my-generations';
    return this.makeRequest(endpoint);
  }

  async saveToGallery(generationId) {
    return this.makeRequest('/api/user-catalog/save-to-gallery', {
      method: 'POST',
      body: JSON.stringify({ generation_id: generationId })
    });
  }

  // AI Chatbot
  async sendChatMessage(message, conversationId = null) {
    return this.makeRequest('/api/ai-chatbot/chat', {
      method: 'POST',
      body: JSON.stringify({ 
        message, 
        conversation_id: conversationId 
      })
    });
  }

  async getChatHistory(conversationId) {
    return this.makeRequest(`/api/ai-chatbot/history/${conversationId}`);
  }

  // Health check
  async healthCheck() {
    return this.makeRequest('/api/health');
  }

  // Billing and Credits
  async getCreditsBalance() {
    return this.makeRequest('/api/billing/credits');
  }

  async purchaseCredits(amount) {
    return this.makeRequest('/api/billing/purchase-credits', {
      method: 'POST',
      body: JSON.stringify({ amount })
    });
  }

  // File Upload Helper
  async uploadFile(file, endpoint) {
    const formData = new FormData();
    formData.append('file', file);
    
    return this.makeRequest(endpoint, {
      method: 'POST',
      body: formData,
      headers: {} // Let browser set Content-Type for FormData
    });
  }

  // Batch operations
  async batchGenerate(requests) {
    return this.makeRequest('/api/generation/batch', {
      method: 'POST',
      body: JSON.stringify({ requests })
    });
  }

  async getBatchStatus(batchId) {
    return this.makeRequest(`/api/generation/batch/${batchId}/status`);
  }
}

// Create and export a singleton instance
const apiService = new ApiService();

export default apiService;

// Export specific methods for convenience
export const {
  login,
  register,
  getProfile,
  getModels,
  generateImage,
  generateVideo,
  getGenerationStatus,
  getGenerationResult,
  getPopularLoRAs,
  getCompatibleLoRAs,
  searchLoRAs,
  getLoRADetails,
  getNSFWStatus,
  updateNSFWPreferences,
  verifyAge,
  getAdminStats,
  getUsers,
  generateLipSync,
  getLipSyncVoices,
  // Runway Gen-3 methods
  getRunwayModels,
  generateRunwayVideo,
  generateRunwayImageToVideo,
  getRunwayTaskStatus,
  getRunwayTasks,
  estimateRunwayCost,
  // NSFW LoRA methods
  getNSFWLoRAs,
  getNSFWLoRACategories,
  getNSFWLoRARecommendations,
  getNSFWLoRADetails,
  getNSFWLoRAStats,
  searchNSFWLoRAs,
  // AI Video Editor methods
  processConversationalEdit,
  analyzeVideoContent,
  generateKeyframes,
  // Enhanced methods
  getVideoModels,
  generateAdvancedVideo,
  getKlingModels,
  generateKlingVideo,
  getGoogleVeoModels,
  generateVeoVideo,
  getSocialPlatforms,
  generateSocialContent,
  scheduleSocialPost,
  getEnhancedModels,
  getModelCapabilities,
  getUserGenerations,
  saveToGallery,
  sendChatMessage,
  getChatHistory,
  healthCheck,
  getCreditsBalance,
  purchaseCredits,
  uploadFile,
  batchGenerate,
  getBatchStatus
} = apiService;
