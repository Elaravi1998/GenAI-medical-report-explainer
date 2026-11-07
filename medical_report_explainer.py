#!/usr/bin/env python3
"""Local educational medical lab-report explainer. Not for diagnosis or treatment."""
import argparse
import json
import re
from pathlib import Path

GLOSSARY = {
    "hemoglobin": "Hemoglobin carries oxygen in red blood cells.",
    "wbc": "White blood cells are part of the immune system.",
    "rbc": "Red blood cells carry oxygen around the body.",
    "platelet": "Platelets help blood clot.",
    "glucose": "Glucose is a type of sugar measured in blood.",
    "hba1c": "HbA1c reflects average blood glucose over roughly 2–3 months.",
    "creatinine": "Creatinine is commonly used, with other information, to assess kidney function.",
    "tsh": "TSH helps assess thyroid function.",
    "cholesterol": "Cholesterol is a blood lipid; interpretation depends on the full profile and personal risk.",
    "hdl": "HDL is a type of cholesterol often called 'good' cholesterol.",
    "ldl": "LDL is a type of cholesterol often called 'bad' cholesterol.",
    "triglycerides": "Triglycerides are a type of fat measured in blood.",
    "alt": "ALT is an enzyme commonly assessed in liver blood testing.",
    "ast": "AST is an enzyme measured in liver and other tissue assessments.",
    "bilirubin": "Bilirubin is a pigment processed by the liver.",
    "sodium": "Sodium is an electrolyte involved in fluid balance and nerve function.",
    "potassium": "Potassium is important for muscle, nerve, and heart function.",
    "calcium": "Calcium is important for bones, muscles, and nerve signalling.",
    "vitamin d": "Vitamin D supports bone health and other body functions.",
    "vitamin b12": "Vitamin B12 supports red blood cell formation and nerve function.",
    "crp": "CRP is a marker that can rise with inflammation; it does not identify the cause.",
}
LINE = re.compile(
    r"^\s*(?P<test>[A-Za-z][A-Za-z0-9 /()_-]{1,50}?)\s*[:\-]\s*"
    r"(?P<value>[<>]?\s*\d+(?:\.\d+)?)\s*(?P<unit>[A-Za-zµμ/%³^._-]+(?:\s*/\s*[A-Za-zµμ³^._-]+)?)?"
    r"(?:\s*\((?P<ref>[^()]*(?:\d)[^()]*)\))?\s*$", re.I
)
RANGE = re.compile(r"(?P<lo>\d+(?:\.\d+)?)\s*(?:-|to)\s*(?P<hi>\d+(?:\.\d+)?)", re.I)

def explain_name(name):
    key = name.lower().strip()
    if key in GLOSSARY:
        return GLOSSARY[key]
    for term, explanation in GLOSSARY.items():
        if term in key:
            return explanation
    return "This test is not in the built-in glossary. Ask your healthcare professional what it measures."

def classify(value_text, ref_text):
    vm, rm = re.search(r"\d+(?:\.\d+)?", value_text), RANGE.search(ref_text or "")
    if not vm or not rm:
        return "Not assessed"
    value, low, high = float(vm.group()), float(rm.group("lo")), float(rm.group("hi"))
    return "Below stated range" if value < low else "Above stated range" if value > high else "Within stated range"

def explain(report_text):
    findings = []
    for line in report_text.splitlines():
        m = LINE.match(line)
        if not m:
            continue
        test, value = m.group("test").strip(), m.group("value").replace(" ", "")
        unit, ref = (m.group("unit") or "").strip(), (m.group("ref") or "").strip()
        findings.append({
            "test": test, "value": value, "unit": unit, "reference_range": ref,
            "status": classify(value, ref), "plain_language_note": explain_name(test)
        })
    counts = {s: sum(x["status"] == s for x in findings) for s in
              ("Within stated range", "Below stated range", "Above stated range", "Not assessed")}
    summary = (f"Recognized {len(findings)} result(s): " + ", ".join(f"{v} {k.lower()}" for k, v in counts.items()) +
               ". These labels compare values only with ranges supplied in the text; they are not a diagnosis.")
    questions = [
        "How should these results be interpreted in light of my symptoms, history, age, and medicines?",
        "Are the laboratory's reference ranges appropriate for me?"
    ]
    flagged = [x["test"] for x in findings if x["status"] in ("Below stated range", "Above stated range")]
    if flagged:
        questions += [f"What could explain the result(s) flagged against the supplied range: {', '.join(flagged)}?",
                      "Do any results need repeat testing or follow-up, and when?"]
    return {
        "summary": summary, "findings": findings, "questions_to_ask_clinician": questions,
        "limitations": [
            "Educational information only; not diagnosis or treatment advice.",
            "Reference ranges vary by laboratory and may depend on personal and clinical context.",
            "A value within range does not guarantee health; an out-of-range value does not prove disease.",
            "This parser supports only simple plain-text lines and may miss or misread complex reports."
        ],
        "privacy": "Processing is local; this script makes no network requests."
    }

def main():
    p = argparse.ArgumentParser(description="Explain simple lab-report text locally (educational use only).")
    p.add_argument("--input", type=Path, help="UTF-8 text file")
    p.add_argument("--text", help="Report text in quotes")
    p.add_argument("--output", type=Path, help="Optional JSON output path")
    a = p.parse_args()
    if a.input:
        raw = a.input.read_text(encoding="utf-8")
    elif a.text:
        raw = a.text
    else:
        p.error("Provide --input report.txt or --text 'Hemoglobin: 13.5 g/dL (12.0 - 16.0)'.")
    result = json.dumps(explain(raw), indent=2, ensure_ascii=False)
    if a.output:
        a.output.write_text(result, encoding="utf-8")
        print(f"Saved JSON to {a.output}")
    else:
        print(result)

if __name__ == "__main__":
    main()
