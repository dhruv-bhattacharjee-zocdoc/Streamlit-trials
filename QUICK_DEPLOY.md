# 🚀 Quick Deployment to Streamlit Cloud

Your app is now on GitHub! Follow these steps to deploy it:

## Step 1: Go to Streamlit Cloud
Visit: https://share.streamlit.io

## Step 2: Sign In
- Click "Sign in" 
- Use your **GitHub account** (same one you used for the repository)

## Step 3: Deploy Your App
1. Click **"New app"** button
2. Select:
   - **Repository**: `dhruv-bhattacharjee-zocdoc/Streamlit-trials`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
3. Click **"Deploy"**

## Step 4: Configure Secrets (Optional but Recommended)
After deployment, go to your app's **Settings** → **Secrets** and add:

```toml
[snowflake]
user = "dhruv.bhattacharjee@zocdoc.com"
account = "OLIKNSY-ZOCDOC_001"
warehouse = "USER_QUERY_WH"
database = "CISTERN"
schema = "PROVIDER_PREFILL"
role = "PROD_OPS_PUNE_ROLE"
```

Click "Save" - the app will automatically redeploy.

## Step 5: Share the Link! 🎉
Once deployed, you'll get a link like:
```
https://streamlit-trials.streamlit.app
```

Share this link with your friend - they can use the app without any code access!

---

## Troubleshooting

**If deployment fails:**
- Make sure `Specialty table.xlsx` is in the repository (check GitHub)
- Verify `requirements.txt` has all dependencies
- Check the deployment logs in Streamlit Cloud

**If the app doesn't connect to Snowflake:**
- Make sure you've added the secrets (Step 4)
- The app will use hardcoded values as fallback, but secrets are more secure
