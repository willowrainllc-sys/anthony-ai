@file:OptIn(ExperimentalMaterial3Api::class, UnstableApi::class)
package com.example.anthony_ai.ui

import android.widget.Toast
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.Chat
import androidx.compose.material.icons.automirrored.filled.Logout
import androidx.compose.material.icons.automirrored.filled.TrendingUp
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.media3.common.MediaItem
import androidx.media3.common.MimeTypes
import androidx.media3.common.Player
import androidx.media3.common.util.UnstableApi
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.ui.AspectRatioFrameLayout
import androidx.media3.ui.PlayerView
import coil.compose.AsyncImage
import com.example.anthony_ai.MainViewModel
import com.example.anthony_ai.NewsBriefResponse
import com.example.anthony_ai.TopicSection
import com.example.anthony_ai.VideoItem
import com.example.anthony_ai.WorldTwinSpatialOverlayScreen
import com.example.anthony_ai.data.model.AIVideo
import com.example.anthony_ai.ui.theme.GlowNeon
import com.example.anthony_ai.ui.theme.glowBorder
import java.util.Locale

@Composable
fun AnthonyAiFeedScreen(
    onLogout: () -> Unit = {},
    onMicPressed: () -> Unit = {},
    onMicReleased: () -> Unit = {}
) {
    val mainViewModel: MainViewModel = viewModel()
    val videos = mainViewModel.supabaseVideos
    var playingVideoUrl by remember { mutableStateOf<String?>(null) }
    var selectedNavTab by remember { mutableIntStateOf(0) }
    val context = LocalContext.current

    LaunchedEffect(Unit) {
        mainViewModel.fetchSupabaseFeed(force = true)
        mainViewModel.fetchNewsBrief()
        mainViewModel.fetchDashboard()
        mainViewModel.fetchRevenueVitals()
    }

    Column(modifier = Modifier.fillMaxSize().background(Color.Black)) {
        // --- CLEAN MINIMAL HEADER ---
        Surface(
            color = Color.Black,
            modifier = Modifier
                .fillMaxWidth()
                .statusBarsPadding()
                .padding(horizontal = 24.dp, vertical = 14.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Box(
                        modifier = Modifier
                            .size(36.dp)
                            .clip(CircleShape)
                            .background(GlowNeon)
                            .clickable {
                                mainViewModel.triggerFullStrikeAll()
                                Toast.makeText(context, "Refreshing...", Toast.LENGTH_SHORT).show()
                            },
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(imageVector = Icons.Default.FlashOn, contentDescription = null, tint = Color.Black, modifier = Modifier.size(20.dp))
                    }
                    Spacer(modifier = Modifier.width(16.dp))
                    @Suppress("DEPRECATION")
                    Text(
                        text = "ANTHONY",
                        color = Color.White,
                        fontSize = 18.sp,
                        fontWeight = FontWeight.ExtraBold,
                        letterSpacing = 1.5.sp
                    )
                }

                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(20.dp)) {
                    Box(modifier = Modifier.size(8.dp).clip(CircleShape).background(Color.Green))
                    
                    IconButton(onClick = { mainViewModel.showControlCenter = true }, modifier = Modifier.size(24.dp)) {
                        Icon(imageVector = Icons.Default.Tune, contentDescription = null, tint = Color.LightGray, modifier = Modifier.size(20.dp))
                    }
                    IconButton(onClick = onLogout, modifier = Modifier.size(24.dp)) {
                        Icon(imageVector = Icons.AutoMirrored.Filled.Logout, contentDescription = null, tint = Color.LightGray, modifier = Modifier.size(18.dp))
                    }
                }
            }
        }

        // CONTENT
        Box(modifier = Modifier.weight(1f)) {
            when (selectedNavTab) {
                0 -> {
                    val categories = listOf("For you", "Shadow", "Alpha", "Archive")
                    Column(modifier = Modifier.fillMaxSize()) {
                        SecondaryScrollableTabRow(
                            selectedTabIndex = categories.indexOf(mainViewModel.selectedCategory).coerceAtLeast(0),
                            containerColor = Color.Black,
                            contentColor = GlowNeon,
                            edgePadding = 16.dp,
                            divider = {},
                            indicator = {
                                val index = categories.indexOf(mainViewModel.selectedCategory).coerceAtLeast(0)
                                TabRowDefaults.SecondaryIndicator(
                                    modifier = Modifier.tabIndicatorOffset(index, matchContentSize = true),
                                    color = GlowNeon
                                )
                            }
                        ) {
                            categories.forEach { category ->
                                Tab(
                                    selected = mainViewModel.selectedCategory == category,
                                    onClick = { mainViewModel.updateCategory(category) },
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

                        if (videos.isEmpty()) {
                            Box(modifier = Modifier.fillMaxSize().weight(1f), contentAlignment = Alignment.Center) {
                                if (mainViewModel.isRefreshing) {
                                    CircularProgressIndicator(color = GlowNeon, strokeWidth = 2.dp)
                                } else {
                                    Text("No content available in ${mainViewModel.selectedCategory}", color = Color.Gray)
                                }
                            }
                        } else {
                            LazyColumn(
                                modifier = Modifier.fillMaxSize().weight(1f),
                                contentPadding = PaddingValues(bottom = 24.dp),
                                verticalArrangement = Arrangement.spacedBy(20.dp)
                            ) {
                                mainViewModel.newsBrief?.let { brief ->
                                    item { NewsBriefCard(brief) }
                                }

                                items(videos) { video ->
                                    VideoFeedCard(video = video, viewModel = mainViewModel)
                                }

                                items(mainViewModel.dashboardSections) { section ->
                                    DashboardSectionCard(section)
                                }
                            }
                        }
                    }
                }
                1 -> WorldTwinSpatialOverlayScreen(
                    viewModel = mainViewModel,
                    onBack = { selectedNavTab = 0 }
                )
                2 -> EmpireManagementScreen(mainViewModel)
                3 -> ChatBoxScreen(viewModel = mainViewModel, onMicPressed = onMicPressed, onMicReleased = onMicReleased)
                4 -> ProfileScreen(mainViewModel, onLogout)
            }

            if (playingVideoUrl != null) {
                Dialog(onDismissRequest = { playingVideoUrl = null }, properties = DialogProperties(usePlatformDefaultWidth = false)) {
                    Box(modifier = Modifier.fillMaxSize()) {
                        VideoPlayer(videoUrl = playingVideoUrl!!, onDismiss = { playingVideoUrl = null })
                        IconButton(onClick = { playingVideoUrl = null }, modifier = Modifier.align(Alignment.TopEnd).statusBarsPadding().padding(16.dp).background(Color.Black.copy(alpha = 0.5f), CircleShape)) {
                            Icon(Icons.Default.Close, "Close", tint = Color.White)
                        }
                    }
                }
            }
            if (mainViewModel.showTacticalHud) TacticalHudOverlay()
            if (mainViewModel.showControlCenter) ControlCenterSheet(onDismiss = { mainViewModel.showControlCenter = false })
        }

        // BOTTOM BAR
        NavigationBar(
            containerColor = Color.Black,
            contentColor = GlowNeon,
            tonalElevation = 0.dp,
            modifier = Modifier.border(0.5.dp, Color.White.copy(alpha = 0.05f))
        ) {
            val tabs = listOf(
                Triple(0, Icons.Default.AutoAwesome, "Live"),
                Triple(1, Icons.Default.Public, "Globe"),
                Triple(2, Icons.Default.AccountBalance, "Profit"),
                Triple(3, Icons.AutoMirrored.Filled.Chat, "Chat"),
                Triple(4, Icons.Default.Person, "Me")
            )
            
            tabs.forEach { (index, icon, label) ->
                NavigationBarItem(
                    selected = (selectedNavTab == index),
                    onClick = { selectedNavTab = index },
                    icon = { Icon(icon, null, modifier = Modifier.size(24.dp)) },
                    label = { Text(label, fontSize = 10.sp, fontWeight = FontWeight.SemiBold) },
                    colors = NavigationBarItemDefaults.colors(
                        selectedIconColor = GlowNeon,
                        unselectedIconColor = Color.DarkGray,
                        indicatorColor = Color.Transparent,
                        selectedTextColor = GlowNeon,
                        unselectedTextColor = Color.Gray
                    )
                )
            }
        }
    }
}

@Composable
fun EmpireManagementScreen(viewModel: MainViewModel) {
    val vitals = viewModel.revenueVitals
    val context = LocalContext.current

    Column(modifier = Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.spacedBy(24.dp)) {
        @Suppress("DEPRECATION")
        Text(text = "Revenue Stream", color = GlowNeon, fontSize = 22.sp, fontWeight = FontWeight.Black)
        
        Card(
            modifier = Modifier.fillMaxWidth().glowBorder(cornerRadius = 24.dp, color = GlowNeon.copy(alpha = 0.1f)),
            colors = CardDefaults.cardColors(containerColor = Color(0xFF0C0C0E))
        ) {
            Column(modifier = Modifier.padding(24.dp), horizontalAlignment = Alignment.CenterHorizontally) {
                Text(text = "TODAY'S PROFIT", color = Color.Gray, fontSize = 12.sp, fontWeight = FontWeight.Bold, letterSpacing = 1.sp)
                Spacer(modifier = Modifier.height(12.dp))
                val revValue = vitals?.totalDailyRevenue ?: 0.0
                Text(
                    text = String.format(Locale.US, "$%,.2f", revValue),
                    color = Color.White,
                    fontSize = 36.sp,
                    fontWeight = FontWeight.Black
                )
            }
        }

        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
            EmpireActionButton(
                label = "BOOST GROWTH",
                icon = Icons.AutoMirrored.Filled.TrendingUp,
                color = GlowNeon,
                onClick = { 
                    Toast.makeText(context, "Engagement engine active...", Toast.LENGTH_SHORT).show()
                }
            )
            EmpireActionButton(
                label = "VIRAL DROP",
                icon = Icons.Default.AutoAwesome,
                color = Color.Cyan,
                onClick = { /* Engagement Logic */ }
            )
        }

        Text(text = "Active Streams", color = Color.Gray, fontSize = 13.sp, fontWeight = FontWeight.Bold)
        
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            SpecialistChip("ARCHIVE", GlowNeon)
            SpecialistChip("AI FORGE", Color.Cyan)
        }

        LazyColumn(verticalArrangement = Arrangement.spacedBy(14.dp), modifier = Modifier.weight(1f)) {
            vitals?.portfolio?.let { portfolio ->
                items(portfolio) { asset ->
                    val changeStr = String.format(Locale.US, "%+,.2f%%", asset.change)
                    EmpireAssetRow(
                        title = asset.id,
                        value = String.format(Locale.US, "$%,.2f", asset.value),
                        change = changeStr,
                        isPositive = asset.change >= 0
                    )
                }
            }
            
            vitals?.commerce?.let { commerce ->
                items(commerce) { store ->
                    EmpireAssetRow(
                        title = store.id.replace("_", " "),
                        value = String.format(Locale.US, "Daily: $%,.2f", store.daily),
                        change = String.format(Locale.US, "Total: $%,.0f", store.total),
                        isPositive = true
                    )
                }
            }
        }
    }
}

@Composable
fun RowScope.EmpireActionButton(label: String, icon: ImageVector, color: Color, onClick: () -> Unit) {
    Button(
        onClick = onClick,
        modifier = Modifier.height(58.dp).weight(1f),
        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF141416)),
        border = BorderStroke(1.dp, color.copy(alpha = 0.2f)),
        shape = RoundedCornerShape(16.dp),
        contentPadding = PaddingValues(0.dp)
    ) {
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            Icon(imageVector = icon, contentDescription = null, tint = color, modifier = Modifier.size(18.dp))
            Text(text = label, color = color, fontSize = 10.sp, fontWeight = FontWeight.Bold)
        }
    }
}

@Composable
fun EmpireAssetRow(title: String, value: String, change: String, isPositive: Boolean) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(20.dp),
        color = Color(0xFF0F0F11),
        border = BorderStroke(0.5.dp, Color.White.copy(alpha = 0.05f))
    ) {
        Row(modifier = Modifier.padding(18.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.SpaceBetween) {
            Column {
                Text(text = title, color = Color.White, fontSize = 15.sp, fontWeight = FontWeight.Bold)
                Text(text = "Operational", color = Color.Gray, fontSize = 11.sp)
            }
            Column(horizontalAlignment = Alignment.End) {
                Text(text = value, color = Color.White, fontSize = 14.sp, fontWeight = FontWeight.Bold)
                Text(text = change, color = if (isPositive) Color.Green else Color.Red, fontSize = 12.sp, fontWeight = FontWeight.Bold)
            }
        }
    }
}

@Composable
fun SpecialistChip(name: String, color: Color) {
    Surface(
        shape = RoundedCornerShape(20.dp),
        color = color.copy(alpha = 0.05f),
        border = BorderStroke(1.dp, color.copy(alpha = 0.2f))
    ) {
        Row(modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp), verticalAlignment = Alignment.CenterVertically) {
            Box(modifier = Modifier.size(6.dp).clip(CircleShape).background(color))
            Spacer(Modifier.width(8.dp))
            Text(text = name, color = color, fontSize = 10.sp, fontWeight = FontWeight.Bold)
        }
    }
}

@Composable
fun TacticalHudOverlay() {
    Box(modifier = Modifier.fillMaxSize().padding(16.dp).statusBarsPadding(), contentAlignment = Alignment.TopEnd) {
        Column(horizontalAlignment = Alignment.End, verticalArrangement = Arrangement.spacedBy(4.dp)) {
            Text(text = "SECURE", color = GlowNeon.copy(alpha = 0.6f), fontSize = 10.sp, fontWeight = FontWeight.Bold)
            Text(text = "LINKED", color = Color.Cyan.copy(alpha = 0.5f), fontSize = 9.sp)
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ControlCenterSheet(onDismiss: () -> Unit) {
    ModalBottomSheet(onDismissRequest = onDismiss, containerColor = Color(0xFF0C0C0E), scrimColor = Color.Black.copy(alpha = 0.8f)) {
        Column(modifier = Modifier.fillMaxWidth().padding(24.dp).padding(bottom = 32.dp), verticalArrangement = Arrangement.spacedBy(20.dp)) {
            Text(text = "Settings", color = GlowNeon, fontSize = 18.sp, fontWeight = FontWeight.Black)
            Button(onClick = onDismiss, modifier = Modifier.fillMaxWidth(), colors = ButtonDefaults.buttonColors(containerColor = GlowNeon), shape = RoundedCornerShape(12.dp)) {
                Text(text = "DONE", color = Color.Black, fontWeight = FontWeight.Bold)
            }
        }
    }
}

@Composable
fun NewsBriefCard(brief: NewsBriefResponse) {
    Card(shape = RoundedCornerShape(24.dp), colors = CardDefaults.cardColors(containerColor = Color(0xFF111113)), modifier = Modifier.fillMaxWidth().padding(horizontal = 12.dp).border(1.dp, Color.White.copy(alpha = 0.05f), RoundedCornerShape(24.dp))) {
        Column(modifier = Modifier.padding(20.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(imageVector = Icons.Default.AutoAwesome, contentDescription = null, tint = GlowNeon, modifier = Modifier.size(18.dp))
                Spacer(modifier = Modifier.width(10.dp))
                Text(text = "INTELLIGENCE", color = GlowNeon, fontSize = 12.sp, fontWeight = FontWeight.Bold)
            }
            Spacer(Modifier.height(14.dp))
            Text(text = brief.headline, color = Color.White, fontSize = 19.sp, fontWeight = FontWeight.ExtraBold)
            Spacer(Modifier.height(8.dp))
            Text(text = brief.brief, color = Color.LightGray, fontSize = 14.sp, lineHeight = 22.sp)
        }
    }
}

@Composable
fun DashboardSectionCard(section: TopicSection) {
    Column(modifier = Modifier.padding(vertical = 12.dp)) {
        Text(text = section.title, color = Color.White, fontSize = 18.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(start = 24.dp, bottom = 14.dp))
        LazyRow(contentPadding = PaddingValues(horizontal = 20.dp), horizontalArrangement = Arrangement.spacedBy(14.dp)) {
            items(section.videos) { video ->
                VideoItemCard(video)
            }
        }
    }
}

@Composable
fun VideoItemCard(video: VideoItem) {
    Card(shape = RoundedCornerShape(20.dp), colors = CardDefaults.cardColors(containerColor = Color(0xFF111113)), modifier = Modifier.width(170.dp)) {
        Column {
            Box(modifier = Modifier.fillMaxWidth().height(95.dp).background(Color.DarkGray)) {
                AsyncImage(model = video.thumbnailUrl, contentDescription = null, modifier = Modifier.fillMaxSize(), contentScale = ContentScale.Crop)
            }
            Column(modifier = Modifier.padding(12.dp)) {
                Text(text = video.title, color = Color.White, fontSize = 13.sp, fontWeight = FontWeight.Bold, maxLines = 1, overflow = TextOverflow.Ellipsis)
                Text(text = video.subtitle, color = Color.Gray, fontSize = 11.sp, maxLines = 1)
            }
        }
    }
}

@Composable
fun VideoFeedCard(video: AIVideo, viewModel: MainViewModel) {
    val context = LocalContext.current
    val exoPlayer = remember(video.videoUrl) {
        ExoPlayer.Builder(context).build().apply {
            if (!video.videoUrl.isNullOrBlank()) {
                val mediaItem = MediaItem.Builder()
                    .setUri(video.videoUrl)
                    .setMimeType(MimeTypes.VIDEO_MP4)
                    .build()
                setMediaItem(mediaItem)
                repeatMode = Player.REPEAT_MODE_ONE
                volume = 0f
                prepare()
                playWhenReady = true
            }
        }
    }
    DisposableEffect(video.videoUrl) { onDispose { exoPlayer.release() } }
    Card(shape = RoundedCornerShape(28.dp), colors = CardDefaults.cardColors(containerColor = Color(0xFF0C0C0E)), modifier = Modifier.fillMaxWidth().padding(horizontal = 12.dp).border(0.5.dp, Color.White.copy(alpha = 0.05f), RoundedCornerShape(28.dp)), elevation = CardDefaults.cardElevation(defaultElevation = 0.dp)) {
        Column {
            Row(modifier = Modifier.fillMaxWidth().padding(20.dp), verticalAlignment = Alignment.CenterVertically) {
                Box(modifier = Modifier.size(38.dp).clip(CircleShape).background(Color(0xFF1A1A1C)), contentAlignment = Alignment.Center) { Text(text = "🐜", fontSize = 18.sp) }
                Spacer(modifier = Modifier.width(16.dp))
                Column {
                    Text(text = video.creator ?: "Anthony AI", color = Color.White, fontSize = 14.sp, fontWeight = FontWeight.Bold)
                    Text(text = "${video.posted} • 🌍", color = Color.Gray, fontSize = 11.sp)
                }
            }
            Text(text = video.title ?: "Sovereign Drop", color = Color.White, fontSize = 17.sp, fontWeight = FontWeight.ExtraBold, modifier = Modifier.padding(horizontal = 20.dp))
            Text(text = video.description ?: "", color = Color.LightGray, fontSize = 14.sp, modifier = Modifier.padding(horizontal = 20.dp, vertical = 8.dp))
            Box(modifier = Modifier.fillMaxWidth().height(450.dp).background(Color.Black), contentAlignment = Alignment.Center) {
                AsyncImage(model = video.thumbnailUrl?.takeIf { it.isNotBlank() } ?: "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1000", contentDescription = null, contentScale = ContentScale.Crop, modifier = Modifier.fillMaxSize())
                if (!video.videoUrl.isNullOrBlank()) {
                    AndroidView(factory = { PlayerView(context).apply { player = exoPlayer; useController = false; resizeMode = AspectRatioFrameLayout.RESIZE_MODE_ZOOM } }, modifier = Modifier.fillMaxSize())
                }
                Box(modifier = Modifier.align(Alignment.BottomEnd).padding(16.dp).background(Color.Black.copy(alpha = 0.7f), RoundedCornerShape(12.dp)).clickable { viewModel.narrateVideo(video) }.padding(horizontal = 10.dp, vertical = 8.dp)) {
                    Text(text = "AUDIO 🔊", color = GlowNeon, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                }
            }
            Row(modifier = Modifier.fillMaxWidth().padding(20.dp), horizontalArrangement = Arrangement.End, verticalAlignment = Alignment.CenterVertically) {
                IconButton(onClick = { viewModel.confirmGlobalStrike(video) }, modifier = Modifier.size(40.dp)) { Icon(imageVector = Icons.Default.AutoAwesome, contentDescription = "Deploy", tint = GlowNeon, modifier = Modifier.size(24.dp)) }
                Spacer(Modifier.width(16.dp))
                IconButton(onClick = { }, modifier = Modifier.size(40.dp)) { Icon(imageVector = Icons.Default.Share, contentDescription = null, tint = Color.Gray, modifier = Modifier.size(22.dp)) }
            }
        }
    }
}
