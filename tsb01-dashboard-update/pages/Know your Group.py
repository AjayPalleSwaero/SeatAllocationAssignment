import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid import JsCode
import os

# Set the page layout to wide mode
st.set_page_config(page_title='Work Risk', page_icon=':material/monitoring:', layout='wide')

@st.cache_data 
def load_parquet(filepath, nrows=40):
    return pd.read_parquet(filepath)



# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one level to project root, then into data folder
csv_path = os.path.join(os.path.dirname(current_dir), 'data', 'group_details.csv')
groups_df = pd.read_csv(csv_path) 


rd_options = [ 'Group Page']

wr_select_bt = st.sidebar.radio(label='Select', options=rd_options, key="wr_dashboard")

st_button_dict = {
    'Group Page': 'group_page'
}



#// Define the custom JavaScript for cell styling
cell_style_jscode = JsCode("""
function(params) {
    if (params.value < 0) {
        return {
            'color': 'white',    // Text color
            'backgroundColor': 'rgba(255, 0, 0, 0.5)'  // Background color
        };
    }
    return null;
};
""")

def display_aggrid(df, date_value, cols_color_pattern=None):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_side_bar()
    gb.configure_default_column(editable=True, groupable=True, filter=True)  # <-- enable filtering
    
    # Explicitly enable text filter on "Names"
    if "Names" in df.columns:
        gb.configure_column("Names", filter="agTextColumnFilter")
    
    if cols_color_pattern:
        cols_color = df.columns[df.columns.str.startswith('delta_')]
        for col in cols_color:
            gb.configure_column(col, cellStyle=cell_style_jscode) 
    
    gridOptions = gb.build()
    AgGrid(df, gridOptions=gridOptions, height=600, width='100%', allow_unsafe_jscode=True)


last_date_value = '25-08-2025'


def main(select_button):
    
    if select_button == 'Group Page':
        st.markdown(f"#### Last Updated: {last_date_value}")
        # Convert DataFrame to CSV
        

        display_aggrid(groups_df, last_date_value, cols_color_pattern='pattern' )

        ai_state_csv_data = groups_df.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="Download raw data as CSV",
            data=ai_state_csv_data,
            file_name="yourgroup_details.csv",
            mime="text/csv",
            )
                
        # --- PDF Download ---
        pdf_path = "pdfs/Know_Your_Group.pdf"   # remove leading "/" if it's relative path
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()   # <-- read as bytes
            st.download_button(
                label="Download Group Report (PDF)",
                data=pdf_bytes,
                file_name="mygroups.pdf",
                mime="application/pdf",
            )





if __name__ == '__main__':
    main(wr_select_bt)




