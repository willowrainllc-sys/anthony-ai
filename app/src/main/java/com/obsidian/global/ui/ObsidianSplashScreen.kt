package com.obsidian.global.ui

import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.scale
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.delay

@Composable
fun ObsidianSplashScreen(onFinish: () -> Unit) {
    val infiniteTransition = rememberInfiniteTransition(label = "SplashTransition")
    
    val scale by infiniteTransition.animateFloat(
        initialValue = 0.8f,
        targetValue = 1.1f,
        animationSpec = infiniteRepeatable(
            animation = tween(2000, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "ScaleAnimation"
    )
    
    val alpha by infiniteTransition.animateFloat(
        initialValue = 0.3f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(2000, easing = LinearEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "AlphaAnimation"
    )

    LaunchedEffect(Unit) {
        delay(3500) // Show for 3.5 seconds
        onFinish()
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFF050505)),
        contentAlignment = Alignment.Center
    ) {
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            Text(
                text = "🔱",
                fontSize = 80.sp,
                modifier = Modifier
                    .scale(scale)
                    .alpha(alpha)
            )
            
            Spacer(modifier = Modifier.height(24.dp))
            
            Text(
                text = "OBSIDIAN GLOBAL",
                color = Color.White,
                fontSize = 20.sp,
                fontWeight = FontWeight.Bold,
                letterSpacing = 4.sp
            )
            
            Text(
                text = "SUPREME COMMAND OS",
                color = Color.Gray,
                fontSize = 12.sp,
                letterSpacing = 2.sp,
                modifier = Modifier.padding(top = 8.dp)
            )
            
            Spacer(modifier = Modifier.height(48.dp))
            
            Text(
                text = "ENTANGLING KERNELS...",
                color = Color(0xFF3b82f6),
                fontSize = 10.sp,
                fontWeight = FontWeight.Bold,
                modifier = Modifier.alpha(alpha)
            )
        }
    }
}
