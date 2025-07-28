import json
import anthropic
from pathlib import Path
from datetime import datetime
from typing import Tuple, Dict, Any

class JDKeywordExtractor:
    """
    Simple Job Description Keyword Extractor
    Just applies the jd_extractor.txt prompt to job description and saves as JSON
    """
    
    def __init__(self, prompts_dir: str = "../prompt", output_dir: str = "../output"):
        """Initialize with directory paths"""
        script_dir = Path(__file__).parent
        self.prompts_dir = script_dir / prompts_dir
        self.output_dir = script_dir / output_dir
        self.client = None
        
        # Ensure directories exist
        self.prompts_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
    
    def setup_ai_client(self, api_key: str) -> bool:
        """Setup Anthropic AI client"""
        try:
            self.client = anthropic.Anthropic(api_key=api_key)
            return True
        except Exception:
            return False
    
    def extract_keywords(self, job_description: str, api_key: str) -> Tuple[bool, str]:
        """
        Extract keywords from job description using jd_extractor.txt prompt
        
        Args:
            job_description: The job description text
            api_key: Anthropic API key
            
        Returns:
            Tuple of (success: bool, result_message: str)
        """
        try:
            # Setup AI client
            if not self.setup_ai_client(api_key):
                return False, "Failed to setup AI client"
            
            # Load prompt template
            prompt_file = self.prompts_dir / "jd_extractor.txt"
            if not prompt_file.exists():
                return False, f"Prompt file not found: {prompt_file}"
            
            with open(prompt_file, 'r', encoding='utf-8') as f:
                prompt_template = f.read()
            
            # Replace placeholder with job description
            final_prompt = prompt_template.replace("[INSERT_JOB_DESCRIPTION]", job_description)
            
            # Call Claude Haiku 3.5
            response = self.client.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=2000,
                temperature=0.1,
                system="You are an expert at extracting keywords from job descriptions. Output only valid JSON with no additional text.",
                messages=[{"role": "user", "content": final_prompt}]
            )
            
            # Get response text
            response_text = response.content[0].text.strip()
            
            # Clean up potential markdown formatting
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            elif response_text.startswith("```"):
                response_text = response_text.replace("```", "").strip()
            
            # Parse JSON
            try:
                extracted_data = json.loads(response_text)
            except json.JSONDecodeError:
                # If parsing fails, save raw response
                extracted_data = {
                    "error": "Failed to parse JSON",
                    "raw_response": response_text
                }
            
            # Save to jd_extracted.json
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = "jd_extracted.json"
            output_path = self.output_dir / filename
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(extracted_data, f, indent=2, ensure_ascii=False)
            
            return True, str(output_path)
            
        except Exception as e:
            return False, f"Error: {str(e)}"


# Simple function for direct integration
def extract_jd_keywords(job_description: str, api_key: str) -> Tuple[bool, str]:
    """
    Simple function to extract keywords from job description
    
    Args:
        job_description: Job description text
        api_key: Anthropic API key
        
    Returns:
        Tuple of (success: bool, result_message: str)
    """
    extractor = JDKeywordExtractor()
    return extractor.extract_keywords(job_description, api_key)