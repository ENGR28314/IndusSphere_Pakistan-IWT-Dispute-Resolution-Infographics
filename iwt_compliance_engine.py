"""Evidence-driven screening helpers for IWT data-exchange questions.
Not a legal opinion and does not determine treaty breach."""
from dataclasses import dataclass, asdict

@dataclass
class ExchangeRecord:
    date: str
    river: str
    dataset: str
    frequency: str
    channel: str
    prior_notice: str = "Unknown"
    source: str = "User-provided record"
    notes: str = ""

ARTICLE_BASELINE = {
    "Article VI": "Provides for exchange of specified hydrological/agricultural data and information, including regular reporting arrangements.",
    "Article VIII": "Establishes the Permanent Indus Commission and Commissioners as the institutional channel for treaty implementation and information exchange.",
    "Article IX": "Provides the treaty's graded mechanism for differences and disputes, including Neutral Expert and Court of Arbitration pathways.",
}

CHANNELS = ["PIC / Commissioners", "Diplomatic channel", "Other / unspecified"]
FREQUENCIES = ["Daily", "Monthly", "More frequently on request", "Ad hoc", "Unknown"]

def classify_record(record: ExchangeRecord):
    """Return a descriptive screening matrix; never labels an event a treaty violation."""
    channel_ok = record.channel == "PIC / Commissioners"
    freq_defined = record.frequency in {"Daily", "Monthly", "More frequently on request"}
    return {
        **asdict(record),
        "channel_against_iwt_baseline": "PIC channel" if channel_ok else "Outside PIC channel / requires legal review",
        "frequency_against_baseline": "Defined treaty reporting pattern" if freq_defined else "Ad hoc or unspecified; requires document review",
        "legal_status": "Requires treaty-text and evidence assessment",
    }

def compliance_matrix(records):
    return [classify_record(r) for r in records]

def gap_score(record: ExchangeRecord):
    """Simple documentation-gap score, not a legal compliance score."""
    score = 0
    if record.channel != "PIC / Commissioners": score += 1
    if record.frequency in {"Ad hoc", "Unknown"}: score += 1
    if record.prior_notice == "No": score += 1
    return score
