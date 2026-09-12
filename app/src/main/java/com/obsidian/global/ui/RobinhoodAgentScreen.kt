package com.obsidian.global.ui

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.delay

@Suppress("unused")
@Composable
fun RobinhoodAgentScreen() {
    var isConnected by remember { mutableStateOf(false) }
    var isConnecting by remember { mutableStateOf(false) }
    var humanApprovalThreshold by remember { mutableFloatStateOf(50.00f) }

    Box(modifier = Modifier.fillMaxSize()) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .background(Color(0xFF0F172A))
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            // Header
            Text(
                text = "Robinhood MCP Agent",
                color = Color.White,
                fontSize = 24.sp,
                fontWeight = FontWeight.Bold,
                modifier = Modifier.padding(top = 24.dp, bottom = 8.dp)
            )

            Text(
                text = "AI Agentic Trading Sandbox",
                color = Color.Gray,
                fontSize = 14.sp,
                modifier = Modifier.padding(bottom = 32.dp)
            )

            // Status Card
            Card(
                modifier = Modifier.fillMaxWidth(),
                colors = CardDefaults.cardColors(containerColor = Color(0xFF1E293B)),
                shape = RoundedCornerShape(12.dp)
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text("Connection Status", color = Color.LightGray, fontSize = 12.sp)
                    Spacer(modifier = Modifier.height(4.dp))
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Box(
                            modifier = Modifier
                                .size(10.dp)
                                .background(
                                    color = if (isConnected) Color(0xFF10B981) else Color(0xFFEF4444),
                                    shape = RoundedCornerShape(50)
                                )
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(
                            text = if (isConnected) "CONNECTED" else "DISCONNECTED",
                            color = Color.White,
                            fontWeight = FontWeight.SemiBold
                        )
                    }
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            // Safety Guards Card
            Card(
                modifier = Modifier.fillMaxWidth(),
                colors = CardDefaults.cardColors(containerColor = Color(0xFF1E293B)),
                shape = RoundedCornerShape(12.dp)
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text(
                        text = "Safety Guards",
                        color = Color.White,
                        fontWeight = FontWeight.Bold,
                        modifier = Modifier.padding(bottom = 8.dp)
                    )

                    Text(
                        text = "Restricted Accounts: Main, IRA, Crypto",
                        color = Color.Gray,
                        fontSize = 14.sp
                    )

                    Spacer(modifier = Modifier.height(16.dp))
                    
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text("Approval Threshold", color = Color.LightGray, fontSize = 14.sp)
                        Text(
                            text = "$${"%.2f".format(humanApprovalThreshold)}",
                            color = Color.White,
                            fontWeight = FontWeight.Bold
                        )
                    }

                    Slider(
                        value = humanApprovalThreshold,
                        onValueChange = { humanApprovalThreshold = it },
                        valueRange = 0f..500f,
                        colors = SliderDefaults.colors(
                            thumbColor = Color(0xFF3B82F6),
                            activeTrackColor = Color(0xFF3B82F6)
                        ),
                        modifier = Modifier.padding(vertical = 8.dp)
                    )
                }
            }

            Spacer(modifier = Modifier.weight(1f))

            // Actions
            Button(
                onClick = { 
                    if (!isConnected) {
                        isConnecting = true
                    } else {
                        isConnected = false
                    }
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(50.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = if (isConnected) Color(0xFFEF4444) else Color(0xFF3B82F6)
                ),
                shape = RoundedCornerShape(8.dp)
            ) {
                Text(
                    text = if (isConnected) "REVOKE ACCESS (KILL SWITCH)" else "CONNECT VIA MCP",
                    fontWeight = FontWeight.Bold
                )
            }
            
            Spacer(modifier = Modifier.height(24.dp))
        }

        // Connecting Splash Overlay
        AnimatedVisibility(
            visible = isConnecting,
            enter = fadeIn(),
            exit = fadeOut()
        ) {
            LaunchedEffect(isConnecting) {
                if (isConnecting) {
                    delay(3000)
                    isConnected = true
                    isConnecting = false
                }
            }

            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(Color(0xFF0F172A).copy(alpha = 0.95f)),
                contentAlignment = Alignment.Center
            ) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    CircularProgressIndicator(color = Color(0xFF3B82F6))
                    Spacer(modifier = Modifier.height(24.dp))
                    Text(
                        text = "ESTABLISHING MCP BRIDGE...",
                        color = Color.White,
                        fontSize = 14.sp,
                        fontWeight = FontWeight.Bold,
                        letterSpacing = 2.sp
                    )
                    Text(
                        text = "Authenticating with Robinhood Server",
                        color = Color.Gray,
                        fontSize = 12.sp,
                        modifier = Modifier.padding(top = 8.dp)
                    )
                }
            }
        }
    }
}
