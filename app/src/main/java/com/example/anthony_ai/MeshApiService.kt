@file:Suppress("unused")

package com.example.anthony_ai

import android.util.Log
import com.google.gson.annotations.SerializedName
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import okhttp3.ResponseBody
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.Part
import okhttp3.MultipartBody
import okhttp3.RequestBody
import retrofit2.http.Multipart
import retrofit2.http.POST
import retrofit2.http.Streaming
import java.util.concurrent.TimeUnit
import com.example.anthony_ai.data.model.AIVideo
import retrofit2.http.Query

data class ChatPayload(val message: String)
data class ChatResponse(val response: String, val channel: String)
data class HandshakeResponse(val status: String, val message: String)
data class NewsBriefResponse(val status: String, val headline: String, val brief: String, val persona: String)
data class AiTvContent(
    val title: String,
    val description: String,
    val duration: String,
    @SerializedName("video_uri") val videoUri: String,
)

data class PublishRequest(
    val title: String? = null,
    val description: String? = null,
    val message: String? = null,
    val text: String? = null,
    val caption: String? = null,
    @SerializedName("media_url") val mediaUrl: String? = null,
    @SerializedName("image_url") val imageUrl: String? = null,
    @SerializedName("video_url") val videoUrl: String? = null, // Alias for unified strike
    val platforms: List<String> = listOf("facebook"),
)

data class CheckpointRequest(
    @SerializedName("target_year") val targetYear: Int? = null,
    @SerializedName("target_month") val targetMonth: Int? = null,
    @SerializedName("target_day") val targetDay: Int? = null,
    @SerializedName("target_hour") val targetHour: Int,
    @SerializedName("target_minute") val targetMinute: Int,
    val timestamp: String
)

data class TelemetryResponse(
    val temporal: Map<String, Any?>,
    val queue: Map<String, Int>,
    @SerializedName("last_strike") val lastStrike: StrikeInfo?,
    val missions: List<MissionInfo> = emptyList(),
    @SerializedName("crypto_bets") val cryptoBets: List<CryptoBetInfo> = emptyList(),
    val clocks: Map<String, Double> = emptyMap(),
    @SerializedName("clocks_info") val clocksInfo: List<ClockInfo> = emptyList(),
    val logs: List<String> = emptyList(),
    val timestamp: Double
)

data class MissionInfo(
    val title: String,
    val channel: String,
    val priority: Int
)

data class CryptoBetInfo(
    val asset: String,
    val amount: Double,
    val timestamp: Double
)

data class ClockInfo(
    val channel: String,
    @SerializedName("last_strike") val lastStrike: Double,
    val total: Int
)

data class StrikeInfo(
    val node: String,
    val time: Double
)

data class ProductionJobResponse(
    @SerializedName("job_id") val jobId: String,
    val status: String,
    val progress: Int,
    val stage: String,
    val title: String,
    @SerializedName("video_url") val videoUrl: String? = null
)

data class OsintNodesResponse(
    val status: String,
    val count: Int,
    val nodes: List<OsintNode>
)

data class RevenueVitalsResponse(
    val status: String,
    val commerce: List<StoreVital>,
    val portfolio: List<AssetVital>,
    @SerializedName("total_daily_revenue") val totalDailyRevenue: Double
)

data class StoreVital(val id: String, val daily: Double, val total: Double)
data class AssetVital(val id: String, val value: Double, val change: Double)

data class HereticResource(val name: String, val url: String, val desc: String, val cat: String)
data class AiTool(val name: String, val url: String, val utility: String, val desc: String)

data class VisualSearchResponse(
    val status: String,
    @SerializedName("match_found") val matchFound: Boolean,
    val target: MatchedNode?
)

data class MatchedNode(
    val id: String,
    val name: String,
    val lat: Double,
    val lng: Double,
    val confidence: Double,
    @SerializedName("stream_url") val streamUrl: String,
    @SerializedName("ai_insight") val aiInsight: String
)

interface MeshApiService {
    @GET("/handshake")
    suspend fun handshake(): HandshakeResponse

    @GET("/api/mesh/telemetry")
    suspend fun getTelemetry(): TelemetryResponse

    @POST("/set-checkpoint")
    suspend fun setCheckpoint(@Body payload: CheckpointRequest): HandshakeResponse

    @GET("/news/brief")
    suspend fun getNewsBrief(): NewsBriefResponse

    @GET("/api/mesh/heartbeat")
    suspend fun nodeHeartbeat(
        @Query("node_id") nodeId: String,
        @Query("status") status: String
    ): HandshakeResponse

    @GET("/api/mesh/ollama-status")
    suspend fun getOllamaStatus(): HandshakeResponse

    @GET("/dashboard")
    suspend fun getDashboard(): List<TopicSection>

    @GET("/api/feed")
    suspend fun getFeed(
        @Query("category") category: String
    ): List<AIVideo>

    @GET("/api/ghost-feed")
    suspend fun getGhostFeed(): List<AIVideo>

    @GET("/api/production/jobs")
    suspend fun getProductionJobs(): List<ProductionJobResponse>

    @GET("/api/ai/thoughts")
    suspend fun getAiThoughts(): List<String>

    @GET("/api/knowledge/heretic")
    suspend fun getHereticResources(): List<HereticResource>

    @GET("/api/knowledge/toolkit")
    suspend fun getAiToolkit(): List<AiTool>

    @GET("/api/revenue/vitals")
    suspend fun getRevenueVitals(): RevenueVitalsResponse

    @GET("/api/osint/cctv-nodes")
    suspend fun getOsintNodes(
        @Query("lat") lat: Double,
        @Query("lng") lng: Double
    ): OsintNodesResponse

    @Streaming
    @POST("/chat/stream")
    suspend fun streamPrompt(
        @Body payload: ChatPayload
    ): Response<ResponseBody>

    @Multipart
    @POST("/api/search/visual-query")
    suspend fun visualSearch(
        @Part file: MultipartBody.Part
    ): VisualSearchResponse

    @POST("/api/publish/facebook")
    suspend fun publishToFacebook(
        @Body payload: PublishRequest
    ): Response<ResponseBody>

    @POST("/api/swarm/strike")
    suspend fun swarmStrike(
        @Body payload: PublishRequest
    ): Response<ResponseBody>

    @POST("/api/swarm/ignite")
    suspend fun igniteFullStrike(): Response<ResponseBody>

    @POST("/api/telemetry/revenue-pulse")
    suspend fun sendRevenuePulse(
        @Body payload: Map<String, Any?>,
    ): Response<ResponseBody>

    @Multipart
    @POST("/api/twin/studio-generate")
    suspend fun studioGenerate(
        @Part("prompt") prompt: RequestBody,
        @Part("style") style: RequestBody,
        @Part inputImage: MultipartBody.Part?,
    ): ChatResponse

    companion object {
        const val SOVEREIGN_API_KEY = "anthony_mesh_secure_key_2026"
        private const val TAG = "MESH_CONNECT"

        // Default to Swarm MagicDNS
        private var currentIp: String = NetworkConfig.currentBaseUrl.replace("http://", "")
        private var _api: MeshApiService? = null

        val api: MeshApiService
            get() = _api ?: create(currentIp).also { _api = it }

        fun updateIp(newIp: String) {
            // Robust sanitization: 
            var sanitized = newIp.trim()
                .replace("http://", "")
                .replace("https://", "")
                .split("/")[0]
                .filter { !it.isWhitespace() }
            
            if (sanitized.isEmpty()) sanitized = NetworkConfig.currentBaseUrl.replace("http://", "")
            
            // Handle ports for manual IP overrides
            val finalTarget = if (sanitized.contains(":")) sanitized else "$sanitized:8000"
            
            if (currentIp != finalTarget) {
                currentIp = finalTarget
                try {
                    _api = create(finalTarget)
                    Log.i(TAG, "API switched to target: $finalTarget")
                } catch (e: Exception) {
                    Log.e(TAG, "Invalid IP provided: $finalTarget", e)
                }
            }
        }

        fun createWithClient(ip: String, customClient: OkHttpClient): MeshApiService {
            // Ensure the custom client also has the required Sovereign Key
            val securedClient = customClient.newBuilder()
                .addInterceptor { chain ->
                    val request = chain.request().newBuilder()
                        .addHeader("x-api-key", SOVEREIGN_API_KEY)
                        .build()
                    chain.proceed(request)
                }
                .build()
            return buildRetrofit(ip, securedClient).create(MeshApiService::class.java)
        }

        private fun buildRetrofit(ip: String, client: OkHttpClient): Retrofit {
            val sanitizedIp = ip.trim().filter { !it.isWhitespace() }
            // Only append port if not present
            val baseUrlWithProtocol = when {
                sanitizedIp.contains(":") -> {
                    if (sanitizedIp.startsWith("http")) sanitizedIp else "http://$sanitizedIp"
                }
                sanitizedIp.startsWith("http") -> "$sanitizedIp:8000"
                else -> "http://$sanitizedIp:8000"
            }
            val finalBaseUrl = if (baseUrlWithProtocol.endsWith("/")) baseUrlWithProtocol else "$baseUrlWithProtocol/"
            
            return Retrofit.Builder()
                .baseUrl(finalBaseUrl)
                .client(client)
                .addConverterFactory(GsonConverterFactory.create())
                .build()
        }

        private fun create(ip: String): MeshApiService {
            Log.d(TAG, "Initializing Mesh Node API at: $ip")

            val logging = HttpLoggingInterceptor { message ->
                Log.d(TAG, message)
            }.apply {
                level = HttpLoggingInterceptor.Level.BODY
            }

            val client = OkHttpClient.Builder()
                .connectTimeout(30, TimeUnit.SECONDS)
                .readTimeout(0, TimeUnit.SECONDS) // Disable read timeout for streaming
                .writeTimeout(30, TimeUnit.SECONDS)
                .addInterceptor(logging)
                .addInterceptor { chain ->
                    val request = chain.request().newBuilder()
                        .addHeader("x-api-key", SOVEREIGN_API_KEY)
                        .build()
                    chain.proceed(request)
                }
                .build()

            return buildRetrofit(ip, client).create(MeshApiService::class.java)
        }
    }
}
