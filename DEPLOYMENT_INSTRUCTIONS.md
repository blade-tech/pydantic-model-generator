# Complete Deployment Instructions

## ✅ Backend Deployed
**URL:** https://pydantic-model-generator-production.up.railway.app

## 🚀 Deploy Frontend to Railway (Step-by-Step)

### Method 1: Via Railway Dashboard (Recommended - No CLI needed)

#### Step 1: Push Code to GitHub (if not already done)
```bash
git add .
git commit -m "Add frontend deployment configuration"
git push origin main
```

#### Step 2: Create New Railway Service
1. Go to https://railway.com/dashboard
2. Open your existing project: **"Pydantic Model Generator"**
3. Click **"+ New"** → **"GitHub Repo"**
4. Select your repository
5. Click **"Add variables"** (or skip for now)

#### Step 3: Configure Build Settings
Railway should auto-detect the Dockerfile, but verify:
- **Root Directory:** `demo-app/frontend`
- **Builder:** Dockerfile
- **Dockerfile Path:** Dockerfile

If not auto-detected:
1. Go to service Settings → **"Build"**
2. Set **"Root Directory"** to `demo-app/frontend`
3. Ensure **"Builder"** is set to Dockerfile

#### Step 4: Set Environment Variable
1. In the frontend service, go to **"Variables"** tab
2. Click **"+ New Variable"**
3. Add:
   - **Variable:** `NEXT_PUBLIC_API_URL`
   - **Value:** `https://pydantic-model-generator-production.up.railway.app`
4. Click **"Add"**

#### Step 5: Generate Public Domain
1. Go to **"Settings"** tab → **"Networking"**
2. Click **"Generate Domain"**
3. Copy the generated URL (e.g., `https://your-frontend.up.railway.app`)

#### Step 6: Update Backend CORS (Important!)
The backend needs to allow requests from the frontend domain:

1. Go to your **Backend service** in Railway
2. Navigate to **"Variables"** tab
3. Add a new variable:
   - **Variable:** `CORS_ORIGINS`
   - **Value:** `https://your-frontend.up.railway.app` (use the domain from Step 5)

Or update the backend code to allow all Railway domains:
```python
# In demo-app/backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3002",
        "https://*.up.railway.app",  # Allow all Railway domains
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### Step 7: Deploy
Railway automatically deploys on push. To manually trigger:
1. Go to **"Deployments"** tab
2. Click **"Deploy"** on the latest commit

---

### Method 2: Via Railway CLI (Alternative)

#### Install Railway CLI
```bash
# Windows (PowerShell)
iwr https://railway.com/install.ps1 | iex

# Mac/Linux
curl -fsSL https://railway.com/install.sh | sh
```

#### Deploy
```bash
cd demo-app/frontend
railway login
railway link  # Link to existing project
railway variables set NEXT_PUBLIC_API_URL=https://pydantic-model-generator-production.up.railway.app
railway up
```

---

## 🧪 Testing After Deployment

### 1. Check Frontend Loads
Visit your frontend URL: `https://your-frontend.up.railway.app`

### 2. Check API Connection
1. Open browser DevTools (F12) → Console
2. Look for API requests to your backend
3. Verify no CORS errors

### 3. Test Full Pipeline
1. Enter a conversation in the UI
2. Specify an outcome
3. Generate LinkML schema (Step 4)
4. Generate Pydantic models (Step 5)
5. Run tests (Step 6)
6. Verify all steps complete successfully

---

## 📁 Files Created for Deployment

### Frontend Files
- ✅ `demo-app/frontend/Dockerfile` - Multi-stage Next.js build
- ✅ `demo-app/frontend/railway.json` - Railway configuration
- ✅ `demo-app/frontend/.dockerignore` - Build optimization
- ✅ `demo-app/frontend/next.config.js` - Updated with standalone output
- ✅ `demo-app/frontend/RAILWAY_DEPLOYMENT.md` - Detailed deployment guide

### Backend Files
- ✅ `demo-app/backend/Dockerfile` - FastAPI Docker build
- ✅ `demo-app/backend/railway.json` - Railway configuration

---

## 🔧 Troubleshooting

### Frontend Build Fails
**Check:**
- Dockerfile exists in `demo-app/frontend/`
- `next.config.js` has `output: 'standalone'`
- Build logs in Railway dashboard for specific errors

### API Calls Fail (CORS Errors)
**Fix:**
1. Add frontend domain to backend CORS origins
2. Or use wildcard: `https://*.up.railway.app`
3. Redeploy backend after changes

### "Application failed to respond"
**Check:**
1. Service Settings → Networking → Port is set to **3000**
2. Dockerfile exposes port 3000
3. Health check path is `/` (or disable health checks)

### Environment Variable Not Working
**Verify:**
1. Variable name is exactly: `NEXT_PUBLIC_API_URL`
2. Variable value has no trailing slashes
3. Redeploy after adding variables (Railway auto-redeploys)

---

## 🎯 Expected Result

### Before Deployment
- ❌ Frontend on localhost:3002
- ❌ Backend on localhost:8000
- ❌ Can't share with others

### After Deployment
- ✅ Frontend on Railway: `https://your-frontend.up.railway.app`
- ✅ Backend on Railway: `https://pydantic-model-generator-production.up.railway.app`
- ✅ Fully functional web app
- ✅ Shareable URL
- ✅ Connected frontend ↔ backend

---

## 📊 Deployment Summary

| Component | Status | URL |
|-----------|--------|-----|
| Backend | ✅ Deployed | https://pydantic-model-generator-production.up.railway.app |
| Frontend | ⏳ Ready to Deploy | Will be: `https://your-frontend.up.railway.app` |
| Database | N/A | File-based (included in containers) |

---

## 🚀 Next Steps After Frontend Deployment

1. Test the complete pipeline end-to-end
2. Share the URL with users
3. Monitor Railway logs for errors
4. Consider adding:
   - Database for persistence (PostgreSQL on Railway)
   - Authentication (Auth0, Clerk, or NextAuth)
   - Analytics (Vercel Analytics, PostHog)
   - Error monitoring (Sentry)

---

**Ready to deploy?** Follow Method 1 above (Railway Dashboard) for the easiest deployment experience!
