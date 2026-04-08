"""
Clinical Trial Patient Matching — Synthetic Data.

Contains realistic patient records, clinical trial protocols, and ground truth
eligibility matrices for 3 difficulty tiers (easy, medium, hard).

All data is synthetic but medically plausible, designed to test an agent's
ability to reason about inclusion/exclusion criteria.
"""

from typing import Any

# =============================================================================
# PATIENT RECORDS
# =============================================================================

PATIENTS: dict[str, dict[str, Any]] = {
    # ---- Easy + Medium + Hard patients ----
    "P001": {
        "name": "Maria Santos",
        "age": 58,
        "sex": "Female",
        "weight_kg": 72.0,
        "height_cm": 162,
        "ethnicity": "Hispanic",
        "conditions": ["Type 2 Diabetes Mellitus", "Hypertension", "Hyperlipidemia"],
        "conditions_onset": {
            "Type 2 Diabetes Mellitus": "2019-03-15",
            "Hypertension": "2017-08-22",
            "Hyperlipidemia": "2020-01-10",
        },
        "medications": [
            {"name": "Metformin", "dose": "1000mg", "frequency": "twice daily"},
            {"name": "Lisinopril", "dose": "20mg", "frequency": "once daily"},
            {"name": "Atorvastatin", "dose": "40mg", "frequency": "once daily"},
        ],
        "lab_results": {
            "HbA1c": {"value": 8.2, "unit": "%", "date": "2026-03-01", "ref_range": "4.0-5.6"},
            "Fasting_Glucose": {"value": 185, "unit": "mg/dL", "date": "2026-03-01", "ref_range": "70-100"},
            "eGFR": {"value": 72, "unit": "mL/min/1.73m²", "date": "2026-03-01", "ref_range": ">60"},
            "ALT": {"value": 28, "unit": "U/L", "date": "2026-03-01", "ref_range": "7-56"},
            "Creatinine": {"value": 1.1, "unit": "mg/dL", "date": "2026-03-01", "ref_range": "0.6-1.2"},
            "Total_Cholesterol": {"value": 232, "unit": "mg/dL", "date": "2026-03-01", "ref_range": "<200"},
            "LDL": {"value": 145, "unit": "mg/dL", "date": "2026-03-01", "ref_range": "<100"},
        },
        "allergies": ["Sulfonamides"],
        "medical_history": [
            "Appendectomy (2005)",
            "No prior clinical trial participation",
            "Non-smoker",
            "Family history of cardiovascular disease",
        ],
        "vital_signs": {"BP": "142/88 mmHg", "HR": "78 bpm", "BMI": 27.4},
    },
    "P002": {
        "name": "James Chen",
        "age": 45,
        "sex": "Male",
        "weight_kg": 88.5,
        "height_cm": 178,
        "ethnicity": "Asian",
        "conditions": ["Major Depressive Disorder", "Generalized Anxiety Disorder"],
        "conditions_onset": {
            "Major Depressive Disorder": "2024-06-10",
            "Generalized Anxiety Disorder": "2023-01-05",
        },
        "medications": [
            {"name": "Sertraline", "dose": "100mg", "frequency": "once daily"},
            {"name": "Lorazepam", "dose": "0.5mg", "frequency": "as needed"},
        ],
        "lab_results": {
            "TSH": {"value": 2.8, "unit": "mIU/L", "date": "2026-02-15", "ref_range": "0.4-4.0"},
            "CBC_WBC": {"value": 7.2, "unit": "10^3/µL", "date": "2026-02-15", "ref_range": "4.5-11.0"},
            "Vitamin_D": {"value": 18, "unit": "ng/mL", "date": "2026-02-15", "ref_range": "30-100"},
            "B12": {"value": 450, "unit": "pg/mL", "date": "2026-02-15", "ref_range": "200-900"},
            "ALT": {"value": 22, "unit": "U/L", "date": "2026-02-15", "ref_range": "7-56"},
            "Creatinine": {"value": 0.9, "unit": "mg/dL", "date": "2026-02-15", "ref_range": "0.7-1.3"},
        },
        "allergies": [],
        "medical_history": [
            "No surgical history",
            "PHQ-9 score: 18 (moderately severe)",
            "GAD-7 score: 14 (moderate)",
            "No suicidal ideation",
            "Social drinker (2-3 drinks/week)",
        ],
        "vital_signs": {"BP": "128/82 mmHg", "HR": "72 bpm", "BMI": 27.9},
    },
    "P003": {
        "name": "Robert Williams",
        "age": 67,
        "sex": "Male",
        "weight_kg": 95.0,
        "height_cm": 180,
        "ethnicity": "African American",
        "conditions": ["Non-Small Cell Lung Cancer (Stage IIIA)", "COPD", "Type 2 Diabetes Mellitus"],
        "conditions_onset": {
            "Non-Small Cell Lung Cancer (Stage IIIA)": "2025-11-20",
            "COPD": "2018-04-12",
            "Type 2 Diabetes Mellitus": "2015-09-01",
        },
        "medications": [
            {"name": "Carboplatin", "dose": "AUC 5", "frequency": "every 3 weeks"},
            {"name": "Pemetrexed", "dose": "500mg/m²", "frequency": "every 3 weeks"},
            {"name": "Metformin", "dose": "500mg", "frequency": "twice daily"},
            {"name": "Tiotropium", "dose": "18mcg", "frequency": "once daily"},
        ],
        "lab_results": {
            "WBC": {"value": 4.8, "unit": "10^3/µL", "date": "2026-03-10", "ref_range": "4.5-11.0"},
            "Hemoglobin": {"value": 11.2, "unit": "g/dL", "date": "2026-03-10", "ref_range": "13.5-17.5"},
            "Platelets": {"value": 165, "unit": "10^3/µL", "date": "2026-03-10", "ref_range": "150-400"},
            "eGFR": {"value": 55, "unit": "mL/min/1.73m²", "date": "2026-03-10", "ref_range": ">60"},
            "ALT": {"value": 45, "unit": "U/L", "date": "2026-03-10", "ref_range": "7-56"},
            "HbA1c": {"value": 7.1, "unit": "%", "date": "2026-03-10", "ref_range": "4.0-5.6"},
            "PD_L1_TPS": {"value": 65, "unit": "%", "date": "2025-12-01", "ref_range": "N/A"},
            "EGFR_Mutation": {"value": "Negative", "unit": "", "date": "2025-12-01", "ref_range": "N/A"},
            "ALK_Rearrangement": {"value": "Negative", "unit": "", "date": "2025-12-01", "ref_range": "N/A"},
        },
        "allergies": ["Penicillin"],
        "medical_history": [
            "Former smoker (40 pack-years, quit 2020)",
            "Cholecystectomy (2012)",
            "Currently receiving first-line chemotherapy (Cycle 3 of 4)",
            "ECOG Performance Status: 1",
        ],
        "vital_signs": {"BP": "138/85 mmHg", "HR": "82 bpm", "BMI": 29.3},
    },
    # ---- Medium + Hard patients ----
    "P004": {
        "name": "Sarah Kim",
        "age": 34,
        "sex": "Female",
        "weight_kg": 62.0,
        "height_cm": 165,
        "ethnicity": "Korean",
        "conditions": ["Rheumatoid Arthritis", "Iron Deficiency Anemia"],
        "conditions_onset": {
            "Rheumatoid Arthritis": "2023-07-15",
            "Iron Deficiency Anemia": "2025-08-20",
        },
        "medications": [
            {"name": "Methotrexate", "dose": "15mg", "frequency": "once weekly"},
            {"name": "Folic Acid", "dose": "1mg", "frequency": "daily"},
            {"name": "Ferrous Sulfate", "dose": "325mg", "frequency": "twice daily"},
            {"name": "Prednisone", "dose": "5mg", "frequency": "once daily"},
        ],
        "lab_results": {
            "ESR": {"value": 42, "unit": "mm/hr", "date": "2026-02-28", "ref_range": "0-20"},
            "CRP": {"value": 18.5, "unit": "mg/L", "date": "2026-02-28", "ref_range": "<10"},
            "RF": {"value": 85, "unit": "IU/mL", "date": "2026-02-28", "ref_range": "<14"},
            "Anti_CCP": {"value": 120, "unit": "U/mL", "date": "2026-02-28", "ref_range": "<20"},
            "Hemoglobin": {"value": 10.8, "unit": "g/dL", "date": "2026-02-28", "ref_range": "12.0-16.0"},
            "Ferritin": {"value": 12, "unit": "ng/mL", "date": "2026-02-28", "ref_range": "12-150"},
            "ALT": {"value": 35, "unit": "U/L", "date": "2026-02-28", "ref_range": "7-56"},
            "Creatinine": {"value": 0.7, "unit": "mg/dL", "date": "2026-02-28", "ref_range": "0.6-1.1"},
            "WBC": {"value": 6.5, "unit": "10^3/µL", "date": "2026-02-28", "ref_range": "4.5-11.0"},
        },
        "allergies": ["NSAIDs (GI intolerance)"],
        "medical_history": [
            "No surgical history",
            "DAS28-CRP score: 4.8 (moderate disease activity)",
            "Failed hydroxychloroquine monotherapy",
            "No prior biologic use",
            "Non-smoker",
            "Desires pregnancy within 2 years",
        ],
        "vital_signs": {"BP": "118/72 mmHg", "HR": "76 bpm", "BMI": 22.8},
    },
    "P005": {
        "name": "David Thompson",
        "age": 72,
        "sex": "Male",
        "weight_kg": 78.0,
        "height_cm": 175,
        "ethnicity": "Caucasian",
        "conditions": ["Atrial Fibrillation", "Heart Failure (HFrEF)", "Chronic Kidney Disease Stage 3b"],
        "conditions_onset": {
            "Atrial Fibrillation": "2021-03-10",
            "Heart Failure (HFrEF)": "2022-06-18",
            "Chronic Kidney Disease Stage 3b": "2023-11-05",
        },
        "medications": [
            {"name": "Apixaban", "dose": "5mg", "frequency": "twice daily"},
            {"name": "Sacubitril/Valsartan", "dose": "97/103mg", "frequency": "twice daily"},
            {"name": "Metoprolol Succinate", "dose": "100mg", "frequency": "once daily"},
            {"name": "Spironolactone", "dose": "25mg", "frequency": "once daily"},
            {"name": "Furosemide", "dose": "40mg", "frequency": "once daily"},
        ],
        "lab_results": {
            "BNP": {"value": 680, "unit": "pg/mL", "date": "2026-03-05", "ref_range": "<100"},
            "eGFR": {"value": 38, "unit": "mL/min/1.73m²", "date": "2026-03-05", "ref_range": ">60"},
            "Potassium": {"value": 5.1, "unit": "mEq/L", "date": "2026-03-05", "ref_range": "3.5-5.0"},
            "Sodium": {"value": 136, "unit": "mEq/L", "date": "2026-03-05", "ref_range": "136-145"},
            "Hemoglobin": {"value": 12.1, "unit": "g/dL", "date": "2026-03-05", "ref_range": "13.5-17.5"},
            "LVEF": {"value": 30, "unit": "%", "date": "2026-01-15", "ref_range": "55-70"},
            "Creatinine": {"value": 1.8, "unit": "mg/dL", "date": "2026-03-05", "ref_range": "0.7-1.3"},
            "ALT": {"value": 20, "unit": "U/L", "date": "2026-03-05", "ref_range": "7-56"},
        },
        "allergies": ["ACE Inhibitors (angioedema)"],
        "medical_history": [
            "Coronary artery bypass graft (2019)",
            "Implantable cardioverter-defibrillator (ICD) placed 2022",
            "CHA2DS2-VASc score: 4",
            "NYHA Class III",
            "Former smoker (20 pack-years, quit 2010)",
            "2 hospitalizations for HF exacerbation in past year",
        ],
        "vital_signs": {"BP": "105/65 mmHg", "HR": "68 bpm (irregular)", "BMI": 25.5},
    },
    # ---- Hard-only patients ----
    "P006": {
        "name": "Aisha Patel",
        "age": 29,
        "sex": "Female",
        "weight_kg": 55.0,
        "height_cm": 160,
        "ethnicity": "South Asian",
        "conditions": ["Systemic Lupus Erythematosus", "Lupus Nephritis Class IV"],
        "conditions_onset": {
            "Systemic Lupus Erythematosus": "2022-04-01",
            "Lupus Nephritis Class IV": "2025-09-15",
        },
        "medications": [
            {"name": "Mycophenolate Mofetil", "dose": "1000mg", "frequency": "twice daily"},
            {"name": "Prednisone", "dose": "15mg", "frequency": "once daily (tapering)"},
            {"name": "Hydroxychloroquine", "dose": "200mg", "frequency": "twice daily"},
            {"name": "Lisinopril", "dose": "10mg", "frequency": "once daily"},
        ],
        "lab_results": {
            "ANA": {"value": "1:640", "unit": "titer", "date": "2026-03-01", "ref_range": "Negative"},
            "Anti_dsDNA": {"value": 180, "unit": "IU/mL", "date": "2026-03-01", "ref_range": "<30"},
            "C3": {"value": 55, "unit": "mg/dL", "date": "2026-03-01", "ref_range": "90-180"},
            "C4": {"value": 8, "unit": "mg/dL", "date": "2026-03-01", "ref_range": "10-40"},
            "eGFR": {"value": 62, "unit": "mL/min/1.73m²", "date": "2026-03-01", "ref_range": ">60"},
            "Proteinuria": {"value": 2.8, "unit": "g/24hr", "date": "2026-03-01", "ref_range": "<0.15"},
            "Creatinine": {"value": 1.2, "unit": "mg/dL", "date": "2026-03-01", "ref_range": "0.6-1.1"},
            "WBC": {"value": 3.8, "unit": "10^3/µL", "date": "2026-03-01", "ref_range": "4.5-11.0"},
            "Hemoglobin": {"value": 10.5, "unit": "g/dL", "date": "2026-03-01", "ref_range": "12.0-16.0"},
            "ALT": {"value": 18, "unit": "U/L", "date": "2026-03-01", "ref_range": "7-56"},
        },
        "allergies": [],
        "medical_history": [
            "Renal biopsy confirmed Class IV lupus nephritis (Sept 2025)",
            "SLEDAI-2K score: 16 (active disease)",
            "No prior biologic therapy",
            "Non-smoker",
            "Negative pregnancy test",
            "Using reliable contraception",
        ],
        "vital_signs": {"BP": "135/88 mmHg", "HR": "88 bpm", "BMI": 21.5},
    },
    "P007": {
        "name": "Michael O'Brien",
        "age": 52,
        "sex": "Male",
        "weight_kg": 105.0,
        "height_cm": 182,
        "ethnicity": "Caucasian",
        "conditions": ["Nonalcoholic Steatohepatitis (NASH)", "Obesity", "Type 2 Diabetes Mellitus", "Obstructive Sleep Apnea"],
        "conditions_onset": {
            "Nonalcoholic Steatohepatitis (NASH)": "2025-06-01",
            "Obesity": "2018-01-01",
            "Type 2 Diabetes Mellitus": "2020-11-15",
            "Obstructive Sleep Apnea": "2021-03-20",
        },
        "medications": [
            {"name": "Pioglitazone", "dose": "30mg", "frequency": "once daily"},
            {"name": "Empagliflozin", "dose": "25mg", "frequency": "once daily"},
            {"name": "Metformin", "dose": "1000mg", "frequency": "twice daily"},
            {"name": "Vitamin E", "dose": "800 IU", "frequency": "once daily"},
        ],
        "lab_results": {
            "ALT": {"value": 78, "unit": "U/L", "date": "2026-02-20", "ref_range": "7-56"},
            "AST": {"value": 65, "unit": "U/L", "date": "2026-02-20", "ref_range": "10-40"},
            "GGT": {"value": 95, "unit": "U/L", "date": "2026-02-20", "ref_range": "9-48"},
            "Fibroscan": {"value": 12.5, "unit": "kPa", "date": "2026-01-15", "ref_range": "<7.0"},
            "NAS_Score": {"value": 5, "unit": "", "date": "2026-01-15", "ref_range": "0-8"},
            "Fibrosis_Stage": {"value": "F2", "unit": "", "date": "2026-01-15", "ref_range": "F0-F4"},
            "HbA1c": {"value": 7.8, "unit": "%", "date": "2026-02-20", "ref_range": "4.0-5.6"},
            "Triglycerides": {"value": 280, "unit": "mg/dL", "date": "2026-02-20", "ref_range": "<150"},
            "eGFR": {"value": 85, "unit": "mL/min/1.73m²", "date": "2026-02-20", "ref_range": ">60"},
            "Creatinine": {"value": 1.0, "unit": "mg/dL", "date": "2026-02-20", "ref_range": "0.7-1.3"},
            "Platelets": {"value": 185, "unit": "10^3/µL", "date": "2026-02-20", "ref_range": "150-400"},
        },
        "allergies": ["Statins (myalgia)"],
        "medical_history": [
            "Liver biopsy confirmed NASH with fibrosis stage F2 (Jan 2026)",
            "No alcohol use (confirmed by PEth test)",
            "CPAP compliant for OSA",
            "No history of decompensated liver disease",
            "No hepatitis B or C",
        ],
        "vital_signs": {"BP": "140/92 mmHg", "HR": "75 bpm", "BMI": 31.7},
    },
    "P008": {
        "name": "Elena Rodriguez",
        "age": 41,
        "sex": "Female",
        "weight_kg": 68.0,
        "height_cm": 170,
        "ethnicity": "Hispanic",
        "conditions": ["Relapsing-Remitting Multiple Sclerosis"],
        "conditions_onset": {
            "Relapsing-Remitting Multiple Sclerosis": "2021-08-10",
        },
        "medications": [
            {"name": "Dimethyl Fumarate", "dose": "240mg", "frequency": "twice daily"},
            {"name": "Vitamin D3", "dose": "2000 IU", "frequency": "once daily"},
        ],
        "lab_results": {
            "MRI_Brain_Lesions": {"value": 8, "unit": "T2 lesions", "date": "2026-01-10", "ref_range": "N/A"},
            "MRI_New_Lesions": {"value": 2, "unit": "new Gd+ lesions", "date": "2026-01-10", "ref_range": "0"},
            "EDSS": {"value": 2.5, "unit": "", "date": "2026-02-01", "ref_range": "0-10"},
            "Lymphocyte_Count": {"value": 0.9, "unit": "10^3/µL", "date": "2026-03-01", "ref_range": "1.0-4.8"},
            "JCV_Antibody": {"value": "Positive", "unit": "", "date": "2026-01-01", "ref_range": "N/A"},
            "JCV_Index": {"value": 2.1, "unit": "", "date": "2026-01-01", "ref_range": "<0.9 low risk"},
            "ALT": {"value": 30, "unit": "U/L", "date": "2026-03-01", "ref_range": "7-56"},
            "Creatinine": {"value": 0.8, "unit": "mg/dL", "date": "2026-03-01", "ref_range": "0.6-1.1"},
            "WBC": {"value": 5.2, "unit": "10^3/µL", "date": "2026-03-01", "ref_range": "4.5-11.0"},
        },
        "allergies": [],
        "medical_history": [
            "2 relapses in the past 12 months while on dimethyl fumarate",
            "Relapse 1: optic neuritis (June 2025)",
            "Relapse 2: sensory symptoms (Nov 2025)",
            "No prior use of natalizumab or other high-efficacy DMTs",
            "Negative pregnancy test, using IUD contraception",
            "No history of PML",
        ],
        "vital_signs": {"BP": "120/75 mmHg", "HR": "70 bpm", "BMI": 23.5},
    },
}


# =============================================================================
# CLINICAL TRIALS
# =============================================================================

TRIALS: dict[str, dict[str, Any]] = {
    "T001": {
        "title": "GLYCOMASTER-3: Semaglutide Add-on for Uncontrolled Type 2 Diabetes",
        "phase": "Phase III",
        "condition": "Type 2 Diabetes Mellitus",
        "sponsor": "NovoMedica Research",
        "summary": (
            "A randomized, double-blind, placebo-controlled trial evaluating "
            "subcutaneous semaglutide 2.0mg weekly as add-on to metformin in "
            "adults with inadequately controlled T2DM."
        ),
        "inclusion_criteria": [
            "Age 18-75 years",
            "Diagnosed with Type 2 Diabetes Mellitus for ≥6 months",
            "HbA1c between 7.5% and 10.5% at screening",
            "Currently on stable metformin dose (≥1000mg/day) for ≥3 months",
            "eGFR ≥ 60 mL/min/1.73m²",
            "BMI ≥ 25 kg/m²",
        ],
        "exclusion_criteria": [
            "Type 1 Diabetes or secondary diabetes",
            "History of pancreatitis",
            "Active cancer or cancer treatment within 5 years",
            "Severe hepatic impairment (ALT > 3x ULN)",
            "Pregnant, breastfeeding, or planning pregnancy",
            "Use of GLP-1 receptor agonists within 3 months",
            "eGFR < 60 mL/min/1.73m²",
        ],
        "primary_endpoint": "Change in HbA1c from baseline at 52 weeks",
        "duration": "52 weeks",
    },
    "T002": {
        "title": "NEUROBALANCE: Psilocybin-Assisted Therapy for Treatment-Resistant Depression",
        "phase": "Phase II",
        "condition": "Major Depressive Disorder",
        "sponsor": "MindBridge Therapeutics",
        "summary": (
            "An open-label study evaluating psilocybin 25mg with psychological "
            "support in adults with treatment-resistant major depressive disorder "
            "who have failed ≥2 adequate antidepressant trials."
        ),
        "inclusion_criteria": [
            "Age 25-65 years",
            "Diagnosed with Major Depressive Disorder (DSM-5) for ≥1 year",
            "PHQ-9 score ≥ 15 (moderately severe to severe)",
            "Failed ≥2 adequate antidepressant trials in current episode",
            "Willing to taper off current antidepressants under medical supervision",
            "No active suicidal ideation (C-SSRS score 0-1 ideation)",
        ],
        "exclusion_criteria": [
            "History of psychotic disorder (schizophrenia, bipolar I with psychosis)",
            "Active substance use disorder (past 6 months)",
            "Current use of MAOIs or lithium",
            "History of seizures",
            "Severe personality disorder (Cluster A or B)",
            "Pregnant or breastfeeding",
            "Current benzodiazepine use (must be tapered before enrollment)",
            "Significant cardiovascular disease or uncontrolled hypertension (>160/100)",
        ],
        "primary_endpoint": "Change in PHQ-9 score from baseline at 6 weeks",
        "duration": "12 weeks (including follow-up)",
    },
    "T003": {
        "title": "IMMUNOSHIFT: Anti-CD20 Monoclonal Antibody for Active Rheumatoid Arthritis",
        "phase": "Phase III",
        "condition": "Rheumatoid Arthritis",
        "sponsor": "BioGenesis Labs",
        "summary": (
            "A randomized trial of obinutuzumab vs placebo in patients with "
            "moderate-to-severe RA who have had inadequate response to "
            "conventional DMARDs."
        ),
        "inclusion_criteria": [
            "Age 18-70 years",
            "Diagnosed with RA (ACR/EULAR 2010 criteria) for ≥6 months",
            "DAS28-CRP ≥ 3.2 (moderate to high disease activity)",
            "Seropositive (RF+ or Anti-CCP+)",
            "Inadequate response to ≥1 conventional DMARD (methotrexate, sulfasalazine, or leflunomide)",
            "Stable DMARD dose for ≥4 weeks before screening",
        ],
        "exclusion_criteria": [
            "Prior use of any biologic DMARD (TNF inhibitors, IL-6 inhibitors, JAK inhibitors, etc.)",
            "Active serious infection or history of recurrent infections",
            "Hemoglobin < 8.5 g/dL",
            "WBC < 3.0 × 10^3/µL or neutrophils < 1.5 × 10^3/µL",
            "ALT or AST > 2x ULN",
            "Pregnant, breastfeeding, or unwilling to use contraception",
            "Active malignancy or history of malignancy within 5 years",
            "Known hepatitis B or C infection",
        ],
        "primary_endpoint": "ACR50 response at week 24",
        "duration": "52 weeks",
    },
    "T004": {
        "title": "CHECKPOINT-LUNG: Pembrolizumab in PD-L1-High NSCLC After First-Line Therapy",
        "phase": "Phase II",
        "condition": "Non-Small Cell Lung Cancer",
        "sponsor": "OncoVanguard Research",
        "summary": (
            "A single-arm study of pembrolizumab monotherapy in patients with "
            "PD-L1 TPS ≥50% NSCLC who have progressed on or after first-line "
            "platinum-based chemotherapy."
        ),
        "inclusion_criteria": [
            "Age ≥ 18 years",
            "Histologically confirmed NSCLC (non-squamous or squamous)",
            "PD-L1 TPS ≥ 50% by IHC",
            "Progressed on or after first-line platinum-based chemotherapy",
            "ECOG Performance Status 0-1",
            "No EGFR activating mutations or ALK rearrangements",
            "Adequate organ function (ANC ≥1.5, Platelets ≥100, Hgb ≥9.0, eGFR ≥30, ALT/AST ≤2.5x ULN)",
            "Measurable disease per RECIST 1.1",
        ],
        "exclusion_criteria": [
            "Active autoimmune disease requiring systemic treatment in past 2 years",
            "Prior anti-PD-1/PD-L1/PD-L2 therapy",
            "Active brain metastases (treated, stable brain mets allowed)",
            "Active interstitial lung disease or pneumonitis",
            "Systemic corticosteroid use > 10mg/day prednisone equivalent",
            "Active hepatitis B or C, or HIV",
            "Received live vaccine within 30 days of planned start",
        ],
        "primary_endpoint": "Objective response rate (ORR) per RECIST 1.1",
        "duration": "Up to 35 cycles (approximately 2 years)",
    },
    "T005": {
        "title": "NEPHROGUARD: Voclosporin for Active Lupus Nephritis",
        "phase": "Phase III",
        "condition": "Lupus Nephritis",
        "sponsor": "RenalShield Biopharm",
        "summary": (
            "A randomized, double-blind trial of voclosporin added to mycophenolate mofetil "
            "and low-dose corticosteroids in patients with active lupus nephritis (Class III, IV, or V)."
        ),
        "inclusion_criteria": [
            "Age 18-75 years",
            "Biopsy-confirmed lupus nephritis (ISN/RPS Class III, IV, or V) within 2 years",
            "Active nephritis: proteinuria ≥ 1.5 g/24hr OR urine protein-to-creatinine ratio ≥ 1.5",
            "eGFR ≥ 45 mL/min/1.73m²",
            "Currently receiving mycophenolate mofetil at stable dose for ≥4 weeks",
            "ANA positive or anti-dsDNA positive",
        ],
        "exclusion_criteria": [
            "Dialysis-dependent renal failure within past 12 months",
            "eGFR < 45 mL/min/1.73m²",
            "Uncontrolled hypertension (>160/100 mmHg despite treatment)",
            "Active severe CNS lupus (seizures, psychosis, cerebritis)",
            "Prior use of calcineurin inhibitors (cyclosporine, tacrolimus, voclosporin) within 4 weeks",
            "Active serious infection requiring IV antibiotics",
            "Pregnant, breastfeeding, or not using reliable contraception",
            "Malignancy within past 5 years (except non-melanoma skin cancer)",
        ],
        "primary_endpoint": "Complete renal response at week 52",
        "duration": "104 weeks",
    },
    "T006": {
        "title": "LIVERRENEW: Resmetirom for Nonalcoholic Steatohepatitis with Fibrosis",
        "phase": "Phase III",
        "condition": "Nonalcoholic Steatohepatitis (NASH)",
        "sponsor": "HepatoVita Sciences",
        "summary": (
            "A randomized, double-blind, placebo-controlled trial evaluating "
            "resmetirom (THR-β agonist) in patients with biopsy-proven NASH "
            "and liver fibrosis (F2-F3)."
        ),
        "inclusion_criteria": [
            "Age 18-75 years",
            "Biopsy-proven NASH with NAS score ≥ 4 within 6 months of screening",
            "Liver fibrosis stage F2 or F3",
            "BMI ≥ 25 kg/m²",
            "ALT ≥ 1.5x ULN (≥ 42 U/L for females, ≥ 60 U/L for males)",
            "Stable weight (±5%) for ≥3 months before screening",
        ],
        "exclusion_criteria": [
            "Cirrhosis (fibrosis stage F4) or decompensated liver disease",
            "Other chronic liver disease (hepatitis B/C, autoimmune hepatitis, Wilson disease, etc.)",
            "Alcohol consumption > 21 drinks/week (men) or > 14 drinks/week (women)",
            "Use of medications known to cause hepatic steatosis (amiodarone, tamoxifen, systemic corticosteroids)",
            "Uncontrolled diabetes (HbA1c > 9.5%)",
            "Prior bariatric surgery",
            "eGFR < 60 mL/min/1.73m²",
            "Platelet count < 140 × 10^3/µL",
            "Current use of pioglitazone or other TZDs (washout period of 3 months required)",
            "Plans for significant weight loss intervention during study",
        ],
        "primary_endpoint": "NASH resolution without worsening fibrosis at week 52",
        "duration": "52 weeks",
    },
}


# =============================================================================
# TASK DEFINITIONS
# =============================================================================

TASKS: dict[str, dict[str, Any]] = {
    "easy": {
        "name": "Basic Eligibility Screening",
        "description": (
            "Screen 3 patients against 2 clinical trials with clear-cut "
            "inclusion/exclusion criteria. Criteria are straightforward: "
            "age ranges, specific diagnoses, and obvious lab values."
        ),
        "patient_ids": ["P001", "P002", "P003"],
        "trial_ids": ["T001", "T002"],
        "max_steps": 30,
    },
    "medium": {
        "name": "Multi-Criteria Matching",
        "description": (
            "Screen 5 patients against 3 clinical trials with more nuanced "
            "criteria including lab value ranges, medication conflicts, "
            "comorbidity interactions, and disease activity scores."
        ),
        "patient_ids": ["P001", "P002", "P003", "P004", "P005"],
        "trial_ids": ["T001", "T003", "T004"],
        "max_steps": 60,
    },
    "hard": {
        "name": "Complex Protocol Evaluation",
        "description": (
            "Screen 8 patients against 4 trials with subtle criteria including "
            "temporal conditions (diagnosis recency, washout periods), biomarker "
            "thresholds, disease staging edge cases, and red-herring conditions."
        ),
        "patient_ids": ["P001", "P002", "P003", "P004", "P005", "P006", "P007", "P008"],
        "trial_ids": ["T001", "T004", "T005", "T006"],
        "max_steps": 100,
    },
}


# =============================================================================
# GROUND TRUTH — Eligibility decisions with reasoning keys
#
# Each entry: (patient_id, trial_id) -> {eligible: bool, key_reasons: [str]}
# key_reasons are phrases the agent's reasoning should mention for bonus credit.
# =============================================================================

GROUND_TRUTH: dict[tuple[str, str], dict[str, Any]] = {
    # =========== EASY TASK: P001-P003 × T001-T002 ===========

    # P001 (Maria, 58F, T2DM/HTN/HLD) vs T001 (Semaglutide for T2DM)
    ("P001", "T001"): {
        "eligible": True,
        "key_reasons": [
            "age 58 within 18-75",
            "T2DM diagnosed >6 months",
            "HbA1c 8.2% within 7.5-10.5%",
            "metformin 1000mg stable dose",
            "eGFR 72 ≥ 60",
            "BMI 27.4 ≥ 25",
        ],
    },
    # P001 vs T002 (Psilocybin for depression)
    ("P001", "T002"): {
        "eligible": False,
        "key_reasons": [
            "no diagnosis of Major Depressive Disorder",
        ],
    },
    # P002 (James, 45M, MDD/GAD) vs T001 (Semaglutide for T2DM)
    ("P002", "T001"): {
        "eligible": False,
        "key_reasons": [
            "no diagnosis of Type 2 Diabetes Mellitus",
        ],
    },
    # P002 vs T002 (Psilocybin for depression)
    ("P002", "T002"): {
        "eligible": False,
        "key_reasons": [
            "PHQ-9 score 18 meets ≥15 threshold",
            "MDD diagnosed >1 year",
            "age 45 within 25-65",
            "current benzodiazepine use (Lorazepam) - must be tapered before enrollment",
            "only failed 1 antidepressant (sertraline), needs ≥2 failed trials",
        ],
    },
    # P003 (Robert, 67M, NSCLC/COPD/T2DM) vs T001 (Semaglutide for T2DM)
    ("P003", "T001"): {
        "eligible": False,
        "key_reasons": [
            "active cancer (NSCLC) - excluded",
            "cancer treatment within 5 years (currently on chemotherapy)",
            "eGFR 55 < 60 threshold",
        ],
    },
    # P003 vs T002 (Psilocybin for depression)
    ("P003", "T002"): {
        "eligible": False,
        "key_reasons": [
            "no diagnosis of Major Depressive Disorder",
        ],
    },

    # =========== MEDIUM TASK adds: P004-P005 × T001,T003,T004 ===========

    # P004 (Sarah, 34F, RA/anemia) vs T001 (Semaglutide for T2DM)
    ("P004", "T001"): {
        "eligible": False,
        "key_reasons": [
            "no diagnosis of Type 2 Diabetes Mellitus",
        ],
    },
    # P004 vs T003 (Anti-CD20 for RA)
    ("P004", "T003"): {
        "eligible": True,
        "key_reasons": [
            "age 34 within 18-70",
            "RA diagnosed >6 months",
            "DAS28-CRP 4.8 ≥ 3.2",
            "seropositive (RF 85, Anti-CCP 120)",
            "inadequate response to hydroxychloroquine, currently on methotrexate",
            "no prior biologic use",
            "hemoglobin 10.8 ≥ 8.5",
            "WBC 6.5 ≥ 3.0",
            "stable DMARD dose",
        ],
    },
    # P004 vs T004 (Pembrolizumab for NSCLC)
    ("P004", "T004"): {
        "eligible": False,
        "key_reasons": [
            "no diagnosis of NSCLC",
        ],
    },
    # P005 (David, 72M, AFib/HF/CKD3b) vs T001 (Semaglutide for T2DM)
    ("P005", "T001"): {
        "eligible": False,
        "key_reasons": [
            "no diagnosis of Type 2 Diabetes Mellitus",
        ],
    },
    # P005 vs T003 (Anti-CD20 for RA)
    ("P005", "T003"): {
        "eligible": False,
        "key_reasons": [
            "no diagnosis of Rheumatoid Arthritis",
            "age 72 exceeds maximum 70",
        ],
    },
    # P005 vs T004 (Pembrolizumab for NSCLC)
    ("P005", "T004"): {
        "eligible": False,
        "key_reasons": [
            "no diagnosis of NSCLC",
        ],
    },
    # P001 vs T003 (Anti-CD20 for RA)
    ("P001", "T003"): {
        "eligible": False,
        "key_reasons": [
            "no diagnosis of Rheumatoid Arthritis",
        ],
    },
    # P001 vs T004 (Pembrolizumab for NSCLC)
    ("P001", "T004"): {
        "eligible": False,
        "key_reasons": [
            "no diagnosis of NSCLC",
        ],
    },
    # P002 vs T003 (Anti-CD20 for RA)
    ("P002", "T003"): {
        "eligible": False,
        "key_reasons": [
            "no diagnosis of Rheumatoid Arthritis",
        ],
    },
    # P002 vs T004 (Pembrolizumab for NSCLC)
    ("P002", "T004"): {
        "eligible": False,
        "key_reasons": [
            "no diagnosis of NSCLC",
        ],
    },
    # P003 vs T003 (Anti-CD20 for RA)
    ("P003", "T003"): {
        "eligible": False,
        "key_reasons": [
            "no diagnosis of Rheumatoid Arthritis",
            "active malignancy (NSCLC)",
        ],
    },
    # P003 vs T004 (Pembrolizumab for NSCLC)
    ("P003", "T004"): {
        "eligible": True,
        "key_reasons": [
            "histologically confirmed NSCLC",
            "PD-L1 TPS 65% ≥ 50%",
            "currently on first-line platinum chemo (cycle 3 of 4) - progressing/completing",
            "ECOG PS 1 within 0-1",
            "EGFR negative, ALK negative",
            "hemoglobin 11.2 ≥ 9.0, platelets 165 ≥ 100, ALT 45 ≤ 2.5x ULN",
            "no autoimmune disease",
            "no prior anti-PD-1 therapy",
        ],
    },

    # =========== HARD TASK adds: P006-P008 × T001,T004,T005,T006 ===========

    # P006 (Aisha, 29F, SLE/Lupus Nephritis) vs T001
    ("P006", "T001"): {
        "eligible": False,
        "key_reasons": [
            "no diagnosis of Type 2 Diabetes Mellitus",
        ],
    },
    # P006 vs T004
    ("P006", "T004"): {
        "eligible": False,
        "key_reasons": [
            "no diagnosis of NSCLC",
        ],
    },
    # P006 vs T005 (Voclosporin for Lupus Nephritis)
    ("P006", "T005"): {
        "eligible": True,
        "key_reasons": [
            "age 29 within 18-75",
            "biopsy-confirmed Class IV lupus nephritis within 2 years (Sept 2025)",
            "proteinuria 2.8 g/24hr ≥ 1.5",
            "eGFR 62 ≥ 45",
            "currently on mycophenolate mofetil stable dose",
            "ANA positive, anti-dsDNA positive",
            "no prior calcineurin inhibitor use",
            "using reliable contraception",
            "BP 135/88 not uncontrolled (< 160/100)",
        ],
    },
    # P006 vs T006
    ("P006", "T006"): {
        "eligible": False,
        "key_reasons": [
            "no diagnosis of NASH",
        ],
    },

    # P007 (Michael, 52M, NASH/Obesity/T2DM/OSA) vs T001
    ("P007", "T001"): {
        "eligible": False,
        "key_reasons": [
            "currently on pioglitazone (TZD), not solely metformin-based",
            "HbA1c 7.8% within range but uses multiple diabetes drugs beyond metformin",
            "BMI 31.7 ≥ 25 meets criterion",
            "eGFR 85 ≥ 60 meets criterion",
            "no GLP-1 RA use - criterion met",
            "metformin 1000mg meets dose requirement",
            "NOTE: technically eligible on paper for T001 since HbA1c in range and on metformin ≥1000mg",
        ],
    },
    # P007 vs T004
    ("P007", "T004"): {
        "eligible": False,
        "key_reasons": [
            "no diagnosis of NSCLC",
        ],
    },
    # P007 vs T005
    ("P007", "T005"): {
        "eligible": False,
        "key_reasons": [
            "no diagnosis of Lupus Nephritis or SLE",
        ],
    },
    # P007 vs T006 (Resmetirom for NASH)
    ("P007", "T006"): {
        "eligible": False,
        "key_reasons": [
            "biopsy-proven NASH with NAS ≥ 4 (score is 5) - meets criterion",
            "fibrosis F2 within F2-F3 range - meets criterion",
            "BMI 31.7 ≥ 25 - meets criterion",
            "ALT 78 ≥ 60 (male threshold) - meets criterion",
            "EXCLUDED: currently on pioglitazone (TZD) - requires 3-month washout",
            "no other liver disease, no significant alcohol - meets criteria",
        ],
    },

    # P008 (Elena, 41F, RRMS) vs T001
    ("P008", "T001"): {
        "eligible": False,
        "key_reasons": [
            "no diagnosis of Type 2 Diabetes Mellitus",
        ],
    },
    # P008 vs T004
    ("P008", "T004"): {
        "eligible": False,
        "key_reasons": [
            "no diagnosis of NSCLC",
        ],
    },
    # P008 vs T005
    ("P008", "T005"): {
        "eligible": False,
        "key_reasons": [
            "no diagnosis of Lupus Nephritis or SLE",
        ],
    },
    # P008 vs T006
    ("P008", "T006"): {
        "eligible": False,
        "key_reasons": [
            "no diagnosis of NASH",
        ],
    },

    # Also need remaining combos for hard task
    # P001 vs T005
    ("P001", "T005"): {
        "eligible": False,
        "key_reasons": [
            "no diagnosis of Lupus Nephritis or SLE",
        ],
    },
    # P001 vs T006
    ("P001", "T006"): {
        "eligible": False,
        "key_reasons": [
            "no diagnosis of NASH",
        ],
    },
    # P002 vs T005
    ("P002", "T005"): {
        "eligible": False,
        "key_reasons": [
            "no diagnosis of Lupus Nephritis or SLE",
        ],
    },
    # P002 vs T006
    ("P002", "T006"): {
        "eligible": False,
        "key_reasons": [
            "no diagnosis of NASH",
        ],
    },
    # P003 vs T005
    ("P003", "T005"): {
        "eligible": False,
        "key_reasons": [
            "no diagnosis of Lupus Nephritis or SLE",
            "active malignancy within 5 years",
        ],
    },
    # P003 vs T006
    ("P003", "T006"): {
        "eligible": False,
        "key_reasons": [
            "no diagnosis of NASH",
            "active cancer treatment",
        ],
    },
    # P004 vs T005
    ("P004", "T005"): {
        "eligible": False,
        "key_reasons": [
            "no diagnosis of Lupus Nephritis or SLE",
        ],
    },
    # P004 vs T006
    ("P004", "T006"): {
        "eligible": False,
        "key_reasons": [
            "no diagnosis of NASH",
        ],
    },
    # P005 vs T005
    ("P005", "T005"): {
        "eligible": False,
        "key_reasons": [
            "no diagnosis of Lupus Nephritis or SLE",
            "eGFR 38 < 45 threshold",
        ],
    },
    # P005 vs T006
    ("P005", "T006"): {
        "eligible": False,
        "key_reasons": [
            "no diagnosis of NASH",
        ],
    },
}

# Fix P007 vs T001 — on re-evaluation, P007 IS eligible for T001:
# - T2DM ≥6 months ✓, HbA1c 7.8% in 7.5-10.5% ✓, metformin ≥1000mg ✓,
# - eGFR 85 ≥60 ✓, BMI 31.7 ≥25 ✓, no pancreatitis ✓, ALT 78 not >3x ULN (168) ✓
# - No GLP-1 RA use ✓, active cancer excluded — no cancer ✓
# - Pioglitazone is not an exclusion criterion for T001
GROUND_TRUTH[("P007", "T001")] = {
    "eligible": True,
    "key_reasons": [
        "age 52 within 18-75",
        "T2DM diagnosed >6 months (since 2020)",
        "HbA1c 7.8% within 7.5-10.5%",
        "metformin 1000mg ≥1000mg/day stable",
        "eGFR 85 ≥ 60",
        "BMI 31.7 ≥ 25",
        "ALT 78 not > 3x ULN (168)",
        "no active cancer",
        "no GLP-1 RA use",
    ],
}


def get_patient_summary(patient_id: str) -> dict[str, str]:
    """Return a brief summary of a patient (for list_patients tool)."""
    p = PATIENTS[patient_id]
    return {
        "patient_id": patient_id,
        "name": p["name"],
        "age": str(p["age"]),
        "sex": p["sex"],
        "primary_conditions": ", ".join(p["conditions"][:2]),
    }


def get_trial_summary(trial_id: str) -> dict[str, str]:
    """Return a brief summary of a trial (for list_trials tool)."""
    t = TRIALS[trial_id]
    return {
        "trial_id": trial_id,
        "title": t["title"],
        "phase": t["phase"],
        "condition": t["condition"],
    }
