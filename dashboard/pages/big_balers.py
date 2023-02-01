import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from pathlib import Path
from dashboard.generators import bb_map


def app():
    # UCC Data CSV to DF
    mdf_csv = Path(__file__).parents[2] / 'data/merged_tdf.csv'
    mdf = pd.read_csv(mdf_csv)

    # Make UCC Data just Big Balers
    bb_df = mdf.loc[mdf['equip_size_descr'] == "SQUARE FOOTAGE 4' OR MORE"]

    # Page Title
    st.markdown("<h1 style='text-align: center;height: 120px;'>BIG BALERS DASHBOARD</h1>",
                unsafe_allow_html=True)

    # First KPI Script
    market_share1 = bb_df['brand'].value_counts(normalize=True)
    market_share2 = market_share1.apply(lambda x: "{:.0f}%".format(x * 100))
    market_share = market_share2.to_frame()
    market_share.columns = ['market share']
    market_value = str(market_share1)
    market_share_value = market_value.split()[0]
    market_share_delta = market_share2[0]

    # Second KPI Script
    bb_models = str(bb_df['model'].value_counts().nlargest(1))
    bb_models_select = bb_models.split()[0]
    bb_model_delta = bb_models.split()[1]

    # Third KPI Script
    bb_model_nh = str(bb_df['model'].value_counts().nlargest(3))
    bb_model_nh_select = bb_model_nh.split()[2]
    bb_model_nh_delta = bb_model_nh.split()[3]

    # KPI Metrics Columns
    kpi1, kpi2, kpi3 = st.columns(3)

    # KPI Metrics
    kpi1.metric(
        label="Top Brand Market Share",
        value=market_share_value,
        delta=f"{market_share_delta}"
    )

    kpi2.metric(
        label="Top Sold Model",
        value=bb_models_select,
        delta=f"{bb_model_delta} units"
    )

    kpi3.metric(
        label="Top Sold New Holland",
        value=f"{bb_model_nh_select}",
        delta=f"{bb_model_nh_delta} units"
    )

    # Bring MapBuilder in and Process Selection to Map
    mb = bb_map.PagesMapBuilder()

    @st.cache
    def process_selection(selection):
        m = mb.pages_build_map(selection)
        m_ = m.get_root().render()
        return m_

    # Column Script
    bb_brands = bb_df['brand'].value_counts()
    bb_brands = bb_brands.to_frame()
    bb_brands.columns = ['count']

    # Two Columns in Middle of Dashboard
    fig_col1, fig_col2 = st.columns(2)

    with fig_col1:
        # Selection Widget
        option_all = ['ALL'] + list(pd.unique(bb_df['brand']))
        st.markdown("<h1 style='text-align: left; font-size: 18px;"
                    "'>DISTRIBUTION MAP</h1>",
                    unsafe_allow_html=True)
        selected = st.selectbox("Choose BRAND to show on map --***Click on point to see details***--",
                                option_all)
        st.components.v1.html(process_selection(selected), height=610)
    with fig_col2:
        bb_brand_shares = bb_brands.merge(market_share, left_index=True, right_index=True)

        # Build Title and Dataframe to show Market Share DF
        st.markdown("<h1 style='text-align: left; font-size: 18px;"
                    "'>BRAND PERCENTAGE OF MARKET</h1>",
                    unsafe_allow_html=True)
        st.dataframe(bb_brand_shares, use_container_width=True)

        # Build Title and Dataframe to show Brand Model Counts
        grouped_df = bb_df.groupby(['brand', 'model']).size().reset_index(name='counts').sort_values(by='counts',
                                                                                                     ascending=False)
        grouped_df.reset_index(drop=True, inplace=True)
        st.markdown("<h1 style='text-align: left; font-size: 18px;"
                    "'>BRAND MODEL COUNTS</h1>",
                    unsafe_allow_html=True)
        st.dataframe(grouped_df, use_container_width=True)

    # Raw Data on Bottom of Dashboard
    st.markdown("### RAW DATA")
    st.dataframe(bb_df, use_container_width=True)
