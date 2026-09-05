package com.example.anthony_ai

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

import com.example.anthony_ai.ui.theme.ObsidianBlack
import com.example.anthony_ai.ui.theme.glowBorder

// Core data models for the AI TV ecosystem
data class TopicSection(val title: String, val videos: List<VideoItem>)
data class VideoItem(val title: String, val subtitle: String, val thumbnailUrl: String, val duration: String, val videoUrl: String)
