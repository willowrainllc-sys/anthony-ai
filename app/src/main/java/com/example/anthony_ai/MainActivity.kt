package com.example.anthony_ai

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.runtime.*
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.anthony_ai.ui.AnthonyAiFeedScreen
import com.example.anthony_ai.ui.LoginScreen
import com.example.anthony_ai.ui.ShimmerMaskOverlay
import com.example.anthony_ai.ui.theme.*
import android.content.Intent
import android.os.Build
import androidx.activity.result.contract.ActivityResultContracts
import android.Manifest
import android.util.Log

class MainActivity : ComponentActivity() {
    private var voiceRecognizerManager: VoiceRecognizerManager? = null
    private var ttsManager: TtsManager? = null

    private val requestPermissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { permissions ->
        if (permissions[Manifest.permission.ACCESS_FINE_LOCATION] == true) {
            Log.d("PERMISSIONS", "Location Granted")
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        
        // Start Autopilot Service
        val serviceIntent = Intent(this, SovereignAutopilotService::class.java)
        startForegroundService(serviceIntent)

        setContent {
            val mainViewModel: MainViewModel = viewModel()
            var showLogin by remember { mutableStateOf(true) }
            
            // --- BACKEND SERVICES ---
            val currentContext = this@MainActivity
            val vrm = remember {
                VoiceRecognizerManager(currentContext, { mainViewModel.onSpeechResult(it) }) { mainViewModel.onSpeechError(it) }
            }
            val tts = remember { TtsManager(currentContext) }
            
            voiceRecognizerManager = vrm
            ttsManager = tts
            
            LaunchedEffect(Unit) {
                mainViewModel.responseFlow.collect { chunk ->
                    if (chunk == "__FINISH__") tts.flushBuffer()
                    else tts.speakStream(chunk)
                }
            }
            
            Anthony_AiTheme {
                if (showLogin) {
                    LoginScreen(
                        onLoginSuccess = { 
                            showLogin = false
                            val permissions = mutableListOf(
                                Manifest.permission.ACCESS_FINE_LOCATION,
                                Manifest.permission.ACCESS_COARSE_LOCATION
                            )
                            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                                permissions.add(Manifest.permission.POST_NOTIFICATIONS)
                            }
                            requestPermissionLauncher.launch(permissions.toTypedArray())
                        },
                        onSkip = { 
                            showLogin = false 
                            requestPermissionLauncher.launch(
                                arrayOf(
                                    Manifest.permission.ACCESS_FINE_LOCATION,
                                    Manifest.permission.ACCESS_COARSE_LOCATION
                                )
                            )
                        }
                    )
                } else {
                    ShimmerMaskOverlay(isLoading = mainViewModel.isLoading) {
                        AnthonyAiFeedScreen(
                            onLogout = { showLogin = true },
                            onMicPressed = { vrm.startListening() },
                            onMicReleased = { vrm.stopListening() }
                        )
                    }
                }
            }
        }
    }
}
