# Railway Frontend Deployment Guide

## Prerequisites
- Railway account with CLI installed
- Backend already deployed at: `https://pydantic-model-generator-production.up.railway.app`

## Deployment Steps

### 1. Navigate to Frontend Directory
```bash
cd demo-app/frontend
```

### 2. Initialize Railway (if not already done)
```bash
railway login
railway link
```

### 3. Set Environment Variables
```bash
railway variables set NEXT_PUBLIC_API_URL=https://pydantic-model-generator-production.up.railway.app
```

### 4. Deploy to Railway
```bash
railway up
```

## Alternative: Deploy via Railway Dashboard

### Option A: Link GitHub Repository
1. Go to Railway Dashboard
2. Create New Project → "Deploy from GitHub repo"
3. Select repository
4. Set root directory: `demo-app/frontend`
5. Add environment variable:
   - Key: `NEXT_PUBLIC_API_URL`
   - Value: `https://pydantic-model-generator-production.up.railway.app`
6. Deploy

### Option B: Deploy from Local
1. Go to Railway Dashboard
2. Create New Project → "Empty Project"
3. Add New Service → "GitHub Repo" or "Empty Service"
4. If empty service, use Railway CLI:
   ```bash
   cd demo-app/frontend
   railway link
   railway up
   ```

## Post-Deployment

### Set Environment Variables
In Railway Dashboard → Frontend Service → Variables:
```
NEXT_PUBLIC_API_URL=https://pydantic-model-generator-production.up.railway.app
PORT=3000
NODE_ENV=production
```

### Generate Domain
1. Go to Frontend Service → Settings → Networking
2. Click "Generate Domain"
3. Your app will be available at: `https://[your-app].up.railway.app`

## Verification

After deployment, test:
1. Visit frontend URL
2. Try creating an outcome specification
3. Verify API calls work (check browser console)
4. Test full pipeline (conversation → schema → tests)

## Troubleshooting

### Build Failures
- Check Dockerfile is present in `demo-app/frontend/`
- Verify `next.config.js` has `output: 'standalone'`
- Check build logs in Railway dashboard

### API Connection Issues
- Verify `NEXT_PUBLIC_API_URL` is set correctly
- Check backend is responding: `https://pydantic-model-generator-production.up.railway.app`
- Check browser console for CORS errors

### Port Issues
- Railway automatically sets PORT to 3000
- Dockerfile exposes port 3000
- No manual configuration needed

## Environment Variables Reference

| Variable | Value | Required |
|----------|-------|----------|
| `NEXT_PUBLIC_API_URL` | `https://pydantic-model-generator-production.up.railway.app` | Yes |
| `PORT` | `3000` | No (auto-set) |
| `NODE_ENV` | `production` | No (auto-set) |

## Files Created for Deployment

- ✅ `Dockerfile` - Multi-stage Next.js Docker build
- ✅ `railway.json` - Railway configuration
- ✅ `.dockerignore` - Optimize build size
- ✅ `next.config.js` - Updated with `output: 'standalone'`
