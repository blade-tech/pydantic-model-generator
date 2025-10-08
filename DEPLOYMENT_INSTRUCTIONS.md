# Railway Deployment Instructions

**🎯 Goal**: Deploy Pydantic Model Generator to Railway with zero code changes

---

## ✅ Current Status

✓ Local repository created and committed
✓ Railway configuration files ready
✓ Documentation complete
✓ Progress tracker created

**Location**: `D:/projects/Pydantic Model Generator/pydantic-model-generator/`

---

## 📤 Step 1: Create GitHub Repository

### Option A: Using GitHub CLI (Recommended)
```bash
cd pydantic-model-generator

# Create public repository (requires GitHub CLI)
gh repo create blade-tech/pydantic-model-generator --public --source=. --remote=origin

# Push code
git push -u origin main
```

### Option B: Using GitHub Web Interface
1. Go to https://github.com/blade-tech
2. Click "New repository" (green button)
3. Repository settings:
   - **Name**: `pydantic-model-generator`
   - **Visibility**: Public
   - **DO NOT** initialize with README, .gitignore, or license
4. Click "Create repository"
5. Copy the repository URL (e.g., `https://github.com/blade-tech/pydantic-model-generator.git`)
6. In your terminal:
   ```bash
   cd pydantic-model-generator
   git remote add origin https://github.com/blade-tech/pydantic-model-generator.git
   git push -u origin main
   ```

---

## 🚂 Step 2: Deploy to Railway

### 2.1 Create Railway Project
1. Go to https://railway.app/dashboard
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose `blade-tech/pydantic-model-generator`
5. Railway creates the project

### 2.2 Add Neo4j Database
1. In Railway project dashboard, click "+ New"
2. Select "Database" → "Add Neo4j"
3. Railway provisions Neo4j instance (takes ~1 minute)
4. Note: Connection variables auto-injected into services

### 2.3 Configure Backend Service

#### Important: No Root Directory Needed!
The repository includes `nixpacks.toml` which automatically handles the monorepo structure. **Do NOT set a Root Directory** - leave it blank.

#### Add Environment Variables
1. Click on **backend service** in Railway
2. Go to "Variables" tab
3. Click "New Variable" for each (refer to `RAILWAY_ENV_VARS.md` for actual values):

```env
# AI API Keys
ANTHROPIC_API_KEY=sk-ant-[YOUR_KEY_HERE]
OPENAI_API_KEY=sk-[YOUR_KEY_HERE]

# Neo4j (auto-injected - use these exact values)
NEO4J_URI=${{Neo4j.NEO4J_URI}}
NEO4J_USER=${{Neo4j.NEO4J_USER}}
NEO4J_PASSWORD=${{Neo4j.NEO4J_PASSWORD}}

# Application Config
PYDANTIC_LIBRARY_PATH=./pydantic_library
CORS_ORIGINS=https://pydantic-model-generator-production.up.railway.app
CLAUDE_MODEL=claude-sonnet-4-5-20250929
CLAUDE_MAX_TOKENS=16384
CLAUDE_TEMPERATURE=0.7
LOG_LEVEL=INFO
DEBUG=false
API_HOST=0.0.0.0
```

**Important**:
- Replace `[YOUR_KEY_HERE]` with actual API keys from `RAILWAY_ENV_VARS.md` (local file, not in repo)
- The `CORS_ORIGINS` will be updated in Step 2.4
- `PYDANTIC_LIBRARY_PATH` is set to `./pydantic_library` because nixpacks.toml copies it into backend during build
- **Do NOT add `API_PORT`** - the port is handled by the start command

### 2.4 Configure Frontend Service

#### Set Root Directory
1. Click on **frontend service** in Railway
2. Go to "Settings" tab
3. Scroll to "Root Directory"
4. Enter: `frontend`
5. Click "Update"

#### Add Environment Variables
1. Go to "Variables" tab
2. Add:

```env
NEXT_PUBLIC_API_URL=https://pydantic-model-generator-production.up.railway.app
```

**Important**: Replace with actual backend URL from Railway

#### Update Backend CORS
1. Go back to **backend service**
2. Go to "Variables" tab
3. Update `CORS_ORIGINS` with actual frontend URL from Railway

---

## 🔄 Step 3: Deploy

Railway auto-deploys when you push to GitHub. Initial deployment takes 5-10 minutes.

### Monitor Deployment
1. Click on each service to see build logs
2. Watch for:
   - ✓ Dependencies installing
   - ✓ Build completing
   - ✓ Service starting
   - ✓ Health check passing

### Get Service URLs
1. Click on **backend service**
2. Go to "Settings" → "Networking"
3. Copy public URL (e.g., `https://backend-xyz.railway.app`)
4. Repeat for **frontend service**

---

## ✅ Step 4: Verify Deployment

### Backend Health Check
```bash
curl https://[backend-url]/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "Pydantic Model Generator Demo API is running",
  "version": "1.0.0"
}
```

### Frontend Check
1. Visit frontend URL in browser
2. Should see Step 1: Business Context Input
3. Open browser DevTools → Console
4. Should see no CORS errors

### API Documentation
Visit: `https://[backend-url]/docs`
- Should show FastAPI Swagger UI
- Test /health endpoint

---

## 🧪 Step 5: Test Full Workflow

1. **Step 1**: Enter business context
   - Example: "Track customer support ticket resolution and escalation patterns"

2. **Step 2**: Run ontology research
   - Verify Claude API connection
   - Check streaming works
   - Approve suggested entities

3. **Step 3**: Generate OutcomeSpec
   - Verify YAML generation
   - Edit if needed
   - Approve

4. **Step 4**: Generate LinkML schema
   - Verify schema generation
   - Check for errors
   - Approve

5. **Step 5**: Generate Pydantic models
   - Verify subprocess execution
   - Check file writes
   - Confirm Python code generated

6. **Step 6**: Run tests
   - Verify pytest works
   - Check test results
   - Confirm all tests pass

---

## 🔧 Troubleshooting

### Build Fails
**Check**:
- Python version detected (should be 3.11+)
- requirements.txt is valid
- package.json is valid

**Fix**:
- Check build logs in Railway
- Verify all dependencies are in requirements.txt

### Backend Won't Start
**Check**:
- All environment variables set
- Neo4j connection variables injected
- PYDANTIC_LIBRARY_PATH is correct

**Fix**:
- Review runtime logs
- Verify API keys are valid
- Check Neo4j service is running

### CORS Errors
**Check**:
- CORS_ORIGINS includes frontend URL
- NEXT_PUBLIC_API_URL points to backend
- Both services are running

**Fix**:
- Update CORS_ORIGINS in backend
- Redeploy backend service
- Hard refresh frontend (Ctrl+Shift+R)

### Subprocess Fails
**Check**:
- gen-pydantic is in requirements.txt
- File write permissions
- PYDANTIC_LIBRARY_PATH is accessible

**Fix**:
- Check backend logs for errors
- Verify linkml package installed
- Test locally first

---

## 📊 Deployment Checklist

Use this alongside `RAILWAY_DEPLOYMENT_PROGRESS.md`:

- [ ] GitHub repository created
- [ ] Code pushed to GitHub main branch
- [ ] Railway project created from repo
- [ ] Neo4j database added
- [ ] Backend service configured (root dir + env vars)
- [ ] Frontend service configured (root dir + env vars)
- [ ] CORS updated with actual URLs
- [ ] Initial deployment complete
- [ ] Backend health check passing
- [ ] Frontend loading correctly
- [ ] Full workflow tested end-to-end
- [ ] Files persisting in pydantic_library/
- [ ] Tests executing successfully

---

## 🎉 Success!

Once all steps complete, your Pydantic Model Generator is live on Railway!

**URLs**:
- Frontend: `https://[frontend-url].railway.app`
- Backend: `https://[backend-url].railway.app`
- API Docs: `https://[backend-url].railway.app/docs`

---

## 📚 Next Steps

### Production Readiness
- [ ] Add custom domain in Railway
- [ ] Enable Railway notifications (for deployment alerts)
- [ ] Set up monitoring (Railway provides metrics)
- [ ] Configure backup strategy for Neo4j
- [ ] Add environment-specific configs (staging/prod)

### Feature Enhancements
- [ ] Add user authentication
- [ ] Implement overlay versioning
- [ ] Add model export functionality
- [ ] Create API rate limiting
- [ ] Add Graphiti knowledge graph UI

### Documentation
- [ ] Add architecture diagrams
- [ ] Create video walkthrough
- [ ] Write API integration guide
- [ ] Document common use cases
- [ ] Add troubleshooting wiki

---

## 🆘 Support

### Railway Issues
- **Docs**: https://docs.railway.app/
- **Discord**: https://discord.gg/railway
- **Status**: https://status.railway.app/

### Application Issues
- **GitHub Issues**: https://github.com/blade-tech/pydantic-model-generator/issues
- **Discussions**: https://github.com/blade-tech/pydantic-model-generator/discussions

---

**Built with ❤️ and deployed with Railway**
