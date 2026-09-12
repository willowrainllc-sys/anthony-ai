package com.obsidian.global.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun NativeRegistrarDashboardScreen(
    onNavigateBrowser: (String) -> Unit
) {
    var searchQuery by remember { mutableStateOf("") }
    var selectedTab by remember { mutableIntStateOf(0) }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFF030305))
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(bottom = 72.dp) // Space for bottom nav
        ) {
            // Native App Header
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(Color(0xFF0A0A0F))
                    .padding(horizontal = 20.dp, vertical = 16.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "OBSIDIAN.CITY",
                    color = Color.White,
                    fontSize = 18.sp,
                    fontWeight = FontWeight.Black
                )
                Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                    Icon(
                        Icons.Default.ShoppingCart,
                        contentDescription = "Cart",
                        tint = Color.White,
                        modifier = Modifier.clickable { onNavigateBrowser("https://obsidian.city/obsidian_unified_checkout.html") }
                    )
                    Icon(
                        Icons.Default.Person,
                        contentDescription = "Account",
                        tint = Color.White,
                        modifier = Modifier.clickable { onNavigateBrowser("https://obsidian.city/obsidian_signin.html") }
                    )
                }
            }

            // Scrollable Native Content
            LazyColumn(
                modifier = Modifier
                    .fillMaxWidth()
                    .weight(1f)
                    .padding(20.dp),
                verticalArrangement = Arrangement.spacedBy(20.dp)
            ) {
                // Native Domain Search Card
                item {
                    Card(
                        shape = RoundedCornerShape(24.dp),
                        colors = CardDefaults.cardColors(containerColor = Color(0xFF0F0F17)),
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Column(modifier = Modifier.padding(20.dp)) {
                            Text(
                                text = "Secure Your Domain",
                                color = Color.White,
                                fontSize = 22.sp,
                                fontWeight = FontWeight.Bold,
                                modifier = Modifier.padding(bottom = 8.dp)
                            )
                            Text(
                                text = "Get a .com for just $0.01 for the 1st year with free lifetime privacy protection.",
                                color = Color(0xFF94A3B8),
                                fontSize = 12.sp,
                                modifier = Modifier.padding(bottom = 16.dp)
                            )
                            OutlinedTextField(
                                value = searchQuery,
                                onValueChange = { searchQuery = it },
                                placeholder = { Text("Search domain (e.g. mybusiness.com)", color = Color(0xFF64748B)) },
                                singleLine = true,
                                shape = RoundedCornerShape(16.dp),
                                colors = OutlinedTextFieldDefaults.colors(
                                    focusedBorderColor = Color(0xFF3B82F6),
                                    unfocusedBorderColor = Color(0xFF334155),
                                    focusedTextColor = Color.White,
                                    unfocusedTextColor = Color.White
                                ),
                                modifier = Modifier.fillMaxWidth()
                            )
                            Spacer(modifier = Modifier.height(12.dp))
                            Button(
                                onClick = { onNavigateBrowser("https://obsidian.city/obsidian_domain_results.html?q=$searchQuery") },
                                shape = RoundedCornerShape(16.dp),
                                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2563EB)),
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .height(50.dp)
                            ) {
                                Text("Search Domains", fontSize = 14.sp, fontWeight = FontWeight.Bold)
                            }
                        }
                    }
                }

                // Native Product Cards
                item {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(16.dp)
                    ) {
                        Card(
                            shape = RoundedCornerShape(20.dp),
                            colors = CardDefaults.cardColors(containerColor = Color(0xFF0F0F17)),
                            modifier = Modifier
                                .weight(1f)
                                .clickable { onNavigateBrowser("https://obsidian.city/obsidian_hosting_landing.html") }
                        ) {
                            Column(modifier = Modifier.padding(16.dp)) {
                                Text("⚡", fontSize = 24.sp)
                                Spacer(modifier = Modifier.height(8.dp))
                                Text("Cloud Hosting", color = Color.White, fontSize = 14.sp, fontWeight = FontWeight.Bold)
                                Text("From $5.99/mo", color = Color(0xFF34D399), fontSize = 11.sp, fontWeight = FontWeight.SemiBold)
                            }
                        }

                        Card(
                            shape = RoundedCornerShape(20.dp),
                            colors = CardDefaults.cardColors(containerColor = Color(0xFF0F0F17)),
                            modifier = Modifier
                                .weight(1f)
                                .clickable { onNavigateBrowser("https://obsidian.city/obsidian_airo_builder.html") }
                        ) {
                            Column(modifier = Modifier.padding(16.dp)) {
                                Text("🤖", fontSize = 24.sp)
                                Spacer(modifier = Modifier.height(8.dp))
                                Text("Obsidian Leo AI", color = Color.White, fontSize = 14.sp, fontWeight = FontWeight.Bold)
                                Text("Prompt to App", color = Color(0xFF3B82F6), fontSize = 11.sp, fontWeight = FontWeight.SemiBold)
                            }
                        }
                    }
                }
            }
        }

        // Native App Bottom Navigation Bar
        Surface(
            color = Color(0xFF0A0A0F),
            shadowElevation = 8.dp,
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .fillMaxWidth()
                .height(72.dp)
        ) {
            Row(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(horizontal = 24.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    modifier = Modifier.clickable { selectedTab = 0 }
                ) {
                    Icon(Icons.Default.Home, contentDescription = "Home", tint = if (selectedTab == 0) Color(0xFF3B82F6) else Color(0xFF64748B))
                    Text("Home", color = if (selectedTab == 0) Color(0xFF3B82F6) else Color(0xFF64748B), fontSize = 10.sp, fontWeight = FontWeight.Bold)
                }

                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    modifier = Modifier.clickable { selectedTab = 1; onNavigateBrowser("https://obsidian.city/obsidian_domains.html") }
                ) {
                    Icon(Icons.Default.Search, contentDescription = "Search", tint = if (selectedTab == 1) Color(0xFF3B82F6) else Color(0xFF64748B))
                    Text("Domains", color = if (selectedTab == 1) Color(0xFF3B82F6) else Color(0xFF64748B), fontSize = 10.sp, fontWeight = FontWeight.Bold)
                }

                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    modifier = Modifier.clickable { selectedTab = 2; onNavigateBrowser("https://obsidian.city/obsidian_unified_checkout.html") }
                ) {
                    Icon(Icons.Default.ShoppingCart, contentDescription = "Cart", tint = if (selectedTab == 2) Color(0xFF3B82F6) else Color(0xFF64748B))
                    Text("Basket", color = if (selectedTab == 2) Color(0xFF3B82F6) else Color(0xFF3B82F6), fontSize = 10.sp, fontWeight = FontWeight.Bold)
                }

                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    modifier = Modifier.clickable { selectedTab = 3; onNavigateBrowser("https://obsidian.city/obsidian_signin.html") }
                ) {
                    Icon(Icons.Default.Person, contentDescription = "Account", tint = if (selectedTab == 3) Color(0xFF3B82F6) else Color(0xFF64748B))
                    Text("Account", color = if (selectedTab == 3) Color(0xFF3B82F6) else Color(0xFF64748B), fontSize = 10.sp, fontWeight = FontWeight.Bold)
                }
            }
        }
    }
}
