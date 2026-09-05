@file:OptIn(ExperimentalMaterial3Api::class)
package com.example.anthony_ai.ui

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.Share
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import androidx.lifecycle.viewmodel.compose.viewModel
import coil.compose.AsyncImage
import com.example.anthony_ai.MainViewModel
import com.example.anthony_ai.data.model.AIVideo
import com.example.anthony_ai.ui.theme.GlowNeon
import com.example.anthony_ai.ui.theme.ObsidianGray
import java.util.Locale

@Composable
fun CheckpointHomeScreen() {
    val viewModel: MainViewModel = viewModel()
    var selectedTab by remember { mutableIntStateOf(0) }

    Scaffold(
        bottomBar = {
            NavigationBar(
                containerColor = MaterialTheme.colorScheme.surface,
                contentColor = GlowNeon,
                modifier = Modifier.border(1.dp, Color.DarkGray.copy(alpha = 0.3f))
            ) {
                NavigationBarItem(
                    selected = selectedTab == 0,
                    onClick = { selectedTab = 0 },
                    icon = { Icon(Icons.Default.Info, "COMMAND") },
                    label = { Text("COMMAND", fontSize = 9.sp) },
                    colors = NavigationBarItemDefaults.colors(
                        selectedIconColor = GlowNeon,
                        unselectedIconColor = Color.Gray,
                        indicatorColor = ObsidianGray
                    )
                )
                NavigationBarItem(
                    selected = selectedTab == 1,
                    onClick = { selectedTab = 1 },
                    icon = { Icon(Icons.Default.PlayArrow, "WORMHOLE") },
                    label = { Text("WORMHOLE", fontSize = 9.sp) },
                    colors = NavigationBarItemDefaults.colors(
                        selectedIconColor = GlowNeon,
                        unselectedIconColor = Color.Gray,
                        indicatorColor = ObsidianGray
                    )
                )
            }
        },
        modifier = Modifier.fillMaxSize(),
        containerColor = MaterialTheme.colorScheme.background
    ) { padding ->
        Box(modifier = Modifier.padding(padding)) {
            if (selectedTab == 0) {
                MissionCommandCenterUI(viewModel)
            } else {
                WormholeFeedSection(viewModel)
            }
        }
    }
}

@Composable
fun MissionCommandCenterUI(viewModel: MainViewModel) {
    val telemetry = viewModel.missionTelemetry
    val activityFeed = viewModel.activityFeed
    val connectionStatus = viewModel.connectionStatus
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .statusBarsPadding()
            .padding(horizontal = 16.dp),
        horizontalAlignment = Alignment.Start,
        verticalArrangement = Arrangement.Top
    ) {
        Spacer(modifier = Modifier.height(24.dp))
        
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column {
                Text(
                    text = "ANTHONY AI",
                    color = Color.Yellow,
                    fontWeight = FontWeight.Black,
                    fontSize = 28.sp,
                    letterSpacing = 1.sp
                )
                Text(
                    text = "CLOUD HUB (v1.0)",
                    color = GlowNeon,
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold,
                    letterSpacing = 1.sp
                )
            }
            IconButton(onClick = { viewModel.reconnect() }) {
                Icon(Icons.Default.Refresh, "Reconnect", tint = GlowNeon)
            }
        }

        Spacer(modifier = Modifier.height(16.dp))

        // --- ACTIVITY FEED (THE HEARTBEAT) ---
        Surface(
            color = Color(0xFF0A0A0A),
            shape = RoundedCornerShape(12.dp),
            border = BorderStroke(1.dp, Color.DarkGray),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(modifier = Modifier.padding(12.dp)) {
                if (telemetry == null) {
                    Text("> SYNCING...", color = Color.Gray, fontSize = 11.sp, fontFamily = FontFamily.Monospace)
                } else {
                    Text("[ CLOUD STATUS ]", color = Color.Cyan, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                    Spacer(Modifier.height(8.dp))
                    
                    val now = System.currentTimeMillis() / 1000
                    telemetry.clocksInfo.forEach { clock ->
                        if (clock.channel != "QUANTUM_LOCK") {
                            val etaSec = (clock.lastStrike + 3600.0) - now.toDouble()
                            val m = (etaSec / 60.0).coerceAtLeast(0.0).toInt()
                            val s = (etaSec % 60).coerceAtLeast(0.0).toInt()
                            val etaStr = if (m > 0 || s > 0) String.format(Locale.US, "%02d:%02d", m, s) else "LIVE"
                            
                            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                                Text(" • ${clock.channel}", color = Color.White, fontSize = 9.sp, fontFamily = FontFamily.Monospace)
                                Text("ETA: $etaStr", color = if (etaStr == "LIVE") Color.Yellow else GlowNeon, fontSize = 9.sp, fontFamily = FontFamily.Monospace)
                            }
                        }
                    }
                }
            }
        }

        Spacer(modifier = Modifier.height(16.dp))

        // --- HUB FEED ---
        Text(
            text = "[ CLOUD ACTIVITY ]",
            color = GlowNeon,
            fontSize = 11.sp,
            fontWeight = FontWeight.Bold,
            modifier = Modifier.padding(bottom = 8.dp)
        )
        
        Surface(
            color = MaterialTheme.colorScheme.background,
            shape = RoundedCornerShape(8.dp),
            border = BorderStroke(1.dp, GlowNeon.copy(alpha = 0.4f)),
            modifier = Modifier
                .fillMaxWidth()
                .weight(1f)
        ) {
            Column {
                val scrollState = rememberLazyListState()
                
                LaunchedEffect(activityFeed.size) {
                    if (activityFeed.isNotEmpty()) {
                        scrollState.animateScrollToItem(activityFeed.size - 1)
                    }
                }

                LazyColumn(
                    state = scrollState,
                    modifier = Modifier.weight(1f).padding(8.dp),
                    verticalArrangement = Arrangement.spacedBy(2.dp)
                ) {
                    items(activityFeed.size) { index ->
                        val log = activityFeed[index]
                        val color = when {
                            log.contains("Success") -> Color.Green
                            log.contains("failed") || log.contains("Interrupted") -> Color.Red
                            log.contains("broadcast") -> Color.Yellow
                            else -> GlowNeon
                        }
                        Text(
                            text = "> $log",
                            color = color,
                            fontSize = 10.sp,
                            fontFamily = FontFamily.Monospace,
                            lineHeight = 12.sp,
                            modifier = Modifier.fillMaxWidth()
                        )
                    }
                }
                
                // --- AGENT COMMAND PROMPT ---
                var commandText by remember { mutableStateOf("") }
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(Color(0xFF050505))
                        .border(1.dp, Color.DarkGray.copy(alpha = 0.2f), RoundedCornerShape(bottomStart = 8.dp, bottomEnd = 8.dp))
                        .padding(10.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text("$ ", color = GlowNeon, fontSize = 14.sp, fontFamily = FontFamily.Monospace)
                    BasicTextField(
                        value = commandText,
                        onValueChange = { commandText = it },
                        modifier = Modifier.weight(1f).padding(start = 4.dp),
                        textStyle = TextStyle(
                            color = Color.White,
                            fontSize = 14.sp,
                            fontFamily = FontFamily.Monospace
                        ),
                        cursorBrush = SolidColor(GlowNeon),
                        singleLine = true,
                        keyboardOptions = KeyboardOptions(
                            keyboardType = KeyboardType.Text,
                            imeAction = ImeAction.Send
                        ),
                        keyboardActions = KeyboardActions(
                            onSend = {
                                if (commandText.isNotBlank()) {
                                    viewModel.sendText(commandText)
                                    commandText = ""
                                }
                            }
                        )
                    )
                }
            }
        }

        Spacer(modifier = Modifier.height(8.dp))

        // --- STATUS FOOTER ---
        Text(
            text = connectionStatus ?: "SCANNING GRID...",
            color = Color.DarkGray,
            fontSize = 8.sp,
            modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp),
            textAlign = TextAlign.Center,
            fontFamily = FontFamily.Monospace
        )
    }
}

@Composable
fun WormholeFeedSection(viewModel: MainViewModel) {
    val videos = viewModel.supabaseVideos
    val categories = listOf("For you", "Shadow", "Alpha", "Archive")
    var playingVideoUrl by remember { mutableStateOf<String?>(null) }
    
    Column(modifier = Modifier.fillMaxSize()) {
        // --- CATEGORY SELECTOR ---
        SecondaryScrollableTabRow(
            selectedTabIndex = categories.indexOf(viewModel.selectedCategory).coerceAtLeast(0),
            containerColor = Color.Black,
            contentColor = GlowNeon,
            edgePadding = 16.dp,
            divider = {},
            indicator = {
                val index = categories.indexOf(viewModel.selectedCategory).coerceAtLeast(0)
                TabRowDefaults.SecondaryIndicator(
                    modifier = Modifier.tabIndicatorOffset(index, matchContentSize = true),
                    color = GlowNeon
                )
            }
        ) {
            categories.forEach { category ->
                Tab(
                    selected = viewModel.selectedCategory == category,
                    onClick = { viewModel.updateCategory(category) },
                    text = { 
                        Text(
                            text = category.uppercase(),
                            fontSize = 10.sp,
                            fontWeight = FontWeight.Bold,
                            letterSpacing = 1.sp
                        )
                    }
                )
            }
        }

        // --- DYNAMIC FETCHING ENGINE ---
        Box(modifier = Modifier.fillMaxSize().weight(1f)) {
            if (videos.isEmpty() && !viewModel.isRefreshing) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator(color = GlowNeon)
                }
            } else {
                LazyColumn(
                    modifier = Modifier.fillMaxSize(),
                    contentPadding = PaddingValues(bottom = 16.dp)
                ) {
                    items(videos.size) { index ->
                        VideoStrikeItem(
                            video = videos[index],
                            viewModel = viewModel,
                            onPlay = { playingVideoUrl = it }
                        )
                    }
                }
            }
            
            // Manual Refresh Trigger
            FloatingActionButton(
                onClick = { viewModel.fetchSupabaseFeed(force = true) },
                containerColor = GlowNeon,
                modifier = Modifier
                    .align(Alignment.BottomEnd)
                    .padding(16.dp)
                    .size(48.dp),
                shape = RoundedCornerShape(12.dp)
            ) {
                Icon(Icons.Default.Refresh, "Refresh Feed", tint = Color.Black)
            }
        }
    }

    if (playingVideoUrl != null) {
        Dialog(
            onDismissRequest = { playingVideoUrl = null },
            properties = DialogProperties(usePlatformDefaultWidth = false)
        ) {
            VideoPlayer(videoUrl = playingVideoUrl!!, onDismiss = { playingVideoUrl = null })
        }
    }
}

@Composable
fun VideoStrikeItem(video: AIVideo, viewModel: MainViewModel, onPlay: (String) -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp)
            .border(BorderStroke(1.dp, Color.DarkGray.copy(alpha = 0.5f)), RoundedCornerShape(16.dp)),
        colors = CardDefaults.cardColors(containerColor = Color(0xFF050505)),
        shape = RoundedCornerShape(16.dp)
    ) {
        Column {
            Box(modifier = Modifier
                .height(220.dp)
                .fillMaxWidth()
                .clickable { video.videoUrl?.let { onPlay(it) } }) {
                AsyncImage(
                    model = video.videoUrl?.let { if (it.contains("?")) "$it&thumb=true" else "$it?thumb=true" } ?: video.thumbnailUrl,
                    contentDescription = null,
                    modifier = Modifier.fillMaxSize(),
                    contentScale = ContentScale.Crop
                )
                
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .background(
                            Brush.verticalGradient(
                                colors = listOf(Color.Transparent, Color.Black.copy(alpha = 0.6f)),
                                startY = 300f
                            )
                        )
                )

                Box(
                    modifier = Modifier
                        .align(Alignment.BottomEnd)
                        .padding(12.dp)
                        .background(Color.Black.copy(alpha = 0.8f), RoundedCornerShape(4.dp))
                        .padding(horizontal = 8.dp, vertical = 4.dp)
                ) {
                    Text(video.duration ?: "REEL", color = GlowNeon, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                }
                
                Icon(
                    imageVector = Icons.Default.PlayArrow,
                    contentDescription = null,
                    tint = Color.White.copy(alpha = 0.8f),
                    modifier = Modifier
                        .size(48.dp)
                        .align(Alignment.Center)
                )
            }
            
            Column(modifier = Modifier.padding(16.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Surface(
                            color = GlowNeon.copy(alpha = 0.1f),
                            shape = RoundedCornerShape(4.dp),
                            border = BorderStroke(1.dp, GlowNeon.copy(alpha = 0.3f)),
                            modifier = Modifier.padding(end = 8.dp)
                        ) {
                            Text(
                                text = "OS SOURCE",
                                color = GlowNeon,
                                fontSize = 9.sp,
                                fontWeight = FontWeight.Black,
                                modifier = Modifier.padding(horizontal = 4.dp, vertical = 2.dp)
                            )
                        }
                        Text(
                            text = video.title ?: "Sovereign Strike",
                            color = Color.White,
                            fontWeight = FontWeight.Bold,
                            fontSize = 16.sp,
                            modifier = Modifier.weight(1f)
                        )
                    }
                
                Spacer(Modifier.height(4.dp))
                
                Text(
                    text = video.description ?: "",
                    color = Color.Gray,
                    fontSize = 12.sp,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis
                )
                
                Spacer(Modifier.height(12.dp))

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.End,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(video.posted ?: "Just Now", color = GlowNeon, fontSize = 10.sp, fontWeight = FontWeight.Medium)
                }

                Spacer(Modifier.height(16.dp))
                
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.End
                ) {
                    OutlinedButton(
                        onClick = { /* Share Logic */ },
                        modifier = Modifier.size(40.dp),
                        shape = RoundedCornerShape(8.dp),
                        contentPadding = PaddingValues(0.dp),
                        border = BorderStroke(1.dp, Color.DarkGray)
                    ) {
                        Icon(Icons.Default.Share, null, tint = Color.White, modifier = Modifier.size(18.dp))
                    }
                }
            }
        }
    }
}
