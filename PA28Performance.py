#!/usr/bin/env python
# coding: utf-8

# # PA 28 Performance Calculator

# In[2]:


################################################################################
# This script takes inputs from the user and calculates TOLD performance for
# PA-28-161 Piper Warrior II.
#
# Written by: Temo Cuna 7/10/2024

############################# INPUTS ###########################################
# [Name]...........[Description].....................[Type].........[Units]
# wing_loading.......W/S aircraft wing loading.........double.........lb/ft^2  

############################## Outputs #########################################
# V-n diagram........KEAS vs load factor................*.fig.........Many
# Va.................Manuever speed.....................double........KEAS
################################################################################

import numpy as np
import plotly.graph_objects as go
import pandas as pd
import plotly.io as pio

def PA28Plot(Weight, OAT_C, Elevation, Altimeter):
    
    pio.renderers.default = 'notebook' #set rendering 

    # Standard atmosphere constants
    Stand_Lapse_Rate = -2 / 1000
    Stand_Temp_C_SL = 15
    Stand_Altimeter = 29.92

    # Calculate density altitude
    Pressure_Alt = ((Stand_Altimeter - Altimeter) * 1000) + Elevation
    Stand_Temp_A_C = (Elevation * Stand_Lapse_Rate) + Stand_Temp_C_SL
    Density_Altitude = ((OAT_C - Stand_Temp_A_C) * 120) + Pressure_Alt



    # Weights and polynomial curves
    Weights = np.array([2325,2300,2250,2200,2150,2100,2050,2000,1950,1900,1850,1800,1750,1700,1650,1600])

    PolyPoints = {

        "One":   [-68,-220,-510,-840,-1120,-1450,-1725,-1985,-2275,-2530,-2785,-3050,-3278,-3490,-3700,-3910],

        "Two":   [1402,1200,800,400,10,-375,-765,-1115,-1450,-1790,-2125,-2415,-2690,-2950,-3225,-3475],

        "Three": [2736,2485,2015,1555,1080,665,225,-200,-585,-950,-1350,-1700,-1995,-2300,-2560,-2810],

        "Four":  [4070,3800,3250,2700,2225,1725,1250,750,350,-100,-550,-925,-1275,-1625,-1935,-2250],

        "Five":  [5404,5100,4500,3950,3350,2750,2200,1700,1200,685,225,-225,-650,-995,-1375,-1700],

        "Six":   [6738,6400,5800,5175,4600,4000,3450,2850,2350,1775,1275,775,300,-150,-600,-995],

        "Seven": [8072,7650,7000,6350,5650,5000,4375,3750,3150,2565,2000,1450,950,410,-50,-450],

        "Eight": [9406,8875,8150,7450,6700,6050,5375,4700,4050,3400,2800,2200,1600,1100,550,100]

    }



    curves_df = pd.DataFrame(PolyPoints)



    # Find bounding curves
    for i in range(curves_df.shape[1] - 1):

        lower = curves_df.iloc[0, i]
        upper = curves_df.iloc[0, i+1]

        if lower < Density_Altitude < upper:
            break

    p1 = np.polyfit(Weights, curves_df.iloc[:, i], 2)
    p2 = np.polyfit(Weights, curves_df.iloc[:, i+1], 2)

    y1 = np.polyval(p1, Weight)
    y2 = np.polyval(p2, Weight)

    # Interpolation ratio
    dist_top = curves_df.iloc[0, i+1] - Density_Altitude
    dist_bot = Density_Altitude - curves_df.iloc[0, i]

    ratio = dist_bot / dist_top
    interpolated_point = ((ratio * y2) + y1) / (1 + ratio)

    # Plotting using Plotly
    fig = go.Figure()

    # Add all curve lines
    for col in curves_df.columns:

        fig.add_trace(go.Scatter(
            x=Weights,
            y=curves_df[col],
            mode='lines',
            line=dict(color='gray'),
            name=col,
            showlegend=False

        ))

    # First add invisible right trace
    fig.add_trace(go.Scatter(
        x=[None],
        y=[None],
        yaxis='y2',
        showlegend=False,
        hoverinfo='skip',
        mode='lines'
    ))

    # Add diagonal curve

    fig.add_trace(go.Scatter(
        x=[2325, Weight],
        y=[Density_Altitude, interpolated_point],
        mode='lines',
        line=dict(dash='dash', width=2, color='red'),
        name='Ground Roll'

    ))

    # Add horizontal curve
    fig.add_trace(go.Scatter(

        x=[Weight, 1400],
        y=[interpolated_point, interpolated_point],
        mode='lines',
        line=dict(dash='dash', width=2, color='red'),
        name='Interpolated Distance',
        showlegend=False

    ))

    fig.update_layout(
    title="PA-28 Ground Roll Performance | 0 deg Flaps",

    xaxis_title="Weight (lb)",
    xaxis=dict(
        autorange='reversed'
    ),

    yaxis2=dict(
        title=dict(
            text="Ground Roll (ft)",
            font=dict(color="gray")
        ),
        range=[0, 2200],
        overlaying="y",
        side="right",
        showgrid=False,
        showticklabels=True,
        tickvals=list(range(0, 2201, 200)),
        tickfont=dict(color="gray")
    ),

    yaxis=dict(
        title=dict(
            text="Density Altitude (ft)"
        ),
        range=[-6602, 8000],
        side="left"
    ),

    height=600
)

    return fig




