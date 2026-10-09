# SEBAL chart error fix

The Streamlit traceback shown in the deployed app points to a `st.bar_chart(...)`
call after the SEBAL results table. That call relied on Streamlit's automatic
column inference. SEBAL summary tables contain mixed text and numeric columns,
which can cause chart rendering/type errors depending on the dataframe returned.

This build replaces that fragile inference with `_safe_sebal_bar_chart()`, which:
- explicitly locates the ET24 field;
- converts it to numeric;
- removes NaN/Inf values;
- explicitly selects a zone/label column;
- renders the result with Plotly using exactly one categorical and one numeric field;
- shows a warning instead of crashing if no usable ET24 field exists.

The SEBAL calculation itself is not silently changed by this fix.
