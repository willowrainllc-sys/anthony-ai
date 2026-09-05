package com.example.anthony_ai

import android.annotation.SuppressLint
import android.webkit.JavascriptInterface
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.AddAPhoto
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Videocam
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.viewinterop.AndroidView
import com.example.anthony_ai.ui.theme.GlowNeon
import com.google.gson.Gson

import androidx.annotation.Keep

@Keep
class GlobeBridge(
    private val callback: (Double, Double) -> Unit
) {
    @JavascriptInterface
    fun onLocationSelected(lat: Double, lng: Double) {
        callback(lat, lng)
    }
}

@SuppressLint("SetJavaScriptEnabled", "JavascriptInterface")
@Composable
fun WorldTwinSpatialOverlayScreen(
    viewModel: MainViewModel,
    onBack: () -> Unit,
    modifier: Modifier = Modifier
) {
    var searchQuery by remember { mutableStateOf("") }
    var webViewInstance by remember { mutableStateOf<WebView?>(null) }
    
    val photoPicker = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent()
    ) { uri ->
        uri?.let { viewModel.performVisualRecon(it) }
    }

    val bridge = remember {
        GlobeBridge { lat, lng ->
            viewModel.searchResultLocation = LatLng(lat, lng)
            viewModel.activityFeed.add("TARGET: Locked at [$lat, $lng]")
        }
    }

    // Sync Data to Globe
    LaunchedEffect(viewModel.streetCameras.size, webViewInstance) {
        if (webViewInstance != null) {
            val gson = Gson()
            val points = viewModel.streetCameras.map { 
                mapOf("lat" to it.lat, "lng" to it.lon, "name" to it.title, "streamUrl" to it.streamUrl) 
            }
            val data = mapOf("points" to points)
            val json = gson.toJson(data)
            webViewInstance?.evaluateJavascript("updateData('$json')", null)
        }
    }

    // Sync User Location to Globe
    LaunchedEffect(viewModel.userLocation, webViewInstance) {
        viewModel.userLocation?.let { loc ->
            webViewInstance?.evaluateJavascript("setUserLocation(${loc.latitude}, ${loc.longitude})", null)
        }
    }

    // Handle Search Location fly-to
    LaunchedEffect(viewModel.searchResultLocation) {
        viewModel.searchResultLocation?.let { loc ->
            webViewInstance?.evaluateJavascript("flyTo(${loc.latitude}, ${loc.longitude}, 2.5)", null)
        }
    }

    Box(modifier = modifier.fillMaxSize().background(Color.Black)) {
        AndroidView(
            modifier = Modifier.fillMaxSize(),
            factory = { context ->
                WebView(context).apply {
                    settings.apply {
                        javaScriptEnabled = true
                        domStorageEnabled = true
                        loadWithOverviewMode = true
                        useWideViewPort = true
                        allowFileAccess = true
                        allowContentAccess = true
                    }
                    addJavascriptInterface(bridge, "AndroidBridge")
                    webViewClient = WebViewClient()
                    loadUrl("file:///android_asset/globe.html")
                    webViewInstance = this
                }
            }
        )

        // HUD: TOP
        Column(modifier = Modifier.fillMaxWidth().padding(24.dp).statusBarsPadding()) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                IconButton(
                    onClick = onBack, 
                    modifier = Modifier.background(Color.Black.copy(alpha = 0.5f), CircleShape)
                ) {
                    Icon(imageVector = Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Color.White)
                }
                Spacer(Modifier.width(12.dp))
                Surface(
                    modifier = Modifier.weight(1f).height(54.dp),
                    shape = RoundedCornerShape(27.dp),
                    color = Color.Black.copy(alpha = 0.8f),
                    border = BorderStroke(1.dp, GlowNeon.copy(alpha = 0.5f))
                ) {
                    Row(modifier = Modifier.fillMaxSize().padding(horizontal = 16.dp), verticalAlignment = Alignment.CenterVertically) {
                        Icon(imageVector = Icons.Default.Search, contentDescription = null, tint = GlowNeon, modifier = Modifier.size(22.dp))
                        Spacer(Modifier.width(12.dp))
                        Box(modifier = Modifier.weight(1f), contentAlignment = Alignment.CenterStart) {
                            if (searchQuery.isEmpty()) Text("Locate Signal...", color = Color.Gray, fontSize = 14.sp)
                            BasicTextField(
                                value = searchQuery,
                                onValueChange = { searchQuery = it },
                                textStyle = TextStyle(color = Color.White, fontSize = 15.sp, fontWeight = FontWeight.Bold),
                                modifier = Modifier.fillMaxWidth()
                            )
                        }
                        IconButton(onClick = { photoPicker.launch("image/*") }) {
                            Icon(imageVector = Icons.Default.AddAPhoto, null, tint = GlowNeon, modifier = Modifier.size(24.dp))
                        }
                    }
                }
            }
        }
        
        // --- HUD: BOTTOM TACTICAL SLOTS ---
        Surface(
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .padding(bottom = 24.dp),
            color = Color.Black.copy(alpha = 0.85f),
            shape = RoundedCornerShape(16.dp),
            border = BorderStroke(1.dp, GlowNeon.copy(alpha = 0.3f))
        ) {
            Row(
                modifier = Modifier.padding(10.dp),
                horizontalArrangement = Arrangement.spacedBy(12.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                repeat(3) { index ->
                    val pinnedId = viewModel.pinnedCameras.getOrNull(index)
                    val camera = viewModel.streetCameras.find { it.id == pinnedId }
                    
                    Box(
                        modifier = Modifier
                            .size(52.dp)
                            .background(Color(0xFF080808), RoundedCornerShape(10.dp))
                            .border(1.dp, if (camera != null) GlowNeon else Color.DarkGray.copy(alpha = 0.5f), RoundedCornerShape(10.dp))
                            .clickable {
                                if (camera != null) {
                                    viewModel.searchResultLocation = LatLng(camera.lat, camera.lon)
                                }
                            },
                        contentAlignment = Alignment.Center
                    ) {
                        if (camera != null) {
                            Icon(Icons.Default.Videocam, null, tint = GlowNeon, modifier = Modifier.size(22.dp))
                        } else {
                            Icon(Icons.Default.Add, null, tint = Color.DarkGray, modifier = Modifier.size(20.dp))
                        }
                    }
                }
            }
        }

        // Action Button
        FloatingActionButton(
            onClick = { webViewInstance?.evaluateJavascript("clearPath()", null) },
            modifier = Modifier.align(Alignment.BottomEnd).padding(bottom = 24.dp, end = 24.dp),
            containerColor = Color.Red.copy(alpha = 0.8f),
            contentColor = Color.White,
            shape = CircleShape
        ) {
            Icon(Icons.Default.Delete, "Clear")
        }
    }
}
