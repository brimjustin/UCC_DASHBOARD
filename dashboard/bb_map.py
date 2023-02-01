import json
import folium
from folium.elements import Element
import pandas as pd
from pathlib import Path
import home_map

# CSV to DF
ucc_csv = Path(__file__).parents[1] / 'data/merged_tdf.csv'
m_data = pd.read_csv(ucc_csv)
m_data = m_data.loc[m_data['equip_size_descr'] == "SQUARE FOOTAGE 4' OR MORE"]


# DETERMINE HOW TO COLOR FOR BRANDS
def value_to_color(value):
    if value == 'MASSEY':
        return '#de3230'
    elif value == 'KRONE':
        return '#f0cc04'
    elif value == 'NEW HOLLAND':
        return '#0174aa'
    elif value == 'DEERE':
        return '#66cc00'
    elif value == 'CHALLENGER':
        return '#100818'


# Color Value Column
m_data['color'] = m_data['brand'].apply(value_to_color)


class PagesMapBuilder:
    @staticmethod
    def pages_build_map(selection):
        # Get the center of our map using our cool function
        center = home_map.get_center_latlon()

        # Selected folium map
        selected_m = folium.Map(location=center,
                                zoom_start=6,
                                tiles='cartodbpositron')

        # Load my geojson file which contains my Polygons
        boundary_file = Path(__file__).parents[1] / 'data/georef-counties.geojson'
        with open(boundary_file, 'r') as f:
            latlon_boundary = json.load(f)

        # Add county polygons
        folium.GeoJson(
            data=latlon_boundary,
            name='geojson',
            style_function=home_map.style_function
        ).add_to(selected_m)

        selected_rows = m_data[m_data['brand'] == selection]

        if selection == "ALL":
            for index, row in m_data.iterrows():
                # Create an HTML table
                selected_html = '<table>'
                selected_html += '<tr><td>Brand:</td><td>{}</td></tr>'.format(row['brand'])
                selected_html += '<tr><td>Model:</td><td>{}</td></tr>'.format(row['model'])
                selected_html += '<tr><td>Company:</td><td>{}</td></tr>'.format(row['company_name'])
                selected_html += '<tr><td>Customer:</td><td>{}</td></tr>'.format(row['customer_name'])
                selected_html += '<tr><td>City:</td><td>{}</td></tr>'.format(row['city'])
                selected_html += '</table>'
                # Create a popup
                selected_popup = folium.Popup(folium.IFrame(selected_html, width=230, height=150, ratio='60%'),
                                              max_width=300)
                # Add a marker to the map
                folium.CircleMarker(
                    location=(row['lat'], row['lon']),
                    radius=2,
                    color=row['color'],
                    fill=True,
                    fill_color='red',
                    fill_opacity=0.6,
                    popup=selected_popup
                ).add_to(selected_m)
        else:
            for index, row in selected_rows.iterrows():
                # Create an HTML table
                selected_html = '<table>'
                selected_html += '<tr><td>Brand:</td><td>{}</td></tr>'.format(row['brand'])
                selected_html += '<tr><td>Model:</td><td>{}</td></tr>'.format(row['model'])
                selected_html += '<tr><td>Company:</td><td>{}</td></tr>'.format(row['company_name'])
                selected_html += '<tr><td>Customer:</td><td>{}</td></tr>'.format(row['customer_name'])
                selected_html += '<tr><td>City:</td><td>{}</td></tr>'.format(row['city'])
                selected_html += '</table>'
                # Create a popup
                selected_popup = folium.Popup(folium.IFrame(selected_html, width=230, height=150, ratio='60%'),
                                              max_width=300)
                # Add a marker to the map
                folium.CircleMarker(
                    location=(row['lat'], row['lon']),
                    radius=2,
                    color=row['color'],
                    fill=True,
                    fill_color='red',
                    fill_opacity=0.6,
                    popup=selected_popup
                ).add_to(selected_m)

        # Legend DF
        bb_count = m_data['brand'].value_counts()

        # Create marker for each group of markers
        group0_marker = bb_count.loc['MASSEY']
        group1_marker = bb_count.loc['NEW HOLLAND']
        group2_marker = bb_count.loc['KRONE']
        group3_marker = bb_count.loc['DEERE']
        group4_marker = bb_count.loc['CHALLENGER']

        # Create HTML code for legend
        legend_html = '''
                           <div style="position: absolute;
                                       top: 20px; right: 20px; width: 155px; height: 180px;
                                       border:2px solid grey; z-index:9999; font-size:12px;
                                       background:rgba(255, 255, 255, 0.8);
                                       ">
                                <h4 style="text-align: center;">TOTAL SALES</h4>
                             <div style="display: flex; flex-direction: row; align-items: center;justify-content: left;">
                               <div style="height: 20px; width: 20px; margin-left: 5px; background-color: #de3230;
                               border-radius: 50%;"></div>
                               <p style="margin-left: 5px;">MASSEY: {}</p>
                             </div>
                             <div style="display: flex; flex-direction: row; align-items: center;justify-content: left;">
                               <div style="height: 20px; width: 20px; margin-left: 5px; background-color: #0174aa;
                               border-radius: 50%;"></div>
                               <p style="margin-left: 5px;">NEW HOLLAND: {}</p>
                             </div>
                             <div style="display: flex; flex-direction: row; align-items: center;justify-content: left;">
                             <div style="height: 20px; width: 20px; margin-left: 5px; background-color: #f0cc04; 
                               border-radius: 50%;"></div>
                               <p style="margin-left: 5px;">KRONE: {}</p>
                             </div>
                             <div style="display: flex; flex-direction: row; align-items: center;justify-content: left;">
                             <div style="height: 20px; width: 20px; margin-left: 5px; background-color: #66cc00;
                               border-radius: 50%;"></div>
                               <p style="margin-left: 5px;">DEERE: {}</p>
                             </div>
                             <div style="display: flex; flex-direction: row; align-items: center;justify-content: left;">
                             <div style="height: 20px; width: 20px; margin-left: 5px; background-color: #100818;
                               border-radius: 50%;"></div>
                               <p style="margin-left: 5px;">CHALLENGER: {}</p>
                             </div>
                           </div>
                           '''.format(group0_marker, group1_marker, group2_marker, group3_marker,
                                      group4_marker)

        selected_m.get_root().html.add_child(folium.elements.Element(legend_html))

        return selected_m
