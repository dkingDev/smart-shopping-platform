# 🚀 COMPLETE HEROKU + GITHUB PAGES DEPLOYMENT

## STEP 1: Deploy Backend to Heroku (3 minutes)

### A) Create Heroku App
1. **Go to:** https://dashboard.heroku.com/new-app
2. **App name:** `smart-shopping-derek` (or your choice)
3. **Region:** United States or Europe
4. **Click:** "Create app"

### B) Upload Backend Files
1. **Go to:** Deploy tab in your new app
2. **Choose:** "GitHub" deployment method (or Manual)
3. **Upload files:** From `backend-deploy/` folder:
   - `secure_aws_shopping.py`
   - `requirements.txt`
   - `Procfile`
   - `runtime.txt`
   - `database/` folder

### C) Add Environment Variables
1. **Go to:** Settings tab → "Reveal Config Vars"
2. **Add these exactly:**

```
AWS_DB_HOST = supermarket-db.cbu8qc0uk2re.eu-north-1.rds.amazonaws.com
AWS_DB_PORT = 5432
AWS_DB_NAME = postgres
AWS_DB_USER = AdminTakeo
AWS_DB_PASSWORD = Alex8nd3r12
JWT_SECRET_KEY = 3f2a8b9c4d1e7f6a5b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b
```

### D) Deploy
1. **Go to:** Deploy tab
2. **Click:** "Deploy Branch" (or enable automatic deploys)
3. **Wait:** ~2 minutes for build
4. **Copy URL:** Your app URL (like `https://smart-shopping-derek.herokuapp.com`)

---

## STEP 2: Deploy Frontend to GitHub Pages (2 minutes)

### A) Create GitHub Repository
1. **Go to:** https://github.com/new
2. **Repository name:** `smart-shopping-platform`
3. **Description:** "Smart Shopping Platform - Live Website"
4. **Public repository:** ✅
5. **Add README:** ✅
6. **Click:** "Create repository"

### B) Upload Frontend Files
1. **Click:** "uploading an existing file" link
2. **Upload ALL files from `github-pages-deploy/` folder:**
   - `index.html`
   - `js/app.js`
   - `package.json` 
   - `README.md`
   - `.nojekyll`
   - `CNAME`
3. **Commit message:** "Initial website deployment"
4. **Click:** "Commit changes"

### C) Enable GitHub Pages
1. **Go to:** Settings tab (in your repository)
2. **Scroll down to:** "Pages" (left sidebar)
3. **Source:** "Deploy from a branch"
4. **Branch:** "main" (or "master")
5. **Folder:** "/ (root)"
6. **Click:** "Save"

---

## STEP 3: Connect Frontend to Backend (1 minute)

### Update API URL
1. **In your GitHub repository:** Click on `js/app.js`
2. **Click:** "Edit" (pencil icon)
3. **Find line ~26:** Look for `API_BASE_URL`
4. **Replace:** `https://your-backend-app.herokuapp.com` 
5. **With:** Your actual Heroku URL (like `https://smart-shopping-derek.herokuapp.com`)
6. **Commit changes**

---

## STEP 4: Get Your Live URLs

### Backend API
- **URL:** `https://YOUR-APP-NAME.herokuapp.com`
- **Health Check:** `https://YOUR-APP-NAME.herokuapp.com/api/system-health`

### Frontend Website  
- **URL:** `https://YOUR-USERNAME.github.io/smart-shopping-platform`
- **Example:** `https://derekking.github.io/smart-shopping-platform`

---

## STEP 5: Test & Share

### Test the Live Website
1. **Visit:** Your GitHub Pages URL
2. **Login:** derek.j.king@live.com / Alex8nd3r!
3. **Test:** Registration, shopping lists, etc.

### Share with Users
**Send them:**
- **Website:** Your GitHub Pages URL  
- **Test Account:** derek.j.king@live.com / Alex8nd3r!
- **Features:** "Try creating an account and making shopping lists!"

---

## 🎯 QUICK DEPLOYMENT CHECKLIST

- [ ] Create Heroku app
- [ ] Upload backend files
- [ ] Add environment variables  
- [ ] Deploy backend
- [ ] Create GitHub repository
- [ ] Upload frontend files
- [ ] Enable GitHub Pages
- [ ] Update API URL in frontend
- [ ] Test live website
- [ ] Share with users

**Total time: ~6 minutes**
**Result: Live website ready for users!**

---

*Your Smart Shopping Platform will be live and accessible worldwide!*
