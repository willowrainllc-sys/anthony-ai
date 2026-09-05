package com.example.anthony_ai

import android.content.Context
import android.net.ConnectivityManager
import android.net.LinkProperties
import android.util.Log
import java.net.InetAddress

/**
 * Central Swarm Network Configuration
 * Supports Dynamic Hotspot Gateway pathing.
 */
object NetworkConfig {
    var currentBaseUrl = "http://localhost:8000"
        private set

    /**
     * Attempts to resolve the 'Presidential Gateway' (The PC)
     * if the phone is acting as a Hotspot.
     */
    fun resolveActiveGateway(context: Context): String {
        val cm = context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
        val linkProperties: LinkProperties? = cm.getLinkProperties(cm.activeNetwork)
        
        val routes = linkProperties?.routes
        val gateway = routes?.find { it.isDefaultRoute }?.gateway?.hostAddress
        
        Log.d("MESH_NET", "Probing Gateway: $gateway")

        return when {
            gateway != null && !gateway.startsWith("fe80") && gateway != "0.0.0.0" -> "http://$gateway:8000"
            else -> "http://10.0.0.1:8000" 
        }
    }

    fun sync(context: Context) {
        currentBaseUrl = resolveActiveGateway(context)
        Log.i("MESH_NET", "Resolved Gateway URL: $currentBaseUrl")
        MeshApiService.updateIp(currentBaseUrl)
    }

    fun syncWithTarget(target: String) {
        val fullUrl = if (target.startsWith("http")) target else "http://$target"
        currentBaseUrl = fullUrl
        MeshApiService.updateIp(fullUrl)
    }

    // Production Vercel Gateway & Secondary Endpoints
    const val VERCEL_PROD_URL = "https://anthony-ai.vercel.app"
    val TURBO_URL get() = currentBaseUrl.replace(":8000", ":8080")
}
