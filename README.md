# Data Annotation Portfolio

Professional portfolio demonstrating text classification and object detection annotation with quality assurance.


---

## Overview

**40 text annotations** (intent classification) + **78 visual annotations** (object detection)

- Text: 5 categories, balanced distribution, 100% approval
- Visual: COCO format, 96.9% approval, 25 images
- QA: Complete tracking system, automated validation

---

## Repository Structure
```
├── 1_visual_annotation/       # Object detection (COCO JSON)
├── 2_text_annotation/         # Intent classification (CSV)
├── 3_qa_tracking/             # QA dashboard & metrics
├── 4_presentation/            # Project slides
└── tools/                     # Python validation scripts
```

---

## Key Metrics

| Metric | Value |
|--------|-------|
| Total Annotations | 118 |
| Approval Rate | 96.9% |
| Average QA Score | 98.3% |
| Error Rate | 16.9 per 100 |
| Issues Corrected | 11/13 (84.6%) |

---

## Annotation Tasks

### Visual (Object Detection)
- **25 images**, 78 bounding boxes
- **Categories:** main_product, secondary_item, background
- **Format:** COCO JSON

[Guidelines](1_visual_annotation/annotation_guidelines.md) • [Quality Report](1_visual_annotation/quality_report.md)

### Text (Intent Classification)
- **40 messages**, 5 intent categories
- **Categories:** cancellation, technical_support, billing_inquiry, feature_request, general_question
- **Format:** CSV with metadata

[Guidelines](2_text_annotation/annotation_guidelines.md) • [Quality Report](2_text_annotation/quality_report.md)

---

## Quality Assurance

- Multi-stage QA process with self-review
- Real-time tracking: [Google Sheets Dashboard](https://docs.google.com/spreadsheets/d/18yzrfgwl5F-HHPl8VHJzn595HxMr9KPeeAEXJl22TIg/edit?usp=sharing)
- Automated validation with Python scripts
- Complete error analysis and corrections

---

## Tools Used

- **Roboflow** - Visual annotations
- **Python** - Validation scripts
- **Google Sheets** - QA tracking
- **Git/GitHub** - Version control

---

## Running Validation
```bash
git clone https://github.com/KapliaIryna/data-annotation-portfolio.git
cd data-annotation-portfolio
pip install -r tools/requirements.txt
python3 tools/validation_checks.py
```

---

## Key Achievements

✅ Balanced class distribution (17-22% per category)  
✅ Comprehensive edge case documentation  
✅ Industry-standard formats (COCO JSON, CSV)  
✅ Automated quality checks  
✅ 98.3% quality score

---

## Contact

**LinkedIn:** [Iryna Kaplia](https://www.linkedin.com/in/iryna-kaplia-804a4917/)  
**Email:** kaplya.po4ta@gmail.com

---

