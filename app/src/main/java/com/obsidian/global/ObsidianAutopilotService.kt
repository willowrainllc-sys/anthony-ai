package com.obsidian.global

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
import java.util.Locale
import java.util.TimeZone
import kotlin.time.Duration.Companion.minutes

class ObsidianAutopilotService : Service() {
    private val serviceJob = SupervisorJob()
    private val serviceScope = CoroutineScope(Dispatchers.IO + serviceJob)
    private lateinit var notificationManager: NotificationManager
    private val channelId = "AUTOPILOT_SERVICE_CHANNEL"
    private var lastVideoCount = 0
    private var lastSquareBalance = 0.0

    override fun onCreate() {
        super.onCreate()
        notificationManager = getSystemService(NOTIFICATION_SERVICE) as NotificationManager
        createNotificationChannel()
        startForeground(1, createNotification("Mission Lockdown Active. Monitoring Revenue Grid..."))
        startAutopilotLoop()
    }

    private fun createNotificationChannel() {
        val channel = NotificationChannel(
            channelId,
            "Anthony AI Autopilot",
            NotificationManager.IMPORTANCE_HIGH
        )
        notificationManager.createNotificationChannel(channel)
    }

    private fun createNotification(content: String): Notification {
        val intent = Intent(this, MainActivity::class.java)
        val pendingIntent = PendingIntent.getActivity(this, 0, intent, PendingIntent.FLAG_IMMUTABLE)

        return NotificationCompat.Builder(this, channelId)
            .setContentTitle("Willow Rain Obsidian")
            .setContentText(content)
            .setSmallIcon(R.drawable.ic_menu_compass)
            .setContentIntent(pendingIntent)
            .setOngoing(true)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .build()
    }

    private fun startAutopilotLoop() {
        serviceScope.launch {
            while (true) {
                try {
                    val currentUrl = NetworkConfig.currentBaseUrl
                    Log.d("AUTOPILOT", "Syncing feed and vitals from: $currentUrl")
                    
                    // 1. Check Video Feed
                    val colonyFeed = MeshApiService.api.getFeed("For you")
                    if (colonyFeed.size > lastVideoCount && lastVideoCount != 0) {
                        val newCount = colonyFeed.size - lastVideoCount
                        updateNotification("New Content: $newCount new cinematic drops detected.")
                    }
                    lastVideoCount = colonyFeed.size
                    
                    // 2. Check Real Square Balance
                    val vitals = MeshApiService.api.getRevenueVitals()
                    if (vitals.status == "success") {
                        val currentBalance = vitals.squareRealSettledUsd
                        if (currentBalance > lastSquareBalance && lastSquareBalance != 0.0) {
                            val gain = currentBalance - lastSquareBalance
                            updateNotification("🔱 REVENUE ALERT: +$${String.format(Locale.US, "%.2f", gain)} USD settled in Square!")
                        }
                        lastSquareBalance = currentBalance
                    }
                    
                    // 3. Time Zone Synchronization
                    val timeZone = TimeZone.getDefault().id
                    val offset = TimeZone.getDefault().rawOffset / (1000 * 60 * 60)
                    Log.d("AUTOPILOT", "Syncing Time Zone: $timeZone (GMT$offset)")
                    
                    // Telemetry Pulse
                    MeshApiService.api.nodeHeartbeat("PHONE_NODE_ANTHONY", "MISSION_LOCKDOWN_ACTIVE")
                    MeshApiService.api.syncTimeHistory("PHONE_NODE_ANTHONY", timeZone, System.currentTimeMillis())
                    
                } catch (e: Exception) {
                    Log.e("AUTOPILOT", "Sync Interrupted: ${e.message}")
                }
                delay(1.minutes) 
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
