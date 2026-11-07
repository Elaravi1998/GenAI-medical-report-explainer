# 🏥 Medical Report Explainer

A privacy-first Python project that converts simple medical laboratory report text into structured educational explanations. It extracts test names, values, units, and reference ranges, compares results with the supplied ranges, explains common medical terms, and generates questions to discuss with healthcare professionals.

> **Medical Disclaimer:** This project is for educational and software demonstration purposes only. It does not diagnose diseases, recommend treatments, or replace professional medical advice.

## 🚀 Features

- Medical laboratory text extraction
- Test name and numerical value identification
- Reference range comparison
- Below-range and above-range identification
- Plain-language explanations of common medical terms
- Questions to discuss with healthcare professionals
- JSON report generation
- Local processing without external API calls

## 🛠️ Technology Stack

- Python 3.9+
- Regular Expressions
- JSON
- Python Standard Library
- Text Processing

## 📂 Project Structure

```text
medical-report-explainer/
│
├── medical_report_explainer.py
├── sample_report.txt
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/medical-report-explainer.git
```

Navigate into the project:

```bash
cd medical-report-explainer
```

No third-party packages are required.

## ▶️ Usage

Run the sample report:

```bash
python medical_report_explainer.py --input sample_report.txt
```

Generate JSON output:

```bash
python medical_report_explainer.py --input sample_report.txt --output explanation.json
```

Pass report text directly:

```bash
python medical_report_explainer.py --text "Hemoglobin: 13.5 g/dL (12.0 - 16.0)"
```

## 📄 Example Input

```text
Hemoglobin: 13.5 g/dL (12.0 - 16.0)
WBC: 7.2 10^3/uL (4.0 - 11.0)
Glucose: 108 mg/dL (70 - 99)
TSH: 2.1 mIU/L (0.4 - 4.0)
```

## 📊 Example Output

The application generates structured JSON containing:

- Recognized laboratory results
- Extracted values and units
- Supplied reference ranges
- Comparison status
- Plain-language explanations
- Questions to ask a healthcare professional
- Important limitations

## 🔍 How It Works

1. Reads medical report text from a local file or command-line argument.
2. Extracts supported laboratory test names and values.
3. Identifies reference ranges explicitly supplied in the text.
4. Compares numerical values with those ranges.
5. Adds glossary explanations for supported medical terms.
6. Generates questions to discuss with a healthcare professional.
7. Produces structured JSON output.

## 🔐 Privacy and Safety

- Report text is processed locally.
- No external API requests are made.
- Do not upload identifiable patient information to GitHub.
- Use synthetic or de-identified reports for demonstrations.
- Reference ranges vary by laboratory and individual circumstances.
- A result within range does not guarantee good health.
- An out-of-range result does not establish a diagnosis.

## ⚠️ Current Limitations

- Supports simple plain-text report formats.
- Does not currently extract text from scanned PDFs or images.
- Does not provide diagnoses or treatment recommendations.
- Does not perform validated clinical risk assessments.
- Extracted values and reference ranges must be checked against the original report.

## 🔮 Future Enhancements

- PDF medical report extraction
- OCR-based scanned report processing
- Clinically reviewed medical terminology
- Validated unit conversion
- Multilingual explanations
- Optional privacy-conscious LLM integration
- Interactive Streamlit user interface
- Medical report history and visualization

## 👨‍💻 Author

Developed as a Python and AI portfolio project.

## 📜 License

Choose a license such as MIT before publishing and include its corresponding LICENSE file.
