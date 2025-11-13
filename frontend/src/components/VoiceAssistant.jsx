import React, { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import { toast } from 'sonner'
import { 
  Mic, MicOff, Volume2, VolumeX, LogOut, Settings,
  Sparkles, Radio, Zap, ArrowLeft
} from 'lucide-react'

const API_URL = 'http://localhost:8000'

export default function VoiceAssistant({ token, onLogout, user, onBack }) {
  const [isListening, setIsListening] = useState(false)
  const [isSpeaking, setIsSpeaking] = useState(false)
  const [voiceEnabled, setVoiceEnabled] = useState(true)
  const [mounted, setMounted] = useState(false)
  const [sessionId, setSessionId] = useState('')
  const [currentTranscript, setCurrentTranscript] = useState('')
  const [isProcessing, setIsProcessing] = useState(false)
  
  const recognitionRef = useRef(null)
  const synthRef = useRef(null)

  useEffect(() => {
    setSessionId(`voice-session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`)
    setMounted(true)
    initializeVoice()
    
    // Welcome voice message
    setTimeout(() => {
      speakResponse("Hello! I'm AIML Voice, your voice-powered academic assistant. How can I help you today?")
    }, 1000)
  }, [])

  const initializeVoice = () => {
    // Initialize Speech Recognition
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
      recognitionRef.current = new SpeechRecognition()
      recognitionRef.current.continuous = false
      recognitionRef.current.interimResults = true
      recognitionRef.current.lang = 'en-US'

      recognitionRef.current.onstart = () => {
        setIsListening(true)
        setCurrentTranscript('')
        toast.success('Listening... Speak now!')
      }

      recognitionRef.current.onresult = (event) => {
        let transcript = ''
        for (let i = event.resultIndex; i < event.results.length; i++) {
          transcript += event.results[i][0].transcript
        }
        setCurrentTranscript(transcript)
        
        if (event.results[event.results.length - 1].isFinal) {
          handleVoiceInput(transcript)
        }
      }

      recognitionRef.current.onend = () => {
        setIsListening(false)
        setCurrentTranscript('')
      }

      recognitionRef.current.onerror = (event) => {
        setIsListening(false)
        setCurrentTranscript('')
        toast.error('Voice recognition error: ' + event.error)
      }
    } else {
      toast.error('Voice recognition not supported in this browser')
    }

    // Initialize Speech Synthesis
    if ('speechSynthesis' in window) {
      synthRef.current = window.speechSynthesis
    } else {
      toast.error('Speech synthesis not supported in this browser')
    }
  }

  const startListening = () => {
    if (recognitionRef.current && !isListening && !isSpeaking) {
      // Stop any ongoing speech first
      if (synthRef.current) {
        synthRef.current.cancel()
        setIsSpeaking(false)
      }
      recognitionRef.current.start()
    }
  }

  const stopListening = () => {
    if (recognitionRef.current && isListening) {
      recognitionRef.current.stop()
    }
  }

  const handleVoiceInput = async (transcript) => {
    if (!transcript.trim()) return

    setIsProcessing(true)
    toast.info(`Processing: "${transcript}"`)

    try {
      const response = await axios.post(
        `${API_URL}/api/chatbot/chat`,
        {
          message: transcript,
          session_id: sessionId
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      )

      // Only speak the response, don't show text
      if (voiceEnabled) {
        speakResponse(response.data.response)
      }
    } catch (error) {
      console.error('Voice chat error:', error)
      
      if (error.response?.status === 401) {
        toast.error('Session expired. Please login again.')
        setTimeout(() => onLogout(), 2000)
        return
      }
      
      speakResponse("I'm sorry, I encountered an error. Please try again.")
    } finally {
      setIsProcessing(false)
    }
  }

  const speakResponse = (text) => {
    if (!voiceEnabled || !window.speechSynthesis) return
    
    // Stop any ongoing speech
    window.speechSynthesis.cancel()
    
    // Make response more conversational and interactive
    let conversationalText = text
      .replace(/[*#`]/g, '')
      .replace(/\n/g, ' ')
      .replace(/•/g, '')
      .replace(/📅|📚|📝|👨‍🏫|⏰|📊|🎓/g, '')
      .trim()
    
    // Add conversational elements
    const greetings = ['Hello!', 'Hi there!', 'Great question!', 'Let me help you with that.']
    const transitions = ['Here\'s what I found:', 'According to the database:', 'Let me explain:']
    const endings = ['Hope this helps!', 'Is there anything else you\'d like to know?', 'Feel free to ask more questions!']
    
    // Add personality to responses
    if (conversationalText.length > 100) {
      const randomGreeting = greetings[Math.floor(Math.random() * greetings.length)]
      const randomTransition = transitions[Math.floor(Math.random() * transitions.length)]
      const randomEnding = endings[Math.floor(Math.random() * endings.length)]
      
      conversationalText = `${randomGreeting} ${randomTransition} ${conversationalText} ${randomEnding}`
    }
    
    const utterance = new SpeechSynthesisUtterance(conversationalText)
    utterance.rate = 0.85  // Slightly slower for better comprehension
    utterance.pitch = 1.2  // More engaging pitch
    utterance.volume = 0.9
    
    // Add pauses for better flow
    utterance.onboundary = (event) => {
      if (event.name === 'sentence') {
        // Add slight pause between sentences
        setTimeout(() => {}, 200)
      }
    }
    
    utterance.onstart = () => setIsSpeaking(true)
    utterance.onend = () => setIsSpeaking(false)
    utterance.onerror = () => setIsSpeaking(false)
    
    window.speechSynthesis.speak(utterance)
  }

  const stopSpeaking = () => {
    if (synthRef.current) {
      synthRef.current.cancel()
      setIsSpeaking(false)
    }
  }

  const toggleVoice = () => {
    if (voiceEnabled) {
      stopSpeaking()
      setVoiceEnabled(false)
      toast.info('Voice output disabled')
    } else {
      setVoiceEnabled(true)
      toast.success('Voice output enabled')
    }
  }

  return (
    <div className="h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-indigo-900 flex flex-col relative overflow-hidden">
      {/* Enhanced Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        {/* Primary floating orbs */}
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-purple-500/30 to-pink-500/20 rounded-full blur-3xl animate-float"></div>
        <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-gradient-to-tr from-blue-500/25 to-cyan-500/15 rounded-full blur-3xl animate-float-delayed"></div>
        
        {/* Central cosmic glow */}
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-gradient-to-r from-indigo-500/10 via-purple-500/8 to-pink-500/10 rounded-full blur-3xl animate-pulse-slow"></div>
        
        {/* Accent elements */}
        <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-gradient-to-br from-indigo-400/20 to-blue-500/15 rounded-full blur-2xl animate-pulse"></div>
        <div className="absolute top-1/4 right-1/3 w-48 h-48 bg-gradient-to-br from-pink-400/20 to-rose-500/15 rounded-full blur-xl animate-bounce-slow"></div>
        <div className="absolute bottom-1/3 right-1/4 w-32 h-32 bg-gradient-to-br from-cyan-400/25 to-teal-500/20 rounded-full blur-lg animate-float"></div>
        <div className="absolute top-2/3 left-1/3 w-40 h-40 bg-gradient-to-br from-violet-400/20 to-purple-500/15 rounded-full blur-xl animate-float-delayed"></div>
        
        {/* Starfield effect */}
        <div className="absolute inset-0" style={{
          backgroundImage: `radial-gradient(2px 2px at 20px 30px, rgba(255,255,255,0.3), transparent),
                           radial-gradient(2px 2px at 40px 70px, rgba(255,255,255,0.2), transparent),
                           radial-gradient(1px 1px at 90px 40px, rgba(255,255,255,0.4), transparent),
                           radial-gradient(1px 1px at 130px 80px, rgba(255,255,255,0.2), transparent),
                           radial-gradient(2px 2px at 160px 30px, rgba(255,255,255,0.3), transparent)`,
          backgroundRepeat: 'repeat',
          backgroundSize: '200px 100px'
        }}></div>
        
        {/* Floating particles */}
        <div className="absolute top-20 left-20 w-4 h-4 bg-blue-400/30 rounded-full animate-bounce"></div>
        <div className="absolute top-40 right-32 w-3 h-3 bg-purple-400/30 rounded-full animate-bounce delay-300"></div>
        <div className="absolute bottom-32 left-40 w-5 h-5 bg-pink-400/30 rounded-full animate-bounce delay-700"></div>
        <div className="absolute bottom-20 right-20 w-2 h-2 bg-cyan-400/30 rounded-full animate-bounce delay-1000"></div>
      </div>

      {/* Header */}
      <div className={`flex items-center justify-between p-6 relative z-10 transition-all duration-1000 ${mounted ? 'translate-y-0 opacity-100' : '-translate-y-10 opacity-0'}`}>
        <button
          onClick={onBack}
          className="flex items-center gap-2 text-white/80 hover:text-white transition-all hover:scale-105"
        >
          <ArrowLeft className="w-5 h-5" />
          <span className="font-medium">Back to Chat</span>
        </button>
        
        <div className="flex items-center gap-4">
          <div className="text-center">
            <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
              AIML_VOICE
            </h1>
            <p className="text-white/60 text-sm">Voice Academic Assistant</p>
          </div>
        </div>

        <button
          onClick={onLogout}
          className="flex items-center gap-2 bg-red-500/20 hover:bg-red-500/30 text-red-300 px-4 py-2 rounded-xl transition-all border border-red-500/30"
        >
          <LogOut className="w-4 h-4" />
          <span className="hidden sm:inline">Logout</span>
        </button>
      </div>

      {/* Main Voice Interface */}
      <div className="flex-1 flex flex-col items-center justify-center relative z-10 px-8">
        {/* Enhanced Central Voice Orb */}
        <div className={`relative mb-12 transition-all duration-1000 ${mounted ? 'scale-100 opacity-100' : 'scale-50 opacity-0'}`}>
          <div className={`w-80 h-80 rounded-full relative transition-all duration-1000 transform hover:scale-105 ${
            isListening 
              ? 'bg-gradient-to-br from-red-400 via-pink-500 to-rose-600 shadow-2xl shadow-red-500/60 animate-pulse' 
              : isProcessing
              ? 'bg-gradient-to-br from-amber-400 via-orange-500 to-yellow-600 shadow-2xl shadow-orange-500/60 animate-spin-slow'
              : isSpeaking
              ? 'bg-gradient-to-br from-emerald-400 via-green-500 to-teal-600 shadow-2xl shadow-green-500/60 animate-pulse'
              : 'bg-gradient-to-br from-blue-400 via-indigo-500 to-purple-600 shadow-2xl shadow-indigo-500/40'
          }`}>
            <div className="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent rounded-full"></div>
            
            {/* Logo */}
            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
              <img 
                src="/logo.jpg" 
                alt="AIML Logo" 
                className="w-32 h-32 rounded-full object-cover border-4 border-white/30"
              />
            </div>
            
            {/* Voice visualizer */}
            {isListening && (
              <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 flex gap-1">
                <div className="w-2 h-8 bg-white/80 rounded-full animate-pulse"></div>
                <div className="w-2 h-12 bg-white/80 rounded-full animate-pulse delay-100"></div>
                <div className="w-2 h-6 bg-white/80 rounded-full animate-pulse delay-200"></div>
                <div className="w-2 h-10 bg-white/80 rounded-full animate-pulse delay-300"></div>
                <div className="w-2 h-4 bg-white/80 rounded-full animate-pulse delay-400"></div>
              </div>
            )}
            
            {/* Speaking indicator */}
            {isSpeaking && (
              <div className="absolute top-8 left-1/2 transform -translate-x-1/2">
                <Volume2 className="w-8 h-8 text-white animate-pulse" />
              </div>
            )}
            
            {/* Processing indicator */}
            {isProcessing && (
              <div className="absolute top-8 right-8">
                <Zap className="w-6 h-6 text-white animate-spin" />
              </div>
            )}
          </div>
        </div>

        {/* Control Buttons */}
        <div className={`flex items-center gap-6 transition-all duration-700 delay-500 ${mounted ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`}>
          {/* Voice Toggle */}
          <button
            onClick={toggleVoice}
            className={`p-4 rounded-2xl transition-all transform hover:scale-110 ${
              voiceEnabled 
                ? 'bg-green-500/20 border-2 border-green-400/50 text-green-300' 
                : 'bg-red-500/20 border-2 border-red-400/50 text-red-300'
            }`}
            title={voiceEnabled ? 'Voice On' : 'Voice Off'}
          >
            {voiceEnabled ? <Volume2 className="w-6 h-6" /> : <VolumeX className="w-6 h-6" />}
          </button>

          {/* Main Microphone Button */}
          <button
            onClick={isListening ? stopListening : startListening}
            disabled={isSpeaking || isProcessing}
            className={`p-8 rounded-full transition-all transform hover:scale-110 disabled:opacity-50 disabled:cursor-not-allowed ${
              isListening 
                ? 'bg-red-500 shadow-2xl shadow-red-500/50 animate-pulse' 
                : 'bg-gradient-to-br from-blue-500 to-purple-600 shadow-2xl shadow-blue-500/50 hover:shadow-purple-500/50'
            }`}
          >
            {isListening ? <MicOff className="w-12 h-12 text-white" /> : <Mic className="w-12 h-12 text-white" />}
          </button>

          {/* Stop Speaking */}
          <button
            onClick={stopSpeaking}
            disabled={!isSpeaking}
            className="p-4 rounded-2xl bg-orange-500/20 border-2 border-orange-400/50 text-orange-300 transition-all transform hover:scale-110 disabled:opacity-50 disabled:cursor-not-allowed"
            title="Stop Speaking"
          >
            <Radio className="w-6 h-6" />
          </button>
        </div>

      </div>
    </div>
  )
}