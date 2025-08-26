# Import libraries that may be useful for this code
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import VarianceThreshold
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm
import math as math
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
import plotly as py
import plotly.express as px
import requests
!pip install dash
from dash import Dash, html, dcc, Input, Output

clean_nan_primary_data=pd.read_excel("clean_nan_primary_data.xlsx") # Read the data (MIT Database) from excel using pandas


average_data = pd.read_excel("Average.xlsx") # Read the data (INEGI averaged AGEBS Database) from excel using pandas
average_data["Estado"] = average_data["Estado"].replace({"Estado de México": "México"})

clean_nan_primary_data['Campus'] = clean_nan_primary_data['Campus'].astype("category")
clean_nan_primary_data['Tipo de negocio'] = clean_nan_primary_data['Tipo de negocio'].astype("category")
clean_nan_primary_data['Año de apertura del negocio'] = clean_nan_primary_data['Año de apertura del negocio'].astype("int64")
clean_nan_primary_data['¿Cuántas personas trabajaron con un salario fijo durante el último mes?'] = clean_nan_primary_data['¿Cuántas personas trabajaron con un salario fijo durante el último mes?'].astype("int64")
clean_nan_primary_data['Durante el último mes, ¿tuviste más, menos, o el mismo número de clientes en tu negocio?'] = clean_nan_primary_data['Durante el último mes, ¿tuviste más, menos, o el mismo número de clientes en tu negocio?'].astype("category")
clean_nan_primary_data['¿Tus ventas actuales están mejor, peor o igual en comparación con hace un mes?'] = clean_nan_primary_data['¿Tus ventas actuales están mejor, peor o igual en comparación con hace un mes?'].astype("category")
clean_nan_primary_data['¿Durante el último mes tu nivel de inventario aumentó, disminuyó o permaneció igual?'] = clean_nan_primary_data['¿Durante el último mes tu nivel de inventario aumentó, disminuyó o permaneció igual?'].astype("category")
clean_nan_primary_data['En promedio, ¿el precio de venta de los productos que vende este establecimiento aumentó, bajó o permaneció igual a hace un mes?'] = clean_nan_primary_data['En promedio, ¿el precio de venta de los productos que vende este establecimiento aumentó, bajó o permaneció igual a hace un mes?'].astype("category")
clean_nan_primary_data['Qué tanto impacta a tu negocio: - El crimen'] = clean_nan_primary_data['Qué tanto impacta a tu negocio: - El crimen'].astype("category")
clean_nan_primary_data['Qué tanto impacta a tu negocio: - La falta de crédito'] = clean_nan_primary_data['Qué tanto impacta a tu negocio: - La falta de crédito'].astype("category")
clean_nan_primary_data['Qué tanto impacta a tu negocio: - La competencia'] = clean_nan_primary_data['Qué tanto impacta a tu negocio: - La competencia'].astype("category")
clean_nan_primary_data['Asume que tienes los medios para hacer crecer tu negocio, ¿quisieras que tu negocio creciera? (por ejemplo, con más empleados, más productos, un local más grande)'] = clean_nan_primary_data['Asume que tienes los medios para hacer crecer tu negocio, ¿quisieras que tu negocio creciera? (por ejemplo, con más empleados, más productos, un local más grande)'].astype("category")
clean_nan_primary_data['¿Cuál sería el salario mensual más bajo que estaría dispuesto a aceptar para cerrar el negocio y'] = clean_nan_primary_data['¿Cuál sería el salario mensual más bajo que estaría dispuesto a aceptar para cerrar el negocio y'].astype("float64")
clean_nan_primary_data['Horario de apertura'] = clean_nan_primary_data['Horario de apertura'].astype("category")
clean_nan_primary_data['Horario de cierre'] = clean_nan_primary_data['Horario de cierre'].astype("category")
clean_nan_primary_data['Sexo del dueño o dueña'] = clean_nan_primary_data['Sexo del dueño o dueña'].astype("category")
clean_nan_primary_data['¿El local de su negocio es rentado o propio?'] = clean_nan_primary_data['¿El local de su negocio es rentado o propio?'].astype("category")
clean_nan_primary_data['Educación del dueño'] = clean_nan_primary_data['Educación del dueño'].astype("category")
clean_nan_primary_data['Edad del dueño o dueña'] = clean_nan_primary_data['Edad del dueño o dueña'].astype("category")

# Variable options for choropleth map
map_variable_options = {
    "Negocios por estado": "Negocios por estado",
    "Ingresos en miles de pesos por año": "Ingresos en miles de pesos por año",
    "Gastos en miles de pesos por año": "Gastos en miles de pesos por año",
    "Utilidad en miles de pesos por año": "Utilidad en miles de pesos por año",
    "Edad del negocio": "Edad del negocio",
    "Trabajadores": "Trabajadores",
    "Trabajadores_Hombres": "Trabajadores_Hombres",
    "Trabajadores_Mujeres": "Trabajadores_Mujeres",
    "Credito": "Credito"
}

# Load GeoJSON (Mexican states)
geojson_url = 'https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json'
mx_regions_geo = requests.get(geojson_url).json()

# Load your dataset 
df = clean_nan_primary_data.copy() # I do not know why that works, but I will leave it like that.

# Create the app
app = Dash(__name__)

# Get unique campus values
campus_options = df['Campus'].dropna().unique()

# Layout
app.layout = html.Div([
    html.Div([
        html.A(
            html.Img(
                src='assets/tec_logo.png',
                style={
                    'height': '90px',
                    'marginRight': 'auto',
                    'objectFit': 'contain'
                }
            ),
            href="https://tec.mx/es?srsltid=AfmBOorzc69ftYggJyk0CVkdXI4RFsWGmT7Yc4_GAgGz9CPBuKxdJWeW",
            target="_blank"
        ),
        html.A(
            html.Img(
                src='assets/mit_logo.png',
                style={
                    'height': '66px',
                    'marginLeft': 'auto',
                    'objectFit': 'contain'
                }
            ),
            href="https://liftlab.mit.edu/",
            target="_blank"
        )
    ], style={
        'display': 'flex',
        'justifyContent': 'space-between',
        'alignItems': 'center',
        'padding': '10px 40px',
        'backgroundColor': '#ffffff'
    }),

    html.H1("Análisis Regional de Nanotiendas 2025", style={"textAlign": "center", "fontFamily": "Segoe UI"}),

    html.Div([
        html.Label("Selecciona un campus:", style={
            "fontWeight": "bold",
            "fontFamily": "Segoe UI",
            "marginBottom": "10px"
        }),
        dcc.Dropdown(
            id="campus-dropdown",
            options=[{"label": campus, "value": campus} for campus in campus_options],
            value=campus_options[0],
            clearable=False,
            style={"width": "175px", "fontFamily": "Segoe UI"}
        )
    ], style={
        "display": "flex",
        "flexDirection": "column",
        "alignItems": "center",
        "marginBottom": "30px"
    }),

    html.Div([
        html.Div([
            html.H2("¿Qué tipos de negocio hay en tu área?", style={"fontWeight": "bold", "marginBottom": "10px"}),
            dcc.Graph(id="bar-graph")
        ], style={
            "backgroundColor": "#f9f9f9",
            "padding": "20px",
            "borderRadius": "12px",
            "boxShadow": "0 4px 6px rgba(0,0,0,0.1)",
            "fontFamily": "Segoe UI",
            "width": "48%",
            "display": "inline-block",
            "verticalAlign": "top"
        }),

        html.Div([
            html.H2("¿Qué tanto impactan a tu negocio...?", style={"fontWeight": "bold", "marginBottom": "10px"}),
            dcc.Graph(id="pie-graph")
        ], style={
            "backgroundColor": "#f9f9f9",
            "padding": "20px",
            "borderRadius": "12px",
            "boxShadow": "0 4px 6px rgba(0,0,0,0.1)",
            "fontFamily": "Segoe UI",
            "width": "48%",
            "display": "inline-block",
            "verticalAlign": "top",
            "marginLeft": "4%"
        })
    ], style={"width": "100%", "display": "flex", "justifyContent": "space-between"}),

    html.Div([
        html.H2("Panorama Nacional de Micronegocios", style={"fontWeight": "bold", "textAlign": "center"}),

        html.Div([
            html.Label("Selecciona una variable:", style={"fontWeight": "bold", "fontFamily": "Segoe UI"}),
            dcc.Dropdown(
                id="map-variable-dropdown",
                options=[{"label": k, "value": v} for k, v in map_variable_options.items()],
                value="Negocios por estado",
                clearable=False,
                style={"width": "400px", "margin": "auto"}
            )
        ], style={"textAlign": "center", "marginBottom": "20px"}),

        dcc.Graph(id="map-graph", style={"height": "600px"})
    ], style={
        "backgroundColor": "#f9f9f9",
        "padding": "20px",
        "borderRadius": "12px",
        "boxShadow": "0 4px 6px rgba(0,0,0,0.1)",
        "fontFamily": "Segoe UI",
        "width": "90%",
        "margin": "40px auto 20px auto"
    }),

    # Footer
    html.Div([
        html.Hr(style={"marginTop": "40px", "borderTop": "1px solid #ccc"}),

        html.Div([
            html.Div([
                html.Img(src="assets/antonio.jpeg", style={
                    "width": "140px", "height": "140px",
                    "borderRadius": "50%", "objectFit": "cover",
                    "marginBottom": "10px"
                }),
                html.P("Antonio Fonseca", style={"fontWeight": "bold", "margin": "0"}),
                html.P([
                    "Bachelor in Industrial Engineering", html.Br(),
                    "with a minor in Systems"
                ], style={"fontSize": "0.9em", "color": "#555", "margin": "0"})
            ], style={"textAlign": "center"}),

            html.Div([
                html.Img(src="assets/alejandro.jpeg", style={
                    "width": "140px", "height": "140px",
                    "borderRadius": "50%", "objectFit": "cover",
                    "marginBottom": "10px"
                }),
                html.P("Alejandro Toledo", style={"fontWeight": "bold", "margin": "0"}),
                html.P([
                    "Bachelor in Industrial Engineering", html.Br(),
                    "with a minor in Systems"
                ], style={"fontSize": "0.9em", "color": "#555", "margin": "0"})
            ], style={"textAlign": "center"}),

            html.Div([
                html.Img(src="assets/profesor.jpg", style={
                    "width": "120px", "height": "120px",
                    "borderRadius": "50%", "objectFit": "cover",
                    "marginBottom": "10px"
                }),
                html.P("Dr. Alan Vázquez", style={"fontWeight": "bold", "margin": "0"}),
                html.P("Supervising Professor", style={"fontSize": "0.85em", "color": "#777", "margin": "0"})
            ], style={"textAlign": "center"})
        ], style={
            "display": "flex",
            "justifyContent": "center",
            "gap": "80px",
            "padding": "30px 0"
        })
    ], style={"fontFamily": "Segoe UI", "backgroundColor": "#f9f9f9"})
], style={"padding": "40px", "backgroundColor": "#ffffff"})
    

# Callbacks
@app.callback(
    [Output("bar-graph", "figure"),
     Output("pie-graph", "figure")],
    [Input("campus-dropdown", "value")]
)
def update_charts(selected_campus):
    filtered_df = df[df["Campus"] == selected_campus]
    count_by_type = filtered_df["Tipo de negocio"].value_counts().reset_index()
    count_by_type.columns = ["Tipo de negocio", "Count"]

    # ✅ Modified Bar Chart (fig1) — horizontal, no legend
    fig1 = px.bar(
        count_by_type.sort_values("Count"),
        x="Count",
        y="Tipo de negocio",
        orientation="h",
        title=f"Tipos de negocio en {selected_campus}",
        color="Tipo de negocio"
    )

    fig1.update_layout(
        showlegend=False,
        xaxis_title="Número de negocios",
        yaxis_title="Tipo de negocio",
        font=dict(family="Segoe UI")
    )

    # Impacto de crimen, crédito y competencia (nuevo gráfico)
    impact_columns = [
        "Qué tanto impacta a tu negocio: - El crimen",
        "Qué tanto impacta a tu negocio: - La falta de crédito",
        "Qué tanto impacta a tu negocio: - La competencia"
    ]

    impact_data = (
        filtered_df[impact_columns]
        .melt(var_name="Factor", value_name="Impacto")
        .groupby(["Impacto", "Factor"])
        .size()
        .reset_index(name="Número de negocios")
    )

    # Aseguramos orden lógico de categorías
    categoria_ordenada = ["Nada", "Poco", "Algo", "Moderado", "Mucho"]
    impact_data["Impacto"] = pd.Categorical(impact_data["Impacto"], categories=categoria_ordenada, ordered=True)
    impact_data = impact_data.sort_values(["Impacto", "Factor"])

    fig2 = px.bar(
        impact_data,
        x="Impacto",
        y="Número de negocios",
        color="Factor",
        barmode="group",
        title=f"Percepción del impacto externo en {selected_campus}"
    )

    fig2.update_layout(
        font=dict(family="Segoe UI"),
        xaxis_title="Nivel de impacto",
        yaxis_title="Número de negocios"
    )

    return fig1, fig2

@app.callback(
    Output("map-graph", "figure"),
    Input("map-variable-dropdown", "value")
)
def update_map(selected_variable):
    # Usamos el segundo DataFrame para el mapa
    df_map = average_data.dropna(subset=["Estado", selected_variable])
    
    grouped = df_map.groupby("Estado", as_index=False)[selected_variable].sum()

    fig = px.choropleth(
        grouped,
        geojson=mx_regions_geo,
        locations="Estado",
        featureidkey="properties.name",
        color=selected_variable,
        color_continuous_scale="burg",
        title=f"{selected_variable} por Estado"
    )

    fig.update_geos(showcountries=True, showcoastlines=True, showland=True, fitbounds="locations")
    fig.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0})
    
    return fig

# Run app (no reloader for RStudio)
app.run(debug=True, port=8050, use_reloader=False)
