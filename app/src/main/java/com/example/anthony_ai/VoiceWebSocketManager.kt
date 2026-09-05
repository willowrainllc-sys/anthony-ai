package com.example.anthony_ai

import android.util.Log
import okhttp3.*
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.SharedFlow

class VoiceWebSocketManager {
    private val client = OkHttpClient()
    private var websocket: WebSocket? = null
    private val TAG = "VoiceWebSocket"

    private val _messages = MutableSharedFlow<String>(extraBufferCapacity = 10)
    val messages: SharedFlow<String> = _messages

    private val listener = object : WebSocketListener() {
        override fun onMessage(webSocket: WebSocket, text: String) {
            super.onMessage(webSocket, text)
            Log.d(TAG, "Received: $text")
            _messages.tryEmit(text)
        }

        override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
            super.onFailure(webSocket, t, response)
            Log.e(TAG, "WebSocket Failure: ${t.message}")
        }

        override fun onClosed(webSocket: WebSocket, code: Int, reason: String) {
            super.onClosed(webSocket, code, reason)
            Log.d(TAG, "WebSocket Closed: $reason")
        }
    }

    fun connect(serverUrl: String, apiKey: String) {
        if (websocket != null) return
        val request = Request.Builder()
            .url(serverUrl)
            .addHeader("x-api-key", apiKey)
            .build()
        websocket = client.newWebSocket(request, listener)
    }

    fun sendTextMessage(text: String) {
        websocket?.send(text)
    }

    fun disconnect() {
        websocket?.close(1000, "Disconnecting")
        websocket = null
    }
}
