# 🚀 Netlify Deployment Guide - Single Steps

## Prerequisites
- GitHub account
- Netlify account (free)
- Project pushed to GitHub repository

## 📋 Single-Step Deployment Process

### Step 1: Prepare Frontend for Production
```bash
cd frontend
npm run build
```

### Step 2: Create netlify.toml Configuration
Create `netlify.toml` in project root:
```toml
[build]
  publish = "frontend/dist"
  command = "cd frontend && npm install && npm run build"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[build.environment]
  NODE_VERSION = "18"
```

### Step 3: Deploy to Netlify
1. **Login to Netlify**: https://netlify.com
2. **Click "New site from Git"**
3. **Connect GitHub repository**
4. **Configure build settings**:
   - Build command: `cd frontend && npm install && npm run build`
   - Publish directory: `frontend/dist`
5. **Click "Deploy site"**

### Step 4: Configure Environment Variables
In Netlify dashboard → Site settings → Environment variables:
```
VITE_API_URL=https://your-backend-url.com
```

### Step 5: Custom Domain (Optional)
- Go to Domain settings
- Add custom domain
- Configure DNS

## 🔧 Backend Deployment (Separate)
For backend, use:
- **Railway**: https://railway.app
- **Render**: https://render.com
- **Heroku**: https://heroku.com

## ✅ Deployment Checklist
- [ ] Frontend builds successfully
- [ ] netlify.toml configured
- [ ] Environment variables set
- [ ] Backend deployed separately
- [ ] API URLs updated
- [ ] Custom domain configured (optional)

## 🌐 Live URL
After deployment: `https://your-site-name.netlify.app`

## 📞 Support
- Netlify Docs: https://docs.netlify.com
- Build logs available in Netlify dashboard
