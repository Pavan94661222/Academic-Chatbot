import React, { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import { toast } from 'sonner'
import { 
  Send, Bot, User, Loader2, Sparkles, LogOut, 
  Calendar, BookOpen, Users, Clock, Menu, X,
  MessageCircle, Zap, Star, CheckCircle, ArrowRight,
  Mic, MicOff, Volume2, VolumeX, Headphones, Radio, Maximize, History 
} from 'lucide-react'
import VoiceAssistant from './VoiceAssistant'

const API_URL = 'http://localhost:8000'

export default function ChatInterface({ token, onLogout, user, setUser }) {
  const [messages, setMessages] = useState([])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [sessionId, setSessionId] = useState('')
  const [quickActions, setQuickActions] = useState([])
  const [showSidebar, setShowSidebar] = useState(false)
  const [mounted, setMounted] = useState(false)
  const [showFullscreenVoice, setShowFullscreenVoice] = useState(false)
  const [showHistory, setShowHistory] = useState(false)
  const [chatHistory, setChatHistory] = useState([])
  const messagesEndRef = useRef(null)

  useEffect(() => {
    setSessionId(`session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`)
    loadQuickActions()
    fetchUserInfo()
    setMounted(true)
    
    // Welcome message
    setTimeout(() => {
      setMessages([{
        id: '1',
        type: 'bot',
        content: "Hello! I'm your AIML Academic Assistant 🎓\n\nI can help you with:\n• Class timetables 📅\n• Course information 📚\n• Exam schedules 📝\n• Faculty details 👨‍🏫\n• Assignment deadlines ⏰\n• Academic policies 📊\n\nWhat would you like to know?",
        timestamp: new Date().toISOString(),
        intent: 'greeting'
      }])
    }, 500)
  }, [])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }


  const fetchUserInfo = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/auth/me`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setUser(response.data)
    } catch (error) {
      console.error('Failed to fetch user info:', error)
      if (error.response?.status === 401) {
        toast.error('Session expired. Please login again.')
        setTimeout(() => onLogout(), 2000)
      }
    }
  }

  const loadChatHistory = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/chatbot/history?limit=20`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setChatHistory(response.data.history || [])
    } catch (error) {
      console.error('Failed to load chat history:', error)
    }
  }

  const loadQuickActions = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/chatbot/quick-actions`)
      setQuickActions(response.data.actions)
    } catch (error) {
      console.error('Failed to load quick actions:', error)
    }
  }

  const sendMessage = async (messageText) => {
    if (!messageText.trim()) return

    const userMessage = {
      id: `user-${Date.now()}`,
      type: 'user',
      content: messageText,
      timestamp: new Date().toISOString()
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsLoading(true)

    try {
      const response = await axios.post(
        `${API_URL}/api/chatbot/chat`,
        {
          message: messageText,
          session_id: sessionId
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      )

      const botMessage = {
        id: `bot-${Date.now()}`,
        type: 'bot',
        content: response.data.response,
        timestamp: response.data.timestamp,
        intent: response.data.intent
      }

      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      console.error('Chat error:', error)
      
      if (error.response?.status === 401) {
        toast.error('Session expired. Please login again.')
        setTimeout(() => onLogout(), 2000)
        return
      }
      
      toast.error('Failed to get response. Please try again.')
      
      const errorMessage = {
        id: `error-${Date.now()}`,
        type: 'bot',
        content: "I'm sorry, I encountered an error. Please try again or rephrase your question.",
        timestamp: new Date().toISOString()
      }
      
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    sendMessage(inputMessage)
  }

  const handleQuickAction = (query) => {
    sendMessage(query)
  }

  const formatMessage = (content) => {
    // Remove asterisks and clean up the content
    const cleanContent = content
      .replace(/\*\*/g, '') // Remove all double asterisks
      .replace(/\*/g, '') // Remove all single asterisks
      .replace(/#{1,6}\s/g, '') // Remove markdown headers
      .trim()

    return cleanContent.split('\n').map((line, i) => {
      const trimmedLine = line.trim()
      
      if (trimmedLine.startsWith('•') || trimmedLine.startsWith('-')) {
        return (
          <div key={i} className="flex items-start gap-2 mb-2">
            <CheckCircle className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
            <span className="text-sm leading-relaxed">{trimmedLine.substring(1).trim()}</span>
          </div>
        )
      } else if (trimmedLine.includes(':') && trimmedLine.length < 100) {
        // Treat as headers/labels
        return (
          <div key={i} className="flex items-center gap-2 mt-3 mb-2 first:mt-0">
            <Star className="w-4 h-4 text-blue-500" />
            <strong className="text-sm font-semibold text-gray-800">{trimmedLine}</strong>
          </div>
        )
      } else if (trimmedLine.length > 0) {
        return (
          <p key={i} className="text-sm leading-relaxed mb-2 text-gray-700">
            {trimmedLine}
          </p>
        )
      }
      return <div key={i} className="h-2" />
    })
  }

  const getQuickActionIcon = (label) => {
    if (label.includes('Timetable')) return <Calendar className="w-4 h-4" />
    if (label.includes('Exam')) return <Clock className="w-4 h-4" />
    if (label.includes('Faculty')) return <Users className="w-4 h-4" />
    if (label.includes('Courses')) return <BookOpen className="w-4 h-4" />
    return <Sparkles className="w-4 h-4" />
  }

  // Show fullscreen voice assistant if requested
  if (showFullscreenVoice) {
    return (
      <VoiceAssistant 
        token={token} 
        onLogout={onLogout} 
        user={user} 
        onBack={() => setShowFullscreenVoice(false)}
      />
    )
  }

  return (
    <div className="h-screen flex flex-col bg-gradient-to-br from-blue-50/50 via-indigo-50/30 to-purple-50/50">
      {/* Enhanced Background Elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        {/* Primary floating orbs */}
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-blue-400/30 to-purple-600/30 rounded-full blur-3xl animate-float"></div>
        <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-gradient-to-tr from-indigo-400/25 to-pink-500/25 rounded-full blur-3xl animate-float-delayed"></div>
        
        {/* Central glow */}
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-gradient-to-r from-cyan-300/8 to-blue-500/8 rounded-full blur-3xl animate-pulse-slow"></div>
        
        {/* Accent orbs */}
        <div className="absolute top-20 left-20 w-32 h-32 bg-gradient-to-br from-yellow-400/40 to-orange-500/40 rounded-full blur-xl animate-bounce-slow"></div>
        <div className="absolute bottom-20 right-20 w-40 h-40 bg-gradient-to-br from-green-400/35 to-teal-500/35 rounded-full blur-xl animate-float"></div>
        <div className="absolute top-1/3 right-1/4 w-24 h-24 bg-gradient-to-br from-pink-400/45 to-rose-500/45 rounded-full blur-lg animate-pulse-slow"></div>
        
        {/* Additional floating elements */}
        <div className="absolute top-3/4 left-1/4 w-20 h-20 bg-gradient-to-br from-violet-400/30 to-purple-500/30 rounded-full blur-md animate-float-delayed"></div>
        <div className="absolute top-1/4 left-3/4 w-28 h-28 bg-gradient-to-br from-emerald-400/25 to-cyan-500/25 rounded-full blur-lg animate-bounce-slow"></div>
        
        {/* Subtle grid pattern */}
        <div className="absolute inset-0 bg-gradient-to-br from-blue-50/5 via-transparent to-purple-50/5"></div>
        <div className="absolute inset-0" style={{
          backgroundImage: `radial-gradient(circle at 25% 25%, rgba(59, 130, 246, 0.05) 0%, transparent 50%), 
                           radial-gradient(circle at 75% 75%, rgba(147, 51, 234, 0.05) 0%, transparent 50%)`
        }}></div>
      </div>

      {/* Header */}
      <div className={`bg-white/80 backdrop-blur-lg border-b border-white/20 shadow-lg relative z-10 transition-all duration-700 ${mounted ? 'translate-y-0 opacity-100' : '-translate-y-10 opacity-0'}`}>
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="relative">
                <img 
                  src="/logo.jpg" 
                  alt="AIML Logo" 
                  className="w-14 h-14 rounded-2xl shadow-lg object-cover border-2 border-white/50 hover:scale-110 transition-all duration-300"
                />
                <div className="absolute -top-1 -right-1 w-4 h-4 bg-gradient-to-r from-green-400 to-blue-500 rounded-full flex items-center justify-center shadow-lg animate-pulse">
                  <Sparkles className="w-2 h-2 text-white" />
                </div>
              </div>
              <div>
                <h1 className="text-2xl font-bold flex items-center gap-2 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
                  AIML Academic Assistant
                  <Radio className="w-5 h-5 text-purple-500 animate-pulse" />
                </h1>
                <p className="text-gray-600 text-sm font-medium">
                  GAT - Department of AI & ML
                </p>
              </div>
            </div>
            
            {/* Tab Navigation */}
            <div className="flex items-center gap-2 bg-white/60 backdrop-blur-sm rounded-xl p-1 border border-white/30">
              <button
                className="flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all bg-gradient-to-r from-blue-500 to-indigo-600 text-white shadow-lg"
              >
                <MessageCircle className="w-4 h-4" />
                <span className="hidden sm:inline">CHAT</span>
              </button>
              
              {/* Fullscreen Voice Button */}
              <button
                onClick={() => setShowFullscreenVoice(true)}
                className="flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all bg-gradient-to-r from-indigo-500 to-purple-600 text-white shadow-lg hover:shadow-xl transform hover:scale-105"
                title="Open AIML_VOICE Fullscreen"
              >
                <Maximize className="w-4 h-4" />
                <span className="hidden sm:inline">AIML VOICE</span>
              </button>
            </div>

            <div className="flex items-center gap-4">
              <button
                onClick={() => {
                  setShowHistory(!showHistory)
                  if (!showHistory) loadChatHistory()
                }}
                className="p-3 bg-blue-500/80 hover:bg-blue-600 text-white rounded-xl backdrop-blur-sm transition-all hover:scale-105 shadow-lg"
                title="Chat History"
              >
                <History className="w-5 h-5" />
              </button>
              {user && (
                <div className="text-right hidden md:block bg-white/60 backdrop-blur-sm rounded-xl px-4 py-2 border border-white/30">
                  <p className="font-semibold text-gray-800">{user.full_name}</p>
                  <p className="text-xs text-gray-600">{user.email}</p>
                </div>
              )}
              <button
                onClick={onLogout}
                className="p-3 bg-red-500/80 hover:bg-red-600 text-white rounded-xl backdrop-blur-sm transition-all hover:scale-105 shadow-lg"
                title="Logout"
              >
                <LogOut className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Chat History Sidebar */}
      {showHistory && (
        <div className="fixed right-0 top-0 h-full w-80 bg-white/95 backdrop-blur-lg shadow-2xl z-50 transform transition-transform duration-300">
          <div className="p-4 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold text-gray-800">Chat History</h3>
              <button
                onClick={() => setShowHistory(false)}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {chatHistory.length > 0 ? (
              chatHistory.map((chat, index) => (
                <div key={chat.id || index} className="p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer">
                  <p className="text-sm font-medium text-gray-800 truncate">{chat.user_message}</p>
                  <p className="text-xs text-gray-600 mt-1 line-clamp-2">{chat.bot_response}</p>
                  <p className="text-xs text-gray-400 mt-2">
                    {new Date(chat.created_at).toLocaleDateString()} {new Date(chat.created_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                  </p>
                </div>
              ))
            ) : (
              <div className="text-center text-gray-500 mt-8">
                <History className="w-12 h-12 mx-auto mb-3 opacity-50" />
                <p>No chat history yet</p>
                <p className="text-sm">Start a conversation to see your history here</p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Main Chat Area */}
      <div className={`flex-1 overflow-hidden flex flex-col max-w-7xl mx-auto w-full transition-all duration-300 ${showHistory ? 'mr-80' : ''}`}>
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-6 relative z-10">
          {messages.map((message, index) => (
            <div
              key={message.id}
              className={`flex gap-4 ${message.type === 'user' ? 'justify-end' : 'justify-start'} animate-message-in`}
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              {message.type === 'bot' && (
                <div className="flex-shrink-0 w-12 h-12 rounded-2xl bg-gradient-to-br from-blue-500 via-indigo-600 to-purple-600 flex items-center justify-center shadow-xl relative overflow-hidden group">
                  <div className="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent"></div>
                  <Bot className="w-7 h-7 text-white relative z-10 group-hover:scale-110 transition-transform" />
                  <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-400 rounded-full border-2 border-white animate-pulse"></div>
                </div>
              )}
              <div
                className={`max-w-4xl p-6 rounded-3xl shadow-xl backdrop-blur-lg relative overflow-hidden group transition-all duration-500 hover:shadow-2xl hover:scale-[1.02] ${
                  message.type === 'user' 
                    ? 'bg-gradient-to-br from-blue-500 via-indigo-600 to-purple-600 text-white ml-8 shadow-blue-500/25' 
                    : 'bg-white/95 text-gray-800 mr-8 border border-white/40 shadow-purple-500/10'
                }`}
              >
                <div className="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent pointer-events-none"></div>
                <div className="relative z-10 p-5">
                  <div className="leading-relaxed">
                    {formatMessage(message.content)}
                  </div>
                  <div className={`flex items-center gap-2 text-xs mt-3 pt-2 border-t ${message.type === 'user' ? 'text-blue-100 border-white/20' : 'text-gray-500 border-gray-200'}`}>
                    <Clock className="w-3 h-3" />
                    {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </div>
                </div>
              </div>
              {message.type === 'user' && (
                <div className="flex-shrink-0 w-12 h-12 rounded-2xl bg-gradient-to-br from-gray-600 to-gray-800 flex items-center justify-center shadow-xl relative overflow-hidden group">
                  <div className="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent"></div>
                  <User className="w-7 h-7 text-white relative z-10 group-hover:scale-110 transition-transform" />
                </div>
              )}
            </div>
          ))}
          
          {isLoading && (
            <div className="flex gap-4 justify-start animate-message-in">
              <div className="flex-shrink-0 w-12 h-12 rounded-2xl bg-gradient-to-br from-blue-500 via-indigo-600 to-purple-600 flex items-center justify-center shadow-xl relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent"></div>
                <Bot className="w-7 h-7 text-white relative z-10" />
                <div className="absolute -top-1 -right-1 w-4 h-4 bg-yellow-400 rounded-full border-2 border-white animate-pulse"></div>
              </div>
              <div className="bg-white/90 backdrop-blur-sm border border-white/30 rounded-2xl p-5 shadow-xl relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent pointer-events-none"></div>
                <div className="flex items-center gap-3 relative z-10">
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce delay-100"></div>
                    <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce delay-200"></div>
                  </div>
                  <span className="text-sm text-gray-600 font-medium">AI is thinking...</span>
                  <Zap className="w-4 h-4 text-yellow-500 animate-pulse" />
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
        {/* Input Area */}
        <form onSubmit={handleSubmit} className="p-4 md:p-6 bg-white/70 backdrop-blur-lg border-t border-white/20 relative z-10">
          <div className="flex gap-4 max-w-7xl mx-auto">
            <div className="flex-1 relative group">
              <input
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="Ask me anything about courses, schedules, exams..."
                disabled={isLoading}
                className="w-full px-6 py-4 rounded-2xl border-2 border-white/30 focus:border-blue-500 focus:ring-4 focus:ring-blue-500/20 transition-all bg-white/60 backdrop-blur-sm focus:bg-white/80 outline-none text-gray-800 placeholder-gray-500 shadow-lg"
              />
              <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-blue-500/5 to-purple-500/5 opacity-0 group-focus-within:opacity-100 transition-opacity pointer-events-none"></div>
            </div>
            
            <button
              type="submit"
              disabled={isLoading || !inputMessage.trim()}
              className="px-8 py-4 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 hover:from-blue-700 hover:via-indigo-700 hover:to-purple-700 text-white rounded-2xl shadow-xl hover:shadow-2xl transition-all disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-105 relative overflow-hidden group"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-white/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <div className="relative z-10 flex items-center gap-2">
                {isLoading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    <span className="hidden sm:inline font-medium">Sending...</span>
                  </>
                ) : (
                  <>
                    <Send className="w-5 h-5" />
                    <span className="hidden sm:inline font-medium">Send</span>
                  </>
                )}
              </div>
            </button>
          </div>
        </form>
      </div>

      <style jsx>{`
        @keyframes message-in {
          from {
            opacity: 0;
            transform: translateY(20px) scale(0.95);
          }
          to {
            opacity: 1;
            transform: translateY(0) scale(1);
          }
        }
        
        @keyframes float {
          0%, 100% { transform: translateY(0px) rotate(0deg) scale(1); }
          33% { transform: translateY(-15px) rotate(120deg) scale(1.02); }
          66% { transform: translateY(-25px) rotate(240deg) scale(0.98); }
        }
        
        @keyframes float-delayed {
          0%, 100% { transform: translateY(0px) rotate(0deg) scale(1); }
          25% { transform: translateY(-20px) rotate(-90deg) scale(1.05); }
          75% { transform: translateY(-35px) rotate(-270deg) scale(0.95); }
        }
        
        @keyframes bounce-slow {
          0%, 100% { transform: translateY(0px) scale(1) rotate(0deg); }
          50% { transform: translateY(-15px) scale(1.1) rotate(5deg); }
        }
        
        @keyframes pulse-slow {
          0%, 100% { opacity: 0.6; transform: scale(1); }
          50% { opacity: 1; transform: scale(1.05); }
        }
        
        .animate-message-in {
          animation: message-in 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
        }
        
        .animate-float {
          animation: float 12s ease-in-out infinite;
        }
        
        .animate-float-delayed {
          animation: float-delayed 15s ease-in-out infinite;
        }
        
        .animate-bounce-slow {
          animation: bounce-slow 6s ease-in-out infinite;
        }
        
        .animate-pulse-slow {
          animation: pulse-slow 4s ease-in-out infinite;
        }
      `}</style>
    </div>
  )
}
