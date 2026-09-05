package com.example.anthony_ai.data.model

import com.google.gson.annotations.SerializedName
import kotlinx.serialization.Serializable
import kotlinx.serialization.SerialName

@Serializable
data class AIVideo(
    @SerializedName("id")
    @SerialName("id")
    val id: String? = null,
    
    @SerializedName("title")
    @SerialName("title")
    val title: String? = "",
    
    @SerializedName("description")
    @SerialName("description")
    val description: String? = "",
    
    @SerializedName("video_url") 
    @SerialName("video_url") 
    val videoUrl: String? = "",
    
    @SerializedName("thumbnail_url") 
    @SerialName("thumbnail_url") 
    val thumbnailUrl: String? = "",
    
    @SerializedName("preview_url") 
    @SerialName("preview_url") 
    val previewUrl: String? = null,
    
    @SerializedName("duration")
    @SerialName("duration")
    val duration: String? = "",
    
    @SerializedName("creator")
    @SerialName("creator")
    val creator: String? = "Anthony AI",
    
    @SerializedName("posted")
    @SerialName("posted")
    val posted: String? = "1h ago",
    
    @SerializedName("likes")
    @SerialName("likes")
    val likes: String? = "0",
    
    @SerializedName("comments")
    @SerialName("comments")
    val comments: String? = "0",
    
    @SerializedName("views")
    @SerialName("views")
    val views: String? = "0",

    @SerializedName("shares")
    @SerialName("shares")
    val shares: String? = "0",

    @SerializedName("permalink_url")
    @SerialName("permalink_url")
    val permalinkUrl: String? = null,
    
    @SerializedName("category")
    @SerialName("category")
    val category: String? = "General",
    
    @SerializedName("style")
    @SerialName("style")
    val style: String? = "Cinematic",

    @SerializedName("raw_payload")
    val rawPayload: Map<String, String>? = null
)
