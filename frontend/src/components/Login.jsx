import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { toast } from 'sonner'
import { Bot, Mail, Lock, User, GraduationCap, LogIn, UserPlus, Sparkles, BookOpen, Brain } from 'lucide-react'

const API_URL = 'http://localhost:8000'

export default function Login({ onLogin }) {
  const [isRegister, setIsRegister] = useState(false)
  const [loading, setLoading] = useState(false)
  const [mounted, setMounted] = useState(false)
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    email: '',
    full_name: '',
    usn: ''
  })

  useEffect(() => {
    setMounted(true)
  }, [])

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      const endpoint = isRegister ? '/api/auth/register' : '/api/auth/login'
      const payload = isRegister 
        ? formData 
        : { username: formData.username, password: formData.password }

      const response = await axios.post(`${API_URL}${endpoint}`, payload)
      
      toast.success(isRegister ? 'Registration successful!' : 'Login successful!')
      onLogin(response.data.access_token)
    } catch (error) {
      console.error('Auth error:', error)
      toast.error(error.response?.data?.detail || 'Authentication failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center p-4 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-blue-400/20 to-indigo-400/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-br from-purple-400/20 to-pink-400/20 rounded-full blur-3xl animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-gradient-to-br from-indigo-400/10 to-blue-400/10 rounded-full blur-3xl animate-pulse delay-500"></div>
      </div>

      <div className={`w-full max-w-md relative z-10 transition-all duration-1000 ${mounted ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`}>
        {/* Header */}
        <div className="text-center mb-8">
          <div className={`relative mb-6 transition-all duration-1000 ${mounted ? 'scale-100 rotate-0' : 'scale-50 rotate-180'}`}>
            <div className="absolute inset-0 bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500 rounded-full blur-2xl opacity-75 animate-pulse"></div>
            <div className="relative w-32 h-32 mx-auto">
              <img 
                src="/logo.jpg" 
                alt="AIML Logo" 
                className="w-full h-full rounded-3xl shadow-2xl object-cover border-4 border-white/50 backdrop-blur-sm hover:scale-110 transition-all duration-500"
              />
              <div className="absolute -top-2 -right-2 w-8 h-8 bg-gradient-to-r from-green-400 to-blue-500 rounded-full flex items-center justify-center shadow-lg animate-bounce">
                <Sparkles className="w-4 h-4 text-white animate-spin" />
              </div>
              <div className="absolute -bottom-2 -left-2 w-6 h-6 bg-gradient-to-r from-purple-400 to-pink-500 rounded-full flex items-center justify-center shadow-lg animate-pulse">
                <Brain className="w-3 h-3 text-white" />
              </div>
            </div>
          </div>
          <h1 className={`text-6xl font-black bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent mb-4 transition-all duration-1000 hover:scale-105 ${mounted ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`}>
            AIML Academic Assistant
          </h1>
          <div className={`flex items-center justify-center gap-3 text-gray-700 transition-all duration-700 delay-200 ${mounted ? 'translate-y-0 opacity-100' : 'translate-y-5 opacity-0'}`}>
            <div className="flex items-center gap-2 bg-white/60 backdrop-blur-sm rounded-full px-4 py-2 border border-white/30 shadow-lg">
              <GraduationCap className="w-5 h-5 text-blue-500 animate-pulse" />
              <span className="font-bold">Global Academy of Technology</span>
            </div>
          </div>
          <div className={`flex items-center justify-center gap-3 mt-3 text-sm transition-all duration-700 delay-300 ${mounted ? 'translate-y-0 opacity-100' : 'translate-y-5 opacity-0'}`}>
            <div className="flex items-center gap-2 bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-full px-4 py-2 shadow-lg hover:shadow-xl transition-all">
              <Brain className="w-4 h-4 animate-pulse" />
              <span className="font-semibold">Department of AI & ML</span>
              <BookOpen className="w-4 h-4 animate-bounce" />
            </div>
          </div>
        </div>

        {/* Form Card */}
        <div className={`bg-white/80 backdrop-blur-lg rounded-3xl shadow-2xl p-8 border border-white/20 relative overflow-hidden transition-all duration-700 delay-400 ${mounted ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`}>
          <div className="absolute inset-0 bg-gradient-to-br from-white/40 to-white/10 pointer-events-none"></div>
          <div className="relative z-10">
            <div className="flex gap-2 mb-8">
              <button
                onClick={() => setIsRegister(false)}
                className={`flex-1 py-3 px-6 rounded-xl font-medium transition-all duration-300 transform hover:scale-105 ${
                  !isRegister
                    ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg shadow-blue-500/25'
                    : 'bg-gray-100/80 text-gray-600 hover:bg-gray-200/80 hover:shadow-md'
                }`}
              >
                <LogIn className="w-4 h-4 inline mr-2" />
                Login
              </button>
              <button
                onClick={() => setIsRegister(true)}
                className={`flex-1 py-3 px-6 rounded-xl font-medium transition-all duration-300 transform hover:scale-105 ${
                  isRegister
                    ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg shadow-blue-500/25'
                    : 'bg-gray-100/80 text-gray-600 hover:bg-gray-200/80 hover:shadow-md'
                }`}
              >
                <UserPlus className="w-4 h-4 inline mr-2" />
                Register
              </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
              {isRegister && (
                <>
                  <div className="transform transition-all duration-300 hover:scale-105">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Full Name
                    </label>
                    <div className="relative group">
                      <User className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400 group-focus-within:text-blue-500 transition-colors" />
                      <input
                        type="text"
                        name="full_name"
                        value={formData.full_name}
                        onChange={handleChange}
                        required={isRegister}
                        className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 bg-white/50 backdrop-blur-sm hover:bg-white/80"
                        placeholder="Enter your full name"
                      />
                    </div>
                  </div>

                  <div className="transform transition-all duration-300 hover:scale-105">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Email
                    </label>
                    <div className="relative group">
                      <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400 group-focus-within:text-blue-500 transition-colors" />
                      <input
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                        required={isRegister}
                        className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 bg-white/50 backdrop-blur-sm hover:bg-white/80"
                        placeholder="your.email@gat.ac.in"
                      />
                    </div>
                  </div>

                  <div className="transform transition-all duration-300 hover:scale-105">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      USN (Optional)
                    </label>
                    <div className="relative group">
                      <GraduationCap className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400 group-focus-within:text-blue-500 transition-colors" />
                      <input
                        type="text"
                        name="usn"
                        value={formData.usn}
                        onChange={handleChange}
                        className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 bg-white/50 backdrop-blur-sm hover:bg-white/80"
                        placeholder="1GA21AI001"
                      />
                    </div>
                  </div>
                </>
              )}

              <div className="transform transition-all duration-300 hover:scale-105">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Username
                </label>
                <div className="relative group">
                  <User className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400 group-focus-within:text-blue-500 transition-colors" />
                  <input
                    type="text"
                    name="username"
                    value={formData.username}
                    onChange={handleChange}
                    required
                    className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 bg-white/50 backdrop-blur-sm hover:bg-white/80"
                    placeholder="Enter username"
                  />
                </div>
              </div>

              <div className="transform transition-all duration-300 hover:scale-105">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Password
                </label>
                <div className="relative group">
                  <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400 group-focus-within:text-blue-500 transition-colors" />
                  <input
                    type="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    required
                    className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 bg-white/50 backdrop-blur-sm hover:bg-white/80"
                    placeholder="Enter password"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 text-white py-4 rounded-xl font-medium hover:from-blue-700 hover:via-indigo-700 hover:to-purple-700 transition-all duration-300 shadow-lg hover:shadow-2xl disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-105 relative overflow-hidden group"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-white/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                <span className="relative z-10 flex items-center justify-center gap-2">
                  {loading ? (
                    <>
                      <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                      Processing...
                    </>
                  ) : (
                    <>
                      {isRegister ? <UserPlus className="w-5 h-5" /> : <LogIn className="w-5 h-5" />}
                      {isRegister ? 'Create Account' : 'Sign In'}
                    </>
                  )}
                </span>
              </button>
            </form>

            <div className="mt-8 text-center">
              <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-4 border border-blue-100">
                <p className="text-sm text-gray-600 mb-2">Demo credentials:</p>
                <div className="font-mono bg-white/80 px-3 py-2 rounded-lg text-sm border border-blue-200">
                  <span className="text-blue-600 font-semibold">student</span> / <span className="text-indigo-600 font-semibold">password123</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className={`text-center mt-8 transition-all duration-700 delay-600 ${mounted ? 'translate-y-0 opacity-100' : 'translate-y-5 opacity-0'}`}>
          <div className="bg-white/60 backdrop-blur-sm rounded-xl p-4 border border-white/20">
            <p className="text-sm text-gray-600 font-medium">NLP Mini Project - Problem Statement 18</p>
            <p className="text-xs text-gray-500 mt-1">Department of AI & ML</p>
          </div>
        </div>
      </div>
    </div>
  )
}
