"""WAPDA telecommunication network data extracted from user-supplied PDFs.

The source documents are diagrammatic and do not provide geographic coordinates
or explicit edge/topology definitions. Therefore this module preserves the
listed network locations as source-derived inventory and does not infer links.
"""

WESTERN_RIVERS = [
    "Mangla Dam", "Tarbela Dam", "Besham", "Jaglot", "Skardu", "Daggar",
    "Phulra", "Oghi", "Shinkiari", "Khairabad", "Nowshera", "Kallar",
    "G. Habibullah", "Muzaffarabad", "Domel", "Kotli", "Kohala",
    "Plandri", "Azadpatan", "Chashma Barrage",
    "Water Resource Management Directorate", "Central Flood Forecasting Division",
]

EASTERN_RIVERS = [
    "Kot Naina", "Jassar", "Ravi Syphon", "Shahdara", "Balloki", "Sidhnai",
    "Bein Nullah at Chak Amru", "Bein Nullah at Shakargarh", "Deg Nullah at Q.S. Singh",
    "Bassantar Nullah", "G.S. Wala", "Bakarke", "Sulemanki", "Islam", "Melsi Syphon",
    "Marala", "Khanki", "Qadirabad", "Chinot Bridge", "Trimmu", "Rawaz Bridge",
    "Punjnad", "Aik Nullah at Ura", "Palku Nullah", "New Rasul", "Khushab Bridge",
    "Kalabagh", "Taunsa", "Mithankot", "Ghazighat", "Chachran Sharif",
]

SOURCE_DOCUMENTS = [
    "HF Radio maintained by WAPDA.pdf",
    "Meteor burst Telecommunication System of WAPDA.pdf",
]

SOURCE_NOTE = (
    "Source-derived inventory from the two user-supplied WAPDA PDFs. "
    "Both PDFs contain the same three-page diagram set: a title page, a High Frequency "
    "Radio Network – Western Rivers diagram, and a Wireless Network – Eastern Rivers diagram."
)

# Visualization-only approximate coordinates. These are NOT extracted from the PDFs.
# They are deliberately separated from source-derived network inventory.
APPROX_COORDS = {
    "Tarbela Dam": (34.0837, 72.8143), "Mangla Dam": (33.1482, 73.6472),
    "Besham": (34.9280, 72.8556), "Jaglot": (35.9180, 74.3110),
    "Skardu": (35.2971, 75.6333), "Daggar": (34.5110, 72.4850),
    "Phulra": (34.2900, 73.3500), "Oghi": (34.5030, 73.9040),
    "Shinkiari": (34.4600, 73.2600), "Khairabad": (33.9600, 72.2400),
    "Nowshera": (34.0159, 72.0052), "Kallar": (32.9820, 73.0300),
    "G. Habibullah": (34.3860, 73.3790), "Muzaffarabad": (34.3700, 73.4711),
    "Domel": (34.3730, 73.4730), "Kotli": (33.5184, 73.9012),
    "Kohala": (34.0470, 73.5020), "Plandri": (33.7150, 73.6860),
    "Azadpatan": (33.8220, 73.6000), "Chashma Barrage": (32.4320, 71.3830),
    "Shahdara": (31.6200, 74.2870), "Balloki": (31.1770, 73.8270),
    "Sidhnai": (30.6900, 72.4600), "Marala": (32.6760, 74.4680),
    "Khanki": (32.4500, 74.1250), "Qadirabad": (32.0850, 73.6800),
    "Chinot Bridge": (31.7200, 72.9780), "Trimmu": (31.2750, 72.2100),
    "Punjnad": (29.3480, 71.0270), "New Rasul": (32.7050, 73.6560),
    "Khushab Bridge": (32.2950, 72.3500), "Kalabagh": (32.9620, 71.5460),
    "Taunsa": (30.7050, 70.6500), "Mithankot": (28.9200, 70.3400),
    "Ghazighat": (30.0500, 71.1500), "Chachran Sharif": (28.7000, 70.3400),
}
