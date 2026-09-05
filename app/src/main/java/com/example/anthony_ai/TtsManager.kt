package com.example.anthony_ai

import android.content.Context
import android.speech.tts.TextToSpeech
import android.util.Log
import java.util.Locale

class TtsManager(context: Context) : TextToSpeech.OnInitListener {
    private var tts: TextToSpeech? = TextToSpeech(context, this)
    private var isInitialized = false
    var onFinishedSpeaking: (() -> Unit)? = null

    private var sentenceBuffer = StringBuilder()

    override fun onInit(status: Int) {
        if (status == TextToSpeech.SUCCESS) {
            val result = tts?.setLanguage(Locale.US)
            
            // Specifically look for a male voice
            val voices = tts?.voices
            val maleVoice = voices?.find { 
                it.name.lowercase().contains("male") || 
                it.name.lowercase().contains("en-us-x-sfg-local") ||
                it.name.lowercase().contains("en-us-x-iol-local")
            }
            if (maleVoice != null) {
                tts?.voice = maleVoice
                Log.d("TTS_MANAGER", "Set voice to: ${maleVoice.name}")
            } else {
                Log.w("TTS_MANAGER", "No specific male voice found, using system default")
            }

            if ((result == TextToSpeech.LANG_MISSING_DATA) || (result == TextToSpeech.LANG_NOT_SUPPORTED)) {
                Log.e("TTS_MANAGER", "Language not supported")
            } else {
                isInitialized = true
                setupProgressListener()
            }
        } else {
            Log.e("TTS_MANAGER", "Initialization failed")
        }
    }

    private fun setupProgressListener() {
        tts?.setOnUtteranceProgressListener(object : android.speech.tts.UtteranceProgressListener() {
            override fun onStart(utteranceId: String?) {}
            override fun onDone(utteranceId: String?) {
                if (utteranceId == "FINISH_SENTENCE") {
                    onFinishedSpeaking?.invoke()
                }
            }
            @Deprecated("Deprecated in Java")
            override fun onError(utteranceId: String?) {}
        })
    }

    /**
     * Appends text to a buffer and speaks only when a full sentence is formed.
     * This avoids choppy audio during streaming.
     */
    fun speakStream(text: String, isStatus: Boolean = false) {
        if (isStatus) {
            speak(text, queueMode = TextToSpeech.QUEUE_ADD)
            return
        }
        
        sentenceBuffer.append(text)
        val fullText = sentenceBuffer.toString()
        
        // Check for sentence delimiters: . ! ?
        val lastDelimiterIndex = fullText.findLastAnyOf(listOf(".", "!", "?"))?.first ?: -1
        
        if (lastDelimiterIndex != -1) {
            val toSpeak = fullText.substring(0, lastDelimiterIndex + 1)
            val remaining = fullText.substring(lastDelimiterIndex + 1)
            
            speak(toSpeak, queueMode = TextToSpeech.QUEUE_ADD)
            sentenceBuffer = StringBuilder(remaining)
        }
    }

    fun speak(text: String, queueMode: Int = TextToSpeech.QUEUE_FLUSH, utteranceId: String? = null) {
        if (isInitialized && text.isNotBlank()) {
            val params = android.os.Bundle()
            params.putString(TextToSpeech.Engine.KEY_PARAM_UTTERANCE_ID, utteranceId ?: "SENTENCE")
            tts?.speak(text, queueMode, params, utteranceId ?: "SENTENCE")
        } else if (!isInitialized) {
            Log.e("TTS_MANAGER", "TTS not initialized yet")
        }
    }

    fun flushBuffer() {
        val remaining = sentenceBuffer.toString()
        if (remaining.isNotBlank()) {
            speak(remaining, queueMode = TextToSpeech.QUEUE_ADD, utteranceId = "FINISH_SENTENCE")
            sentenceBuffer.clear()
        } else {
            // Signal finished even if buffer is empty
            onFinishedSpeaking?.invoke()
        }
    }

    fun stop() {
        tts?.stop()
    }

    fun destroy() {
        tts?.shutdown()
    }
}
