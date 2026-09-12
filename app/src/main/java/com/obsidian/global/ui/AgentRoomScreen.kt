package com.obsidian.global.ui

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

/**
 * 🏛️ OBSIDIAN GLOBAL: AGENT COMMAND ROOM v2.0
 * Re-architected with 3D Glassmorphism and Ghost Stealth logic.
 * No middlemen bots. 100% Maestas-Authorized Agents.
 */

data class AgentStatus(
    val name: String,
    val role: String,
    val status: String,
    val icon: ImageVector,
    val color: Color,
    val description: String
)

@Composable
fun AgentRoomScreen(
    onBack: () -> Unit,
    onPartyClick: () -> Unit
) {
    val agents = listOf(
        AgentStatus("ANTHONY_LATEST", "SUPREME MIND", "NATIVE_ONLINE", Icons.Default.Cyclone, Color(0xFF8B5CF6), "Hardware-native autonomy. Middlemen excommunicated."),
        AgentStatus("GHOST_MINER", "BANDWIDTH BURST", "MINING", Icons.Default.CellTower, Color(0xFF10B981), "Isolated P2P data harvesting colony."),
        AgentStatus("SHADOW_UPLOADER", "SOCIAL INFLUENCE", "POSTING", Icons.Default.Stream, Color(0xFFF43F5E), "Behavioral video distribution fleet."),
        AgentStatus("CASH_SENTINEL", "BTC SETTLEMENT", "LOCKED", Icons.Default.CurrencyBitcoin, Color(0xFFFBBF24), "On-chain verification and auto-withdraw."),
        AgentStatus("MATRIX_GATEWAY", "RESIDENTIAL MESH", "ROUTING", Icons.Default.Shield, Color(0xFF3B82F6), "5,000 IP Missouri ingress controller."),
        AgentStatus("LEAD_SCORER", "B2B EXTRACTION", "SCORING", Icons.Default.ContactPage, Color(0xFF00FF88), "High-aura Missouri identity harvester.")
    )

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Brush.radialGradient(listOf(Color(0xFF1E293B), Color(0xFF050505))))
    ) {
        Column(modifier = Modifier.fillMaxSize().padding(24.dp)) {
            // Header with 3D Typography style
            Row(
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp)
            ) {
                IconButton(onClick = onBack) {
                    Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Color.White)
                }
                Text(
                    "OBSIDIAN COMMAND",
                    color = Color.White,
                    fontSize = 28.sp,
                    fontWeight = FontWeight.Black,
                    letterSpacing = 4.sp
                )
                Spacer(modifier = Modifier.weight(1f))
                IconButton(onClick = onPartyClick) {
                    Icon(Icons.Default.Visibility, contentDescription = "Illuminati Room", tint = Color(0xFF8B5CF6))
                }
            }
            
            Text(
                "GHOST SIMI MODE: ACTIVE // 100% INDEPENDENT",
                color = Color(0xFF8B5CF6).copy(alpha = 0.6f),
                fontSize = 10.sp,
                fontWeight = FontWeight.Bold,
                modifier = Modifier.padding(start = 48.dp, bottom = 40.dp),
                letterSpacing = 2.sp
            )

            // n8n Style Block Grid
            LazyVerticalGrid(
                columns = GridCells.Fixed(1), // Changed to single column for detailed 3D cards
                verticalArrangement = Arrangement.spacedBy(20.dp),
                modifier = Modifier.fillMaxSize()
            ) {
                items(agents) { agent ->
                    ObsidianAgentBlock(agent)
                }
            }
        }
    }
}

@Composable
fun ObsidianAgentBlock(agent: AgentStatus) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .height(140.dp)
            .border(
                1.dp,
                Brush.linearGradient(listOf(agent.color.copy(0.4f), Color.Transparent)),
                RoundedCornerShape(32.dp)
            ),
        colors = CardDefaults.cardColors(containerColor = Color(0xFF0F172A).copy(alpha = 0.8f)),
        shape = RoundedCornerShape(32.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 10.dp)
    ) {
        Row(
            modifier = Modifier.padding(24.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // High-Aura Icon with Glow
            Box(
                contentAlignment = Alignment.Center,
                modifier = Modifier
                    .size(64.dp)
                    .background(agent.color.copy(alpha = 0.05f), RoundedCornerShape(20.dp))
                    .border(0.5.dp, agent.color.copy(alpha = 0.2f), RoundedCornerShape(20.dp))
            ) {
                Icon(
                    agent.icon,
                    contentDescription = null,
                    tint = agent.color,
                    modifier = Modifier.size(32.dp)
                )
            }

            Spacer(modifier = Modifier.width(20.dp))

            Column(modifier = Modifier.weight(1f)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(
                        agent.name,
                        color = Color.White,
                        fontSize = 16.sp,
                        fontWeight = FontWeight.ExtraBold,
                        letterSpacing = 1.sp
                    )
                    Spacer(modifier = Modifier.width(12.dp))
                    // Status Badge
                    Surface(
                        color = agent.color.copy(alpha = 0.15f),
                        shape = RoundedCornerShape(100.dp),
                        border = BorderStroke(1.dp, SolidColor(agent.color.copy(0.3f)))
                    ) {
                        Text(
                            agent.status,
                            color = agent.color,
                            fontSize = 8.sp,
                            fontWeight = FontWeight.Black,
                            modifier = Modifier.padding(horizontal = 10.dp, vertical = 2.dp)
                        )
                    }
                }
                Text(
                    agent.role,
                    color = Color.Gray,
                    fontSize = 10.sp,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.padding(top = 4.dp)
                )
                Text(
                    agent.description,
                    color = Color.DarkGray,
                    fontSize = 10.sp,
                    lineHeight = 14.sp,
                    modifier = Modifier.padding(top = 8.dp)
                )
            }
        }
    }
}
