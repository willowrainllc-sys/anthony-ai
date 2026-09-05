package com.example.anthony_ai.data.repository

import android.util.Log
import com.example.anthony_ai.SupabaseClient
import com.example.anthony_ai.data.model.AIVideo
import io.github.jan.supabase.postgrest.postgrest
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class AIVideoRepository {
    
    suspend fun getVideos(): List<AIVideo> = withContext(Dispatchers.IO) {
        try {
            // Priority check for the 'videos' table which is used by the backend
            val response = SupabaseClient.client.postgrest["videos"]
                .select()
            
            val data = response.decodeList<AIVideo>()
            Log.d("SUPABASE_SYNC", "SUCCESS: Decoded ${data.size} videos from Supabase")
            data
        } catch (e: Exception) {
            val msg = e.localizedMessage ?: "Unknown Supabase Error"
            if (msg.contains("PGRST205") || msg.contains("not found")) {
                Log.w("SUPABASE_SYNC", "Table 'videos' not found. This is expected if using the Backend API as primary source.")
            } else {
                Log.e("SUPABASE_SYNC", "Fetch failed: $msg", e)
            }
            emptyList()
        }
    }

    suspend fun addVideo(video: AIVideo) = withContext(Dispatchers.IO) {
        try {
            SupabaseClient.client.postgrest["videos"].insert(video)
        } catch (e: Exception) {
            // Log or handle error
        }
    }
}
