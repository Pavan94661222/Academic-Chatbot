# 🚀 Backend Deployment Guide - AIML_VOICE_ASSISTANT

## 📋 Quick Deployment Summary

### 🎯 **Recommended: Railway (Easiest)**

1. **Go to**: https://railway.app
2. **Sign up** with GitHub
3. **New Project** → **Deploy from GitHub**
4. **Select**: `Pavan94661222/Academic-Chatbot`
5. **Root Directory**: `app`
6. **Add Environment Variables**:
   ```
   GEMINI_API_KEY=your_actual_gemini_api_key
   SECRET_KEY=your_secret_key_here
   CORS_ORIGINS=https://aiml-voice-assistant.netlify.app
   ```
7. **Deploy** - Railway handles the rest automatically!

---

## 🔧 **Detailed Deployment Options**

### 1. **Railway Deployment** (Recommended)

#### ✅ **Why Railway?**
- Automatic Python detection
- Zero-config deployment
- Free tier available
- Automatic HTTPS
- Easy environment variables

#### 📋 **Step-by-Step:**

1. **Visit Railway**: https://railway.app
2. **Sign Up/Login** with your GitHub account
3. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `Pavan94661222/Academic-Chatbot`

4. **Configure Project**:
   - **Root Directory**: `app`
   - Railway auto-detects Python and FastAPI
   - Uses `requirements.txt` and `Procfile` automatically

5. **Environment Variables** (Add in Railway dashboard):
   ```env
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   SECRET_KEY=your_jwt_secret_key_change_this
   CORS_ORIGINS=https://aiml-voice-assistant.netlify.app
   DATABASE_URL=sqlite:///./feedback.db
   ```

6. **Deploy**: Railway automatically builds and deploys
7. **Get URL**: Railway provides a URL like `https://your-app.railway.app`

---

### 2. **Render Deployment**

#### 📋 **Steps:**

1. **Visit Render**: https://render.com
2. **Connect GitHub** and select your repository
3. **Create Web Service**:
   - **Repository**: `Pavan94661222/Academic-Chatbot`
   - **Root Directory**: `app`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Environment Variables**:
   ```env
   GEMINI_API_KEY=your_gemini_api_key
   SECRET_KEY=your_secret_key
   CORS_ORIGINS=https://aiml-voice-assistant.netlify.app
   ```

5. **Deploy**: Render builds and provides a URL

---

### 3. **Heroku Deployment**

#### 📋 **Prerequisites:**
- Heroku CLI installed
- Git initialized in `app` folder

#### 📋 **Steps:**

1. **Install Heroku CLI**: https://devcenter.heroku.com/articles/heroku-cli

2. **Login and Create App**:
   ```bash
   heroku login
   heroku create aiml-voice-assistant-api
   ```

3. **Deploy from app folder**:
   ```bash
   cd app
   git init
   heroku git:remote -a aiml-voice-assistant-api
   git add .
   git commit -m "Deploy FastAPI backend"
   git push heroku master
   ```

4. **Set Environment Variables**:
   ```bash
   heroku config:set GEMINI_API_KEY=your_key
   heroku config:set SECRET_KEY=your_secret
   heroku config:set CORS_ORIGINS=https://aiml-voice-assistant.netlify.app
   ```

---

## 🔗 **After Backend Deployment**

### Step 1: Get Your Backend URL
After deployment, you'll get a URL like:
- Railway: `https://your-app.railway.app`
- Render: `https://your-app.onrender.com`
- Heroku: `https://aiml-voice-assistant-api.herokuapp.com`

### Step 2: Update Frontend
1. **Create `.env` file** in `frontend` folder:
   ```env
   VITE_API_URL=https://your-backend-url-here
   ```

2. **Redeploy Frontend** to Netlify:
   ```bash
   cd frontend
   npm run build
   netlify deploy --prod --dir=dist
   ```

### Step 3: Test Connection
1. **Visit**: https://aiml-voice-assistant.netlify.app
2. **Login/Register** - should work without errors
3. **Test Chat** - should get responses from backend
4. **Test Voice** - should process voice input

---

## 🛠️ **Troubleshooting**

### Common Issues:

#### 1. **CORS Errors**
- Ensure `CORS_ORIGINS` includes your Netlify URL
- Check backend logs for CORS-related errors

#### 2. **Database Issues**
- SQLite database is created automatically
- Check if `feedback.db` exists in backend

#### 3. **Gemini API Errors**
- Verify `GEMINI_API_KEY` is correct
- Check Gemini API quota/limits

#### 4. **Build Failures**
- Ensure `requirements.txt` has all dependencies
- Check Python version compatibility

---

## 🎯 **Quick Test Commands**

### Test Backend Health:
```bash
curl https://your-backend-url/
# Should return: {"message": "Academic Chatbot API"}
```

### Test API Endpoint:
```bash
curl https://your-backend-url/api/chatbot/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "session_id": "test"}'
```

---

## 📊 **Deployment Comparison**

| Platform | Free Tier | Ease | Speed | Features |
|----------|-----------|------|-------|----------|
| **Railway** | ✅ Yes | 🟢 Easy | 🟢 Fast | Auto-deploy, HTTPS |
| **Render** | ✅ Yes | 🟡 Medium | 🟡 Medium | Free SSL, Git integration |
| **Heroku** | ⚠️ Limited | 🟡 Medium | 🟡 Medium | Mature platform |

**🏆 Recommendation: Use Railway for the easiest deployment experience!**

---

## 🎉 **Success Checklist**

- [ ] Backend deployed successfully
- [ ] Environment variables configured
- [ ] Frontend updated with backend URL
- [ ] Frontend redeployed to Netlify
- [ ] Login/Register works
- [ ] Chat responses working
- [ ] Voice assistant functional
- [ ] No CORS errors in browser console

**🎯 Your AIML_VOICE_ASSISTANT will be fully functional once both frontend and backend are deployed!**
