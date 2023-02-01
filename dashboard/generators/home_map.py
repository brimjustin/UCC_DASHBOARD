import json
import folium
from folium.elements import Element
import pandas as pd
from pathlib import Path


# CSV to DF
ucc_csv = Path(__file__).parents[0] / 'data/merged_tdf.csv'
ucc_data = pd.read_csv(ucc_csv)


# Get the center of my map for plotting
def get_center_latlon():
    center_lat = (ucc_data['lat'].max() + ucc_data['lat'].min()) / 2
    center_lon = (ucc_data['lon'].max() + ucc_data['lon'].min()) / 2
    return center_lat, center_lon


# Create a style function
def style_function():
    return {
        'fillColor': 'white',
        'color': 'black',
        'weight': 2,
        'fillOpacity': 0.5
    }


def value_to_color(value):
    if value == 0:
        return '#f0cc04'
    elif value < 23:
        return '#de3230'
    elif value < 25:
        return '#66cc00'
    elif value < 26:
        return '#0174aa'
    elif value < 40:
        return '#ff9342'
    elif value < 50:
        return '#e29fe6'
    elif value < 60:
        return '#d46fd9'
    elif value < 70:
        return '#c53fcd'
    elif value < 80:
        return '#b70fc0'
    elif value < 90:
        return '#9f9ca3'
    elif value < 100:
        return '#706b74'
    elif value < 130:
        return '#100818'
    elif value < 160:
        return '#100818'
    elif value < 190:
        return '#100818'
    elif value < 210:
        return '#100818'
    elif value < 290:
        return '#100818'
    else:
        return '#100818'


# Color Value Column
ucc_data['color'] = ucc_data['hp'].apply(value_to_color)


class MapBuilder:
    @staticmethod
    def build_map(selection):
        # Get the center of our map using our cool function
        center = get_center_latlon()

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
            style_function=style_function
        ).add_to(selected_m)

        selected_rows = ucc_data[ucc_data['descr'] == selection]

        if selection == "ALL":
            for index, row in ucc_data.iterrows():
                # Create an HTML table
                selected_html = '<table>'
                selected_html += '<tr><td>Brand:</td><td>{}</td></tr>'.format(row['brand'])
                selected_html += '<tr><td>Model:</td><td>{}</td></tr>'.format(row['model'])
                selected_html += '<tr><td>HP:</td><td>{}</td></tr>'.format(row['hp'])
                selected_html += '</table>'
                # Create a popup
                selected_popup = folium.Popup(folium.IFrame(selected_html, width=200, height=100),
                                              max_width=250)
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
                selected_html += '<tr><td>HP:</td><td>{}</td></tr>'.format(row['hp'])
                selected_html += '</table>'
                # Create a popup
                selected_popup = folium.Popup(folium.IFrame(selected_html, width=200, height=100),
                                              max_width=250)
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
        hps = ucc_data['hp'].value_counts()

        # Create marker for each group of markers
        group0_marker = hps.at[0]
        group1_marker = hps.loc[[18, 19, 20, 22]].sum()
        group2_marker = hps.loc[[23, 24]].sum()
        group3_marker = hps.loc[[25]].sum()
        group4_marker = hps.loc[[30, 31, 33, 34, 35, 36, 37]].sum()
        group5_marker = hps.loc[[38, 39, 40, 42, 45, 47]].sum()
        group6_marker = hps.loc[[49, 50, 52, 53, 54, 55, 56]].sum()
        group7_marker = hps.loc[[59, 60, 61, 62, 63, 65]].sum()
        group8_marker = hps.loc[[70, 71, 74, 75]].sum()
        group9_marker = hps.loc[[80, 84, 85, 86]].sum()
        group10_marker = hps.loc[[90, 98]].sum()
        group11_marker = hps.loc[[100, 105, 106, 110, 113, 115, 117, 120,
                                  123, 125, 130, 145, 150, 155, 160, 175,
                                  220, 230, 240, 260, 300, 310, 350, 520]].sum()

        # Create HTML code for legend
        legend_html = '''
                   <div style="position: absolute;
                               top: 20px; right: 20px; width: 160px; height: 410px;
                               border:2px solid grey; z-index:9999; font-size:14px;
                               background:rgba(255, 255, 255, 0.8);
                               ">
                        <h4 style="text-align: center;">ALL COUNT</h4>
                     <div style="display: flex; flex-direction: row; align-items: center;justify-content: left;">
                       <div style="height: 20px; width: 20px; margin-left: 5px; background-color: #f0cc04;
                       border-radius: 50%;"></div>
                       <p style="margin-left: 5px;">0 HP: {}</p>
                     </div>
                     <div style="display: flex; flex-direction: row; align-items: center;justify-content: left;">
                       <div style="height: 20px; width: 20px; margin-left: 5px; background-color: #de3230;
                       border-radius: 50%;"></div>
                       <p style="margin-left: 5px;"> > 22 HP: {}</p>
                     </div>
                     <div style="display: flex; flex-direction: row; align-items: center;justify-content: left;">
                     <div style="height: 20px; width: 20px; margin-left: 5px; background-color: #66cc00;
                       border-radius: 50%;"></div>
                       <p style="margin-left: 5px;"> > 24 HP: {}</p>
                     </div>
                     <div style="display: flex; flex-direction: row; align-items: center;justify-content: left;">
                     <div style="height: 20px; width: 20px; margin-left: 5px; background-color: #ff9342;
                       border-radius: 50%;"></div>
                       <p style="margin-left: 5px;"> = 25 HP: {}</p>
                     </div>
                     <div style="display: flex; flex-direction: row; align-items: center;justify-content: left;">
                     <div style="height: 20px; width: 20px; margin-left: 5px; background-color: #0174aa;
                       border-radius: 50%;"></div>
                       <p style="margin-left: 5px;"> 30s HP: {}</p>
                     </div>
                     <div style="display: flex; flex-direction: row; align-items: center;justify-content: left;">
                     <div style="height: 20px; width: 20px; margin-left: 5px; background-color: #e29fe6;
                       border-radius: 50%;"></div>
                       <p style="margin-left: 5px;">40s HP: {}</p>
                     </div>
                     <div style="display: flex; flex-direction: row; align-items: center;justify-content: left;">
                     <div style="height: 20px; width: 20px; margin-left: 5px; background-color: #d46fd9;
                       border-radius: 50%;"></div>
                       <p style="margin-left: 5px;">50s HP: {}</p>
                     </div>
                     <div style="display: flex; flex-direction: row; align-items: center;justify-content: left;">
                     <div style="height: 20px; width: 20px; margin-left: 5px; background-color: #c53fcd;
                       border-radius: 50%;"></div>
                       <p style="margin-left: 5px;">60s HP: {}</p>
                     </div>
                     <div style="display: flex; flex-direction: row; align-items: center;justify-content: left;">
                     <div style="height: 20px; width: 20px; margin-left: 5px; background-color: #b70fc0;
                       border-radius: 50%;"></div>
                       <p style="margin-left: 5px;">70s HP: {}</p>
                     </div>
                     <div style="display: flex; flex-direction: row; align-items: center;justify-content: left;">
                     <div style="height: 20px; width: 20px; margin-left: 5px; background-color: #9f9ca3;
                       border-radius: 50%;"></div>
                       <p style="margin-left: 5px;">80s HP: {}</p>
                     </div>
                     <div style="display: flex; flex-direction: row; align-items: center;justify-content: left;">
                     <div style="height: 20px; width: 20px; margin-left: 5px; background-color: #706b74;
                       border-radius: 50%;"></div>
                       <p style="margin-left: 5px;">90s HP: {}</p>
                     </div>
                     <div style="display: flex; flex-direction: row; align-items: center;justify-content: left;">
                     <div style="height: 20px; width: 20px; margin-left: 5px; background-color: #100818;
                       border-radius: 50%;"></div>
                       <p style="margin-left: 5px;">100-300+ HP: {}</p>
                     </div>
                   </div>
                   '''.format(group0_marker, group1_marker, group2_marker, group3_marker,
                              group4_marker, group5_marker, group6_marker,
                              group7_marker, group8_marker, group9_marker,
                              group10_marker, group11_marker)

        selected_m.get_root().html.add_child(folium.elements.Element(legend_html))

        return selected_m
