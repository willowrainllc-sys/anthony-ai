package com.example.anthony_ai

import android.annotation.SuppressLint
import android.app.Application
import android.content.Context
import android.util.Log
import androidx.compose.runtime.*
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import kotlinx.coroutines.withTimeoutOrNull
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.WebSocket
import org.json.JSONObject
import java.util.concurrent.TimeUnit
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.asSharedFlow
import com.example.anthony_ai.data.model.AIVideo
import android.net.Uri
import com.google.android.gms.location.LocationServices
import com.google.android.gms.location.Priority
import com.google.android.gms.tasks.CancellationTokenSource
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.asRequestBody
import okhttp3.MediaType.Companion.toMediaType
import org.json.JSONArray
import kotlin.time.Duration.Companion.seconds
import java.io.File
import java.net.URLEncoder

data class ChatMessage(val text: String, val isUser: Boolean, val imageUrl: String? = null)

data class LatLng(val latitude: Double, val longitude: Double)

data class StreetCamera(
    val id: String,
    val title: String,
    val lat: Double,
    val lon: Double,
    val thumbnailUrl: String,
    val streamUrl: String,
    val aiInsight: String = "Analyzing grid vector sync..."
)

data class OsintNode(
    val id: String,
    val lat: Double,
    val lng: Double,
    val name: String,
    val type: String,
    val operator: String,
    val streamUrl: String? = null
)

class MainViewModel(application: Application) : AndroidViewModel(application) {
    private val sharedPreferences = application.getSharedPreferences("mesh_settings", Context.MODE_PRIVATE)
    
    private val client = OkHttpClient.Builder()
        .readTimeout(10, TimeUnit.SECONDS)
        .connectTimeout(10, TimeUnit.SECONDS)
        .build()
        
    private var nexusWebSocket: WebSocket? = null
    private var hudWebSocket: WebSocket? = null
    private var promptJob: Job? = null
    
    var meshIp: String by mutableStateOf(sharedPreferences.getString("mesh_ip", NetworkConfig.currentBaseUrl.replace("http://", "")) ?: NetworkConfig.currentBaseUrl.replace("http://", ""))

    val chatHistory = mutableStateListOf<ChatMessage>()

    var userTag: String by mutableStateOf("@anthony_creator_01")

    var isLoading: Boolean by mutableStateOf(false)

    var connectionStatus: String? by mutableStateOf(null)

    val activityFeed = mutableStateListOf<String>()

    var searchResultLocation: LatLng? by mutableStateOf(null)

    val supabaseVideos = mutableStateListOf<AIVideo>()

    val streetCameras = mutableStateListOf<StreetCamera>()

    val legacyFeedVideos = mutableStateListOf<AIVideo>()

    var newsBrief: NewsBriefResponse? by mutableStateOf(null)

    val dashboardSections = mutableStateListOf<TopicSection>()

    val productionJobs = mutableStateListOf<ProductionJobResponse>()

    var linkedTeamTag: String? by mutableStateOf(null)

    val osintNodes = mutableStateListOf<OsintNode>()

    var reconMatchLocation: LatLng? by mutableStateOf(null)

    var isReconActive: Boolean by mutableStateOf(false)

    val hereticResources = mutableStateListOf<HereticResource>()

    val aiToolkit = mutableStateListOf<AiTool>()

    val quickPanelSuggestions = mutableStateListOf<String>()

    var revenueVitals: RevenueVitalsResponse? by mutableStateOf(null)

    var userLocation: LatLng? by mutableStateOf(null)

    var missionTelemetry: TelemetryResponse? by mutableStateOf(null)
    
    var selectedCategory: String by mutableStateOf("For you")

    var showControlCenter: Boolean by mutableStateOf(false)
    var showTacticalHud: Boolean by mutableStateOf(false)
    var isRefreshing: Boolean by mutableStateOf(false)

    var selectedImageUri: Uri? by mutableStateOf(null)

    val pinnedCameras = mutableStateListOf<String>()

    private val fusedLocationClient = LocationServices.getFusedLocationProviderClient(application)

    private val localFallbackVideos = listOf(
        AIVideo(id="v1", title="CYBER STREETS 2099", description="The neon glow of the future. Walking through the rain in Shibuya.", thumbnailUrl="https://images.unsplash.com/photo-1545143333-14387679366a?q=80&w=1000", videoUrl="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4", category="Urban", views="1.8M", posted="Just Now", creator = "Anthony AI"),
        AIVideo(id="v2", title="NEURAL MESH SYNC", description="The empire is conscious. Data flows through the global swarm.", thumbnailUrl="https://images.unsplash.com/photo-1506318137071-a8e063b4b4bf?q=80&w=1000", videoUrl="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4", category="Tech", views="2.5M", posted="10m ago", creator = "Anthony AI"),
        AIVideo(id="v3", title="DEEP SEA ABYSS", description="What lies beneath the surface? Exploring the bioluminescent mysteries.", thumbnailUrl="https://images.unsplash.com/photo-1551244072-5d12893278ab?q=80&w=1000", videoUrl="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4", category="Nature", views="3.1M", posted="1h ago", creator = "Anthony AI"),
        AIVideo(id="v4", title="MARTIAN FRONTIER", description="The first colony on the red planet. A new era for humanity.", thumbnailUrl="https://images.unsplash.com/photo-1614728894747-a83421e2b9c9?q=80&w=1000", videoUrl="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4", category="Space", views="5.4M", posted="3h ago", creator = "Anthony AI"),
        AIVideo(id="v5", title="QUANTUM BREACH", description="Encryption is dead. The grid is open. Are you watching?", thumbnailUrl="https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=1000", videoUrl="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4", category="Tech", views="1.2M", posted="5h ago", creator = "Anthony AI")
    )

    init {
        legacyFeedVideos.addAll(localFallbackVideos)
        supabaseVideos.addAll(localFallbackVideos) // Initial fallbacks
        NetworkConfig.sync(application)
        startConnectionLoop()
        loadStreetCameras()
    }

    private fun loadStreetCameras() {
        streetCameras.addAll(listOf(
            StreetCamera("c1", "NYC: 7th Ave & W 47th St", 40.758896, -73.985130, "https://images.unsplash.com/photo-1534430480872-3498386e7856?q=80&w=400", "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4", "Grid Analysis: 243 vectors. Status: OPTIMAL."),
            StreetCamera("c2", "LA: Hollywood & Highland", 34.101625, -118.339255, "https://images.unsplash.com/photo-1542736667-069246b84d4b?q=80&w=400", "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4", "Grid Sync: Clear sky. Tracked objects: 42."),
            StreetCamera("c3", "Chicago: Michigan Ave", 41.889077, -87.624263, "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?q=80&w=400", "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4", "Structural Node active. Sync confidence: 99.4%."),
            StreetCamera("c4", "Miami: Ocean Drive", 25.780650, -80.130045, "https://images.unsplash.com/photo-1535498730771-e735b998cd64?q=80&w=400", "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4", "Spectrum Analysis: Stable. No anomalies detected."),
            StreetCamera("c5", "Seattle: Space Needle", 47.610889, -122.336981, "https://images.unsplash.com/photo-1502175353174-a7a70e73b362?q=80&w=400", "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4", "Visibility: 10mi. Recon scan: COMPLETED.")
        ))
    }

    override fun onCleared() {
        nexusWebSocket?.close(1000, "App Cleared")
        hudWebSocket?.close(1000, "App Cleared")
    }

    private fun startConnectionLoop() {
        viewModelScope.launch {
            while (true) {
                NetworkConfig.sync(getApplication())
                meshIp = NetworkConfig.currentBaseUrl.replace("http://", "").replace("/", "")
                
                fetchSupabaseFeed()
                fetchNewsBrief()
                fetchDashboard()
                fetchProductionJobs()
                fetchAiThoughts()
                fetchTelemetry()

                if (connectionStatus == null || !connectionStatus!!.contains("Ready")) {
                    reconnect()
                } else {
                    runHeartbeat()
                }
                delay(30.seconds)
            }
        }
    }

    private fun fetchAiThoughts() {
        viewModelScope.launch {
            try {
                val thoughts = withTimeoutOrNull(5.seconds) { MeshApiService.api.getAiThoughts() }
                if (thoughts != null) {
                    withContext(Dispatchers.Main) {
                        quickPanelSuggestions.clear()
                        quickPanelSuggestions.addAll(thoughts)
                    }
                }
            } catch (_: Exception) {}
        }
    }

    private fun fetchTelemetry() {
        viewModelScope.launch {
            try {
                missionTelemetry = withTimeoutOrNull(5.seconds) { MeshApiService.api.getTelemetry() }
            } catch (_: Exception) {}
        }
    }

    private fun runHeartbeat() {
        viewModelScope.launch {
            try {
                withTimeoutOrNull(3.seconds) { MeshApiService.api.nodeHeartbeat("PHONE_NODE_ANTHONY", "Healthy") }
            } catch (_: Exception) {}
        }
    }

    fun reconnect() {
        viewModelScope.launch {
            connectionStatus = "Connecting..."
            val target = NetworkConfig.currentBaseUrl
            try {
                val probeApi = MeshApiService.createWithClient(target, client)
                val result = withTimeoutOrNull(5.seconds) { probeApi.handshake() }
                if (result?.status == "success") {
                    connectionStatus = "Ready"
                }
            } catch (_: Exception) {}
        }
    }

    fun fetchSupabaseFeed(force: Boolean = false) {
        viewModelScope.launch {
            if (force) {
                isRefreshing = true
                activityFeed.add("GRID: Fetching fresh content...")
            }
            try {
                val swarmFeed = withTimeoutOrNull(8.seconds) { MeshApiService.api.getFeed(selectedCategory) }
                if (swarmFeed != null && swarmFeed.isNotEmpty()) {
                    supabaseVideos.clear()
                    supabaseVideos.addAll(swarmFeed)
                    activityFeed.add("GRID: Successfully synced ${swarmFeed.size} items.")
                } else {
                    val fallbackSwarmFeed = withTimeoutOrNull(8.seconds) { MeshApiService.api.getFeed("For you") }
                    if (fallbackSwarmFeed != null && fallbackSwarmFeed.isNotEmpty()) {
                        supabaseVideos.clear()
                        supabaseVideos.addAll(fallbackSwarmFeed)
                    } else if (supabaseVideos.isEmpty()) {
                        supabaseVideos.addAll(localFallbackVideos)
                    }
                }
            } catch (e: Exception) {
                Log.e("FEED", "Sync fail: ${e.message}")
                if (supabaseVideos.isEmpty()) {
                    supabaseVideos.addAll(localFallbackVideos)
                }
            } finally {
                isRefreshing = false
            }
        }
    }

    fun updateCategory(category: String) {
        selectedCategory = category
        fetchSupabaseFeed(force = true)
    }

    fun fetchProductionJobs() {
        viewModelScope.launch {
            try {
                val jobs = withTimeoutOrNull(5.seconds) { MeshApiService.api.getProductionJobs() }
                if (jobs != null) {
                    productionJobs.clear()
                    productionJobs.addAll(jobs)
                }
            } catch (_: Exception) {}
        }
    }

    fun fetchNewsBrief() {
        viewModelScope.launch {
            try {
                newsBrief = withTimeoutOrNull(5.seconds) { MeshApiService.api.getNewsBrief() }
            } catch (_: Exception) {}
        }
    }

    fun fetchDashboard() {
        viewModelScope.launch {
            try {
                val sections = withTimeoutOrNull(5.seconds) { MeshApiService.api.getDashboard() }
                if (sections != null) {
                    dashboardSections.clear()
                    dashboardSections.addAll(sections)
                }
            } catch (_: Exception) {}
        }
    }

    fun onImageSelected(uri: Uri?) {
        selectedImageUri = uri
    }

    fun unlinkTeam() {
        linkedTeamTag = null
    }

    fun sendText(message: String, imageUri: Uri? = null) {
        if (message.isBlank() && imageUri == null) return
        chatHistory.add(ChatMessage(message, isUser = true, imageUrl = imageUri?.toString()))
        sendPrompt(message, imageUri)
    }

    fun sendPrompt(message: String, imageUri: Uri? = null) {
        promptJob?.cancel()
        promptJob = viewModelScope.launch {
            isLoading = true
            try {
                val payload = ChatPayload(message = message)
                val response = MeshApiService.api.streamPrompt(payload)
                if (response.isSuccessful) {
                    var currentResponse = ""
                    response.body()?.byteStream()?.bufferedReader()?.useLines { lines ->
                        lines.forEach { line ->
                            if (line.startsWith("data: ")) {
                                val json = JSONObject(line.removePrefix("data: "))
                                val textChunk = json.optString("response", "")
                                currentResponse += textChunk
                                viewModelScope.launch(Dispatchers.Main) {
                                    if (chatHistory.isNotEmpty() && !chatHistory.last().isUser) {
                                        chatHistory[chatHistory.size - 1] = ChatMessage(currentResponse, isUser = false)
                                    } else {
                                        chatHistory.add(ChatMessage(currentResponse, isUser = false))
                                    }
                                }
                            }
                        }
                    }
                }
            } catch (e: Exception) {
                Log.e("CHAT", "Request error: ${e.message}")
            } finally {
                isLoading = false
            }
        }
    }

    private fun getFileFromUri(uri: Uri): File {
        val context = getApplication<Application>()
        val inputStream = context.contentResolver.openInputStream(uri)
        val file = File(context.cacheDir, "upload_${System.currentTimeMillis()}.jpg")
        file.outputStream().use { inputStream?.copyTo(it) }
        return file
    }

    fun confirmGlobalStrike(video: AIVideo) {
        viewModelScope.launch {
            try {
                val payload = PublishRequest(
                    title = video.title,
                    description = video.description,
                    videoUrl = video.videoUrl,
                    platforms = listOf("YOUTUBE", "FACEBOOK", "INSTA_THREADS", "TIKTOK")
                )
                MeshApiService.api.swarmStrike(payload)
                activityFeed.add("Strike deployed: ${video.title}")
            } catch (e: Exception) {
                Log.e("STRIKE", "Failed: ${e.message}")
            }
        }
    }

    fun triggerFullStrikeAll() {
        viewModelScope.launch {
            try {
                MeshApiService.api.igniteFullStrike()
                activityFeed.add("Full grid strike ignited.")
                fetchSupabaseFeed(force = true)
            } catch (_: Exception) {}
        }
    }

    fun onSpeechResult(text: String) {
        sendText(text)
    }

    fun onSpeechError(error: String) {
        Log.e("VOICE", error)
    }

    fun narrateVideo(video: AIVideo) {
        viewModelScope.launch {
            val prompt = "You are Anthony AI. Narrate this drop: '${video.title}'"
            try {
                val response = MeshApiService.api.streamPrompt(ChatPayload(message = prompt))
                if (response.isSuccessful) {
                    response.body()?.byteStream()?.bufferedReader()?.useLines { lines ->
                        lines.forEach { line ->
                            if (line.startsWith("data: ")) {
                                val json = JSONObject(line.removePrefix("data: "))
                                val textChunk = json.optString("response", "")
                                _responseFlow.emit(textChunk)
                            }
                        }
                    }
                    _responseFlow.emit("__FINISH__")
                }
            } catch (e: Exception) {
                _responseFlow.emit("__FINISH__")
            }
        }
    }

    private val _responseFlow = MutableSharedFlow<String>()
    val responseFlow = _responseFlow.asSharedFlow()

    fun searchLocation(query: String) {
        if (query.isBlank()) return
        viewModelScope.launch(Dispatchers.IO) {
            try {
                val url = "https://nominatim.openstreetmap.org/search?q=${URLEncoder.encode(query, "UTF-8")}&format=json&limit=1"
                val request = Request.Builder().url(url).header("User-Agent", "AnthonyAI").build()
                client.newCall(request).execute().use { response ->
                    if (response.isSuccessful) {
                        val body = response.body?.string() ?: ""
                        val jsonArray = JSONArray(body)
                        if (jsonArray.length() > 0) {
                            val first = jsonArray.getJSONObject(0)
                            val lat = first.getDouble("lat")
                            val lon = first.getDouble("lon")
                            withContext(Dispatchers.Main) {
                                searchResultLocation = LatLng(lat, lon)
                            }
                        }
                    }
                }
            } catch (_: Exception) {}
        }
    }

    fun fetchOsintNodes(lat: Double, lng: Double) {
        viewModelScope.launch {
            try {
                val nodes = withTimeoutOrNull(5.seconds) { MeshApiService.api.getOsintNodes(lat, lng) }
                if (nodes != null) {
                    osintNodes.clear()
                    osintNodes.addAll(nodes.nodes)
                }
            } catch (_: Exception) {}
        }
    }

    fun performVisualRecon(imageUri: Uri) {
        viewModelScope.launch {
            isReconActive = true
            try {
                val file = getFileFromUri(imageUri)
                val requestFile = file.asRequestBody("image/*".toMediaType())
                val body = MultipartBody.Part.createFormData("file", file.name, requestFile)
                val result = withTimeoutOrNull(15.seconds) { MeshApiService.api.visualSearch(body) }
                if (result != null && result.matchFound && result.target != null) {
                    reconMatchLocation = LatLng(result.target.lat, result.target.lng)
                    searchResultLocation = reconMatchLocation
                }
            } catch (_: Exception) {} finally {
                isReconActive = false
            }
        }
    }

    fun togglePinCamera(camId: String) {
        if (pinnedCameras.contains(camId)) {
            pinnedCameras.remove(camId)
            activityFeed.add("GRID: Node unpinned.")
        } else {
            pinnedCameras.add(camId)
            activityFeed.add("GRID: Node pinned to tactical tray.")
        }
    }

    fun fetchKnowledgeBases() {
        viewModelScope.launch {
            try {
                val heretic = withTimeoutOrNull(5.seconds) { MeshApiService.api.getHereticResources() }
                val toolkit = withTimeoutOrNull(5.seconds) { MeshApiService.api.getAiToolkit() }
                if (heretic != null) {
                    hereticResources.clear()
                    hereticResources.addAll(heretic)
                }
                if (toolkit != null) {
                    aiToolkit.clear()
                    aiToolkit.addAll(toolkit)
                }
            } catch (_: Exception) {}
        }
    }

    fun fetchRevenueVitals() {
        viewModelScope.launch {
            try {
                revenueVitals = withTimeoutOrNull(5.seconds) { MeshApiService.api.getRevenueVitals() }
            } catch (_: Exception) {}
        }
    }

    @SuppressLint("MissingPermission")
    fun syncToUserLocation() {
        viewModelScope.launch {
            try {
                activityFeed.add("GRID: Syncing location...")
                val result = fusedLocationClient.getCurrentLocation(Priority.PRIORITY_HIGH_ACCURACY, CancellationTokenSource().token)
                result.addOnSuccessListener { location ->
                    if (location != null) {
                        val latLng = LatLng(location.latitude, location.longitude)
                        userLocation = latLng
                        searchResultLocation = latLng
                        fetchOsintNodes(location.latitude, location.longitude)
                    }
                }
            } catch (_: Exception) {}
        }
    }

    fun clearAllAppData() {
        viewModelScope.launch(Dispatchers.IO) {
            sharedPreferences.edit().clear().apply()
            withContext(Dispatchers.Main) {
                chatHistory.clear()
                supabaseVideos.clear()
            }
        }
    }
}
