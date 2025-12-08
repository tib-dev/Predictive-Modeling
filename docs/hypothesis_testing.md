# A/B Hypothesis Testing Pipeline — Results Summary

## 🔧 Pipeline Overview
1. **Select KPIs**
   - ClaimFrequency  
   - ClaimSeverity  
   - Margin  

2. **Create Groups (A/B Segmentation)**
   - Group A: Baseline category  
   - Group B: Comparison category  
   - Ensured confounder balance before testing.

3. **Check Confounder Balance**
   - Confounders tested: `CapitalOutstanding`, `VehicleType`, `Province`, `Gender`
   - Used:
     - t-tests for numeric confounders  
     - chi-square tests for categorical confounders  

4. **Run Statistical Tests**
   - Chi-square → categorical KPIs or categorical splits  
   - ANOVA → margin differences across many groups  
   - t-test (when applicable)

5. **Interpret p-values**
   - p < 0.05 → **Reject H₀**  
   - p ≥ 0.05 → **Fail to reject H₀**

---

# 📊 Final Hypothesis Test Results

## **1. Province**
| KPI            | p-value | Decision            | Interpretation |
|----------------|---------|---------------------|----------------|
| ClaimFrequency | 0.0000  | **Reject H₀**       | Risk differs across provinces |
| ClaimSeverity  | 0.0000  | **Reject H₀**       | Severity varies by province |
| Margin         | 0.0011  | **Reject H₀**       | Profitability differs by province |

**Takeaway:** Provinces show strong and consistent differences across all metrics. Regional pricing adjustments may be justified.

---

## **2. PostalCode**
| KPI            | p-value | Decision            | Interpretation |
|----------------|---------|---------------------|----------------|
| ClaimFrequency | 0.0000  | **Reject H₀**       | Risk varies by zip code |
| ClaimSeverity  | NaN     | **No test result**  | Some areas have no claims |
| Margin         | 0.9977  | **Fail to reject H₀** | Margin is similar across zip codes |

**Takeaway:** Zip code is a frequency driver but not a profitability driver.

---

## **3. Gender**
| KPI            | p-value | Decision            | Interpretation |
|----------------|---------|---------------------|----------------|
| ClaimFrequency | 0.0266  | **Reject H₀**       | Filing probability differs |
| ClaimSeverity  | 0.0899  | **Fail to reject H₀** | Claim size is similar |
| Margin         | 0.7323  | **Fail to reject H₀** | Profitability is similar |

**Takeaway:** Gender influences claim likelihood but not severity or margin.

---

# ✅ Overall Insights
- **Province** is the strongest and most consistent driver of risk and profitability.  
- **PostalCode** affects claim frequency but not claim size or margins.  
- **Gender** only affects claim frequency slightly.  
- **Margin is stable** across Gender and PostalCode, but **not** across Province.  

These results support **targeted pricing strategies**, **risk segmentation**, and **geographical underwriting adjustments**.
