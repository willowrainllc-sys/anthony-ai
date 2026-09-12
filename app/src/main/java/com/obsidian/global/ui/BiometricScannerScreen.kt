package com.obsidian.global.ui

import androidx.camera.core.CameraSelector
import androidx.camera.core.Preview
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.camera.view.PreviewView
import androidx.compose.animation.core.*
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.platform.LocalContext
import androidx.lifecycle.compose.LocalLifecycleOwner
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.core.content.ContextCompat
import com.google.mlkit.vision.codescanner.GmsBarcodeScanning
import kotlinx.coroutines.delay
import kotlin.time.Duration.Companion.milliseconds
import kotlin.time.Duration.Companion.seconds

/**
 * 👁️ BIOMETRIC FACE SCANNER:
 * The final security gate before Phone Hive ingress.
 * 1. LIVE CAMERA: Activates the front-facing camera.
 * 2. NEURAL SCAN: Visual overlay simulating real-time biometric analysis.
 * 3. QR HANDSHAKE: Optionally scan a terminal QR code to bridge the session.
 * 4. IDENTITY LOCK: Confirms "The Living Anthony" via simulated recognition.
 */
@Composable
fun BiometricScannerScreen(onIdentityConfirmed: () -> Unit) {
    val context = LocalContext.current
    val lifecycleOwner = LocalLifecycleOwner.current
    val cameraProviderFuture = remember { ProcessCameraProvider.getInstance(context) }
    
    var isScanning by remember { mutableStateOf(value = false) }
    var startTrigger by remember { mutableStateOf(value = false) }
    var scanProgress by remember { mutableFloatStateOf(0f) }
    var statusText by remember { mutableStateOf("INITIALIZING OPTICAL SENSORS...") }

    val infiniteTransition = rememberInfiniteTransition(label = "ScanTransition")
    val scanLineY by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(2500, easing = LinearEasing),
            repeatMode = RepeatMode.Reverse,
        ),
        label = "ScanLineAnimation"
    )

    fun startQrScanner() {
        val scanner = GmsBarcodeScanning.getClient(context)
        scanner.startScan()
            .addOnSuccessListener { barcode ->
                val rawValue: String? = barcode.rawValue
                if (rawValue?.startsWith("obsidian://handshake") == true) {
                    statusText = "HANDSHAKE VERIFIED. GRANTED."
                    scanProgress = 1f
                    onIdentityConfirmed()
                }
            }
            .addOnFailureListener {
                statusText = "QR HANDSHAKE FAILED."
            }
    }

    LaunchedEffect(startTrigger) {
        if (startTrigger) {
            isScanning = true
            delay(1.5.seconds)
            statusText = "SCANNING NEURAL MESH..."
            while (scanProgress < 1f) {
                delay(50.milliseconds)
                scanProgress += 0.01f
            }
            statusText = "IDENTITY CONFIRMED: ANTHONY CHRISTOPHER"
            delay(1.5.seconds)
            isScanning = false
            onIdentityConfirmed()
        }
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFF050505)),
        contentAlignment = Alignment.Center
    ) {
        // 🔱 The Eye (Camera Feed)
        Box(
            modifier = Modifier
                .size(300.dp)
                .clip(CircleShape)
                .border(2.dp, Color(0xFF3b82f6), CircleShape)
                .background(Color.DarkGray)
                .clickable { startQrScanner() } // Tap eye to switch to QR mode
        ) {
            AndroidView(
                factory = { ctx ->
                    val previewView = PreviewView(ctx)
                    val executor = ContextCompat.getMainExecutor(ctx)
                    cameraProviderFuture.addListener(
                        {
                            val cameraProvider = cameraProviderFuture.get()
                            val preview = Preview.Builder().build().also {
                                it.surfaceProvider = previewView.surfaceProvider
                            }
                            val cameraSelector = CameraSelector.DEFAULT_FRONT_CAMERA
                            try {
                                cameraProvider.unbindAll()
                                cameraProvider.bindToLifecycle(
                                    lifecycleOwner,
                                    cameraSelector,
                                    preview,
                                )
                            } catch (_: Exception) {
                                // Handle error
                            }
                        },
                        executor,
                    )
                    previewView
                },
                modifier = Modifier.fillMaxSize()
            )

            // Biometric Overlay
            Canvas(modifier = Modifier.fillMaxSize()) {
                val height = size.height
                val width = size.width
                
                // Scan Line
                val lineY = scanLineY * height
                drawLine(
                    color = Color(0xFF00FF88).copy(alpha = 0.8f),
                    start = Offset(0f, lineY),
                    end = Offset(width, lineY),
                    strokeWidth = 2.dp.toPx()
                )
                
                // HUD Hexagon or Circle Frame
                drawCircle(
                    color = Color(0xFF3b82f6).copy(alpha = 0.2f),
                    style = Stroke(width = 1.dp.toPx()),
                    radius = (width / 2) - 10.dp.toPx()
                )
            }
        }

        // Status HUD
        Column(
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .padding(bottom = 60.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = statusText,
                color = if (scanProgress >= 1f) Color(0xFF00FF88) else Color(0xFF3b82f6),
                fontSize = 12.sp,
                fontWeight = FontWeight.Bold,
                letterSpacing = 2.sp
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            LinearProgressIndicator(
                progress = { scanProgress },
                modifier = Modifier
                    .width(200.dp)
                    .height(2.dp),
                color = Color(0xFF3b82f6),
                trackColor = Color(0xFF111111)
            )
            
            Text(
                text = "${(scanProgress * 100).toInt()}%",
                color = Color.Gray,
                fontSize = 10.sp,
                modifier = Modifier.padding(top = 8.dp)
            )
            
            if (!startTrigger) {
                Spacer(modifier = Modifier.height(24.dp))
                Button(
                    onClick = { startTrigger = true },
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF3b82f6)),
                    shape = RoundedCornerShape(8.dp)
                ) {
                    Text("START BIOMETRIC SCAN", fontWeight = FontWeight.Bold)
                }
                
                TextButton(
                    onClick = { startQrScanner() },
                    modifier = Modifier.padding(top = 8.dp)
                ) {
                    Text("OR TAP IN VIA QR", color = Color.Gray, fontSize = 10.sp)
                }
            }
        }
        
        // Security Lock Icon
        Icon(
            imageVector = Icons.Default.Lock,
            contentDescription = null,
            tint = Color.White.copy(alpha = 0.1f),
            modifier = Modifier
                .align(Alignment.TopCenter)
                .padding(top = 40.dp)
                .size(48.dp)
        )
    }
}
