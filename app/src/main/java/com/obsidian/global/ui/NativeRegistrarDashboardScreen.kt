package com.obsidian.global.ui

import androidx.annotation.OptIn
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.media3.common.MediaItem
import androidx.media3.common.MimeTypes
import androidx.media3.common.Player
import androidx.media3.common.util.UnstableApi
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.ui.AspectRatioFrameLayout
import androidx.media3.ui.PlayerView
import com.obsidian.global.BannerAdView

@OptIn(UnstableApi::class)
@Composable
fun InlineLoopVideoPlayer(videoUrl: String, modifier: Modifier = Modifier) {
    val context = LocalContext.current
    val exoPlayer = remember(videoUrl) {
        ExoPlayer.Builder(context).build().apply {
            val mediaItem = MediaItem.Builder()
                .setUri(videoUrl)
                .setMimeType(MimeTypes.VIDEO_MP4)
                .build()
            setMediaItem(mediaItem)
            repeatMode = Player.REPEAT_MODE_ONE
            volume = 0f // Silent theme background loop
            prepare()
            playWhenReady = true
        }
    }

    DisposableEffect(exoPlayer) {
        onDispose {
            exoPlayer.release()
        }
    }

    AndroidView(
        factory = {
            PlayerView(context).apply {
                player = exoPlayer
                useController = false
                resizeMode = AspectRatioFrameLayout.RESIZE_MODE_ZOOM
                setBackgroundColor(android.graphics.Color.TRANSPARENT)
            }
        },
        modifier = modifier
    )
}

@Composable
fun NativeRegistrarDashboardScreen(
    onNavigateBrowser: (String) -> Unit
) {
    var searchQuery by remember { mutableStateOf("") }
    var selectedTab by remember { mutableIntStateOf(0) }
    val clipboardManager = LocalClipboardManager.current
    var copiedText by remember { mutableStateOf(false) }
    
    // FAQ expanded states map
    val faqExpanded = remember { mutableStateMapOf<Int, Boolean>() }

    val techVideos = listOf(
        "https://assets.mixkit.co/videos/preview/mixkit-futuristic-technology-background-loop-911-large.mp4",
        "https://player.vimeo.com/external/371728562.hd.mp4?s=447702f23cf5354900cb3e23630f9a5676a6b986&profile_id=170&oauth2_token_id=57447761"
    )

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFF020204))
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(bottom = 72.dp)
        ) {
            // Premium Cyber Top Navbar
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(Color(0xFF08080E))
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 20.dp, vertical = 18.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        Box(
                            modifier = Modifier
                                .size(10.dp)
                                .clip(RoundedCornerShape(50))
                                .background(Color(0xFF00FFCC))
                        )
                        Text(
                            text = "OBSIDIAN.CITY",
                            color = Color.White,
                            fontSize = 20.sp,
                            fontWeight = FontWeight.Black,
                            letterSpacing = 1.5.sp
                        )
                        Box(
                            modifier = Modifier
                                .background(Color(0xFF1E1E3F), RoundedCornerShape(4.dp))
                                .padding(horizontal = 6.dp, vertical = 2.dp)
                        ) {
                            Text("PRO BUILDER", color = Color(0xFF00FFCC), fontSize = 9.sp, fontWeight = FontWeight.Bold)
                        }
                    }
                    Row(horizontalArrangement = Arrangement.spacedBy(20.dp), verticalAlignment = Alignment.CenterVertically) {
                        Icon(
                            Icons.Default.ShoppingCart,
                            contentDescription = "Cart",
                            tint = Color(0xFF00FFCC),
                            modifier = Modifier
                                .size(24.dp)
                                .clickable { onNavigateBrowser("https://obsidian.city/obsidian_unified_checkout.html") }
                        )
                        Icon(
                            Icons.Default.Person,
                            contentDescription = "Account",
                            tint = Color.White,
                            modifier = Modifier
                                .size(24.dp)
                                .clickable { onNavigateBrowser("https://obsidian.city/obsidian_signin.html") }
                        )
                    }
                }
                Box(modifier = Modifier.fillMaxWidth().height(1.dp).background(Color(0xFF1E1E2F)))
            }

            // AdMob Header Banner
            BannerAdView(adUnitId = "ca-app-pub-9539640812310468/8547091855")

            // Main Content Area
            LazyColumn(
                modifier = Modifier
                    .fillMaxWidth()
                    .weight(1f),
                contentPadding = PaddingValues(16.dp),
                verticalArrangement = Arrangement.spacedBy(20.dp)
            ) {
                
                // 1. POPUP PROMO CARD: Welcome Discount Offer
                item {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(24.dp))
                            .background(Color(0xFF0B0E14))
                            .border(1.dp, Color(0xFF1A2333), RoundedCornerShape(24.dp))
                    ) {
                        Row(modifier = Modifier.fillMaxWidth().height(IntrinsicSize.Min)) {
                            // Video Background Left Banner Half
                            Box(
                                modifier = Modifier
                                    .weight(0.4f)
                                    .fillMaxHeight()
                                    .background(Color.Black)
                            ) {
                                InlineLoopVideoPlayer(
                                    videoUrl = techVideos[1],
                                    modifier = Modifier.fillMaxSize()
                                )
                                Box(
                                    modifier = Modifier
                                        .fillMaxSize()
                                        .background(
                                            Brush.horizontalGradient(
                                                colors = listOf(Color.Transparent, Color(0xFF0B0E14)),
                                                startX = 100f
                                            )
                                        )
                                )
                                Column(
                                    modifier = Modifier
                                        .fillMaxSize()
                                        .padding(12.dp),
                                    verticalArrangement = Arrangement.Bottom
                                ) {
                                    Text("STRAP IN.", color = Color.White, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                                    Text("LOOK OUT.", color = Color(0xFF00FFCC), fontSize = 14.sp, fontWeight = FontWeight.Black)
                                }
                            }
                            
                            // Promotional Right Content Half
                            Column(
                                modifier = Modifier
                                    .weight(0.6f)
                                    .padding(16.dp)
                            ) {
                                Row(
                                    verticalAlignment = Alignment.CenterVertically,
                                    horizontalArrangement = Arrangement.spacedBy(6.dp)
                                ) {
                                    Icon(Icons.Default.Star, contentDescription = null, tint = Color(0xFFFBBF24), modifier = Modifier.size(16.dp))
                                    Text("LAUNCH SPECS", color = Color(0xFF94A3B8), fontSize = 11.sp, fontWeight = FontWeight.Bold)
                                }
                                Spacer(modifier = Modifier.height(6.dp))
                                Text(
                                    text = "Your idea deserves an identity, launch your network domain for just $4.99.",
                                    color = Color.White,
                                    fontSize = 16.sp,
                                    fontWeight = FontWeight.Bold,
                                    lineHeight = 22.sp
                                )
                                Spacer(modifier = Modifier.height(14.dp))
                                
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .background(Color(0xFF161F30), RoundedCornerShape(12.dp))
                                        .padding(horizontal = 12.dp, vertical = 8.dp),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Text(
                                        text = "OBSIDIANWELCOME",
                                        color = Color.White,
                                        fontSize = 13.sp,
                                        fontFamily = FontFamily.Monospace
                                    )
                                    Button(
                                        onClick = {
                                            clipboardManager.setText(AnnotatedString("OBSIDIANWELCOME"))
                                            copiedText = true
                                        },
                                        colors = ButtonDefaults.buttonColors(containerColor = if (copiedText) Color(0xFF10B981) else Color.White),
                                        contentPadding = PaddingValues(horizontal = 10.dp, vertical = 4.dp),
                                        shape = RoundedCornerShape(8.dp),
                                        modifier = Modifier.height(28.dp)
                                    ) {
                                        Text(
                                            text = if (copiedText) "Copied!" else "Copy Code",
                                            color = if (copiedText) Color.White else Color.Black,
                                            fontSize = 11.sp,
                                            fontWeight = FontWeight.Bold
                                        )
                                    }
                                }
                                Spacer(modifier = Modifier.height(8.dp))
                                Text(
                                    text = "Valid for one .com, .net, .org, .co, or .tech domain. 1-year terms.",
                                    color = Color(0xFF64748B),
                                    fontSize = 10.sp
                                )
                            }
                        }
                    }
                }

                // 2. HERO CYBER DOMAIN SEARCH AREA
                item {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(24.dp))
                            .background(Color(0xFF0F0F1A))
                            .border(1.dp, Color(0xFF2563EB).copy(alpha = 0.3f), RoundedCornerShape(24.dp))
                            .padding(20.dp)
                    ) {
                        Column {
                            Box(
                                modifier = Modifier
                                    .background(Color(0xFF2563EB).copy(alpha = 0.2f), RoundedCornerShape(6.dp))
                                    .padding(horizontal = 8.dp, vertical = 4.dp)
                            ) {
                                Text("🔥 OBSIDIAN MESH REGISTRAR", color = Color(0xFF60A5FA), fontSize = 10.sp, fontWeight = FontWeight.Bold)
                            }
                            Spacer(modifier = Modifier.height(10.dp))
                            Text(
                                text = "Your domain unlocks everything, get a .com for just $0.01/1st yr",
                                color = Color.White,
                                fontSize = 24.sp,
                                fontWeight = FontWeight.Black,
                                lineHeight = 30.sp
                            )
                            Spacer(modifier = Modifier.height(6.dp))
                            Text(
                                text = "Save $23 when you lock in 3/yr terms. Includes advanced secure DNS configuration.",
                                color = Color(0xFF94A3B8),
                                fontSize = 12.sp
                            )
                            Spacer(modifier = Modifier.height(16.dp))
                            
                            OutlinedTextField(
                                value = searchQuery,
                                onValueChange = { searchQuery = it },
                                placeholder = { Text("Type the domain you want...", color = Color(0xFF4B5563)) },
                                singleLine = true,
                                leadingIcon = { Icon(Icons.Default.Search, contentDescription = null, tint = Color(0xFF60A5FA)) },
                                shape = RoundedCornerShape(16.dp),
                                colors = OutlinedTextFieldDefaults.colors(
                                    focusedBorderColor = Color(0xFF00FFCC),
                                    unfocusedBorderColor = Color(0xFF2B2B40),
                                    focusedContainerColor = Color(0xFF07070C),
                                    unfocusedContainerColor = Color(0xFF07070C),
                                    focusedTextColor = Color.White,
                                    unfocusedTextColor = Color.White
                                ),
                                modifier = Modifier.fillMaxWidth()
                            )
                            Spacer(modifier = Modifier.height(12.dp))
                            Button(
                                onClick = { onNavigateBrowser("https://obsidian.city/obsidian_domain_results.html?q=$searchQuery") },
                                shape = RoundedCornerShape(16.dp),
                                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2563EB)),
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .height(52.dp)
                            ) {
                                Row(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalAlignment = Alignment.CenterVertically) {
                                    Icon(Icons.Default.Done, contentDescription = null, tint = Color.White)
                                    Text("Find Your .com", fontSize = 15.sp, fontWeight = FontWeight.Bold)
                                }
                            }
                        }
                    }
                }

                // 3. FEATURE SECTION HEADER: Everything you need to grow online
                item {
                    Column(modifier = Modifier.padding(vertical = 4.dp)) {
                        Text(
                            text = "Everything you need to grow online",
                            color = Color.White,
                            fontSize = 20.sp,
                            fontWeight = FontWeight.Bold
                        )
                        Spacer(modifier = Modifier.height(4.dp))
                        Text(
                            text = "Industrial architecture tailored for extreme performance.",
                            color = Color(0xFF64748B),
                            fontSize = 12.sp
                        )
                    }
                }

                // GRID CARDS
                item {
                    Card(
                        shape = RoundedCornerShape(20.dp),
                        colors = CardDefaults.cardColors(containerColor = Color(0xFF0A0D14)),
                        modifier = Modifier
                            .fillMaxWidth()
                            .border(1.dp, Color(0xFF1E293B), RoundedCornerShape(20.dp))
                            .clickable { onNavigateBrowser("https://obsidian.city/obsidian_domains.html") }
                    ) {
                        Column(modifier = Modifier.padding(20.dp)) {
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Text("😎", fontSize = 28.sp)
                                Box(
                                    modifier = Modifier
                                        .background(Color(0xFF10B981).copy(alpha = 0.2f), RoundedCornerShape(4.dp))
                                        .padding(horizontal = 8.dp, vertical = 2.dp)
                                ) {
                                    Text("RECOMMENDED", color = Color(0xFF34D399), fontSize = 10.sp, fontWeight = FontWeight.Bold)
                                }
                            }
                            Spacer(modifier = Modifier.height(12.dp))
                            Text("Domains & Privacy", color = Color.White, fontSize = 18.sp, fontWeight = FontWeight.Bold)
                            Spacer(modifier = Modifier.height(4.dp))
                            Text(
                                text = "Get started with a .com domain, which comes with free lifetime domain privacy protection forever.",
                                color = Color(0xFF94A3B8),
                                fontSize = 12.sp,
                                lineHeight = 18.sp
                            )
                            Spacer(modifier = Modifier.height(12.dp))
                            Text("Domain Names →", color = Color(0xFF60A5FA), fontSize = 13.sp, fontWeight = FontWeight.Bold)
                        }
                    }
                }

                item {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(14.dp)
                    ) {
                        Card(
                            shape = RoundedCornerShape(20.dp),
                            colors = CardDefaults.cardColors(containerColor = Color(0xFF0F111A)),
                            modifier = Modifier
                                .weight(1f)
                                .border(1.dp, Color(0xFF1E293B), RoundedCornerShape(20.dp))
                                .clickable { onNavigateBrowser("https://obsidian.city/obsidian_hosting_landing.html") }
                        ) {
                            Column(modifier = Modifier.padding(16.dp)) {
                                Text("📧", fontSize = 24.sp)
                                Spacer(modifier = Modifier.height(8.dp))
                                Text("Email & M365", color = Color.White, fontSize = 14.sp, fontWeight = FontWeight.Bold)
                                Spacer(modifier = Modifier.height(4.dp))
                                Text("Match email to domain to build instant credibility.", color = Color(0xFF64748B), fontSize = 11.sp)
                                Spacer(modifier = Modifier.height(12.dp))
                                Text("Get Email", color = Color(0xFF60A5FA), fontSize = 12.sp, fontWeight = FontWeight.Bold)
                            }
                        }

                        Card(
                            shape = RoundedCornerShape(20.dp),
                            colors = CardDefaults.cardColors(containerColor = Color(0xFF0F111A)),
                            modifier = Modifier
                                .weight(1f)
                                .border(1.dp, Color(0xFF1E293B), RoundedCornerShape(20.dp))
                                .clickable { onNavigateBrowser("https://obsidian.city/anthony_ai_supremero_builder.html") }
                        ) {
                            Column(modifier = Modifier.padding(16.dp)) {
                                Row(horizontalArrangement = Arrangement.spacedBy(4.dp), verticalAlignment = Alignment.CenterVertically) {
                                    Text("🤖", fontSize = 24.sp)
                                    Box(
                                        modifier = Modifier.background(Color(0xFF3B82F6), RoundedCornerShape(4.dp)).padding(horizontal = 4.dp)
                                    ) {
                                        Text("FREE", color = Color.White, fontSize = 8.sp, fontWeight = FontWeight.Bold)
                                    }
                                }
                                Spacer(modifier = Modifier.height(8.dp))
                                Text("Obsidian AI Builder", color = Color.White, fontSize = 14.sp, fontWeight = FontWeight.Bold)
                                Spacer(modifier = Modifier.height(4.dp))
                                Text("Get your website up fast. Describe it, AI builds it.", color = Color(0xFF64748B), fontSize = 11.sp)
                                Spacer(modifier = Modifier.height(12.dp))
                                Text("Start Free", color = Color(0xFF60A5FA), fontSize = 12.sp, fontWeight = FontWeight.Bold)
                            }
                        }
                    }
                }

                // 4. LIVE TECH BACKGROUND VIDEO CONTAINER ROW
                item {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(180.dp)
                            .clip(RoundedCornerShape(24.dp))
                            .background(Color.Black)
                            .border(1.dp, Color(0xFF3B82F6), RoundedCornerShape(24.dp))
                    ) {
                        InlineLoopVideoPlayer(
                            videoUrl = techVideos[0],
                            modifier = Modifier.fillMaxSize()
                        )
                        // Gradient Overlay for readability
                        Box(
                            modifier = Modifier
                                .fillMaxSize()
                                .background(
                                    Brush.verticalGradient(
                                        colors = listOf(Color.Black.copy(alpha = 0.4f), Color.Black.copy(alpha = 0.85f))
                                    )
                                )
                        )
                        Column(
                            modifier = Modifier
                                .fillMaxSize()
                                .padding(16.dp),
                            verticalArrangement = Arrangement.SpaceBetween
                        ) {
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Box(
                                    modifier = Modifier
                                        .background(Color(0xFF00FFCC).copy(alpha = 0.2f), RoundedCornerShape(4.dp))
                                        .padding(horizontal = 8.dp, vertical = 2.dp)
                                ) {
                                    Text("VPN TUNNEL QUANTUM PULSE", color = Color(0xFF00FFCC), fontSize = 10.sp, fontWeight = FontWeight.Bold)
                                }
                                Icon(Icons.Default.Refresh, contentDescription = null, tint = Color.White, modifier = Modifier.size(16.dp))
                            }
                            
                            Column {
                                Text(
                                    text = "High-Security Web Infrastructure",
                                    color = Color.White,
                                    fontSize = 16.sp,
                                    fontWeight = FontWeight.Bold
                                )
                                Spacer(modifier = Modifier.height(4.dp))
                                Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                                    Text("Nodes: Active (8,429)", color = Color(0xFF94A3B8), fontSize = 11.sp)
                                    Text("Latency: 12ms", color = Color(0xFF34D399), fontSize = 11.sp, fontWeight = FontWeight.Bold)
                                    Text("Uptime: 99.99%", color = Color(0xFF60A5FA), fontSize = 11.sp)
                                }
                            }
                        }
                    }
                }

                // 5. TEMPLATES DESIGNED TO SELL SECTION
                item {
                    Column {
                        Text(
                            text = "Templates designed to sell",
                            color = Color.White,
                            fontSize = 18.sp,
                            fontWeight = FontWeight.Bold
                        )
                        Text(
                            text = "Choose from hundreds of premium high-performance industry layouts.",
                            color = Color(0xFF64748B),
                            fontSize = 12.sp,
                            modifier = Modifier.padding(bottom = 12.dp)
                        )
                        
                        LazyRow(
                            horizontalArrangement = Arrangement.spacedBy(14.dp),
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            val templates = listOf(
                                "Black Edge Portfolio" to "⚡ Minimalist Dev",
                                "Quantum Tech Systems" to "🛡️ VPN Registrar",
                                "Supreme AI Studio" to "🤖 Intelligent Agent"
                            )
                            items(templates) { (title, subtitle) ->
                                Box(
                                    modifier = Modifier
                                        .width(180.dp)
                                        .clip(RoundedCornerShape(16.dp))
                                        .background(Color(0xFF0E111A))
                                        .border(1.dp, Color(0xFF26293B), RoundedCornerShape(16.dp))
                                        .padding(14.dp)
                                ) {
                                    Column {
                                        Box(
                                            modifier = Modifier
                                                .fillMaxWidth()
                                                .height(90.dp)
                                                .clip(RoundedCornerShape(10.dp))
                                                .background(Color(0xFF1B2233)),
                                            contentAlignment = Alignment.Center
                                        ) {
                                            Text("👁️", fontSize = 28.sp)
                                        }
                                        Spacer(modifier = Modifier.height(8.dp))
                                        Text(title, color = Color.White, fontSize = 13.sp, fontWeight = FontWeight.Bold)
                                        Text(subtitle, color = Color(0xFF00FFCC), fontSize = 10.sp, fontWeight = FontWeight.SemiBold)
                                        Spacer(modifier = Modifier.height(10.dp))
                                        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                            Text(
                                                text = "Start Editing",
                                                color = Color(0xFF60A5FA),
                                                fontSize = 11.sp,
                                                fontWeight = FontWeight.Bold,
                                                modifier = Modifier.clickable { onNavigateBrowser("https://obsidian.city/anthony_ai_supremero_builder.html") }
                                            )
                                            Text(
                                                text = "Preview",
                                                color = Color(0xFF94A3B8),
                                                fontSize = 11.sp,
                                                modifier = Modifier.clickable { onNavigateBrowser("https://obsidian.city/anthony_ai_supremero_builder.html") }
                                            )
                                        }
                                    }
                                }
                            }
                        }
                    }
                }

                // 6. DEV SUPPORT BANNER WITH ACTUAL PHONE NUMBER
                item {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(20.dp))
                            .background(Color(0xFF0B1528))
                            .border(1.dp, Color(0xFF1E3A8A), RoundedCornerShape(20.dp))
                            .padding(20.dp)
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                            Text("👩‍💻", fontSize = 36.sp)
                            Column {
                                Text("Obsidian Guides & Expert Support", color = Color.White, fontSize = 15.sp, fontWeight = FontWeight.Bold)
                                Text("We love to help. Seriously. Call us anytime at:", color = Color(0xFF94A3B8), fontSize = 12.sp)
                                Spacer(modifier = Modifier.height(4.dp))
                                Text("1-480-366-3546", color = Color(0xFF00FFCC), fontSize = 16.sp, fontWeight = FontWeight.Black)
                            }
                        }
                    }
                }

                // 7. FREQUENTLY ASKED QUESTIONS (FAQ) DROPDOWNS
                item {
                    Column {
                        Text(
                            text = "Frequently Asked Questions",
                            color = Color.White,
                            fontSize = 18.sp,
                            fontWeight = FontWeight.Bold,
                            modifier = Modifier.padding(bottom = 12.dp)
                        )

                        val faqs = listOf(
                            "How does Obsidian help small business owners succeed?" to "We provide lightning fast decentralized domain registration, lifetime integrated free privacy protection, full autonomous AI layout builders, and advanced cloud nodes setup instantly without zero manual code requirements.",
                            "Why do I need a website for my business?" to "A secure cloud hosted app gives your entity global cryptographic presence, solidifies user identity parameters, and allows automated workflows or AI agents to complete checkout loops smoothly 24/7.",
                            "Why do I need a professional email?" to "Matching your identity domain address instantly boosts security confidence, passes corporate anti-spam firewalls seamlessly, and authenticates database keys accurately.",
                            "What makes Obsidian Web Hosting the world leader?" to "Every cluster operates with state-of-the-art localized memory backups, low latency endpoints, and full edge-node replication matrices.",
                            "What is Obsidian Payments and is it secure?" to "Our automated secure token payment infrastructure is fully operational, perfectly integrated with zero interruptions. Checkout systems are rigorously verified and highly functional."
                        )

                        faqs.forEachIndexed { index, (question, answer) ->
                            val expanded = faqExpanded[index] == true
                            Column(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .background(Color(0xFF070911))
                                    .padding(vertical = 4.dp)
                            ) {
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .clickable { faqExpanded[index] = !expanded }
                                        .padding(vertical = 12.dp, horizontal = 4.dp),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Text(
                                        text = question,
                                        color = Color.White,
                                        fontSize = 13.sp,
                                        fontWeight = FontWeight.SemiBold,
                                        modifier = Modifier.weight(0.9f)
                                    )
                                    Icon(
                                        imageVector = if (expanded) Icons.Default.KeyboardArrowUp else Icons.Default.KeyboardArrowDown,
                                        contentDescription = null,
                                        tint = Color(0xFF60A5FA)
                                    )
                                }
                                AnimatedVisibility(visible = expanded) {
                                    Text(
                                        text = answer,
                                        color = Color(0xFF94A3B8),
                                        fontSize = 12.sp,
                                        lineHeight = 18.sp,
                                        modifier = Modifier.padding(bottom = 12.dp, start = 4.dp, end = 4.dp)
                                    )
                                }
                                Divider(color = Color(0xFF1E293B), modifier = Modifier.fillMaxWidth())
                            }
                        }
                    }
                }
            }
        }

        // High-Tech Bottom Sticky Navigation Bar
        Surface(
            color = Color(0xFF08080E),
            shadowElevation = 16.dp,
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .fillMaxWidth()
                .height(72.dp)
        ) {
            Column {
                Box(modifier = Modifier.fillMaxWidth().height(1.dp).background(Color(0xFF1E1E2F)))
                Row(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(horizontal = 16.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    val navItems = listOf(
                        Triple(Icons.Default.Home, "Home", 0),
                        Triple(Icons.Default.Search, "Domains", 1),
                        Triple(Icons.Default.ShoppingCart, "Basket", 2),
                        Triple(Icons.Default.Person, "Account", 3),
                        Triple(Icons.Default.Dashboard, "Admin", 4)
                    )

                    navItems.forEach { (icon, label, index) ->
                        val isSelected = selectedTab == index
                        Column(
                            horizontalAlignment = Alignment.CenterHorizontally,
                            modifier = Modifier
                                .weight(1f)
                                .clickable { 
                                    selectedTab = index
                                    when (index) {
                                        1 -> onNavigateBrowser("https://obsidian.city/obsidian_domains.html")
                                        2 -> onNavigateBrowser("https://obsidian.city/obsidian_unified_checkout.html")
                                        3 -> onNavigateBrowser("https://obsidian.city/obsidian_signin.html")
                                        4 -> onNavigateBrowser("https://obsidian.city/obsidian_city_dashboard.html")
                                    }
                                }
                        ) {
                            Icon(
                                imageVector = icon,
                                contentDescription = label,
                                tint = if (isSelected) Color(0xFF00FFCC) else if (index == 4) Color(0xFFFBBF24) else Color(0xFF64748B),
                                modifier = Modifier.size(if (index == 4) 24.dp else 20.dp)
                            )
                            Spacer(modifier = Modifier.height(3.dp))
                            Text(
                                text = label,
                                color = if (isSelected) Color(0xFF00FFCC) else if (index == 4) Color(0xFFFBBF24) else Color(0xFF64748B),
                                fontSize = 9.sp,
                                fontWeight = FontWeight.Bold
                            )
                        }
                    }
                }
            }
        }
    }
}
