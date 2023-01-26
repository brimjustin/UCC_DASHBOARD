import pandas as pd
import streamlit as st
import home_map
import streamlit.components.v1 as components
from pathlib import Path
from PIL import Image


def app():
    # UCC Data CSV to DF
    tdf_csv = Path(__file__).parents[1] / 'merged_tdf.csv'
    tdf = pd.read_csv(tdf_csv)

    # NH CSV to DF
    nh_df_csv = Path(__file__).parents[1] / 'data/nh_df.csv'
    nh_df = pd.read_csv(nh_df_csv)
    tdf_dfm = tdf.query("brand != 'NEW HOLLAND' & brand != 'YANMAR'")

    # Merge DFs
    dfm = pd.merge(tdf_dfm, nh_df, on='hp', how='right')
    dfm_subset = dfm[['brand', 'model_x', 'hp', 'model_y']]

    # First KPI script
    top_seller = tdf['model'].value_counts().nlargest(1).index
    top_seller_delta = tdf['model'].value_counts().nlargest(1)
    delta_value = top_seller_delta[0].astype(str)
    top_seller_str = ",".join(str(i) for i in top_seller)

    # Second KPI script
    tdf2 = tdf[tdf.hp != '0']
    tdf2 = tdf2['hp']
    top_hp = str(tdf2.value_counts().nlargest(2))
    top_hp_select = top_hp.split()[2]
    top_hp_delta = tdf2.value_counts()
    hp_delta_value = top_hp_delta.loc[25].astype(int)

    # Third KPI script
    top_eqv_model = str(dfm_subset.value_counts().nlargest(1))
    top_eqv_select = top_eqv_model.split()[7]
    top_eqv_delta = dfm_subset.value_counts()
    eqv_delta_value = top_eqv_delta.iloc[0].astype(str)

# remove to run whole script necessary?? or Keep and add main() at the end (see chatgpt log)
#     def main():
    # Add Brim Logo
    brim_logo = Path(__file__).parents[1] / 'data/brimlogo3.png'
    image = Image.open(brim_logo)

    # Create three columns for Logo to be centered
    one, two, three = st.columns(3)
    one.empty()
    two.image(image)
    three.empty()

    # Page Title
    st.markdown("<h1 style='text-align: center;height: 120px;'>UCC DATA DASHBOARD</h1>", unsafe_allow_html=True)

    # Top KPI Columns
    kpi1, kpi2, kpi3 = st.columns(3)

    # KPI Metrics
    kpi1.metric(
        label="Top Sold Model",
        value=top_seller_str,
        delta=f"{delta_value} units"
    )

    kpi2.metric(
        label="Top Sold HP",
        value=f"{top_hp_select} HP",
        delta=f"{hp_delta_value} units"
    )

    kpi3.metric(
        label="Top Equivalent Model",
        value=top_eqv_select,
        delta=f"{eqv_delta_value} units"
    )

    # Bring MapBuilder in and Process Selection to Map
    mb = home_map.MapBuilder()

    @st.cache
    def process_selection(selection):
        m = mb.build_map(selection)
        m_ = m.get_root().render()
        return m_

    # Two Columns in Middle of Dashboard
    fig_col1, fig_col2 = st.columns(2)

    with fig_col1:
        # Selection Widget
        option_all = ['ALL'] + list(pd.unique(tdf['descr']))
        st.markdown("<h1 style='text-align: left; font-size: 18px;"
                    "'>DISTRIBUTION MAP</h1>",
                    unsafe_allow_html=True)
        selected = st.selectbox("Choose TYPE to show on map --***Click on point to see details***--",
                                option_all)
        st.components.v1.html(process_selection(selected), height=680)

    with fig_col2:
        # Equivalents Selection Widget/DF
        model_y_options = dfm_subset['model_y'].unique()
        model_y_options.sort()
        st.markdown("<h1 style='text-align: left; font-size: 18px;"
                    "'>MODEL EQUIVALENTS</h1>",
                    unsafe_allow_html=True)
        selected_model_y = st.selectbox("Choose New Holland or Yanmar MODEL to see equivalents by HP range.",
                                        model_y_options)
        # Use the selected value to filter the rows in the dataframe
        selected_rows = dfm_subset.loc[dfm_subset['model_y'] == selected_model_y]
        # Get the mean hp value
        mean_hp = selected_rows['hp'].mean()
        # Set a fixed tolerance value
        tolerance = 3
        # Filter the DataFrame to get the rows where the hp column is
        # within the selected range and the model_y column is not the selected one
        equivalents = tdf_dfm.loc[
            (tdf_dfm['hp'] >= mean_hp - tolerance) & (tdf_dfm['hp'] <= mean_hp + tolerance - 1) & (
                        dfm_subset['model_y'] != selected_model_y)].drop_duplicates(
            subset=['brand', 'model', 'hp'])

        st.dataframe(equivalents[['brand', 'model', 'hp']], use_container_width=True, height=200)

        st.markdown("<h1 style='text-align: left; font-size: 18px; height: 80px;"
                    "'>Amount of instances for TYPE or GROUP:</h1>",
                    unsafe_allow_html=True)
        grouped_df = tdf.groupby('group_sale')['descr'].apply(list).value_counts()
        st.dataframe(grouped_df, use_container_width=True)

    # Raw Data on Bottom of Dashboard
    st.markdown("### RAW DATA")
    st.dataframe(tdf, use_container_width=True)
