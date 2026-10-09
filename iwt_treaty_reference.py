"""Reference pages for the Indus Waters Treaty (IWT), with neutral legal framing."""
from pathlib import Path
import streamlit as st

ASSET = Path(__file__).parent / "assets" / "iwt_article_xii3_infographic.png"
DISPUTE_ASSET = Path(__file__).parent / "assets" / "iwt_treaty_dispute_resolution.png"

PAGES = {
    "1960 Dam Design": {
        "subtitle": "How the Treaty frames storage and hydropower design on the Western Rivers",
        "points": [
            ("Design is treaty-specific", "Hydroelectric projects on the Western Rivers are governed by the Treaty and the relevant annexures, including Annexure D for generation of hydro-electric power and Annexure E for storage works."),
            ("Run-of-river is not a blanket exemption", "The permitted design and operation must be assessed against the applicable treaty criteria. A project label alone does not establish compliance or non-compliance."),
            ("Review the evidence", "Relevant evidence can include approved design documents, pondage and storage calculations, freeboard, spillway and outlet arrangements, operating rules, river-flow data, and the applicable treaty provisions."),
            ("Dashboard limitation", "This page is a screening guide, not an engineering certification. Project-specific findings require primary technical documents and the applicable legal record."),
        ],
        "source_note": "Treaty text and annexures should be consulted for the project and issue being assessed."
    },
    "Western Rivers Pakistan": {
        "subtitle": "Indus, Jhelum and Chenab — the Western Rivers under the IWT",
        "points": [
            ("Treaty definition", "The Treaty defines the Western Rivers as the Indus, Jhelum and Chenab taken together."),
            ("Pakistan's use", "Article III(1) provides for Pakistan's unrestricted use of waters India is obliged to let flow under the Treaty. Article III(2) sets out India's obligation to let flow the waters of the Western Rivers, subject to the specified treaty-permitted uses."),
            ("Permitted uses", "The Treaty permits specified Indian uses including domestic, non-consumptive and limited agricultural uses, and hydro-electric generation subject to applicable provisions. Storage works are addressed by the Treaty and Annexure E."),
            ("Practical relevance", "Flow, timing, reservoir operation, irrigation supply, hydropower and ecosystem conditions should be assessed with verified gauge data and project-specific evidence."),
        ],
        "source_note": "The wording above summarizes the Treaty; it is not a substitute for the complete text and annexures."
    },
    "IWT Main points": {
        "subtitle": "Core institutions, allocations, data exchange and dispute-resolution structure",
        "points": [
            ("Signed in 1960", "The Indus Waters Treaty was signed at Karachi on 19 September 1960 and entered into force on 12 January 1961, with retrospective effect from 1 April 1960."),
            ("River allocation framework", "The Treaty distinguishes the Eastern Rivers (Ravi, Beas and Sutlej) from the Western Rivers (Indus, Jhelum and Chenab) and defines rights and permitted uses for each group."),
            ("Permanent Indus Commission", "The two national Commissioners provide a regular channel for communication and treaty implementation, including data exchange and discussion of questions arising under the Treaty."),
            ("Dispute-resolution pathways", "The Treaty provides structured processes for questions and disputes, including the Commission, a Neutral Expert for specified technical differences, and a Court of Arbitration for disputes within its jurisdiction."),
            ("Use primary records", "For legal or operational conclusions, cite the Treaty text, relevant annexure, official correspondence, technical submissions, and published procedural orders or awards."),
        ],
        "source_note": "Dates and framework are based on the treaty record maintained by the UN Treaty Series and official treaty text."
    },
    "Impact on Transboundary Water Cooperation": {
        "subtitle": "How treaty institutions and shared evidence can support basin cooperation",
        "points": [
            ("Predictability", "Defined rights, obligations and procedures can reduce uncertainty for irrigation planning, hydropower operations and water management."),
            ("Shared information", "Consistent gauge readings, discharge measurements, reservoir releases, project data and timely technical exchanges help parties evaluate flow questions on a common evidentiary basis."),
            ("Institutional channels", "Regular communication through the Permanent Indus Commission can preserve technical dialogue even when political relations are difficult."),
            ("Dispute management", "Treaty-based procedures create routes for addressing technical differences and legal disputes without treating every disagreement as proof of a breach."),
            ("Climate and operational pressures", "More variable monsoons, glacier change, floods, droughts and growing demand increase the value of transparent data, contingency planning and sustained cooperation."),
        ],
        "source_note": "These are general cooperation implications, not a finding about the conduct of either state in a specific dispute."
    },
    "The IWT Treaty": {
        "subtitle": "The Indus Waters Treaty 1960 — structure and continuing legal framework",
        "points": [
            ("Instrument", "The Treaty was concluded by India and Pakistan with specified roles for the International Bank for Reconstruction and Development in particular treaty mechanisms."),
            ("Treaty components", "The instrument includes its preamble, Articles I–XII and Annexures A–H. The annexures provide detailed rules for specific matters, including hydropower, storage and dispute settlement."),
            ("Article XII", "Article XII covers final provisions. Paragraph (2) addresses ratification and entry into force; paragraph (3) provides for modification by a duly ratified treaty concluded for that purpose between the two governments; paragraph (4) addresses continuation and termination."),
            ("Interpretation matters", "A summary or infographic cannot resolve contested questions of interpretation, jurisdiction, compliance or treaty status. Those questions should be attributed to the relevant party or adjudicative record."),
        ],
        "source_note": "The complete authentic treaty text should be used for legal interpretation."
    },
    "Article XII(3) Modification by Consent": {
        "subtitle": "Modification through a duly ratified treaty concluded between both governments",
        "points": [
            ("Text of the rule", "Article XII(3) states that the Treaty provisions may from time to time be modified by a duly ratified treaty concluded for that purpose between the two governments."),
            ("What the text specifies", "The paragraph describes a treaty-based modification route requiring a duly ratified treaty between the governments. The dashboard should quote this requirement accurately and distinguish it from either government's position on current events."),
            ("Related continuation clause", "Article XII(4) says the Treaty, or the Treaty as modified under paragraph (3), continues in force until terminated by a duly ratified treaty concluded for that purpose between the two governments."),
            ("Attributed positions", "Pakistan has argued that the Treaty remains binding and that modification or termination must follow the Treaty text. India has announced that it is holding the Treaty in abeyance and has advanced its own stated rationale. These are attributed positions; this dashboard does not adjudicate the legal dispute."),
            ("Evidence standard", "When recording developments, retain the date, issuing authority, exact document, and whether a statement is a party position, a procedural order, an award, or an independent legal analysis."),
        ],
        "source_note": "Official Treaty text: United Nations Treaty Series, No. 6032. See the source links below."
    },
}

SOURCES = [
    ("United Nations Treaty Series — Indus Waters Treaty 1960 (No. 6032)", "https://treaties.un.org/Pages/showDetails.aspx?clang=_en&objid=0800000280135336"),
    ("Full Treaty text — UN Treaty Series, Volume 419", "https://treaties.un.org/doc/Publication/UNTS/Volume%20419/v419.pdf"),
    ("Government of India, Ministry of External Affairs — Indus Waters Treaty", "https://www.mea.gov.in/bilateral-documents.htm?dtl%2F6439%2FIndus="),
    ("Pakistan Ministry of Water Resources — Pakistan Commissioner for Indus Waters", "https://mowr.gov.pk/Detail/MDQ1NDQ1YTQtMzQ1MC00YTU5LTljMWEtMzliZTVhM2QxMjhl"),
]

def render(title: str) -> None:
    page = PAGES.get(title)
    if not page:
        st.error(f"Unknown IWT reference page: {title}")
        return
    st.title(title)
    st.caption(page["subtitle"])
    if title == "The IWT Treaty" and DISPUTE_ASSET.exists():
        st.subheader("Three-tier dispute-resolution mechanism")
        st.image(str(DISPUTE_ASSET), use_container_width=True, caption="User-provided infographic. It is a visual overview; verify procedural details and project-specific references against the Treaty text and official records.")
    if title == "Article XII(3) Modification by Consent" and ASSET.exists():
        st.image(str(ASSET), use_container_width=True, caption="User-provided infographic. Read alongside the official Treaty text; it is illustrative, not an adjudication.")
    for heading, body in page["points"]:
        st.subheader(heading)
        st.write(body)
    st.info(page["source_note"])
    st.markdown("### Primary references")
    for label, url in SOURCES:
        st.markdown(f"- [{label}]({url})")
