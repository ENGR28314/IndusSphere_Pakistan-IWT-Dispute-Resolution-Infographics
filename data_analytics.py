"""Generic data ingestion and charting helpers for IndusSphere Pakistan."""
from __future__ import annotations

import io
import re
from typing import Any

import pandas as pd


def _clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [re.sub(r"\s+", " ", str(c)).strip() or f"column_{i+1}" for i, c in enumerate(df.columns)]
    for c in df.columns:
        if df[c].dtype == "object":
            df[c] = df[c].map(lambda x: x.strip() if isinstance(x, str) else x)
    return df.dropna(axis=1, how="all").dropna(axis=0, how="all")


def read_csv_bytes(raw: bytes) -> pd.DataFrame:
    attempts = [
        {"encoding": "utf-8"},
        {"encoding": "utf-8-sig"},
        {"encoding": "cp1252"},
        {"encoding": "latin1"},
    ]
    last = None
    for kw in attempts:
        try:
            return _clean_columns(pd.read_csv(io.BytesIO(raw), **kw))
        except Exception as exc:
            last = exc
    raise ValueError(f"Could not read CSV: {last}")


def _table_to_df(table: list[list[Any]]) -> pd.DataFrame | None:
    rows = [[str(x).strip() if x is not None else "" for x in row] for row in table if row]
    rows = [r for r in rows if any(v for v in r)]
    if len(rows) < 2:
        return None
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    header = rows[0]
    # Make duplicate/blank headers safe.
    seen: dict[str, int] = {}
    clean_header = []
    for i, h in enumerate(header):
        base = h or f"column_{i+1}"
        seen[base] = seen.get(base, 0) + 1
        clean_header.append(base if seen[base] == 1 else f"{base}_{seen[base]}")
    return _clean_columns(pd.DataFrame(rows[1:], columns=clean_header))


def _parse_extracted_text(text: str) -> pd.DataFrame:
    rows = []
    for line in text.splitlines():
        line = re.sub(r"\s+", " ", line).strip()
        if not line:
            continue
        if "\t" in line:
            parts = [p.strip() for p in line.split("\t")]
        elif "|" in line:
            parts = [p.strip() for p in line.split("|") if p.strip()]
        else:
            parts = [p.strip() for p in re.split(r"\s{2,}", line) if p.strip()]
            if len(parts) == 1 and ":" in line:
                parts = [p.strip() for p in line.split(":", 1)]
        if len(parts) >= 2:
            rows.append(parts)
    if len(rows) < 2:
        return pd.DataFrame()
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    return _clean_columns(pd.DataFrame(rows))


def _ocr_pdf(raw: bytes) -> str:
    """OCR image/scanned PDF pages when PyMuPDF + Tesseract are available."""
    import fitz
    import pytesseract
    from PIL import Image

    pages = []
    doc = fitz.open(stream=raw, filetype="pdf")
    try:
        for page in doc:
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            pages.append(pytesseract.image_to_string(img))
    finally:
        doc.close()
    return "\n".join(pages).strip()


def read_pdf_bytes(raw: bytes) -> tuple[pd.DataFrame, str, list[str]]:
    """Extract tables/text and fall back to OCR for scanned/image-only PDFs."""
    tables: list[pd.DataFrame] = []
    pages_text: list[str] = []
    warnings: list[str] = []

    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(raw)) as pdf:
            for page_no, page in enumerate(pdf.pages, start=1):
                text = page.extract_text() or ""
                pages_text.append(text)
                try:
                    for table in page.extract_tables() or []:
                        df = _table_to_df(table)
                        if df is not None and len(df) >= 1:
                            df.insert(0, "source_page", page_no)
                            tables.append(df)
                except Exception as exc:
                    warnings.append(f"Page {page_no}: table extraction skipped ({exc}).")
    except Exception as exc:
        raise ValueError(f"Could not open PDF: {exc}")

    if tables:
        combined = pd.concat(tables, ignore_index=True, sort=False)
        return _clean_columns(combined), "table", warnings

    text = "\n".join(pages_text).strip()
    if not text:
        warnings.append("No selectable text or tables were found. This may be a scanned/image-only PDF; OCR is required.")
        return pd.DataFrame(), "empty", warnings

    # Try common delimited text embedded in PDF extraction.
    df = _parse_extracted_text(text)
    if not df.empty:
        warnings.append("PDF contained text rather than a reliably structured table; columns were inferred from extracted text.")
        return df, "text", warnings

    # Scanned/image-only PDF fallback.
    try:
        ocr_text = _ocr_pdf(raw)
        if ocr_text:
            ocr_df = _parse_extracted_text(ocr_text)
            if not ocr_df.empty:
                warnings.append("OCR was used because the PDF did not contain a reliable selectable-text table. Review extracted columns before analysis.")
                return ocr_df, "ocr", warnings
            warnings.append("OCR extracted text, but no reliable tabular structure could be inferred.")
            return pd.DataFrame({"text": ocr_text.splitlines()}), "ocr_text", warnings
    except Exception as exc:
        warnings.append(f"OCR fallback unavailable or failed: {exc}. Install/enable Tesseract OCR for scanned PDFs.")

    # Keep the text available for downstream inspection.
    return pd.DataFrame({"text": text.splitlines()}), "text", warnings


def load_uploaded_file(uploaded_file) -> tuple[pd.DataFrame, dict[str, Any]]:
    name = uploaded_file.name.lower()
    raw = uploaded_file.getvalue()
    if name.endswith(".csv"):
        return read_csv_bytes(raw), {"type": "csv", "filename": uploaded_file.name}
    if name.endswith(".pdf"):
        df, extraction, warnings = read_pdf_bytes(raw)
        return df, {"type": "pdf", "filename": uploaded_file.name, "extraction": extraction, "warnings": warnings}
    if name.endswith((".xlsx", ".xls")):
        return _clean_columns(pd.read_excel(io.BytesIO(raw))), {"type": "excel", "filename": uploaded_file.name}
    raise ValueError("Supported formats are CSV, PDF, XLSX and XLS.")


def coerce_numeric(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for c in out.columns:
        if out[c].dtype == "object":
            converted = pd.to_numeric(out[c].astype(str).str.replace(",", "", regex=False).str.replace("%", "", regex=False), errors="coerce")
            if converted.notna().mean() >= 0.70:
                out[c] = converted
    return out


def numeric_columns(df: pd.DataFrame) -> list[str]:
    work = coerce_numeric(df)
    return [c for c in work.columns if pd.api.types.is_numeric_dtype(work[c]) and work[c].notna().any()]


def categorical_columns(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if not pd.api.types.is_numeric_dtype(coerce_numeric(df[[c]])[c])]


def chart_candidates(df: pd.DataFrame) -> dict[str, list[str]]:
    work = coerce_numeric(df)
    nums = [c for c in work.columns if pd.api.types.is_numeric_dtype(work[c])]
    cats = [c for c in work.columns if c not in nums]
    return {"numeric": nums, "categorical": cats}
