package com.obsidian.global.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.*
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.delay
import java.text.SimpleDateFormat
import java.util.*

/**
 * CLOAKED CLOCK:
 * The ultimate stealth ingress for the Pixel Backend.
 * 1. DECOY UI: Displays a standard Android digital clock.
 * 2. GHOST TRIGGER: Long-press the ":" to unlock the Supreme Command OS.
 * 3. DIRECTOR BYPASS: Triple-tap the battery icon to skip login.
 * 4. BACKGROUND SYNC: Keeps the Autopilot Service running invisibly.
 */
@Suppress("unused")
@Composable
fun CloakedClockScreen(
    onUnlock: () -> Unit,
    onDirectorBypass: () -> Unit
) {
    var currentTime by remember { mutableStateOf(Calendar.getInstance().time) }
    
    LaunchedEffect(Unit) {
        while (true) {
            currentTime = Calendar.getInstance().time
            delay(1000L)
        }
    }

    val timeFormat = SimpleDateFormat("HH:mm", Locale.getDefault())
    val dateFormat = SimpleDateFormat("EEEE, MMMM d", Locale.getDefault())
    
    val formattedTime = timeFormat.format(currentTime)
    val formattedDate = dateFormat.format(currentTime)

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.Black),
        contentAlignment = Alignment.Center
    ) {
        Column(
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            // The Date Decoy
            Text(
                text = formattedDate,
                color = Color.LightGray,
                fontSize = 18.sp,
                fontWeight = FontWeight.Medium
            )
            
            Spacer(modifier = Modifier.height(8.dp))

            // The Time Decoy (Ghost Trigger)
            Row(verticalAlignment = Alignment.CenterVertically) {
                val parts = formattedTime.split(":")
                
                Text(
                    text = parts[0],
                    color = Color.White,
                    fontSize = 110.sp,
                    fontWeight = FontWeight.Light,
                    fontFamily = FontFamily.SansSerif
                )
                
                // The Secret Gate: Long press this colon
                Text(
                    text = ":",
                    color = Color.White,
                    fontSize = 100.sp,
                    fontWeight = FontWeight.Light,
                    modifier = Modifier
                        .padding(horizontal = 4.dp)
                        .pointerInput(Unit) {
                            detectTapGestures(
                                onLongPress = {
                                    onUnlock()
                                }
                            )
                        }
                )
                
                Text(
                    text = parts[1],
                    color = Color.White,
                    fontSize = 110.sp,
                    fontWeight = FontWeight.Light,
                    fontFamily = FontFamily.SansSerif
                )
            }
        }
        
        // Stealth Battery Indicator (Director Bypass Trigger)
        Text(
            text = "⚡ 100%",
            color = Color(0xFF333333),
            fontSize = 12.sp,
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .padding(bottom = 40.dp)
                .pointerInput(Unit) {
                    detectTapGestures(
                        onTap = {
                            // Can be used for hidden metrics or further triggers
                        },
                        onDoubleTap = {
                            // Secret Admin Bypass
                            onDirectorBypass()
                        }
                    )
                }
        )
    }
}
