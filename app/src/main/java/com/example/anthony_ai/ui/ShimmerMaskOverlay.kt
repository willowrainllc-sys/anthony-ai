package com.example.anthony_ai.ui

import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color

@Composable
fun ShimmerMaskOverlay(isLoading: Boolean, content: @Composable () -> Unit) {
    if (!isLoading) {
        content()
        return
    }

    // Infinite transition for the shimmering light sweep effect
    val transition = rememberInfiniteTransition(label = "ShimmerTransition")
    val translateAnim = transition.animateFloat(
        initialValue = 0f,
        targetValue = 2000f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = 1500, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "ShimmerTranslate"
    )

    val shimmerColors = listOf(
        Color(0xFF00CCFF).copy(alpha = 0.1f),
        Color(0xFF00CCFF).copy(alpha = 0.6f),
        Color(0xFF00CCFF).copy(alpha = 0.1f)
    )

    val brush = Brush.linearGradient(
        colors = shimmerColors,
        start = Offset(x = translateAnim.value - 1000f, y = translateAnim.value - 1000f),
        end = Offset(x = translateAnim.value, y = translateAnim.value)
    )

    Box(modifier = Modifier.fillMaxSize()) {
        // Render the "paused" or frozen app frame underneath
        content()

        // Overlay the shimmering mask to seamlessly cover the background reload
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(brush)
        )
    }
}
