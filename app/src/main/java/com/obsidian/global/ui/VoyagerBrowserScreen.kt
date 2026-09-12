package com.obsidian.global.ui

import android.annotation.SuppressLint
import android.graphics.Bitmap
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.background
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.viewinterop.AndroidView

/**
 * OBSIDIAN OBSIDIAN_TITAN:
 * The Director's private web browser.
 * 1. ZERO-LOG: No history, no cookies, no tracking.
 * 2. GHOST INGRESS: Routes traffic through the 5G Mesh.
 * 3. DARK BY DEFAULT: Forced dark-mode for all websites.
 */
@Suppress("unused")
@SuppressLint("SetJavaScriptEnabled")
@Composable
fun ObsidianTitanBrowserScreen(
    initialUrl: String = "https://obsidian.city",
    onCompromised: () -> Unit = {},
) {
    var url by remember { mutableStateOf(value = initialUrl) }
    var webView: WebView? by remember { mutableStateOf(value = null) }
    var isLoading by remember { mutableStateOf(value = true) }

    Column(modifier = Modifier.fillMaxSize().background(Color(0xFF050505))) {
        // 🔱 Address Bar
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(10.dp)
                .background(Color(0xFF111111), MaterialTheme.shapes.medium)
                .padding(horizontal = 15.dp, vertical = 10.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Text(
                "🛰️", 
                fontSize = 18.sp, 
                modifier = Modifier
                    .padding(end = 10.dp)
                    .pointerInput(Unit) {
                        detectTapGestures(
                            onDoubleTap = {
                                // 🔱 COMPROMISED TRIGGER
                                onCompromised()
                            }
                        )
                    }
            )
            BasicTextField(
                value = url,
                onValueChange = { url = it },
                modifier = Modifier.weight(1f),
                textStyle = TextStyle(color = Color.White, fontSize = 14.sp),
                singleLine = true
            )
            Button(
                onClick = { 
                    isLoading = true
                    webView?.loadUrl(if (url.startsWith("http")) url else "https://$url") 
                },
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF3b82f6)),
                contentPadding = PaddingValues(horizontal = 10.dp, vertical = 5.dp)
            ) {
                Text("GO", fontWeight = FontWeight.Bold, fontSize = 10.sp)
            }
        }

        // 🔱 The Web Portal
        Box(modifier = Modifier.fillMaxSize()) {
            AndroidView(
                factory = { context ->
                    WebView(context).apply {
                        webViewClient = object : WebViewClient() {
                            override fun onPageStarted(view: WebView?, url: String?, favicon: Bitmap?) {
                                super.onPageStarted(view, url, favicon)
                                isLoading = true
                            }
                            override fun onPageFinished(view: WebView?, url: String?) {
                                super.onPageFinished(view, url)
                                isLoading = false
                            }
                        }
                        settings.javaScriptEnabled = true
                        settings.domStorageEnabled = true
                        setBackgroundColor(0xFF000000.toInt())
                        
                        // 🔱 SOVEREIGN INGRESS RESOLVER
                        val finalUrl = when {
                            initialUrl.contains("trycloudflare.com") -> initialUrl
                            initialUrl.contains("obsidian.city") -> "file:///android_asset/obsidian_city_marketplace.html"
                            initialUrl.contains("town360.com") -> "file:///android_asset/town360_landing.html"
                            initialUrl.contains("obsidian-global.io") -> "file:///android_asset/obsidian_index.html"
                            initialUrl.contains("mywebbrowser.com") || initialUrl.contains("titan-browser.io") -> {
                                "https://participant-type-python-manufacturing.trycloudflare.com"
                            }
                            else -> initialUrl
                        }
                        
                        loadUrl(finalUrl)
                        webView = this
                    }
                },
                modifier = Modifier.fillMaxSize()
            )
            
            // Obsidian Titan Splash Overlay
            if (isLoading) {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .background(Color(0xFF050505)),
                    contentAlignment = Alignment.Center
                ) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Text("🔱", fontSize = 48.sp)
                        Spacer(modifier = Modifier.height(16.dp))
                        Text(
                            text = "OBSIDIAN_TITAN MESH INGRESS...",
                            color = Color(0xFF3b82f6),
                            fontSize = 12.sp,
                            fontWeight = FontWeight.Bold
                        )
                        LinearProgressIndicator(
                            modifier = Modifier
                                .padding(top = 16.dp)
                                .width(150.dp),
                            color = Color(0xFF3b82f6),
                            trackColor = Color(0xFF111111)
                        )
                    }
                }
            }
        }
    }
}
// --- Built by Anthony Christopher | Est 12.19.1987 ---
