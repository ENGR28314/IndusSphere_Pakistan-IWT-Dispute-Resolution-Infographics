import pandas as pd

DESERTS = pd.DataFrame([
    ["Thar Desert","Sindh; Punjab","Tharparkar, Umerkot and adjoining districts","Arid to semi-arid","Dunes, sandy plains, scrub and seasonal wetlands","Desert ecology, pastoralism and cultural tourism"],
    ["Cholistan Desert","Punjab","Bahawalpur, Bahawalnagar, Rahim Yar Khan","Arid","Sand dunes, desert plains and seasonal water bodies","Fort Derawar, desert tourism, livestock"],
    ["Thal Desert","Punjab","Mianwali, Bhakkar, Khushab, Layyah, Muzaffargarh","Semi-arid","Sand sheets and dunes between Indus and Jhelum/Chenab systems","Dryland agriculture, pastoralism and local tourism"],
    ["Kharan Desert","Balochistan","Kharan and surrounding Balochistan","Arid","Gravel/sand desert plains and mountain margins","Desert landscape and dryland ecology"],
    ["Katpana Cold Desert","Gilgit-Baltistan","Skardu","Cold/arid highland","High-altitude sand dunes and cold-desert terrain","Landscape tourism and high-altitude recreation"],
    ["Sarfaranga Cold Desert","Gilgit-Baltistan","Shigar/Skardu region","Cold/arid highland","High-altitude dunes and mountain desert","Tourism and adventure landscape"],
], columns=["name","region","location","climate","landscape","tourism_or_livelihood"])
