package com.example.anthony_ai

import android.R
import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Intent
import android.os.IBinder
import android.util.Log
import androidx.core.app.NotificationCompat
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import kotlin.time.Duration.Companion.minutes

class SovereignAutopilotService : Service() {
    private val serviceJob = SupervisorJob()
    private val serviceScope = CoroutineScope(Dispatchers.IO + serviceJob)
    private lateinit var notificationManager: NotificationManager
    private val channelId = "AUTOPILOT_SERVICE_CHANNEL"
    private var lastVideoCount = 0

    override fun onCreate() {
        super.onCreate()
        notificationManager = getSystemService(NOTIFICATION_SERVICE) as NotificationManager
        createNotificationChannel()
        startForeground(1, createNotification("Autopilot loop active. Monitoring the Grid..."))
        startAutopilotLoop()
    }

    private fun createNotificationChannel() {
        val channel = NotificationChannel(
            channelId,
            "Anthony AI Autopilot",
            NotificationManager.IMPORTANCE_LOW,
        )
        notificationManager.createNotificationChannel(channel)
    }

    private fun createNotification(content: String): Notification {
        val intent = Intent(this, MainActivity::class.java)
        val pendingIntent = PendingIntent.getActivity(this, 0, intent, PendingIntent.FLAG_IMMUTABLE)

        return NotificationCompat.Builder(this, channelId)
            .setContentTitle("Anthony AI Assistant")
            .setContentText(content)
            .setSmallIcon(R.drawable.ic_menu_compass)
            .setContentIntent(pendingIntent)
            .setOngoing(true)
            .build()
    }

    private fun startAutopilotLoop() {
        serviceScope.launch {
            while (true) {
                try {
                    val currentUrl = NetworkConfig.currentBaseUrl
                    Log.d("AUTOPILOT", "Syncing feed from: $currentUrl")
                    val swarmFeed = MeshApiService.api.getFeed("For you")
                    
                    if (swarmFeed.size > lastVideoCount && lastVideoCount != 0) {
                        val newCount = swarmFeed.size - lastVideoCount
                        updateNotification("New Content: $newCount new cinematic drops detected.")
                    }
                    lastVideoCount = swarmFeed.size
                    
                    // Telemetry Pulse
                    MeshApiService.api.nodeHeartbeat("AUTOPILOT_SERVICE", "Synchronized")
                    
                } catch (e: Exception) {
                    Log.e("AUTOPILOT", "Sync Interrupted: ${e.message}")
                }
                delay(2.minutes)
            }
        }
    }

    private fun updateNotification(content: String) {
        val notification = createNotification(content)
        notificationManager.notify(1, notification)
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        return START_STICKY
    }

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onDestroy() {
        super.onDestroy()
        serviceJob.cancel()
    }
}
