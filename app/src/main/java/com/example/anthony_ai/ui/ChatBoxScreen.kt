@file:OptIn(ExperimentalMaterial3Api::class, UnstableApi::class)
package com.example.anthony_ai.ui

import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.animation.*
import androidx.compose.animation.core.*
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.rememberTransformableState
import androidx.compose.foundation.gestures.transformable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.Send
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.media3.common.util.UnstableApi
import coil.compose.AsyncImage
import com.example.anthony_ai.ChatMessage
import com.example.anthony_ai.MainViewModel
import com.example.anthony_ai.ui.theme.GlowNeon
import kotlinx.coroutines.delay
import kotlin.time.Duration.Companion.seconds

@Composable
fun ChatBoxScreen(
    viewModel: MainViewModel,
    onMicPressed: () -> Unit = {},
    onMicReleased: () -> Unit = {}
) {
    var messageInput by remember { mutableStateOf("") }
    var textScale by remember { mutableFloatStateOf(1f) }
    var isLiveMode by remember { mutableStateOf(false) }

    val infiniteTransition = rememberInfiniteTransition(label = "LivePulse")
    val liveColor by infiniteTransition.animateColor(
        initialValue = Color.Red,
        targetValue = Color(0xFFFF8C00),
        animationSpec = infiniteRepeatable(
            animation = tween(1000, easing = LinearEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "LiveColor"
    )
    
    val liveGlowAlpha by infiniteTransition.animateFloat(
        initialValue = 0.4f,
        targetValue = 0.8f,
        animationSpec = infiniteRepeatable(
            animation = tween(1000, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "LiveGlow"
    )

    val transformableState = rememberTransformableState { zoomChange, _, _ ->
        textScale = (textScale * zoomChange).coerceIn(0.5f, 3f)
    }

    val imagePicker = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent()
    ) { uri ->
        viewModel.onImageSelected(uri)
    }

    LaunchedEffect(Unit) {
        if (viewModel.chatHistory.isEmpty()) {
            viewModel.chatHistory.add(
                ChatMessage(
                    text = "Welcome back. How can I help you today?",
                    isUser = false
                )
            )
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.Black)
    ) {
        // CHAT LIST
        Box(modifier = Modifier.weight(1f).transformable(state = transformableState)) {
            LazyColumn(
                modifier = Modifier.fillMaxSize().padding(horizontal = 16.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp),
                contentPadding = PaddingValues(top = 16.dp, bottom = 16.dp)
            ) {
                val history = viewModel.chatHistory
                items(count = history.size) { index ->
                    ChatBubble(history[index], textScale)
                }
                if (viewModel.isLoading) {
                    item {
                        NeuralPulseVisualizer(textScale)
                    }
                }
            }

            if (viewModel.linkedTeamTag != null) {
                Surface(
                    color = Color.Black.copy(alpha = 0.8f),
                    shape = RoundedCornerShape(20.dp),
                    border = BorderStroke(1.dp, GlowNeon),
                    modifier = Modifier.align(Alignment.TopCenter).padding(top = 12.dp)
                ) {
                    Row(
                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(6.dp)
                    ) {
                        Icon(imageVector = Icons.Default.Link, contentDescription = null, tint = GlowNeon, modifier = Modifier.size(14.dp))
                        Text(
                            text = "GRID_SYNC: ${viewModel.linkedTeamTag}",
                            color = GlowNeon,
                            fontSize = 10.sp,
                            fontWeight = FontWeight.Bold
                        )
                        IconButton(onClick = { viewModel.unlinkTeam() }, modifier = Modifier.size(16.dp)) {
                            Icon(imageVector = Icons.Default.Close, contentDescription = null, tint = Color.Gray, modifier = Modifier.size(12.dp))
                        }
                    }
                }
            }
        }

        // COMMANDS & INPUT
        Column {
            QuickStrikeBar(
                suggestions = viewModel.quickPanelSuggestions,
                onCommandSelected = { cmd -> 
                    if (cmd.contains("ARCHIVE")) {
                        messageInput = "Consult the archives about "
                    } else if (cmd.contains("FORGE")) {
                        messageInput = "Use the AI forge to create "
                    } else {
                        viewModel.sendText(cmd, null)
                    }
                }
            )

            Surface(
                color = Color(0xFF0C0C0E),
                modifier = Modifier.fillMaxWidth().border(0.5.dp, Color.DarkGray)
            ) {
                Column {
                    if (viewModel.selectedImageUri != null) {
                        Box(modifier = Modifier.padding(12.dp).size(100.dp)) {
                            Surface(shape = RoundedCornerShape(8.dp), color = Color.DarkGray, modifier = Modifier.fillMaxSize()) {
                                AsyncImage(model = viewModel.selectedImageUri, contentDescription = null, contentScale = ContentScale.Crop, modifier = Modifier.fillMaxSize())
                            }
                            IconButton(onClick = { viewModel.onImageSelected(null) }, modifier = Modifier.align(Alignment.TopEnd).size(24.dp).background(Color.Black.copy(alpha = 0.6f), CircleShape)) {
                                Icon(imageVector = Icons.Default.Close, contentDescription = null, tint = Color.White, modifier = Modifier.size(16.dp))
                            }
                        }
                    }

                    Row(
                        modifier = Modifier.fillMaxWidth().padding(12.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Box(
                            modifier = Modifier
                                .size(52.dp)
                                .clip(CircleShape)
                                .background(if (isLiveMode) liveColor else Color(0xFF1A1A1C))
                                .border(1.dp, if (isLiveMode) liveColor.copy(alpha = liveGlowAlpha) else Color.DarkGray, CircleShape)
                                .clickable {
                                    isLiveMode = !isLiveMode
                                    if (isLiveMode) onMicPressed() else onMicReleased()
                                },
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(imageVector = Icons.Default.Mic, contentDescription = null, tint = if (isLiveMode) Color.White else GlowNeon, modifier = Modifier.size(26.dp))
                        }

                        Spacer(modifier = Modifier.width(8.dp))

                        IconButton(onClick = { imagePicker.launch("image/*") }) {
                            Icon(imageVector = Icons.Default.AddPhotoAlternate, contentDescription = null, tint = GlowNeon)
                        }

                        Spacer(modifier = Modifier.width(4.dp))

                        OutlinedTextField(
                            value = messageInput,
                            onValueChange = { messageInput = it },
                            placeholder = { Text(text = "Issue a command...", color = Color.Gray, fontSize = 14.sp) },
                            shape = RoundedCornerShape(26.dp),
                            colors = OutlinedTextFieldDefaults.colors(
                                focusedBorderColor = GlowNeon,
                                unfocusedBorderColor = Color.DarkGray,
                                focusedContainerColor = Color(0xFF161618),
                                unfocusedContainerColor = Color(0xFF161618),
                                focusedTextColor = Color.White,
                                unfocusedTextColor = Color.White
                            ),
                            modifier = Modifier.weight(1f).height(52.dp)
                        )

                        Spacer(modifier = Modifier.width(12.dp))

                        IconButton(
                            onClick = {
                                if (messageInput.isNotBlank() || viewModel.selectedImageUri != null) {
                                    val text = messageInput
                                    val uri = viewModel.selectedImageUri
                                    messageInput = ""
                                    viewModel.sendText(text, uri)
                                }
                            },
                            modifier = Modifier.size(48.dp).clip(CircleShape).background(GlowNeon)
                        ) {
                            Icon(imageVector = Icons.AutoMirrored.Filled.Send, contentDescription = null, tint = Color.Black, modifier = Modifier.size(22.dp))
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun QuickStrikeBar(suggestions: List<String>, onCommandSelected: (String) -> Unit) {
    val commands = if (suggestions.isNotEmpty()) suggestions else listOf(
        "📖 ARCHIVES",
        "🛠️ AI FORGE",
        "🛰️ Recon Area",
        "🎬 Create Reel",
        "📊 Profit Stats"
    )
    
    LazyRow(
        modifier = Modifier.fillMaxWidth().background(Color.Black).padding(vertical = 8.dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        contentPadding = PaddingValues(horizontal = 16.dp)
    ) {
        items(count = commands.size) { index ->
            val cmd = commands[index]
            Surface(
                onClick = { onCommandSelected(cmd) },
                shape = RoundedCornerShape(20.dp),
                color = Color(0xFF1A1A1C),
                border = BorderStroke(1.dp, Color.DarkGray)
            ) {
                Text(
                    text = cmd,
                    color = if (cmd.contains("ARCHIVE") || cmd.contains("FORGE")) GlowNeon else Color.LightGray,
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.padding(horizontal = 14.dp, vertical = 8.dp)
                )
            }
        }
    }
}

@Composable
fun NeuralPulseVisualizer(textScale: Float) {
    var statusText by remember { mutableStateOf("Querying Overpass API...") }
    val statuses = remember {
        listOf(
            "Accessing Forbidden Archives...",
            "Consulting Shadow Librarian...",
            "Syncing AI Production Toolkit...",
            "Analyzing UFO Sighting Density...",
            "Baking Viral Logistics..."
        )
    }

    LaunchedEffect(Unit) {
        while(true) {
            delay(2.seconds)
            statusText = statuses.random()
        }
    }

    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.Start) {
        Box(modifier = Modifier.size(28.dp).clip(CircleShape).background(Color(0xFF1A1A1C)), contentAlignment = Alignment.Center) {
            Text(text = "🐜", fontSize = (14 * textScale).sp)
        }
        Spacer(modifier = Modifier.width(10.dp))
        Surface(
            shape = RoundedCornerShape(topStart = 16.dp, topEnd = 16.dp, bottomStart = 4.dp, bottomEnd = 16.dp),
            color = Color(0xFF111114),
            border = BorderStroke(0.5.dp, GlowNeon.copy(alpha = 0.3f)),
            modifier = Modifier.widthIn(max = 240.dp)
        ) {
            Column(modifier = Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    val infiniteTransition = rememberInfiniteTransition(label = "pulse")
                    repeat(3) { i ->
                        val alpha by infiniteTransition.animateFloat(
                            initialValue = 0.2f,
                            targetValue = 1f,
                            animationSpec = infiniteRepeatable(
                                animation = tween(600, delayMillis = i * 200),
                                repeatMode = RepeatMode.Reverse
                            ),
                            label = "pulseDot"
                        )
                        Box(modifier = Modifier.size(6.dp).clip(CircleShape).background(GlowNeon.copy(alpha = alpha)))
                    }
                }
                Text(
                    text = statusText,
                    color = GlowNeon.copy(alpha = 0.7f),
                    fontSize = (11 * textScale).sp,
                    fontWeight = FontWeight.Light,
                    letterSpacing = 0.5.sp
                )
            }
        }
    }
}

@Composable
fun ChatBubble(msg: ChatMessage, textScale: Float = 1f) {
    val isUser = msg.isUser
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = if (isUser) Arrangement.End else Arrangement.Start
    ) {
        if (!isUser) {
            Box(modifier = Modifier.size(32.dp).clip(CircleShape).background(Color(0xFF1A1A1C)), contentAlignment = Alignment.Center) {
                Text(text = "🐜", fontSize = (16 * textScale).sp)
            }
            Spacer(modifier = Modifier.width(10.dp))
        }

        Surface(
            shape = RoundedCornerShape(
                topStart = 20.dp,
                topEnd = 20.dp,
                bottomStart = if (isUser) 20.dp else 4.dp,
                bottomEnd = if (isUser) 4.dp else 20.dp
            ),
            color = if (isUser) GlowNeon else Color(0xFF161618),
            border = if (!isUser) BorderStroke(0.5.dp, Color.DarkGray) else null,
            modifier = Modifier.widthIn(max = 310.dp)
        ) {
            Column(modifier = Modifier.padding(14.dp)) {
                if (!msg.imageUrl.isNullOrBlank()) {
                    AsyncImage(
                        model = msg.imageUrl,
                        contentDescription = null,
                        contentScale = ContentScale.Crop,
                        modifier = Modifier.fillMaxWidth().height(220.dp).clip(RoundedCornerShape(12.dp))
                    )
                    Spacer(modifier = Modifier.height(10.dp))
                }
                if (msg.text.isNotBlank()) {
                    Text(
                        text = msg.text,
                        color = if (isUser) Color.Black else Color.White,
                        fontSize = (15 * textScale).sp,
                        lineHeight = (20 * textScale).sp
                    )
                }
            }
        }
    }
}
