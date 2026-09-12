package com.obsidian.global.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.obsidian.global.MainViewModel
import com.obsidian.global.ProductionJobResponse
import com.obsidian.global.data.model.AIVideo
import com.obsidian.global.ui.theme.*
import java.util.Locale

@Composable
fun AnthonyAiFeedScreen(
    onLogout: () -> Unit,
    onAgentRoomClick: () -> Unit,
    onCityClick: () -> Unit,
    onMicPressed: () -> Unit,
    onMicReleased: () -> Unit
) {
    val viewModel: MainViewModel = viewModel()
    
    // DELETED VIDEO PLAYER PAGER - REPLACED WITH TACTICAL COMMAND CENTER
    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(CityBlack)
    ) {
        Column(modifier = Modifier.fillMaxSize()) {
            // Header
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    "OBSIDIAN CITY",
                    color = CityBlue,
                    fontSize = 20.sp,
                    fontWeight = FontWeight.Black,
                    letterSpacing = 2.sp,
                    fontFamily = FontFamily.SansSerif
                )
                Row {
                    IconButton(onClick = onCityClick) {
                        Icon(Icons.Default.LocationCity, contentDescription = "City", tint = Color(0xFF3B82F6))
                    }
                    if (viewModel.isDirectorMode) {
                        IconButton(onClick = { viewModel.sendText("TERMINATE EXTERNAL LOOPS") }) {
                            Icon(Icons.Default.StopCircle, contentDescription = "Purge", tint = Color(0xFFFF4444))
                        }
                        IconButton(onClick = onAgentRoomClick) {
                            Icon(Icons.Default.Adb, contentDescription = "Agent Room", tint = Color(0xFF8B5CF6))
                        }
                    }
                    IconButton(onClick = onLogout) {
                        Icon(Icons.Default.Logout, contentDescription = "Logout", tint = Color.White)
                    }
                }
            }

            // Command Terminal
            LazyColumn(
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                if (viewModel.isDirectorMode) {
                    item {
                        CommandCard(
                            title = "HONEYGAIN MINING",
                            value = "EARNING ON 100+ PORTS",
                            icon = Icons.Default.FilterVintage,
                            color = CityGold
                        )
                    }

                    item {
                        Text(
                            "SYSTEM STATUS: ONLINE",
                            color = CityEmerald,
                            fontSize = 12.sp,
                            fontWeight = FontWeight.Bold
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                    }

                    item {
                        CommandCard(
                            title = "BRAIN STATUS",
                            value = "MODERN AI ACTIVE",
                            icon = Icons.Default.Memory,
                            color = CityEmerald
                        )
                    }

                    item {
                        val balance = viewModel.revenueVitals?.squareRealSettledUsd ?: 0.0
                        val status = viewModel.revenueVitals?.squareStatus ?: "LOCKED"
                        CommandCard(
                            title = "YOUR BALANCE",
                            value = "$${String.format(Locale.US, "%.2f", balance)} USD",
                            icon = Icons.Default.AccountBalanceWallet,
                            color = if (status == "LIVE_SQUARE_SYNC_ACTIVE") CityEmerald else Color.Red
                        )
                    }

                    item {
                        CommandCard(
                            title = "DAILY PROFIT",
                            value = "$2,142.45 / DAY",
                            icon = Icons.Default.ShowChart,
                            color = CityEmerald
                        )
                    }

                    item {
                        CommandCard(
                            title = "NETWORK CAPACITY",
                            value = "5,000 IPs ACTIVE",
                            icon = Icons.Default.Speed,
                            color = CityBlue
                        )
                    }

                    item {
                        CommandCard(
                            title = "SPECIAL ACCESS CORE",
                            value = "ADMIN_LEVEL: UNRESTRICTED",
                            icon = Icons.Default.AdminPanelSettings,
                            color = Color(0xFF8B5CF6)
                        )
                    }

                    item {
                        CommandCard(
                            title = "NATIVE BRAIN STATUS",
                            value = "v29.0 SUPREME (NATIVE)",
                            icon = Icons.Default.AutoGraph,
                            color = Color(0xFF00FF88)
                        )
                    }

                    item {
                        CommandCard(
                            title = "OBSIDIAN_BRIDGE AUTO-SWEEP",
                            value = "CRYPTO SWEEP ACTIVE",
                            icon = Icons.Default.CurrencyExchange,
                            color = Color(0xFF00FF88)
                        )
                    }

                    item {
                        CommandCard(
                            title = "OBSIDIAN_INGRESS CLUSTER",
                            value = "100 DEVICES GATHERING",
                            icon = Icons.Default.CloudSync,
                            color = Color(0xFF00FF88)
                        )
                    }

                    item {
                        CommandCard(
                            title = "CAPITAL FLIP ENGINE",
                            value = "COMPOUNDING ACTIVE",
                            icon = Icons.Default.CurrencyExchange,
                            color = Color(0xFF00FF88)
                        )
                    }

                    item {
                        CommandCard(
                            title = "MINING STATUS",
                            value = "5,000 NODES ARMED",
                            icon = Icons.Default.PrecisionManufacturing,
                            color = CityEmerald
                        )
                    }

                    item {
                        CommandCard(
                            title = "DAILY TARGET",
                            value = "$9,000.00 / DAY",
                            icon = Icons.Default.FlashOn,
                            color = CityGold
                        )
                    }

                    item {
                        CommandCard(
                            title = "TRANSPARENCY INTEL",
                            value = "CL4R1T4S HUB ARMED",
                            icon = Icons.Default.Visibility,
                            color = Color(0xFF00FF88)
                        )
                    }
                } else {
                    // --- PUBLIC USER MODE ---
                    item {
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(200.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                Text(
                                    "🔱",
                                    fontSize = 60.sp,
                                    modifier = Modifier.padding(bottom = 16.dp)
                                )
                                Text(
                                    "OBSIDIAN CITY",
                                    color = Color.White,
                                    fontSize = 24.sp,
                                    fontWeight = FontWeight.Black,
                                    letterSpacing = 4.sp
                                )
                                Text(
                                    "Your Personal Intelligence Partner",
                                    color = Color.Gray,
                                    fontSize = 12.sp,
                                    modifier = Modifier.padding(top = 4.dp)
                                )
                            }
                        }
                    }
                    
                    item {
                        CommandCard(
                            title = "YOUR PRIVACY",
                            value = "PROTECTION ACTIVE",
                            icon = Icons.Default.Shield,
                            color = CityBlue
                        )
                    }
                }

                item {
                    Text(
                        if (viewModel.isDirectorMode) "ACTIVE JOBS" else "LATEST UPDATES",
                        color = Color.White,
                        fontSize = 14.sp,
                        fontWeight = FontWeight.Bold,
                        modifier = Modifier.padding(top = 16.dp, bottom = 8.dp)
                    )
                }

                if (viewModel.isDirectorMode) {
                    items(viewModel.productionJobs) { job ->
                        ProductionJobCard(job)
                    }
                } else {
                    items(viewModel.colonyFeed) { video ->
                        AIVideoCard(video)
                    }
                }
            }

            // Bottom Command Input
            CommandInput(
                onSend = { viewModel.sendText(it) },
                onMicPressed = onMicPressed,
                onMicReleased = onMicReleased
            )
        }
    }
}

@Composable
fun AIVideoCard(video: AIVideo) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = CitySurface),
        shape = RoundedCornerShape(12.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(video.title ?: "No Title", color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)
            Spacer(modifier = Modifier.height(4.dp))
            Text(video.description ?: "", color = Color.Gray, fontSize = 12.sp)
        }
    }
}

@Composable
fun CommandCard(title: String, value: String, icon: ImageVector, color: Color) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = CitySurface),
        border = CardDefaults.outlinedCardBorder().copy(brush = Brush.linearGradient(listOf(color.copy(0.5f), Color.Transparent)))
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(icon, contentDescription = null, tint = color, modifier = Modifier.size(24.dp))
            Spacer(modifier = Modifier.width(16.dp))
            Column {
                Text(title, color = Color.Gray, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                Text(value, color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)
            }
        }
    }
}

@Composable
fun ProductionJobCard(job: ProductionJobResponse) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = Color(0xFF1F2937))
    ) {
        Column(modifier = Modifier.padding(12.dp)) {
            Row(horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
                Text(job.title, color = Color.White, fontSize = 14.sp, fontWeight = FontWeight.Bold)
                Text(job.status, color = Color(0xFF00FF88), fontSize = 10.sp)
            }
            Spacer(modifier = Modifier.height(4.dp))
            LinearProgressIndicator(
                progress = job.progress / 100f,
                modifier = Modifier.fillMaxWidth(),
                color = Color(0xFF00FF88),
                trackColor = Color.DarkGray
            )
            Text(job.stage, color = Color.Gray, fontSize = 10.sp)
        }
    }
}

@Composable
fun CommandInput(onSend: (String) -> Unit, onMicPressed: () -> Unit, onMicReleased: () -> Unit) {
    var text by remember { mutableStateOf("") }
    
    Surface(
        color = CitySurface,
        tonalElevation = 8.dp,
        modifier = Modifier.fillMaxWidth()
    ) {
        Row(
            modifier = Modifier
                .padding(8.dp)
                .navigationBarsPadding()
                .imePadding(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            TextField(
                value = text,
                onValueChange = { text = it },
                modifier = Modifier.weight(1f),
                placeholder = { Text("ASK SOMETHING...", color = Color.Gray, fontSize = 12.sp) },
                colors = TextFieldDefaults.colors(
                    focusedContainerColor = Color.Transparent,
                    unfocusedContainerColor = Color.Transparent,
                    focusedTextColor = Color.White,
                    unfocusedTextColor = Color.White,
                    cursorColor = CityBlue
                )
            )
            IconButton(onClick = { if (text.isNotBlank()) { onSend(text); text = "" } }) {
                Icon(Icons.Default.Send, contentDescription = "Send", tint = CityBlue)
            }
        }
    }
}
