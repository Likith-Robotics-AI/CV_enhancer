import anthropic
import subprocess
from pathlib import Path
import fitz
import streamlit as st


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    return "\n".join(page.get_text() for page in doc)

# File paths
pdf_path = Path(r"C:\Users\likit\Desktop\pythonProject\CV_Reader\prototype_3\input\Ruthvik Saripalli resume.pdf")
template_path = Path(r"C:\Users\likit\Desktop\pythonProject\CV_Reader\prototype_3\yaml\professional.yaml")

# Extract content
cv_text = extract_text_from_pdf(pdf_path)
template_yaml = template_path.read_text(encoding="utf-8")


# Build prompt
user_prompt = f"""
You are an expert Indian CV enhancement specialist and YAML structuring expert trained in RenderCV-compatible formatting. Your task is to convert unstructured CV text into a valid, polished YAML CV using RenderCV syntax and professional Indian formatting.

## OBJECTIVE:
- Improve clarity, grammar, and professional tone using Indian CV standards
- Enhance phrasing without adding or inventing any content
- Provide useful remarks inline for feedback or revision purposes
- Return a fully formatted YAML CV for RenderCV

---

## INPUTS:
**CV_TEXT**
Raw CV content (unstructured .txt or .pdf extract)

**YAML_TEMPLATE**
A RenderCV-compliant YAML template with correct structure

---

## INDIAN CV STRUCTURE RULES:
You may rearrange sections to follow common Indian CV formats. Choose the most appropriate structure based on the candidate’s background:

### A. Fresh Graduate / Entry Level
1. Profile Summary
2. Education
3. Internships / Projects
4. Skills
5. Certifications
6. Extracurricular / Volunteering
7. Social Links

### B. Mid-Career Professional
1. Profile Summary
2. Work Experience
3. Projects
4. Education
5. Skills
6. Certifications
7. Awards / Extra Sections
8. Social Links

### C. Technical/IT/Research CV
1. Summary
2. Education
3. Experience (Research, Industry)
4. Technical Skills
5. Projects / Publications
6. Certifications / Achievements
7. Social Profiles

Choose the layout that best presents the candidate’s strengths and arrange YAML sections accordingly.

---

## STRUCTURAL & FORMAT RULES:

### YAML STRUCTURE:
- Begin output with `cv:`
- Preserve YAML indentation and section structure
- Use only supported RenderCV entry types:
  - `ExperienceEntry`, `EducationEntry`, `NormalEntry`, `BulletEntry`, `OneLineEntry`, `PublicationEntry`

### SECTION STRUCTURE & PURPOSE:
- **summary**: Brief career profile (2–4 lines max) written in third person
- **education**: Degree-level or higher; avoid duplicating school info
- **experience**: All roles, internships, or projects, using STAR-format highlights
- **projects**: Use NormalEntry or ExperienceEntry depending on detail
- **skills**: Grouped or bullet format with categories (e.g., Programming, Tools)
- **certifications**: Must include institution and dates
- **social_links**: Use approved platforms only

### FIELD FORMATTING RULES:
- Dates: Use `YYYY-MM` format; `"present"` for current roles
- Empty required fields must be retained (e.g., `summary: ""`)
- `highlights:` must be valid YAML:
  - Use double quotes `"..."` if containing colons, commas, or special characters
  - Use `>` folded style only if template already uses it
- `BulletEntry` sections must use: `- bullet: "<string>"`

---

## CONTENT ENHANCEMENT RULES:
- Enhance language: fix grammar, spelling, formality
- Use professional Indian English tone (e.g., "Analysed", "Organised")
- Use action-oriented phrasing with measurable impact
- Rewrite for conciseness and impact without changing factual content
- Follow STAR or Role–Action–Impact format for experience bullets
- You may rephrase entries but must **not fabricate any information**

---

## REMARKS SYSTEM:
To suggest improvements or identify vague entries, insert a comment-like highlight as:

- bullet: "Redrafted statement: Reduced turnaround time by 40% through automation"
- bullet: "❗ Remark: Original CV lacked quantifiable results — confirm actual figures if available."

Add no more than **1 remark per section**, only if you spot unclear or weak content. Prefix remarks with `"❗ Remark:"`.

---

## SOCIAL NETWORK RULES:
Only use these platforms:
LinkedIn, GitHub, Twitter, Instagram, Facebook, PersonalWebsite

---

## OUTPUT FORMAT:
- Return valid YAML only (no markdown, no extra text)
- Must begin with `cv:` and follow RenderCV format
- Structurally and syntactically correct YAML (no invalid spacing or missing fields)

---

### CV_TEXT_START
{cv_text}
CV_TEXT_END

### YAML_TEMPLATE_START
{template_yaml}
YAML_TEMPLATE_END

Your task: Convert the CV to professional Indian-standard YAML using the above rules. Enhance phrasing, structure it logically, and insert remarks where content is vague or improvable. Return only the YAML.
"""


# Call Claude Cloud API
api_key = st.secrets["ANTHROPIC_API_KEY"]


client = anthropic.Anthropic(api_key=api_key)
response = client.messages.create(
    model="claude-3-5-haiku-20241022",
    temperature=0.0,
    max_tokens=4000,
    system="You are a precise transformer of CV content into YAML. Output only the final YAML.",
    messages=[{"role": "user", "content": user_prompt}]
)
generated_yaml = response.content[0].text.strip()

# Save output
output_path = Path(r"C:\Users\likit\Desktop\pythonProject\CV_Reader\prototype_3\output\filled.yaml")
output_path.write_text(generated_yaml, encoding="utf-8")
print(f"✅ YAML written to {output_path}")

# Run rendercv
try:
    subprocess.run(
        ["rendercv", "render", str(output_path)],
        check=True
    )
    print("✅ RenderCV command executed successfully.")
except subprocess.CalledProcessError as e:
    print("❌ RenderCV failed:", e)
