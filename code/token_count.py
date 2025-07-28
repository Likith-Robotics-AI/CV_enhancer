import anthropic
import PyPDF2
import streamlit as st


api_key = st.secrets["ANTHROPIC_API_KEY"]


client = anthropic.Anthropic(api_key=api_key)

# Load content from your YAML or text file

def output():
    with open(r"C:\Users\likit\Desktop\pythonProject\CV_Reader\prototype_3\output\optimized_cv_professional_20250723_165426.yaml", "r") as f:
        file_content = f.read()

# Send to token counting endpoint
    response = client.messages.count_tokens(
        model="claude-3-5-haiku-20241022",
        messages=[
            {"role": "user", "content": f"Here is the YAML CV:\n```yaml\n{file_content}\n```"}
        ]
    )    
    print(f"Token count: {response.input_tokens}")

def input():
    

    # File paths
    prompt_path = r"C:\Users\likit\Desktop\pythonProject\CV_Reader\prototype_3\prompt\prompt_1.txt"
    yaml_path = r"C:\Users\likit\Desktop\pythonProject\CV_Reader\prototype_3\yaml\professional.yaml"
    cv_pdf_path = r"C:\Users\likit\Desktop\pythonProject\CV_Reader\prototype_3\input\CV_42.pdf"

    # Hardcoded job description (replace as needed)
    job_description = """
Engineered Arts Ltd logo
Engineered Arts Ltd
Share
Show more options
Robotics R&D Software Engineer 
Falmouth, England, United Kingdom · 2 weeks ago · Over 100 applicants
Promoted by hirer · Actively reviewing applicants


 On-site
Matches your job preferences, workplace type is On-site.

 Full-time
Matches your job preferences, job type is Full-time.

Easy Apply

Save
Save Robotics R&D Software Engineer  at Engineered Arts Ltd
How your profile and resume fit this job
Get AI-powered advice on this job and more exclusive features with Premium. Try Premium for £0



Tailor my resume to this job

Am I a good fit for this job?

How can I best position myself for this job?

Meet the hiring team
Hannah Typhair is hiring
Hannah Typhair  
 2nd
Senior Talent Acquisition Specialist at Engineered Arts 🤖
Job poster · 7 mutual connections

Message
About the job
Engineered Arts is the leading manufacturer of full-size humanoid robots used for entertainment, education and communication. With 20 years of hardware and software development, our robots have been sold in over 30 countries worldwide with customers such as NASA, PwC, Meta and many more.


About the Role



The Robotics Software Engineer will be responsible for developing locomotion algorithms and ensuring real-time control stability for dynamic walking robots. This role involves collaboration with other engineers to optimize motion strategies and integrate various sensors for accurate feedback.




Responsibilities



Develop locomotion algorithms - Implement algorithms for gait planning, state estimation, and balance control
Simulation & testing - Validate software using physics-based simulations
Sensor data processing - Utilize IMUs, force sensors, and cameras for robot perception
RTOS integration - Develop software modules for real-time robot control




Required Skills



Strong programming skills in C/C++ and Python
Experience with RTOS (ROS), Gazebo, and real-time locomotion algorithms
Experience with real world hardware
Simulation & real-world testing - Work in both physics-based simulations and real hardware for validation and performance optimization




Our internal motto is ‘Be Wow’, everything we do is fun, entertaining or surprising to encounter. We always push the boundaries of what is possible in humanoid robotics, researching and developing new systems and techniques to further their appeal. We explore and challenge the human perception of robots as well as the fear and discomfort and the excitement and joy life-like mechanical humanoids present.
    """

    # Read YAML template as plain text
    with open(yaml_path, "r", encoding="utf-8") as f:
        yaml_template = f.read()

    # Extract text from CV PDF
    def extract_text_from_pdf(pdf_path):
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())

    cv_text = extract_text_from_pdf(cv_pdf_path)

    # Load and fill the prompt template
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_template = f.read()

    final_prompt = (
        prompt_template
        .replace("[INSERT_TEMPLATE]", yaml_template)
        .replace("[INSERT_CV]", cv_text)
        .replace("[INSERT_JOB_DESCRIPTION]", job_description)
    )

    print(final_prompt)

    # Send to token counting endpoint
    response = client.messages.count_tokens(
        model="claude-3-5-haiku-20241022",
        messages=[
            {"role": "user", "content": f"{final_prompt}"}
        ]
    )    
    print(f"Token count: {response.input_tokens}")

input()



# response = client.messages.create(
#     model="claude-3-5-haiku-20241022",
#     max_tokens=1000,
#     messages=[{"role": "user", "content": "Hello, Claude!"}]
# )

# Token counts are in the usage field



# print(f"Token count: {response['token_count']}")


