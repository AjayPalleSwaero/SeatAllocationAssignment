import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid import JsCode

# Set the page layout to wide mode
st.set_page_config(page_title='Work Risk', page_icon=':material/monitoring:', layout='wide')

@st.cache_data 
def load_parquet(filepath, nrows=40):
    return pd.read_parquet(filepath)

ai_block_df = load_parquet('./data/ai_blocks_rule.parquet')
ai_state_df = load_parquet('./data/ai_state_rule.parquet')
gis_block_df = load_parquet('./data/geo_blocks_rule.parquet')
gis_state_df = load_parquet('./data/geo_state_rule.parquet')
dashboard_block_df = load_parquet('./data/workrisk_dashboard_blocks_rule.parquet')
dashboard_state_df = load_parquet('./data/workrisk_dashboard_state_rule.parquet')

rd_options = ['Summary', 'AI Rule', 'GIS Rule', 'Power Bi Dashboard']

wr_select_bt = st.sidebar.radio(label='Select', options=rd_options, key="wr_dashboard")

st_button_dict = {
    'Summary': 'summary_page',
    'AI Rule': 'ai_rule_page', 
    'GIS Rule':'gis_rule_page', 
    'Power Bi Dashboard':'powerbi_rule_page'
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



def display_aggrid(df, date_value, cols_color_pattern =None):
    """
    cols_color_pattern: 
    """
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_side_bar()
    gb.configure_default_column(editable=True, groupable=True)

    # List of columns to apply the custom CSS
    #columns_to_style = ['delta_fetch_stage2', 'delta_processed_stage2', 'yet_another_column']
    #gb.configure_column('delta_processed_stage2', cellStyle=cell_style_jscode)

        # Apply bold and font-size directly to column headers
  
    if cols_color_pattern:
        cols_color = df.columns[df.columns.str.startswith('delta_')]
    #Apply the custom CSS to each column in the list
        for col in cols_color:
            gb.configure_column(col, cellStyle=cell_style_jscode) 
    gridOptions = gb.build()
    #gridOptions['getRowStyle'] = jscode
    AgGrid(df, gridOptions=gridOptions, height=600, width='100%', allow_unsafe_jscode=True,)


date_value = '01-07-2024'

# show_column_def =  f"""
# -   **state_name** : state_name
# -   **state_code** : state_code 
# -   **block_name** : block_name
# -   **block_code** : block_code
# -   **stage2_works_api** : Aggregate numbers of stage2 image counts received from NIC nrega through API
# -   **stage2_works_db** :  Individual stage2 images received from NIC nrega through API
# -   **delta_fetch_stage2** : **stage2_works_api** - **stage2_works_db** (checking aggregate number and indivual fetched numbers differnce. If differnce is not 0 it means we missed that many number of works to fetch from individual api) 
# -   **works_sent_mq** : Total works/images sent to Messaging Queue (MQ) 
# -   **works_processed_function_app** : Total works/images processed by the Azure Function APP
# -   **delta_processed_stage2** : **stage2_works_api** - **delta_processed_stage2** (Total works in DIU db - total works processed by Azure Function App)
# -   **flagged_works_ai_rule** : Number of works/images did not match claimed category
# """
# show_column_def_exp = """ - **stage2_works_sent_nic** : Total works sent to NIC through API"""
ai_show_cols_st= """
- **sno** : Sno
- **state_name** : State name
- **state_code** : State Code 
- **stage2_works_api** : Aggregate numbers of stage2 works counts received blockwise from NIC nrega through API
- **stage2_works_db** :  Individual stage2 works received from NIC nrega through API
- **delta_api_stage2** : **stage2_works_api** - **stage2_works_db** (checking aggregate and indivualfetched numbers are same. If differnce is not 0 it means we missed that many number of works to fetch
- **delta_api_stage2_percen** : (**stage2_works_api** - **stage2_works_db**)*100/**stage2_works_api** in other terms expressed delta_api_stage2 in percent
- **works_sent_mq** : Total works sent to Messaging Queue(MQ) from database
- **works_processed_function_app** : Total works processed by Azure Function app
- **delta_processed_stage2** : **stage2_works_db** - **works_processed_function_app** (Total works in DIU db - total works processed by Azure Function App)
- **delta_stage2_processed_percen** : (**stage2_works_db** - **works_processed_function_app**)*100 / **stage2_works_db**
- **flagged_works_ai_rule** : Number of works did not match claimed category
- **flagged_works_ai_rule_percen** :  **flagged_works_ai_rule**  *100 / **works_processed_function_app*
- **stage2_works_sent_nic** : Total ai rule works sent to NIC through API
        
"""

ai_show_cols_blocks =  """
- **sno** : Sno
- **state_name** : State name
- **state_code** : State Code 
- **block_name** : Block Name
- **block_code** : Block Code
- **stage2_works_api** : Aggregate numbers of stage2 works counts received blockwise from NIC nrega through API
- **stage2_works_db** :  Individual stage2 works received from NIC nrega through API
- **delta_api_stage2** : **stage2_works_api** - **stage2_works_db** (checking aggregate and indivualfetched numbers are same. If differnce is not 0 it means we missed that many number of works to fetch
- **delta_api_stage2_percen** : (**stage2_works_api** - **stage2_works_db**)*100/**stage2_works_api** in other terms expressed delta_api_stage2 in percent
- **works_sent_mq** : Total works sent to Messaging Queue(MQ) from database
- **works_processed_function_app** : Total works processed by Azure Function app
- **delta_processed_stage2** : **stage2_works_db** - **works_processed_function_app** (Total works in DIU db - total works processed by Azure Function App)
- **delta_stage2_processed_percen** : (**stage2_works_db** - **works_processed_function_app**)*100 / **stage2_works_db**
- **flagged_works_ai_rule** : Number of works did not match claimed category
- **flagged_works_ai_rule_percen** :  **flagged_works_ai_rule**  *100 / **works_processed_function_app*
- **stage2_works_sent_nic** : Total ai rule works sent to NIC through API    
"""

gis_show_cols_st = """
- **sno** : Sno
- **state_name** : State name
- **state_code** : State Code 
- **ongoing_works_api** : Aggregate numbers of ongoing works counts received blockwise from NIC nrega through API
- **ongoing_works_db** : Individual numbers of ongoing works counts received blockwise from NIC nrega through API
- **delta_api_ongoing** :  **ongoing_works_api** - **ongoing_works_db**
- **delta_api_ongoing_percen** : (**ongoing_works_api** - **ongoing_works_db**)*100/ongoing_works_api
- **all_works_geotagged_api** : Aggregate numbers of all works counts received blockwise from NIC nrega through API
- **all_works_geotagged_db** :  Individual numbers of ongoing works counts received blockwise from NIC nrega through API
- **delta_api_all_works** : **all_works_geotagged_api** - **all_works_geotagged_db**
- **delta_api_all_works_percen** : (**all_works_geotagged_api** - **all_works_geotagged_db**)*100/all_works_geotagged_db
- **ongoing_works_processed** :Total number of works processed by the geoquery
- **delta_processed_ongoing** : **ongoing_works_db** - **ongoing_works_processed**
- **delta_processed_ongoing_percen** :  (**ongoing_works_db** - **ongoing_works_processed**)*100/**ongoing_works_db**
- **flagged_works_gis_rule** : Total number of works flagged as per gis rule
- **flagged_works_gis_rule_percen** :  **flagged_works_gis_rule**  *100 / **ongoing_works_db**
- **ongoing_works_sent_nic** : Total geo rule works sent to NIC through API                                                              

"""


gis_show_cols_blocks = """
- **sno** : Sno
- **state_name** : State name
- **state_code** : State Code 
- **block_name** : Block Name
- **block_code** : Block Code
- **ongoing_works_api** : Aggregate numbers of ongoing works counts received blockwise from NIC nrega through API
- **ongoing_works_db** : Individual numbers of ongoing works counts received blockwise from NIC nrega through API
- **delta_api_ongoing** :  **ongoing_works_api** - **ongoing_works_db**
- **delta_api_ongoing_percen** : (**ongoing_works_api** - **ongoing_works_db**)*100/ongoing_works_api
- **all_works_geotagged_api** : Aggregate numbers of all works counts received blockwise from NIC nrega through API
- **all_works_geotagged_db** :  Individual numbers of ongoing works counts received blockwise from NIC nrega through API
- **delta_api_all_works** : **all_works_geotagged_api** - **all_works_geotagged_db**
- **delta_api_all_works_percen** : (**all_works_geotagged_api** - **all_works_geotagged_db**)*100/all_works_geotagged_db
- **ongoing_works_processed** :Total number of works processed by the geoquery
- **delta_processed_ongoing** : **ongoing_works_db** - **ongoing_works_processed**
- **delta_processed_ongoing_percen** :  (**ongoing_works_db** - **ongoing_works_processed**)*100/**ongoing_works_db**
- **flagged_works_gis_rule** : Total number of works flagged as per gis rule
- **flagged_works_gis_rule_percen** :  **flagged_works_gis_rule**  *100 / **ongoing_works_db**
- **ongoing_works_sent_nic** : Total geo rule works sent to NIC through API                                                              

"""

dashboard_show_cols_st = """
- **sno** : sno
- **state_name** : State name
- **state_code** : State Code 
- **dashboard_works_api** : Aggregate numbers of dashboard works counts received from NIC nrega through API
- **dashboard_works_db** :  Individual dashboard works received from NIC nrega through API
- **ongoing_works_db** : Individual onoing works received from NIC nrega through API
- **delta_dashboard** : **dashboard_works_api** - **dashboard_works_db** 
- **delta_dashboard_percen** : (**dashboard_works_api** - **dashboard_works_db**)*100/**dashboard_works_api**
- **delta_ong_dashboard** :  **dashboard_works_api** - **ongoing_works_db**
- **delta_dashboard_ongoing_percen** :  (**dashboard_works_api** - **ongoing_works_db**)*100/dashboard_works_api
"""

dashboard_show_cols_blocks = """ 
- **sno** : sno
- **state_name** : State name
- **state_code** : State Code 
- **block_name** : Block Name
- **block_code** : Block Code
- **dashboard_works_api** : Aggregate numbers of dashboard works counts received from NIC nrega through API
- **dashboard_works_db** :  Individual dashboard works received from NIC nrega through API
- **ongoing_works_db** : Individual onoing works received from NIC nrega through API
- **delta_dashboard** : **dashboard_works_api** - **dashboard_works_db** 
- **delta_dashboard_percen** : (**dashboard_works_api** - **dashboard_works_db**)*100/**dashboard_works_api**
- **delta_ong_dashboard** :  **dashboard_works_api** - **ongoing_works_db**
- **delta_dashboard_ongoing_percen** :  (**dashboard_works_api** - **ongoing_works_db**)*100/dashboard_works_api


"""

def main(select_button):

    if select_button == 'Summary':
        st.success('Work Risk 25th June (SP1) run got successful. The below table overall run stats !', icon="✅")

        st.success('Work Risk 1st July (SP2) run got successful. The below table overall run stats !', icon="✅")


        stats_dict = {'sno':1, 'ai_rule_total_received': int(ai_block_df['stage2_works_db'].sum()) , 
         'flagged_works_ai_rule' : int(ai_block_df['flagged_works_ai_rule'].sum()) , 
         'gis_rule_total_received': int(gis_block_df['ongoing_works_db'].sum())  , 
         'gis_rule_total_flagged' : int(gis_block_df['flagged_works_gis_rule'].sum())  }
        
        st.markdown(f"#### Last Updated: {date_value}")
        stats_df = pd.DataFrame([stats_dict])

        st.dataframe(stats_df)
    

        # display_aggrid(stats_df, date_value, cols_color_pattern='pattern' )

        st.write('Kindly click below side rule buttons to get detailed overall process flow ')

    elif select_button == 'AI Rule':
        state, block = st.tabs(['State', 'Block'])
        with state:
            st.markdown(f"#### Last Updated: {date_value}")
            # Convert DataFrame to CSV
           
            with st.expander("Click here to see column definitions"):
                st.write(ai_show_cols_st)

            display_aggrid(ai_state_df, date_value, cols_color_pattern='pattern' )

            ai_state_csv_data = ai_state_df.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="Download raw data as CSV",
                data=ai_state_csv_data,
                file_name="ai_rule_state_dwn.csv",
                mime="text/csv",
                )

        with block:
            st.markdown(f"#### Last Updated: {date_value}")
            with st.expander(" Click here to see column definitions"):
                st.write(ai_show_cols_blocks)

            display_aggrid(ai_block_df, date_value, cols_color_pattern='pattern' )

            ai_blocks_csv_data = ai_block_df.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="Download raw data as CSV",
                data=ai_blocks_csv_data,
                file_name="ai_rule_block_dwn.csv",
                mime="text/csv",
                )

    elif select_button == 'GIS Rule':
        state, block = st.tabs(['State', 'Block'])
        with state:
            st.markdown(f"#### Last Updated: {date_value}")

            with st.expander("Click here to see column definitions"):
                st.write(gis_show_cols_st)

            display_aggrid(gis_state_df, date_value, cols_color_pattern='pattern' )

            gis_state_csv_data = gis_state_df.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="Download raw data as CSV",
                data=gis_state_csv_data,
                file_name="gis_rule_state_dwn.csv",
                mime="text/csv",
                )
        with block:
            st.markdown(f"#### Last Updated: {date_value}")
            with st.expander(" Click here to see column definitions"):
                st.write(gis_show_cols_blocks)
            display_aggrid(gis_block_df, date_value, cols_color_pattern='pattern' )


            gis_blocks_csv_data = gis_block_df.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="Download raw data as CSV",
                data=gis_blocks_csv_data,
                file_name="gis_rule_block_dwn.csv",
                mime="text/csv",
                )

    elif select_button == 'Power Bi Dashboard':
        state, block = st.tabs(['State', 'Block'])
        with state:
            st.markdown(f"#### Last Updated: {date_value}")

            with st.expander("Click here to see column definitions"):
                st.write(dashboard_show_cols_st)

            display_aggrid(dashboard_state_df, date_value, cols_color_pattern='pattern' )

            workrisk_dashboard_state_csv_data = dashboard_state_df.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="Download raw data as CSV",
                data=workrisk_dashboard_state_csv_data,
                file_name="workrisk_dashboard_rule_state_dwn.csv",
                mime="text/csv",
                )
        with block:
            st.markdown(f"#### Last Updated: {date_value}")
            with st.expander(" Click here to see column definitions"):
                st.write(dashboard_show_cols_blocks)
            display_aggrid(dashboard_block_df, date_value, cols_color_pattern='pattern' )

            workrisk_dashboard_blocks_csv_data = dashboard_block_df.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="Download raw data as CSV",
                data=workrisk_dashboard_blocks_csv_data,
                file_name="workrisk_dashboard_rule_block_dwn.csv",
                mime="text/csv",
                )



if __name__ == '__main__':
    main(wr_select_bt)




