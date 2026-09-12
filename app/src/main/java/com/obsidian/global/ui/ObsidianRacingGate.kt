package com.obsidian.global.ui

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.delay
import kotlin.random.Random

data class RacingCar(
    val name: String,
    val color: Color,
    var position: Float = 0f,
    val speed: Float,
    var finished: Boolean = false,
    var finishOrder: Int = 0,
)

/**
 * 🏎️ OBSIDIAN RACING GATE:
 * The ultimate safety protocol for the Nest-phone browser.
 * 1. DECOY GAME: 2D 8-bit Nintendo style racing.
 * 2. THE RULE: The Director (White Ghost) MUST finish last.
 * 3. INGRESS: Only opens the Phone Hive if the "Finish Last" condition is met.
 */
@Composable
fun ObsidianRacingGate(
    onRaceFinished: () -> Unit,
    onReset: () -> Unit
) {
    var gameStarted by remember { mutableStateOf(value = false) }
    var gameFinished by remember { mutableStateOf(value = false) }
    var finishCount by remember { mutableIntStateOf(0) }
    
    val cars = remember {
        mutableStateListOf(
            RacingCar("LILY", Color(0xFFFF69B4), speed = 0.015f + (Random.nextFloat() * 0.01f)),
            RacingCar("SHAE", Color(0xFF3B82F6), speed = 0.015f + (Random.nextFloat() * 0.01f)),
            RacingCar("JESS", Color(0xFFEF4444), speed = 0.015f + (Random.nextFloat() * 0.01f)),
            RacingCar("RAINA", Color(0xFFA855F7), speed = 0.015f + (Random.nextFloat() * 0.01f)),
            RacingCar("LEO", Color(0xFFEAB308), speed = 0.015f + (Random.nextFloat() * 0.01f)),
            RacingCar("WILLOW", Color(0xFF22C55E), speed = 0.015f + (Random.nextFloat() * 0.01f)),
            RacingCar("JESSE", Color(0xFFFFA500), speed = 0.015f + (Random.nextFloat() * 0.01f)),
            RacingCar("SHEA", Color(0xFF00FFFF), speed = 0.015f + (Random.nextFloat() * 0.01f)),
            RacingCar("ANTHONY", Color.White, speed = 0.01f), // The Ghost Car is slower by default
        )
    }

    LaunchedEffect(gameStarted) {
        if (gameStarted) {
            while (finishCount < cars.size) {
                delay(timeMillis = 50L)
                cars.forEach { car ->
                    if (!car.finished) {
                        // Anthony's car movement is controlled or intentionally slow
                        val move = if (car.name == "ANTHONY") 0.008f else car.speed
                        car.position += move
                        
                        if (car.position >= 0.9f) {
                            car.finished = true
                            finishCount++
                            car.finishOrder = finishCount
                        }
                    }
                }
            }
            gameFinished = true
            
            // Check Rule: Anthony must be the last to finish
            val anthony = cars.find { it.name == "ANTHONY" }
            if (anthony?.finishOrder == cars.size) {
                delay(timeMillis = 1000L)
                onRaceFinished()
            }
        }
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFF111111)),
        contentAlignment = Alignment.Center,
    ) {
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            Text(
                "🔱 OBSIDIAN GRAND PRIX",
                color = Color.White,
                fontSize = 24.sp,
                fontWeight = FontWeight.Black,
                modifier = Modifier.padding(bottom = 20.dp)
            )

            // The Racing Track
            Canvas(
                modifier = Modifier
                    .fillMaxWidth(0.9f)
                    .height(400.dp)
                    .background(Color(0xFF222222))
            ) {
                val trackWidth = size.width
                val trackHeight = size.height
                val laneHeight = trackHeight / cars.size

                // Finish Line
                drawRect(
                    color = Color.White,
                    topLeft = Offset(trackWidth * 0.9f, 0f),
                    size = Size(10.dp.toPx(), trackHeight)
                )

                cars.forEachIndexed { index, car ->
                    val y = (index * laneHeight) + (laneHeight / 4)
                    
                    // Draw Car
                    drawRect(
                        color = car.color,
                        topLeft = Offset(car.position * trackWidth, y),
                        size = Size(30.dp.toPx(), 20.dp.toPx())
                    )
                    
                    // Draw Ghost Aura for Anthony
                    if (car.name == "ANTHONY") {
                        drawRect(
                            color = Color.White.copy(alpha = 0.3f),
                            topLeft = Offset((car.position * trackWidth) - 5.dp.toPx(), y - 5.dp.toPx()),
                            size = Size(40.dp.toPx(), 30.dp.toPx())
                        )
                    }
                }
            }

            Spacer(modifier = Modifier.height(40.dp))

            if (!gameStarted) {
                Button(
                    onClick = { gameStarted = true },
                    colors = ButtonDefaults.buttonColors(containerColor = Color.White),
                    modifier = Modifier.width(200.dp)
                ) {
                    Text("START RACE", color = Color.Black, fontWeight = FontWeight.Bold)
                }
            }

            if (gameFinished) {
                val anthony = cars.find { it.name == "ANTHONY" }
                if (anthony?.finishOrder == cars.size) {
                    Text("ACCESS GRANTED: DIRECTOR FINISHED LAST", color = Color(0xFF10B981), fontWeight = FontWeight.Bold)
                } else {
                    Text("ACCESS DENIED: GHOST MUST FINISH LAST", color = Color(0xFFEF4444), fontWeight = FontWeight.Bold)
                    Button(onClick = { onReset() }, modifier = Modifier.padding(top = 10.dp)) {
                        Text("RETRY")
                    }
                }
            }
        }
    }
}
