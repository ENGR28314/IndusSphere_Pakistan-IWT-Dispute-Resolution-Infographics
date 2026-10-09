def scenario_summary(exposure,vulnerability,sensitivity,adaptive,scenario):
    factors={"Baseline":1.00,"Medium":1.20,"Worst-Case":1.45}
    # This is an index for educational scenario comparison, not a hydraulic calculation.
    raw=(0.30*exposure+0.30*vulnerability+0.20*sensitivity+0.20*(100-adaptive))*factors[scenario]
    risk=round(min(100,raw),1)
    label="Low" if risk<40 else "Moderate" if risk<70 else "High"
    return {
        "risk_index":risk,"risk_class":label,"scenario_factor":factors[scenario],
        "components":{"Exposure":exposure,"Vulnerability":vulnerability,
                      "Sensitivity":sensitivity,"Adaptive-capacity inverse":100-adaptive},
        "explanation":"The index increases with exposure, vulnerability and sensitivity and decreases with adaptive capacity. "
                      "Scenario factors are illustrative and should not be interpreted as a calibrated probability or hydraulic model."
    }
