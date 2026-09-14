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
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.obsidian.global.MainViewModel
import com.obsidian.global.ui.theme.*

@Composable
fun NativeAIStudioScreen(
    onBack: () -> Unit
) {
    val viewModel: MainViewModel = viewModel()
    var prompt by remember { mutableStateOf("") }
    val logs = remember { mutableStateListOf("> ARES IDE v1.0 INITIALIZED", "> System Ready for Mission...") }

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
                Row(verticalAlignment = Alignment.CenterVertically) {
                    IconButton(onClick = onBack) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back", tint = Color.White)
                    }
                    Text(
                        "AI STUDIO",
                        color = Color.White,
                        fontSize = 18.sp,
                        fontWeight = FontWeight.Black,
                        letterSpacing = 2.sp
                    )
                }
                Text(
                    "v29.0 SUPREME",
                    color = CityEmerald,
                    fontSize = 10.sp,
                    fontWeight = FontWeight.Bold
                )
            }

            // Virtual Editor Area
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .weight(1f)
                    .padding(horizontal = 16.dp),
                colors = CardDefaults.cardColors(containerColor = Color(0xFF0F0F17)),
                shape = RoundedCornerShape(20.dp),
                border = CardDefaults.outlinedCardBorder().copy(brush = SolidColor(Color.White.copy(0.05f)))
            ) {
                Column(modifier = Modifier.fillMaxSize()) {
                    // Tab Bar
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .background(Color.Black.copy(0.3f))
                            .padding(8.dp)
                    ) {
                        Surface(
                            color = Color(0xFF1E1E1E),
                            shape = RoundedCornerShape(4.dp),
                            modifier = Modifier.padding(end = 4.dp)
                        ) {
                            Text(
                                "synthesis_node.py",
                                color = Color.White,
                                fontSize = 10.sp,
                                modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp)
                            )
                        }
                        Text(
                            "visual_dna.css",
                            color = Color.Gray,
                            fontSize = 10.sp,
                            modifier = Modifier.padding(start = 8.dp, top = 6.dp)
                        )
                    }
                    
                    // Code Content (Terminal/Editor Hybrid)
                    LazyColumn(
                        modifier = Modifier
                            .fillMaxSize()
                            .padding(16.dp),
                        verticalArrangement = Arrangement.spacedBy(4.dp)
                    ) {
                        item {
                            Text(
                                text = "> [ARES] SECURING INGRESS PORT 8080...",
                                color = CityBlue,
                                fontSize = 11.sp,
                                fontFamily = FontFamily.Monospace
                            )
                        }
                        items(logs) { log ->
                            Text(
                                text = log,
                                color = if (log.startsWith(">")) CityBlue else if (log.startsWith("✓") || log.startsWith("[+]")) CityEmerald else Color.Gray,
                                fontSize = 11.sp,
                                fontFamily = FontFamily.Monospace,
                                fontWeight = FontWeight.Medium
                            )
                        }
                    }
                }
            }

            // High-Aura Blueprint Chooser (Simplified for Mobile)
            if (logs.size > 2 && logs.any { it.contains("Directing") }) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp),
                    horizontalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    val blueprints = listOf("MINIMAL", "GLASS", "INDUSTRIAL")
                    blueprints.forEach { name ->
                        Button(
                            onClick = { 
                                logs.add("> BLUEPRINT [$name] SELECTED.")
                                logs.add("> DISPATCHING FULL-STACK SYNTHESIS...")
                                logs.add("[+] THRONE SECURED AT THE EDGE.")
                            },
                            modifier = Modifier.weight(1f),
                            colors = ButtonDefaults.buttonColors(containerColor = Color.White.copy(0.05f)),
                            shape = RoundedCornerShape(12.dp)
                        ) {
                            Text(name, fontSize = 9.sp, fontWeight = FontWeight.Black)
                        }
                    }
                }
            }

            // Command Ingress
            Surface(
                color = Color(0xFF0A0A0F),
                tonalElevation = 8.dp,
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(
                    modifier = Modifier
                        .padding(16.dp)
                        .navigationBarsPadding()
                        .imePadding()
                ) {
                    Text(
                        "MISSION PARAMETERS",
                        color = Color.Gray,
                        fontSize = 9.sp,
                        fontWeight = FontWeight.Black,
                        letterSpacing = 1.sp,
                        modifier = Modifier.padding(bottom = 8.dp)
                    )
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        TextField(
                            value = prompt,
                            onValueChange = { prompt = it },
                            placeholder = { Text("Describe your vision...", color = Color.DarkGray, fontSize = 13.sp) },
                            modifier = Modifier.weight(1f),
                            colors = TextFieldDefaults.colors(
                                focusedContainerColor = Color.Transparent,
                                unfocusedContainerColor = Color.Transparent,
                                focusedTextColor = Color.White,
                                unfocusedTextColor = Color.White,
                                cursorColor = CityBlue
                            )
                        )
                        Button(
                            onClick = {
                                if (prompt.isNotBlank()) {
                                    logs.add("> Ingress: \"$prompt\"")
                                    logs.add("> Directing ARES to synthesize visual DNA...")
                                    prompt = ""
                                }
                            },
                            shape = RoundedCornerShape(12.dp),
                            colors = ButtonDefaults.buttonColors(containerColor = CityBlue)
                        ) {
                            Text("IGNITE", fontSize = 11.sp, fontWeight = FontWeight.Black)
                        }
                    }
                }
            }
        }
    }
}
