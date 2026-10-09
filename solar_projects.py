"""Pakistan solar project/program inventory for IndusSphere Pakistan.

Values are source-derived where an official source provides a capacity.  Program
records without a published aggregate MW value intentionally use None rather than
inventing a capacity. Coordinates are representative visualization points unless
otherwise noted.
"""
import pandas as pd

SOURCE_PPIB = "https://www.ppib.gov.pk/upcomming_ipps.html"
SOURCE_PUNJAB = "https://energy.punjab.gov.pk/projects"
SOURCE_PUNJAB_PUBLIC = "https://energy.punjab.gov.pk/node/169"
SOURCE_SINDH_NEPRA = "https://nepra.org.pk/news.php"
SOURCE_KP = "https://pedokp.gov.pk/wp-content/uploads/2024/04/KP_Power_Sector_Business_Plan.pdf"
SOURCE_BALOCH = "https://energy.balochistan.gov.pk/?p=1581"
SOURCE_BALOCH_PSDP = "https://energy.balochistan.gov.pk/wp-content/uploads/2024/12/ENERGY_PSDP_2024-25.pdf"
SOURCE_GB = "https://pc.gov.pk/web/press/get_press/1742"
SOURCE_AJK = "https://www.app.com.pk/domestic/ajk-dwp-approves-26-projects-worth-rs-7-384-billion/"
SOURCE_ICT = "https://www.cda.gov.pk/public/tenders/providing-installation-of-300-kw-on-grid-solar-panel-system-judicial-academy-sector-h-84-islamabad"
SOURCE_TUBEWELLS = "https://www.pc.gov.pk/uploads/downloads/Schemes%20approved%20by%20CDWP%20%26%20ECNEC%202024.pdf"

ROWS = [
    # Punjab
    ["Quaid-e-Azam Solar Power Plant, Bahawalpur", "Punjab", "Bahawalpur", "Operational", "Utility-scale solar PV", 100.0, 29.3956, 71.6836, SOURCE_PUNJAB, "Punjab Energy Department lists a 100 MW project; QASP has larger phased/park capacity references."],
    ["Quaid-e-Azam Solar Park — Zonergy blocks", "Punjab", "Bahawalpur", "Operational", "Utility-scale solar PV", 300.0, 29.3956, 71.6836, SOURCE_PUNJAB, "Punjab Energy Department lists three 100 MW COD entries."],
    ["Zhenfa Solar Project", "Punjab", "Bahawalpur", "Operational / source-listed", "Utility-scale solar PV", 100.0, 29.3956, 71.6836, SOURCE_PUNJAB, "Listed by Punjab Energy Department."],
    ["Solarization of 24 tertiary hospitals & 6 Daanish schools", "Punjab", "Multiple districts", "Implementation", "Public-sector solar PV", 21.119, 31.5204, 74.3587, SOURCE_PUNJAB_PUBLIC, "Published aggregate solar PV capacity across 24 hospitals and 6 schools."],
    ["Solarization of 15,000 schools and 2,000 BHUs", "Punjab", "Punjab-wide", "Program", "Distributed solar", None, 31.5204, 74.3587, SOURCE_PUNJAB, "Program record; aggregate MW not stated on cited page."],
    ["600 MWp Muzaffargarh Solar PV Project", "Punjab", "Muzaffargarh", "Competitive-bidding / proposed", "Utility-scale solar PV", 600.0, 30.0754, 71.1921, "https://nepra.org.pk/news.php", "NEPRA public-hearing notice for AEDB RFP."],
    # Sindh
    ["Helios Solar", "Sindh", "Sukkur", "Operational / source-listed", "Utility-scale solar PV", 50.0, 27.7244, 68.8228, SOURCE_PPIB, "PPIB/official planning records list Helios at Sukkur."],
    ["Meridian Solar", "Sindh", "Sukkur", "Operational / source-listed", "Utility-scale solar PV", 50.0, 27.7244, 68.8228, SOURCE_PPIB, "PPIB/official planning records list Meridian at Sukkur."],
    ["HNDS Solar", "Sindh", "Sukkur", "Operational / source-listed", "Utility-scale solar PV", 50.0, 27.7244, 68.8228, SOURCE_PPIB, "PPIB/official planning records list HNDS at Sukkur."],
    ["50 MW Manjhand Solar PV Power Plant", "Sindh", "Jamshoro", "Proposed / competitive bidding", "Utility-scale solar PV", 50.0, 25.9260, 67.9029, SOURCE_SINDH_NEPRA, "NEPRA public-hearing notice for Government of Sindh project."],
    ["Siachen Energy Ltd Solar", "Sindh", "Mirpur Sakro, Thatta", "Upcoming", "Utility-scale solar PV", 100.0, 24.5470, 67.7240, SOURCE_PPIB, "PPIB upcoming-project portfolio as of 30 Jun 2026."],
    ["Agriculture Tubewell Solarization Program", "Sindh", "Sindh-wide", "Program", "Agricultural distributed PV", None, 26.0000, 68.0000, SOURCE_TUBEWELLS, "Federal program covers Punjab, Sindh, KP and Balochistan; aggregate target is 100,000 tubewells nationally."],
    # KP
    ["Facilitation to Solar IPPs", "Khyber Pakhtunkhwa", "KP-wide", "Ongoing pipeline", "Private solar IPPs", 249.5, 34.0151, 71.5249, SOURCE_KP, "PEDO business plan portfolio total."],
    ["Electrification of Villages — solar", "Khyber Pakhtunkhwa", "KP-wide", "Completed / portfolio", "Distributed solar", 2.0, 34.0151, 71.5249, SOURCE_KP, "PEDO portfolio total."],
    ["Installation of Mini Grids", "Khyber Pakhtunkhwa", "KP-wide", "Ongoing", "Solar mini-grids", 1.3, 34.0151, 71.5249, SOURCE_KP, "PEDO portfolio total."],
    ["Solarization of Schools & Primary Health Facilities", "Khyber Pakhtunkhwa", "KP-wide", "Ongoing", "Public-sector solar PV", 12.0, 34.0151, 71.5249, SOURCE_KP, "PEDO portfolio total."],
    ["Solarization of 4,000 Masajid", "Khyber Pakhtunkhwa", "KP-wide", "Ongoing", "Distributed solar", 7.08, 34.0151, 71.5249, SOURCE_KP, "PEDO portfolio total."],
    ["Agriculture Tubewell Solarization Program", "Khyber Pakhtunkhwa", "KP-wide", "Program", "Agricultural distributed PV", None, 34.0151, 71.5249, SOURCE_TUBEWELLS, "Federal program covers KP."],
    # Balochistan
    ["LIEDA Solarization Project", "Balochistan", "Hub", "Planned / PSDP 2025-26", "Industrial-estate solarization", 50.0, 25.0280, 66.8808, SOURCE_BALOCH, "Balochistan Energy Department lists 50 MW."],
    ["QITE Solarization Project", "Balochistan", "Quetta", "Planned / PSDP 2025-26", "Industrial-estate solarization", 20.0, 30.1798, 66.9750, SOURCE_BALOCH, "Balochistan Energy Department lists 20 MW."],
    ["GIEDA Solarization Project", "Balochistan", "Gwadar", "Planned / PSDP 2025-26", "Industrial-estate solarization", 10.0, 25.1264, 62.3225, SOURCE_BALOCH, "Balochistan Energy Department lists 10 MW."],
    ["Bostan SEZ Solarization Project", "Balochistan", "Bostan", "Planned / PSDP 2025-26", "Industrial-estate solarization", 5.0, 30.1667, 67.0167, SOURCE_BALOCH, "Balochistan Energy Department lists 5 MW."],
    ["Chaghi Mining Area Solarization Project", "Balochistan", "Chaghi", "Planned / PSDP 2025-26", "Mining-area solarization", 50.0, 29.3000, 64.4167, SOURCE_BALOCH, "Balochistan Energy Department lists 50 MW."],
    ["Roshan Balochistan — Solarization Phase I", "Balochistan", "Province-wide", "Ongoing", "Off-grid solar", None, 30.1798, 66.9750, SOURCE_BALOCH_PSDP, "PSDP project; cited source does not state aggregate MW."],
    ["15,000 Solar Home Systems", "Balochistan", "Province-wide", "Program / implementation", "Solar home systems", None, 30.1798, 66.9750, "https://energy.balochistan.gov.pk/?p=1047", "Energy Department reports 15,000 home solar systems under a grant-in-aid program."],
    ["Agriculture Tubewell Solarization Program", "Balochistan", "Province-wide", "Program", "Agricultural distributed PV", None, 30.1798, 66.9750, SOURCE_TUBEWELLS, "Federal program covers Balochistan."],
    # GB
    ["100 MW Distributed Solar PV Plants at Various Sites", "Gilgit-Baltistan", "Multiple districts", "Under development / priority", "Distributed + utility-scale solar PV", 100.0, 35.9200, 74.3080, SOURCE_GB, "Official Planning Commission update: rooftop and utility-scale components."],
    # AJK
    ["Solar Energy Systems for 64 Basic Health Units", "Azad Jammu & Kashmir", "Multiple districts", "Approved / implementation", "Public-health solar PV", None, 34.3700, 73.4700, SOURCE_AJK, "AJK DWP approved installation for 64 BHUs; aggregate MW not stated in cited source."],
    # ICT
    ["Judicial Academy H-8/4 300 kW Solar System", "Islamabad Capital Territory", "Islamabad", "Procurement / tender", "Institutional on-grid solar PV", 0.3, 33.6938, 73.0652, SOURCE_ICT, "CDA tender for a 300 kW on-grid solar panel system."],
    ["CDA Buildings & Street Lights Solarization", "Islamabad Capital Territory", "Islamabad", "Feasibility / proposed", "Public infrastructure solarization", None, 33.6844, 73.0479, "https://www.cda.gov.pk/storage/app/public/public_notices/KEh7eW0dYYa2C85xL8AMLmbB3RREtqoil7lJB5J1.pdf", "CDA board directed a feasibility study for PV installations."],
]

COLUMNS = ["project","province_region","district_area","status","solar_type","capacity_mw","latitude","longitude","source_url","source_note"]
PROJECTS_DF = pd.DataFrame(ROWS, columns=COLUMNS)

PROVINCE_ORDER = ["Punjab","Sindh","Khyber Pakhtunkhwa","Balochistan","Gilgit-Baltistan","Azad Jammu & Kashmir","Islamabad Capital Territory"]


def known_capacity_by_region(df=None):
    x = PROJECTS_DF if df is None else df
    return x.dropna(subset=["capacity_mw"]).groupby("province_region", as_index=False)["capacity_mw"].sum().sort_values("capacity_mw", ascending=False)


def source_urls():
    return sorted(PROJECTS_DF["source_url"].dropna().unique().tolist())
