package com.obsidian.global

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.runtime.*
import androidx.lifecycle.viewmodel.compose.viewModel
import com.obsidian.global.ui.AnthonyAiFeedScreen
import com.obsidian.global.ui.LoginScreen
import com.obsidian.global.ui.ShimmerMaskOverlay
import com.obsidian.global.ui.theme.*
import android.content.Intent
import android.os.Build
import androidx.activity.result.contract.ActivityResultContracts
import android.Manifest
import android.util.Log
import com.obsidian.global.ui.AgentRoomScreen
import com.obsidian.global.ui.CloakedClockScreen
import com.obsidian.global.ui.ObsidianPartyScreen
import com.obsidian.global.ui.BiometricScannerScreen
import com.obsidian.global.ui.ObsidianRacingGate
import com.obsidian.global.ui.ObsidianSplashScreen
import com.obsidian.global.ui.ObsidianTitanBrowserScreen

class MainActivity : ComponentActivity() {
    private var voiceRecognizerManager: VoiceRecognizerManager? = null
    private var ttsManager: TtsManager? = null

    private val requestPermissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions(),
    ) { permissions ->
        if (permissions[Manifest.permission.ACCESS_FINE_LOCATION] == true) {
            Log.d("PERMISSIONS", "Location Granted")
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        
        // Start Autopilot Service
        val serviceIntent = Intent(this, ObsidianAutopilotService::class.java)
        startForegroundService(serviceIntent)

        setContent {
            val mainViewModel: MainViewModel = viewModel()
            var currentScreen by remember { mutableStateOf("splash") }
            
            // --- BACKEND SERVICES ---
            val currentContext = this@MainActivity
            val vrm = remember {
                VoiceRecognizerManager(currentContext, { mainViewModel.onSpeechResult(it) }) { mainViewModel.onSpeechError(it) }
            }
            val tts = remember { TtsManager(currentContext) }
            
            var browserUrl by remember { mutableStateOf("https://obsidian.city") }
            
            voiceRecognizerManager = vrm
            ttsManager = tts
            
            LaunchedEffect(Unit) {
                mainViewModel.responseFlow.collect { chunk ->
                    if (chunk == "__FINISH__") tts.flushBuffer()
                    else tts.speakStream(chunk)
                }
            }
            
            Obsidian_GlobalTheme {
                when (currentScreen) {
                    "splash" -> {
                        ObsidianSplashScreen { currentScreen = "cloak" }
                    }
                    "cloak" -> {
                        CloakedClockScreen(onUnlock = { currentScreen = "login" }) {
                            currentScreen = "feed"
                        }
                    }
                    "login" -> {
                        LoginScreen(
                            onLoginSuccess = { 
                                currentScreen = "feed"
                                val permissions = mutableListOf(
                                    Manifest.permission.ACCESS_FINE_LOCATION,
                                    Manifest.permission.ACCESS_COARSE_LOCATION,
                                )
                                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                                    permissions.add(Manifest.permission.POST_NOTIFICATIONS)
                                }
                                requestPermissionLauncher.launch(permissions.toTypedArray())
                            },
                            onSkip = {
                                currentScreen = "feed"
                                requestPermissionLauncher.launch(
                                    arrayOf(
                                        Manifest.permission.ACCESS_FINE_LOCATION,
                                        Manifest.permission.ACCESS_COARSE_LOCATION,
                                    )
                                )
                            }
                        )
                    }
                    "feed" -> {
                        ShimmerMaskOverlay(isLoading = mainViewModel.isLoading) {
                            AnthonyAiFeedScreen(
                                onLogout = { currentScreen = "login" },
                                onAgentRoomClick = { currentScreen = "agent_room" },
                                onCityClick = { 
                                    browserUrl = "https://obsidian.city"
                                    currentScreen = "voyager" 
                                },
                                onMicPressed = { vrm.startListening() },
                                onMicReleased = { vrm.stopListening() }
                            )
                        }
                    }
                    "agent_room" -> {
                        AgentRoomScreen(
                            onBack = { currentScreen = "feed" },
                            onPartyClick = { currentScreen = "obsidian_party" }
                        )
                    }
                    "obsidian_party" -> {
                        ObsidianPartyScreen(
                            onBack = { currentScreen = "agent_room" }
                        )
                    }
                    "voyager" -> {
                        ObsidianTitanBrowserScreen(
                            initialUrl = browserUrl,
                            onCompromised = { currentScreen = "racing_gate" }
                        )
                    }
                    "racing_gate" -> {
                        ObsidianRacingGate(
                            onRaceFinished = { currentScreen = "biometric_scan" },
                            onReset = { currentScreen = "racing_gate" } // Refresh game
                        )
                    }
                    "biometric_scan" -> {
                        BiometricScannerScreen(
                            onIdentityConfirmed = { currentScreen = "phone_hive" }
                        )
                    }
                    "phone_hive" -> {
                        ObsidianTitanBrowserScreen(initialUrl = "file:///android_asset/obsidian_device_grid.html")
                    }
                }
            }
        }
    }
}
