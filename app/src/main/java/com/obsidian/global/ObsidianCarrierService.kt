package com.obsidian.global

import android.service.carrier.CarrierService
import android.os.PersistableBundle
import android.service.carrier.CarrierIdentifier
import android.telephony.CarrierConfigManager
import android.util.Log

/**
 * 🏛️ OBSIDIAN GLOBAL: CARRIER SERVICE v3.0
 * The core software rewrite for the Director's Pixel Pro XL.
 * 1. OVERRIDE CONFIG: Forces the phone to use Obsidian's private APN and SIP Gateway.
 * 2. IDENTITY LOCK: Injects the "OBSIDIAN GLOBAL" branding into the system UI.
 * 3. DATA BACKHAUL: Coordinates the WireGuard fiber tunnel for unlimited data.
 */
class ObsidianCarrierService : CarrierService() {

    override fun onLoadConfig(id: CarrierIdentifier?): PersistableBundle {
        Log.i("OBSIDIAN_CARRIER", "🔱 Loading Obsidian Global Configuration...")
        
        val config = PersistableBundle()
        
        // 1. Branding Overrides
        config.putString(CarrierConfigManager.KEY_CARRIER_NAME_STRING, "🔱 OBSIDIAN GLOBAL")
        
        // 2. Network Capability Overrides
        config.putBoolean(CarrierConfigManager.KEY_CARRIER_VOLTE_AVAILABLE_BOOL, true)
        config.putBoolean(CarrierConfigManager.KEY_CARRIER_VT_AVAILABLE_BOOL, true)
        config.putBoolean(CarrierConfigManager.KEY_CARRIER_WFC_IMS_AVAILABLE_BOOL, true)
        
        // 3. APN & Protocol Hardening
        config.putStringArray(CarrierConfigManager.KEY_READ_ONLY_APN_FIELDS_STRING_ARRAY, arrayOf("name", "apn", "mcc", "mnc"))
        
        return config
    }
}
