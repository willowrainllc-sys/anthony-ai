# Implementation Plan - Anthony AI Video Feed Integration

Integrate the Jetpack Compose video feed UI and connect it to the backend content pipeline (n8n/API).

## User Review Required

> [!IMPORTANT]
> The provided `MainActivity.kt` used package `com.example.anthonyai`. I will use the project's existing package `com.example.anthony_ai` to avoid build errors.
> I will integrate the new components into your **existing** `MainActivity.kt` to preserve your BLE, Voice, and Chat logic.

## Proposed Changes

### [Component] Dependencies
#### [MODIFY] [build.gradle.kts](file:///C:/Users/willo/OneDrive/Desktop/Anthony_Ai/app/build.gradle.kts)
- Add Media3 ExoPlayer and UI dependencies for video playback.

### [Component] Data Layer
#### [NEW] [AIVideo.kt](file:///C:/Users/willo/OneDrive/Desktop/Anthony_Ai/app/src/main/java/com/example/anthony_ai/data/model/AIVideo.kt)
- Define the `AIVideo` data class matching the backend JSON schema.

### [Component] UI Layer
#### [MODIFY] [MainActivity.kt](file:///C:/Users/willo/OneDrive/Desktop/Anthony_Ai/app/src/main/java/com/example/anthony_ai/MainActivity.kt)
- Add `AIVideoCard`, `TopHeader`, and `CategoryTabs` composables.
- Implement a `VideoPlayer` component using `ExoPlayer`.
- Update `HomeScreen` to display the scrollable AI video feed.
- Wire the "Play" button on video cards to launch the player.

## Verification Plan

### Automated Tests
- Gradle build to verify dependency integration.

### Manual Verification
- Deploy to device/emulator.
- Verify the "Anthony AI" header and category tabs are visible.
- Verify video thumbnails load via Coil.
- Verify tapping the Play button opens/starts video playback (using a sample URL).
