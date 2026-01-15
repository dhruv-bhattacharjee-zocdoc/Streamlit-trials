# NPI Provider Search App

A Streamlit web application to search for healthcare providers by NPI number, with automatic Excel export functionality.

## Features

- 🔍 Search providers by NPI number
- 📊 View provider details (Name, NPI, Specialties)
- 🏥 Automatic specialty name lookup from Specialty ID
- 📥 Automatic Excel file generation (`{NPI}.xlsx`)
- ☁️ Ready for cloud deployment

## Quick Start

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app:**
   ```bash
   streamlit run streamlit_app.py
   ```
   The app will automatically open in your browser!

### Deploy to Share with Others

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

**Quick steps:**
1. Upload files to GitHub (streamlit_app.py, requirements.txt, Specialty table.xlsx)
2. Deploy to [Streamlit Cloud](https://share.streamlit.io)
3. Share the link with your friends!

## Files Required

- `streamlit_app.py` - Main application
- `requirements.txt` - Python dependencies
- `Specialty table.xlsx` - Specialty lookup table

## Default NPI

If no NPI is entered, the app uses default NPI: `1033933064` (for connection testing)
