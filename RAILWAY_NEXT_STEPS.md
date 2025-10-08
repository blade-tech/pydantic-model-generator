# Railway Deployment - Next Steps

## ✅ What Just Happened

Created `nixpacks.toml` to solve the monorepo detection problem. This file tells Railway how to:
1. Detect Python (even though we're in a monorepo)
2. Install dependencies from `backend/requirements.txt`
3. Copy `pydantic_library/` into `backend/` during build
4. Start the FastAPI app correctly

**Files Updated**:
- ✅ `nixpacks.toml` - Created and pushed to GitHub
- ✅ `RAILWAY_ENV_VARS.md` - Updated PYDANTIC_LIBRARY_PATH to `./pydantic_library`
- ✅ `DEPLOYMENT_INSTRUCTIONS.md` - Updated with correct configuration

---

## 🚀 What You Need to Do in Railway

### Step 1: Update Environment Variable
1. Go to Railway dashboard → Backend Service
2. Click "Variables" tab
3. Find `PYDANTIC_LIBRARY_PATH`
4. Change value from `../pydantic_library` to `./pydantic_library`
5. Click "Update"

### Step 2: Clear Root Directory (If Set)
1. Go to "Settings" tab
2. Scroll to "Root Directory"
3. If it says `backend`, click "Clear" or delete the value
4. Leave it **blank** (empty)
5. Click "Update"

### Step 3: Remove Start Command (If Set)
1. Still in "Settings" tab
2. Scroll to "Custom Start Command"
3. If there's a command, click "Clear" or delete it
4. Leave it **blank** (nixpacks.toml handles this)
5. Click "Update"

### Step 4: Trigger Redeploy
1. Go to "Deployments" tab
2. Click the "⋮" menu on latest deployment
3. Click "Redeploy"
4. Or just push a small change to GitHub (Railway auto-deploys)

---

## 🔍 What to Watch For

### During Deployment (Build Logs)
You should see:
```
✓ Detected Python (from nixpacks.toml)
✓ Installing dependencies from backend/requirements.txt
✓ Copying pydantic_library into backend
✓ Starting: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Success Indicators
- ✅ Build completes without errors
- ✅ Service starts (no crash)
- ✅ Health check passes
- ✅ No "FileNotFoundError: pydantic_library not found"
- ✅ No "ValidationError: api_port"

---

## 🆘 If It Still Fails

**Share the new deployment logs** and I'll help debug further.

Common issues:
- Environment variable typo
- API keys invalid
- Neo4j connection issue

---

## 📊 Environment Variables Quick Reference

**Backend Service (13 variables)**:
- ANTHROPIC_API_KEY ✓
- OPENAI_API_KEY ✓
- NEO4J_URI ✓
- NEO4J_USER ✓
- NEO4J_PASSWORD ✓
- PYDANTIC_LIBRARY_PATH=`./pydantic_library` ← **Must update this**
- CORS_ORIGINS ✓
- CLAUDE_MODEL ✓
- CLAUDE_MAX_TOKENS ✓
- CLAUDE_TEMPERATURE ✓
- LOG_LEVEL ✓
- DEBUG ✓
- API_HOST ✓

**Do NOT add**: API_PORT (handled by start command)
**Do NOT set**: Root Directory (nixpacks.toml handles it)
**Do NOT set**: Custom Start Command (nixpacks.toml handles it)

---

## 🎯 Expected Result

After these changes and redeployment:
- Backend should start successfully
- `/health` endpoint should respond
- No file or validation errors
- Ready for frontend configuration

Then we'll configure the frontend service and test end-to-end!
