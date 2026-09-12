package com.obsidian.global.ui

import android.view.ViewGroup
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.viewinterop.AndroidView

/**
 * 👁️ OBSIDIAN-PARTY: GHOST REDIRECT v2.0
 * This screen is no longer hard-coded on the device.
 * It loads from the remote Obsidian Cloud to ensure no local traces.
 */
@Composable
fun ObsidianPartyScreen(onBack: () -> Unit) {
    // The remote URL for the secret room
    val ghostUrl = "https://anthony-ai.vercel.app/obsidian_party.html"

    AndroidView(
        modifier = Modifier.fillMaxSize(),
        factory = { context ->
            WebView(context).apply {
                layoutParams = ViewGroup.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT,
                    ViewGroup.LayoutParams.MATCH_PARENT
                )
                webViewClient = WebViewClient()
                settings.javaScriptEnabled = true
                loadUrl(ghostUrl)
            }
        },
        update = { webView ->
            // Update logic if needed
        }
    )
}
