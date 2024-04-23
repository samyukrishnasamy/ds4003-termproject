# ds4003-termproject
Samyu Krishnasamy DS4003 Term Project

Render Website: https://dashboard.render.com/web/srv-co72js7109ks738169h0/deploys/dep-co7dkbmd3nmc73e8utjg](https://ds4003-termproject.onrender.com

Original Data URL: https://github.com/rfordatascience/tidytuesday/tree/master/data/2019/2019-10-29

Description of Data: The NYC Squirrel Census data is a unique dataset that provides insights into squirrel populations in Central Park, New York City. The dataset contains squirrel data for 2822 sightings and includes information such as location, latitude and longitudinal coordinates, age, fur color, acitivities, and, interactions between squirrels and humans.

Data Provenance: The data was collected as part of the 2018 Central Park Squirrel Census by a team of volunteers and the Squirrel Census organization. This dataset was published on NYC Open Data. Their purpose was to count and document the squirrel population in Central Park, gather data on their activities and behaviors, and engage the public in both science and nature. The data collection involved visual surveys and standardized data recording practices to ensure consistency and reliability.

Why I chose this data and data provenance: I chose the NYC Squirrel Census data due to its unique combination of wildlife data and urban environment. It's fascinating to explore how squirrels thrive in Central Park, one of the most iconic parks in the world, situated in the midst of the urban landscape of New York City. This dataset provides a platform to understand the behaviors, seasonal patterns, and interactions of one of the most iconic creatures in New York City. I chose to delete certain variables such as 'color_notes', 'above_ground_sighter_measurement', 'zip_codes', 'lat_long', 'specific_location', 'highlight_fur_color', 'combination_of_primary_and_highlight_color', 'other_activities', 'other_interactions', and 'hectare_squirrel_number'. I will not be using these variables because they either contain too many missing observations or they are similar to other variables. I also deleted observations that had N/A for the columns I did use because I was not using those in my graphs as a part of my observations. I sorted the hectares column for my dropdown in the map, as well as changed the date to be datetime type for my line graph.
