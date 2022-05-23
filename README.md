# Animated KPI Dashboard for Surfers

Esteban Zuniga <br>
May 23, 2022 <br>
Analytics Engineer 

# Abstract

This dashboard provides insights on wether conditions are favorable for surfing on Mavericks Beach by way of building a dashboard with [Dash Plotly](https://plotly.com/dash/), an awesome framework that is built on top of flask that interacts with react.js and html/css for design.

### But what makes conditions favorable? 

**Ideal formation**

There are three main factors that affect the size of a wave in open sea.

- Wind Speed - The greater the wind speed the greater the wave.
- Wind Duration - The longer the wind blows the larger the wave.
- Fetch - The greater the area the wind affects the larger the wave.

**Surf Geography**

- Swell Exposure - The breaks need to have expsoure to the swell from offsure.
- Sea Floor - The sea floor has an effect on the size and type of waves that form.

**Assumptions**

*Geography*

This project assumes that Mavericks beach has favorable geography for waves.

*Offsure Factors*

 - If it is windy, rainy, and the barometric pressure is low offsure it will produce nice swells for surfers. 
 - If winds are strong 48 to 24 hours ago it will produce nice waves currently.

### Dashboard Purpose

The dashboard's main purpose is to track these conditions so that the user can make an educated decision to load up and head to the beach.

# Data
I collected data for this dashboard by making [Open Weather](https://openweathermap.org/api) and [Open Evlevation](https://open-elevation.com/) API calls from several different end points to gather information about weather events in the San Francisco area. 

I am currently pulling historic weather, current weather by the minute, and the forecast for the next 48 hours and pushing the data to a SQLite3 db.

The data is then queried from the database filtering the features mentioned above, 
then used as inputs for the graphs.

# Design

![main](/images/design.png) 

# Demo
Please press play and feel free to download it.

[![Video Download](/images/dash-recording.mov)](https://user-images.githubusercontent.com/60893597/169880535-5a1b2c36-4dec-4701-b8b1-e10bc1544803.mov)

