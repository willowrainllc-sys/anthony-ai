package com.example.anthony_ai.ui.theme

import androidx.compose.foundation.border
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Paint
import androidx.compose.ui.graphics.drawscope.drawIntoCanvas
import androidx.compose.ui.graphics.nativeCanvas
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp

import androidx.compose.ui.geometry.Offset
import androidx.compose.animation.core.*
import androidx.compose.ui.graphics.Brush

// Obsidian & Glow Theme Colors
val ObsidianBlack = Color(0xFF080808)
val ObsidianGray = Color(0xFF121212)
val GlowNeon = Color(0xFFB6FF00) // Lime Neon
val GlowCyan = Color(0xFF00FFFF)
val GlowPurple = Color(0xFFBF40BF)

@Composable
fun shimmerBrush(
    targetValue: Float = 1300f,
    showShimmer: Boolean = true
): Brush {
    return if (showShimmer) {
        val shimmerColors = listOf(
            GlowCyan.copy(alpha = 0.1f),
            Color.White.copy(alpha = 0.5f),
            GlowCyan.copy(alpha = 0.1f),
        )

        val transition = rememberInfiniteTransition(label = "shimmer")
        val translateAnimation = transition.animateFloat(
            initialValue = 0f,
            targetValue = targetValue,
            animationSpec = infiniteRepeatable(
                animation = tween(800, easing = LinearEasing), // Faster shimmer
                repeatMode = RepeatMode.Restart
            ),
            label = "shimmer"
        )

        Brush.linearGradient(
            colors = shimmerColors,
            start = Offset.Zero,
            end = Offset(x = translateAnimation.value, y = translateAnimation.value)
        )
    } else {
        Brush.linearGradient(
            colors = listOf(Color.Transparent, Color.Transparent),
            start = Offset.Zero,
            end = Offset.Zero
        )
    }
}

@Composable
fun Modifier.shimmerGlowBorder(
    color: Color = GlowCyan,
    width: Dp = 1.5.dp,
    cornerRadius: Dp = 16.dp,
    glowRadius: Dp = 8.dp
): Modifier = this.drawBehind {
    val paint = Paint().asFrameworkPaint().apply {
        this.color = color.copy(alpha = 0.5f).toArgb()
        this.maskFilter = android.graphics.BlurMaskFilter(glowRadius.toPx(), android.graphics.BlurMaskFilter.Blur.OUTER)
    }
    
    drawIntoCanvas { canvas ->
        canvas.nativeCanvas.drawRoundRect(
            0f, 0f, size.width, size.height,
            cornerRadius.toPx(), cornerRadius.toPx(),
            paint
        )
    }
}.border(width, shimmerBrush(targetValue = 2000f), RoundedCornerShape(cornerRadius))

fun Modifier.glowBorder(
    color: Color = GlowNeon,
    width: Dp = 1.dp,
    cornerRadius: Dp = 16.dp,
    glowRadius: Dp = 6.dp,
    alpha: Float = 0.6f
): Modifier = this.drawBehind {
    val paint = Paint().asFrameworkPaint().apply {
        this.color = color.copy(alpha = alpha).toArgb()
        this.maskFilter = android.graphics.BlurMaskFilter(glowRadius.toPx(), android.graphics.BlurMaskFilter.Blur.OUTER)
    }
    
    drawIntoCanvas { canvas ->
        canvas.nativeCanvas.drawRoundRect(
            0f, 0f, size.width, size.height,
            cornerRadius.toPx(), cornerRadius.toPx(),
            paint
        )
    }
}.border(width, color.copy(alpha = 0.3f), RoundedCornerShape(cornerRadius))

@Composable
fun Modifier.obsidianGlass(
    cornerRadius: Dp = 16.dp,
    glowColor: Color = GlowNeon
): Modifier = this
    .glowBorder(color = glowColor, cornerRadius = cornerRadius)
    .drawBehind {
        drawRect(
            color = ObsidianBlack.copy(alpha = 0.8f),
            size = size
        )
    }
