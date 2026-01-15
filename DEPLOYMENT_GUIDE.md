# Deployment Guide - Share Your Streamlit App

## Option 1: Streamlit Cloud (Recommended - Free & Easy)

### Step 1: Create a GitHub Repository
1. Go to [GitHub](https://github.com) and create a new account (if you don't have one)
2. Create a new repository (e.g., "npi-search-app")
3. Make it **public** (required for free Streamlit Cloud)

### Step 2: Upload Your Files to GitHub
You need to upload these files to your GitHub repository:
- ✅ `streamlit_app.py` (main app file)
- ✅ `requirements.txt` (dependencies)
- ✅ `Specialty table.xlsx` (required for the app to work)

**Important:** Make sure `Specialty table.xlsx` is in the same directory as `streamlit_app.py`

### Step 3: Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository and branch
5. Set the **Main file path** to: `streamlit_app.py`
6. Click "Deploy"

### Step 4: Share the Link
Once deployed, Streamlit Cloud will give you a link like:
```
https://your-app-name.streamlit.app
```
Share this link with your friend! 🎉

---

## Option 2: Run Locally and Share via ngrok (Temporary)

If you want to test quickly without deploying:

1. **Install ngrok:**
   ```bash
   # Download from https://ngrok.com/download
   # Or install via: pip install pyngrok
   ```

2. **Run your Streamlit app:**
   ```bash
   streamlit run streamlit_app.py
   ```

3. **In another terminal, create a tunnel:**
   ```bash
   ngrok http 8501
   ```

4. **Share the ngrok URL** (e.g., `https://abc123.ngrok.io`)

**Note:** This is temporary - the URL changes each time you restart ngrok (unless you have a paid plan).

---

## Option 3: Deploy to Other Platforms

### Railway.app
- Free tier available
- Connect GitHub repo
- Auto-deploys on push

### Render.com
- Free tier available
- Connect GitHub repo
- Easy deployment

### Heroku
- Free tier discontinued, but paid options available
- More complex setup

---

## Security Note ⚠️

**Good news!** The app is already configured to use Streamlit Secrets. 

### For Streamlit Cloud Deployment:

1. After deploying to Streamlit Cloud, go to your app's **Settings** → **Secrets**
2. Add the following in TOML format:
   ```toml
   [snowflake]
   user = "dhruv.bhattacharjee@zocdoc.com"
   account = "OLIKNSY-ZOCDOC_001"
   warehouse = "USER_QUERY_WH"
   database = "CISTERN"
   schema = "PROVIDER_PREFILL"
   role = "PROD_OPS_PUNE_ROLE"
   ```
3. Click "Save" - your app will automatically redeploy with the secrets

**Note:** The app will work without secrets (uses hardcoded fallback), but using secrets is more secure for production.

### For Local Development:
- The app works out of the box with hardcoded values
- Optionally, create `.streamlit/secrets.toml` (see `.streamlit/secrets.toml.example`)

---

## Quick Start Commands

### Local Development (Auto-opens browser):
```bash
streamlit run streamlit_app.py
```

### Check if everything is ready:
```bash
# Verify all files exist
ls streamlit_app.py requirements.txt "Specialty table.xlsx"
```
