import streamlit as st
import snowflake.connector
import pandas as pd
import numpy as np
import json
import os

# Page configuration
st.set_page_config(page_title="NPI Search", layout="wide")

# Title
st.title("NPI Provider Search")
st.markdown("---")

# Default NPI
default_npi = "1033933064"

# Load Specialty table mapping (cached for performance)
@st.cache_data
def load_specialty_mapping():
    """Load the Specialty table and create a mapping from Specialty ID to Specialty Name"""
    try:
        specialty_df = pd.read_excel('Specialty table.xlsx', engine='openpyxl')
        # Create a dictionary mapping Specialty ID to Specialty Name
        # Convert Specialty ID to string for matching
        mapping = dict(zip(
            specialty_df['Specialty ID'].astype(str),
            specialty_df['Specialty Name']
        ))
        return mapping
    except Exception as e:
        st.error(f"Error loading Specialty table: {str(e)}")
        return {}

# Load specialty mapping
specialty_mapping = load_specialty_mapping()

# Sidebar for input
with st.sidebar:
    st.header("Search Parameters")
    npi_input = st.text_input(
        "Enter NPI number:",
        placeholder="Leave blank to use default NPI",
        key="npi_input"
    )
    
    # Use default if empty
    npi = npi_input.strip() if npi_input.strip() else default_npi
    
    search_button = st.button("Search", type="primary", use_container_width=True)
    
    if npi_input.strip() == "":
        st.info(f"Using default NPI: {default_npi}")

# Main content area
if search_button or st.session_state.get('search_triggered', False):
    # Reset the trigger
    st.session_state.search_triggered = False
    
    # Show loading spinner
    with st.spinner("Connecting to Snowflake and querying database..."):
        try:
            # Connect to Snowflake using SSO (external browser authentication)
            # Use Streamlit secrets if available (for deployed apps), otherwise use defaults (for local)
            try:
                snowflake_config = st.secrets["snowflake"]
                user = snowflake_config.get("user", "dhruv.bhattacharjee@zocdoc.com")
                account = snowflake_config.get("account", "OLIKNSY-ZOCDOC_001")
                warehouse = snowflake_config.get("warehouse", "USER_QUERY_WH")
                database = snowflake_config.get("database", "CISTERN")
                schema = snowflake_config.get("schema", "PROVIDER_PREFILL")
                role = snowflake_config.get("role", "PROD_OPS_PUNE_ROLE")
            except (KeyError, FileNotFoundError):
                # Fallback to hardcoded values for local development
                user = "dhruv.bhattacharjee@zocdoc.com"
                account = "OLIKNSY-ZOCDOC_001"
                warehouse = "USER_QUERY_WH"
                database = "CISTERN"
                schema = "PROVIDER_PREFILL"
                role = "PROD_OPS_PUNE_ROLE"
            
            conn = snowflake.connector.connect(
                user=user,
                account=account,
                warehouse=warehouse,
                database=database,
                schema=schema,
                role=role,
                authenticator='externalbrowser'
            )
            
            try:
                cs = conn.cursor()
                query = f"""
                SELECT * FROM merged_provider
                WHERE NPI:value::string = '{npi}'
                """
                cs.execute(query)
                results = cs.fetchall()
                columns = [desc[0] for desc in cs.description]
                
                if not results:
                    st.warning(f"No results found for NPI: {npi}")
                    # Check connection status if using default NPI
                    if npi == default_npi:
                        st.error("❌ couldn't connect")
                else:
                    # Check connection status if using default NPI
                    if npi == default_npi:
                        st.success("✅ connection was successful")
                    
                    df = pd.DataFrame(results, columns=columns)
                    
                    # Remove timezone info from all datetime columns
                    for col in df.select_dtypes(include=['datetimetz']).columns:
                        df[col] = df[col].dt.tz_localize(None)
                    for col in df.columns:
                        if df[col].dtype == 'object':
                            if df[col].apply(lambda x: hasattr(x, 'tzinfo') and x.tzinfo is not None).any():
                                df[col] = df[col].apply(lambda x: x.tz_localize(None) if hasattr(x, 'tzinfo') and x.tzinfo is not None else x)
                    
                    # Select only the required columns
                    selected_columns = ['NPI', 'FIRST_NAME', 'LAST_NAME', 'SPECIALTIES']
                    df_selected = df[selected_columns].copy()
                    
                    # Extract 'value' from JSON strings in each cell, with special handling for SPECIALTIES
                    def extract_value(val, colname):
                        if isinstance(val, str):
                            try:
                                parsed = json.loads(val)
                                if colname == 'SPECIALTIES' and isinstance(parsed, list) and len(parsed) > 0:
                                    first = parsed[0]
                                    if isinstance(first, dict) and 'value' in first:
                                        return first['value']
                                if isinstance(parsed, dict) and 'value' in parsed:
                                    return parsed['value']
                            except Exception:
                                pass
                        return val
                    
                    for col in selected_columns:
                        df_selected[col] = df_selected[col].apply(lambda x: extract_value(x, col))
                    
                    # Drop rows where SPECIALTIES is blank or null
                    df_selected = df_selected[df_selected['SPECIALTIES'].notnull() & (df_selected['SPECIALTIES'] != '')]
                    
                    # Remove duplicate rows based on NPI and SPECIALTIES
                    df_selected = df_selected.drop_duplicates(subset=['NPI', 'SPECIALTIES'], keep='first')
                    
                    # Add 'Specialty Derived' column by looking up Specialty ID in the mapping
                    def get_specialty_name(specialty_id):
                        """Look up Specialty Name from Specialty ID"""
                        if pd.isna(specialty_id) or specialty_id == '':
                            return None
                        # Convert to string for lookup
                        specialty_id_str = str(specialty_id)
                        return specialty_mapping.get(specialty_id_str, None)
                    
                    df_selected['Specialty Derived'] = df_selected['SPECIALTIES'].apply(get_specialty_name)
                    
                    # Display results
                    st.subheader("Search Results")
                    st.dataframe(df_selected, use_container_width=True)
                    
                    # Export to Excel
                    if not df_selected.empty:
                        excel_filename = f"{npi}.xlsx"
                        df_selected.to_excel(excel_filename, index=False, engine='openpyxl')
                        st.success(f"✅ Excel file created: **{excel_filename}**")
                        
                        # Provide download button
                        with open(excel_filename, 'rb') as f:
                            st.download_button(
                                label="📥 Download Excel File",
                                data=f.read(),
                                file_name=excel_filename,
                                mime="application/vnd.openpyxl.formats-officedocument.spreadsheetml.sheet"
                            )
                    
            finally:
                cs.close()
                conn.close()
                
        except Exception as e:
            st.error(f"Error occurred: {str(e)}")
            st.exception(e)

else:
    # Initial state - show instructions
    st.info("👆 Enter an NPI number in the sidebar and click 'Search' to begin.")
    st.markdown("""
    ### Instructions:
    1. Enter an NPI number in the sidebar (or leave blank to use default NPI)
    2. Click the 'Search' button
    3. View results in the table below
    4. Download the automatically generated Excel file
    """)
