import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from pathlib import Path
from dashboard.pages import wr_map


def app():
    # UCC Data CSV to DF
    mdf_csv = Path(__file__).parents[1] / 'data/merged_tdf.csv'
    mdf = pd.read_csv(mdf_csv)

    # Make UCC Data just Big Balers
    wr_df = mdf.loc[mdf['descr'] == 'WINDROWER']

    # Page Title
    st.markdown("<h1 style='text-align: center;height: 120px;'>WINDROWER DASHBOARD</h1>",
                unsafe_allow_html=True)

    # First KPI Script
    market_share1 = wr_df['brand'].value_counts(normalize=True)
    market_share2 = market_share1.apply(lambda x: "{:.0f}%".format(x * 100))
    market_share = market_share2.to_frame()
    market_share.columns = ['market share']
    market_value = str(market_share1)
    market_share_value = market_value.split()[0]
    market_share_delta = market_share2[0]

    # Second KPI Script
    wr_models = str(wr_df['model'].value_counts().nlargest(1))
    wr_models_select = wr_models.split()[0]
    wr_model_delta = wr_models.split()[1]

    # Third KPI Script
    wr_model_nh = str(wr_df['model'].value_counts().nlargest(9))
    wr_model_nh_select = wr_model_nh.split()[16]
    wr_model_nh_delta = wr_model_nh.split()[17]

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
        value=wr_models_select,
        delta=f"{wr_model_delta} units"
    )

    kpi3.metric(
        label="Top Sold New Holland",
        value=f"{wr_model_nh_select}",
        delta=f"{wr_model_nh_delta} units"
    )

    # Bring MapBuilder in and Process Selection to Map
    mb = wr_map.PagesMapBuilder()

    @st.cache
    def process_selection(selection):
        m = mb.pages_build_map(selection)
        m_ = m.get_root().render()
        return m_

    # Column Script
    wr_brands = wr_df['brand'].value_counts()
    wr_brands = wr_brands.to_frame()
    wr_brands.columns = ['count']

    # Two Columns in Middle of Dashboard
    fig_col1, fig_col2 = st.columns(2)

    with fig_col1:
        # Selection Widget
        option_all = ['ALL'] + list(pd.unique(wr_df['brand']))
        st.markdown("<h1 style='text-align: left; font-size: 18px;"
                    "'>DISTRIBUTION MAP</h1>",
                    unsafe_allow_html=True)
        selected = st.selectbox("Choose BRAND to show on map --***Click on point to see details***--",
                                option_all)
        st.components.v1.html(process_selection(selected), height=610)
    with fig_col2:
        wr_brand_shares = wr_brands.merge(market_share, left_index=True, right_index=True)

        # Build Title and Dataframe to show Market Share DF
        st.markdown("<h1 style='text-align: left; font-size: 18px;"
                    "'>BRAND PERCENTAGE OF MARKET</h1>",
                    unsafe_allow_html=True)
        st.dataframe(wr_brand_shares, use_container_width=True)

        # Build Title and Dataframe to show Brand Model Counts
        grouped_df = wr_df.groupby(['brand', 'model']).size().reset_index(name='counts').sort_values(by='counts',
                                                                                                     ascending=False)
        grouped_df.reset_index(drop=True, inplace=True)
        st.markdown("<h1 style='text-align: left; font-size: 18px;"
                    "'>BRAND MODEL COUNTS</h1>",
                    unsafe_allow_html=True)
        st.dataframe(grouped_df, use_container_width=True)

    # Raw Data on Bottom of Dashboard
    st.markdown("### RAW DATA")
    st.dataframe(wr_df, use_container_width=True)
