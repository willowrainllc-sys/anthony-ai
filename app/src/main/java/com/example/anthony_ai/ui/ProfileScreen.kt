package com.example.anthony_ai.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ExitToApp
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material.icons.filled.Palette
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.anthony_ai.MainViewModel
import com.example.anthony_ai.ui.theme.GlowNeon

@Suppress("DEPRECATION")
@Composable
fun ProfileScreen(viewModel: MainViewModel, onLogout: () -> Unit) {
    var showTermsModal by remember { mutableStateOf(false) }
    var showPrivacyModal by remember { mutableStateOf(false) }
    val clipboardManager = LocalClipboardManager.current

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background)
            .verticalScroll(rememberScrollState())
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(modifier = Modifier.height(24.dp))

        // --- AVATAR / PROFILE HEADER ---
        Box(
            modifier = Modifier
                .size(80.dp)
                .clip(CircleShape)
                .background(MaterialTheme.colorScheme.surfaceVariant),
            contentAlignment = Alignment.Center
        ) {
            Text("🐜", fontSize = 36.sp)
        }

        Spacer(modifier = Modifier.height(12.dp))

        Text(
            text = "Anthony AI User",
            color = MaterialTheme.colorScheme.onBackground,
            fontSize = 24.sp,
            fontWeight = FontWeight.Black
        )
        
        // --- USER TAG SECTION ---
        Surface(
            onClick = { 
                clipboardManager.setText(AnnotatedString(viewModel.userTag))
            },
            shape = RoundedCornerShape(20.dp),
            color = GlowNeon.copy(alpha = 0.2f),
            modifier = Modifier.padding(top = 10.dp)
        ) {
            Row(
                modifier = Modifier.padding(horizontal = 16.dp, vertical = 6.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = viewModel.userTag,
                    color = GlowNeon,
                    fontSize = 15.sp,
                    fontWeight = FontWeight.Bold
                )
                Spacer(modifier = Modifier.width(8.dp))
                Icon(Icons.Default.Info, contentDescription = "Copy", tint = GlowNeon, modifier = Modifier.size(16.dp))
            }
        }

        Text(
            text = "AI Media Assistant",
            color = MaterialTheme.colorScheme.onBackground.copy(alpha = 0.6f),
            fontSize = 12.sp,
            modifier = Modifier.padding(top = 8.dp)
        )

        Spacer(modifier = Modifier.height(32.dp))

        // --- SECTIONS CARD ---
        Card(
            shape = RoundedCornerShape(16.dp),
            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text(
                    text = "SETTINGS & POLICIES",
                    color = GlowNeon,
                    fontSize = 12.sp,
                    fontWeight = FontWeight.Bold,
                    letterSpacing = 1.sp
                )

                Spacer(modifier = Modifier.height(16.dp))

                // Theme setting info
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.Palette, contentDescription = "Theme", tint = MaterialTheme.colorScheme.onSurface)
                        Spacer(modifier = Modifier.width(12.dp))
                        Text(text = "Theme Mode", color = MaterialTheme.colorScheme.onSurface, fontSize = 14.sp)
                    }
                    Text(text = "System Default (Auto)", color = Color.Gray, fontSize = 12.sp)
                }

                HorizontalDivider(modifier = Modifier.padding(vertical = 12.dp), color = Color.DarkGray.copy(alpha = 0.3f))

                // Terms of Service
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable { showTermsModal = true }
                        .padding(vertical = 8.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.Info, contentDescription = "ToS", tint = MaterialTheme.colorScheme.onSurface)
                        Spacer(modifier = Modifier.width(12.dp))
                        Text(text = "Terms of Service", color = MaterialTheme.colorScheme.onSurface, fontSize = 14.sp)
                    }
                    Text(text = "View", color = GlowNeon, fontSize = 12.sp)
                }

                HorizontalDivider(modifier = Modifier.padding(vertical = 12.dp), color = Color.DarkGray.copy(alpha = 0.3f))

                // Privacy Policy
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable { showPrivacyModal = true }
                        .padding(vertical = 8.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.Lock, contentDescription = "Privacy", tint = MaterialTheme.colorScheme.onSurface)
                        Spacer(modifier = Modifier.width(12.dp))
                        Text(text = "Privacy Policy", color = MaterialTheme.colorScheme.onSurface, fontSize = 14.sp)
                    }
                    Text(text = "View", color = GlowNeon, fontSize = 12.sp)
                }
            }
        }

        Spacer(modifier = Modifier.height(32.dp))

        // --- LOG OUT BUTTON ---
        Button(
            onClick = onLogout,
            colors = ButtonDefaults.buttonColors(containerColor = Color.Red.copy(alpha = 0.8f)),
            shape = RoundedCornerShape(12.dp),
            modifier = Modifier
                .fillMaxWidth()
                .height(50.dp)
        ) {
            Icon(Icons.AutoMirrored.Filled.ExitToApp, contentDescription = "Log Out", tint = Color.White)
            Spacer(modifier = Modifier.width(8.dp))
            Text(text = "Log Out", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 16.sp)
        }

        Spacer(modifier = Modifier.height(24.dp))
    }

    // Terms of Service Dialog
    if (showTermsModal) {
        AlertDialog(
            onDismissRequest = { showTermsModal = false },
            title = { Text("Terms of Service") },
            text = {
                Column(modifier = Modifier.verticalScroll(rememberScrollState())) {
                    Text(
                        "Welcome to Anthony AI. By accessing or using our application, you agree to be bound by these Terms of Service.\n\n" +
                        "1. Use of Service: You agree to use Anthony AI for lawful AI content generation, creative exploration, and AI assistance.\n" +
                        "2. Intellectual Property: Generated videos, chats, and content created through your account remain associated with your personal account.\n" +
                        "3. Prohibited Content: Users must not generate illegal, harmful, or abusive content.\n" +
                        "4. Modifications: We reserve the right to update these terms at any time."
                    )
                }
            },
            confirmButton = {
                TextButton(onClick = { showTermsModal = false }) {
                    Text("Close", color = GlowNeon)
                }
            }
        )
    }

    // Privacy Policy Dialog
    if (showPrivacyModal) {
        AlertDialog(
            onDismissRequest = { showPrivacyModal = false },
            title = { Text("Privacy Policy") },
            text = {
                Column(modifier = Modifier.verticalScroll(rememberScrollState())) {
                    Text(
                        "At Anthony AI, your privacy is paramount. This Privacy Policy outlines how we handle your data:\n\n" +
                        "1. Data Collection: We collect account credentials and media generation prompts required to provide AI media processing.\n" +
                        "2. Secure Storage: All cloud data and media assets are stored securely using encrypted infrastructure.\n" +
                        "3. Third-Party Sharing: We do not sell or share your personal data with third parties.\n" +
                        "4. Security: We employ industry-standard security protocols to protect your information."
                    )
                }
            },
            confirmButton = {
                TextButton(onClick = { showPrivacyModal = false }) {
                    Text("Close", color = GlowNeon)
                }
            }
        )
    }
}
