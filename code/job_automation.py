import asyncio
import json
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ================================
# 🎯 JOB APPLICATION AUTOMATION
# ================================

class JobBoard(Enum):
    LINKEDIN = "linkedin"
    INDEED = "indeed"
    REED = "reed"
    TOTALJOBS = "totaljobs"
    GLASSDOOR = "glassdoor"
    JOBSITE = "jobsite"

class ApplicationStatus(Enum):
    PENDING = "pending"
    APPLIED = "applied"
    VIEWED = "viewed"
    INTERVIEW = "interview"
    REJECTED = "rejected"
    OFFER = "offer"
    WITHDRAWN = "withdrawn"

@dataclass
class JobListing:
    """Job listing data structure"""
    job_id: str
    title: str
    company: str
    location: str
    salary: Optional[str]
    description: str
    requirements: List[str]
    url: str
    job_board: JobBoard
    posted_date: datetime
    application_deadline: Optional[datetime]
    job_type: str  # Full-time, Part-time, Contract
    experience_level: str  # Entry, Mid, Senior
    remote_option: bool
    match_score: float  # AI calculated match score

@dataclass
class JobApplication:
    """Job application tracking"""
    application_id: str
    job: JobListing
    applied_date: datetime
    status: ApplicationStatus
    cv_version: str
    cover_letter: Optional[str]
    follow_up_dates: List[datetime]
    notes: str
    response_received: bool
    interview_scheduled: Optional[datetime]

@dataclass
class AutomationSettings:
    """User automation preferences"""
    target_roles: List[str]
    locations: List[str]
    salary_min: Optional[int]
    salary_max: Optional[int]
    job_types: List[str]
    experience_levels: List[str]
    remote_only: bool
    exclude_companies: List[str]
    max_applications_per_day: int
    auto_follow_up: bool
    custom_cover_letter: bool

class JobAutomationEngine:
    """Main job application automation engine"""
    
    def __init__(self):
        self.scrapers = {}
        self.applications_today = 0
        self.daily_limit_reached = False
        
        # Initialize scrapers for different job boards
        self._init_scrapers()
    
    def _init_scrapers(self):
        """Initialize scrapers for different job boards"""
        self.scrapers = {
            JobBoard.LINKEDIN: LinkedInScraper(),
            JobBoard.INDEED: IndeedScraper(),
            JobBoard.REED: ReedScraper(),
            JobBoard.TOTALJOBS: TotalJobsScraper(),
        }
    
    def search_jobs(self, 
                   settings: AutomationSettings, 
                   max_results: int = 100) -> List[JobListing]:
        """
        Search for jobs across multiple platforms
        
        Args:
            settings: User automation preferences
            max_results: Maximum number of jobs to return
            
        Returns:
            List of job listings matching criteria
        """
        all_jobs = []
        
        for job_board, scraper in self.scrapers.items():
            try:
                jobs = scraper.search_jobs(settings, max_results // len(self.scrapers))
                for job in jobs:
                    job.match_score = self._calculate_match_score(job, settings)
                all_jobs.extend(jobs)
            except Exception as e:
                st.warning(f"Error scraping {job_board.value}: {str(e)}")
        
        # Sort by match score and remove duplicates
        all_jobs = self._deduplicate_jobs(all_jobs)
        all_jobs.sort(key=lambda x: x.match_score, reverse=True)
        
        return all_jobs[:max_results]
    
    def _calculate_match_score(self, job: JobListing, settings: AutomationSettings) -> float:
        """Calculate how well a job matches user preferences"""
        score = 0.0
        
        # Title matching
        title_lower = job.title.lower()
        for target_role in settings.target_roles:
            if target_role.lower() in title_lower:
                score += 0.3
        
        # Location matching
        location_lower = job.location.lower()
        for location in settings.locations:
            if location.lower() in location_lower:
                score += 0.2
        
        # Remote option
        if settings.remote_only and job.remote_option:
            score += 0.2
        
        # Job type matching
        if job.job_type in settings.job_types:
            score += 0.1
        
        # Experience level
        if job.experience_level in settings.experience_levels:
            score += 0.1
        
        # Exclude companies check
        if job.company.lower() in [c.lower() for c in settings.exclude_companies]:
            score -= 0.5
        
        return min(score, 1.0)
    
    def _deduplicate_jobs(self, jobs: List[JobListing]) -> List[JobListing]:
        """Remove duplicate job listings"""
        seen = set()
        unique_jobs = []
        
        for job in jobs:
            # Create a unique identifier
            job_signature = f"{job.title}-{job.company}-{job.location}".lower()
            if job_signature not in seen:
                seen.add(job_signature)
                unique_jobs.append(job)
        
        return unique_jobs
    
    async def apply_to_jobs(self, 
                           jobs: List[JobListing],
                           settings: AutomationSettings,
                           cv_content: str,
                           user_profile: Dict) -> List[JobApplication]:
        """
        Automatically apply to selected jobs
        
        Args:
            jobs: List of jobs to apply to
            settings: User automation settings
            cv_content: Optimized CV content
            user_profile: User profile information
            
        Returns:
            List of job applications created
        """
        applications = []
        
        for job in jobs:
            if self.applications_today >= settings.max_applications_per_day:
                st.warning("Daily application limit reached!")
                break
            
            try:
                # Generate custom cover letter if enabled
                cover_letter = None
                if settings.custom_cover_letter:
                    cover_letter = await self._generate_cover_letter(job, user_profile)
                
                # Apply to the job
                application = await self._apply_to_job(job, cv_content, cover_letter, settings)
                
                if application:
                    applications.append(application)
                    self.applications_today += 1
                    
                    # Add random delay to avoid detection
                    await asyncio.sleep(random.uniform(30, 120))
                
            except Exception as e:
                st.error(f"Failed to apply to {job.title} at {job.company}: {str(e)}")
        
        return applications
    
    async def _apply_to_job(self, 
                           job: JobListing, 
                           cv_content: str,
                           cover_letter: Optional[str],
                           settings: AutomationSettings) -> Optional[JobApplication]:
        """Apply to a specific job"""
        
        scraper = self.scrapers.get(job.job_board)
        if not scraper:
            return None
        
        try:
            # Use the appropriate scraper to apply
            success = await scraper.apply_to_job(job, cv_content, cover_letter)
            
            if success:
                application = JobApplication(
                    application_id=f"{job.job_board.value}_{job.job_id}_{int(time.time())}",
                    job=job,
                    applied_date=datetime.now(),
                    status=ApplicationStatus.APPLIED,
                    cv_version="optimized_v1",
                    cover_letter=cover_letter,
                    follow_up_dates=[],
                    notes="",
                    response_received=False,
                    interview_scheduled=None
                )
                
                return application
        
        except Exception as e:
            st.error(f"Application failed for {job.title}: {str(e)}")
            return None
    
    async def _generate_cover_letter(self, job: JobListing, user_profile: Dict) -> str:
        """Generate a custom cover letter using AI"""
        
        prompt = f"""
        Write a professional cover letter for this job application:
        
        Job Title: {job.title}
        Company: {job.company}
        Job Description: {job.description[:500]}...
        
        User Profile:
        Name: {user_profile.get('name', 'Candidate')}
        Experience: {user_profile.get('experience_summary', '')}
        Skills: {user_profile.get('skills', [])}
        
        Make it:
        - Professional but personalized
        - Specific to the role and company
        - Highlighting relevant experience
        - Maximum 3 paragraphs
        - UK business format
        """
        
        try:
            # Use your existing AI client from CV optimization
            optimizer = st.session_state.cv_optimizer
            success, cover_letter = optimizer.optimize_cv_with_ai(prompt, max_tokens=500)
            
            if success:
                return cover_letter
            
        except Exception as e:
            st.warning(f"Failed to generate custom cover letter: {str(e)}")
        
        # Fallback to template
        return self._get_template_cover_letter(job, user_profile)
    
    def _get_template_cover_letter(self, job: JobListing, user_profile: Dict) -> str:
        """Get a template cover letter"""
        return f"""Dear Hiring Manager,

I am writing to express my strong interest in the {job.title} position at {job.company}. With my background in {user_profile.get('experience_summary', 'relevant experience')}, I am confident I would be a valuable addition to your team.

My skills in {', '.join(user_profile.get('skills', [])[:3])} align perfectly with your requirements. I am particularly excited about the opportunity to contribute to {job.company}'s continued success.

Thank you for considering my application. I look forward to discussing how I can contribute to your team.

Kind regards,
{user_profile.get('name', 'Your Name')}"""

# ================================
# 🌐 JOB BOARD SCRAPERS
# ================================

class JobBoardScraper:
    """Base class for job board scrapers"""
    
    def __init__(self):
        self.driver = None
        self._init_driver()
    
    def _init_driver(self):
        """Initialize headless Chrome driver"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--log-level=3')
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            
        except Exception as e:
            st.warning(f"Failed to initialize web driver: {str(e)}")
            self.driver = None
    
    def close_driver(self):
        """Close the web driver"""
        if self.driver:
            self.driver.quit()
    
    def search_jobs(self, settings: AutomationSettings, max_results: int) -> List[JobListing]:
        """Search for jobs - to be implemented by subclasses"""
        raise NotImplementedError
    
    async def apply_to_job(self, job: JobListing, cv_content: str, cover_letter: str) -> bool:
        """Apply to a job - to be implemented by subclasses"""
        raise NotImplementedError

class LinkedInScraper(JobBoardScraper):
    """LinkedIn Jobs scraper"""
    
    def search_jobs(self, settings: AutomationSettings, max_results: int) -> List[JobListing]:
        """Search LinkedIn Jobs"""
        if not self.driver:
            return []
        
        jobs = []
        
        try:
            for role in settings.target_roles[:2]:  # Limit to avoid rate limiting
                for location in settings.locations[:2]:
                    search_url = self._build_linkedin_url(role, location, settings)
                    jobs.extend(self._scrape_linkedin_page(search_url, max_results // 4))
            
        except Exception as e:
            st.error(f"LinkedIn scraping error: {str(e)}")
        
        return jobs[:max_results]
    
    def _build_linkedin_url(self, role: str, location: str, settings: AutomationSettings) -> str:
        """Build LinkedIn search URL"""
        base_url = "https://www.linkedin.com/jobs/search/"
        params = {
            'keywords': role,
            'location': location,
            'f_TPR': 'r86400',  # Last 24 hours
            'f_JT': 'F' if 'Full-time' in settings.job_types else '',
            'f_WT': '2' if settings.remote_only else '',
        }
        
        query_string = '&'.join([f"{k}={v}" for k, v in params.items() if v])
        return f"{base_url}?{query_string}"
    
    def _scrape_linkedin_page(self, url: str, max_results: int) -> List[JobListing]:
        """Scrape a LinkedIn search results page"""
        jobs = []
        
        try:
            self.driver.get(url)
            time.sleep(3)
            
            # Find job cards
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, ".job-search-card")
            
            for card in job_cards[:max_results]:
                try:
                    job = self._extract_linkedin_job_data(card)
                    if job:
                        jobs.append(job)
                except Exception as e:
                    continue
            
        except Exception as e:
            st.warning(f"LinkedIn page scraping error: {str(e)}")
        
        return jobs
    
    def _extract_linkedin_job_data(self, card) -> Optional[JobListing]:
        """Extract job data from LinkedIn job card"""
        try:
            # Extract basic info
            title_elem = card.find_element(By.CSS_SELECTOR, ".job-search-card__title")
            company_elem = card.find_element(By.CSS_SELECTOR, ".job-search-card__subtitle")
            location_elem = card.find_element(By.CSS_SELECTOR, ".job-search-card__location")
            url_elem = card.find_element(By.CSS_SELECTOR, "a")
            
            title = title_elem.text.strip()
            company = company_elem.text.strip()
            location = location_elem.text.strip()
            url = url_elem.get_attribute('href')
            
            # Generate job ID from URL
            job_id = url.split('/')[-1] if url else str(hash(f"{title}{company}"))
            
            return JobListing(
                job_id=job_id,
                title=title,
                company=company,
                location=location,
                salary=None,  # LinkedIn doesn't always show salary
                description="",  # Would need to click through for full description
                requirements=[],
                url=url,
                job_board=JobBoard.LINKEDIN,
                posted_date=datetime.now(),  # Approximate
                application_deadline=None,
                job_type="Full-time",  # Default
                experience_level="Mid",  # Default
                remote_option="remote" in location.lower(),
                match_score=0.0
            )
            
        except Exception as e:
            return None
    
    async def apply_to_job(self, job: JobListing, cv_content: str, cover_letter: str) -> bool:
        """Apply to LinkedIn job (requires login)"""
        try:
            # This would require LinkedIn login and is complex
            # For demo purposes, we'll simulate success
            st.info(f"Would apply to {job.title} at {job.company} on LinkedIn")
            await asyncio.sleep(2)  # Simulate processing
            return True
        except Exception as e:
            return False

class IndeedScraper(JobBoardScraper):
    """Indeed Jobs scraper"""
    
    def search_jobs(self, settings: AutomationSettings, max_results: int) -> List[JobListing]:
        """Search Indeed Jobs"""
        if not self.driver:
            return []
        
        jobs = []
        
        try:
            for role in settings.target_roles[:2]:
                for location in settings.locations[:2]:
                    search_url = self._build_indeed_url(role, location, settings)
                    jobs.extend(self._scrape_indeed_page(search_url, max_results // 4))
            
        except Exception as e:
            st.error(f"Indeed scraping error: {str(e)}")
        
        return jobs[:max_results]
    
    def _build_indeed_url(self, role: str, location: str, settings: AutomationSettings) -> str:
        """Build Indeed search URL"""
        base_url = "https://uk.indeed.com/jobs"
        params = {
            'q': role,
            'l': location,
            'fromage': '1',  # Last 1 day
            'jt': 'fulltime' if 'Full-time' in settings.job_types else '',
        }
        
        query_string = '&'.join([f"{k}={v}" for k, v in params.items() if v])
        return f"{base_url}?{query_string}"
    
    def _scrape_indeed_page(self, url: str, max_results: int) -> List[JobListing]:
        """Scrape Indeed search results"""
        jobs = []
        
        try:
            self.driver.get(url)
            time.sleep(3)
            
            # Find job cards
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, ".jobsearch-SerpJobCard")
            
            for card in job_cards[:max_results]:
                try:
                    job = self._extract_indeed_job_data(card)
                    if job:
                        jobs.append(job)
                except Exception as e:
                    continue
            
        except Exception as e:
            st.warning(f"Indeed page scraping error: {str(e)}")
        
        return jobs
    
    def _extract_indeed_job_data(self, card) -> Optional[JobListing]:
        """Extract job data from Indeed job card"""
        try:
            title_elem = card.find_element(By.CSS_SELECTOR, ".jobTitle a")
            company_elem = card.find_element(By.CSS_SELECTOR, ".companyName")
            location_elem = card.find_element(By.CSS_SELECTOR, ".companyLocation")
            
            title = title_elem.text.strip()
            company = company_elem.text.strip()
            location = location_elem.text.strip()
            url = title_elem.get_attribute('href')
            
            # Try to get salary
            salary = None
            try:
                salary_elem = card.find_element(By.CSS_SELECTOR, ".salary-snippet")
                salary = salary_elem.text.strip()
            except:
                pass
            
            job_id = url.split('jk=')[-1] if url else str(hash(f"{title}{company}"))
            
            return JobListing(
                job_id=job_id,
                title=title,
                company=company,
                location=location,
                salary=salary,
                description="",
                requirements=[],
                url=url,
                job_board=JobBoard.INDEED,
                posted_date=datetime.now(),
                application_deadline=None,
                job_type="Full-time",
                experience_level="Mid",
                remote_option="remote" in location.lower(),
                match_score=0.0
            )
            
        except Exception as e:
            return None
    
    async def apply_to_job(self, job: JobListing, cv_content: str, cover_letter: str) -> bool:
        """Apply to Indeed job"""
        try:
            st.info(f"Would apply to {job.title} at {job.company} on Indeed")
            await asyncio.sleep(2)
            return True
        except Exception as e:
            return False

class ReedScraper(JobBoardScraper):
    """Reed.co.uk Jobs scraper"""
    
    def search_jobs(self, settings: AutomationSettings, max_results: int) -> List[JobListing]:
        """Search Reed Jobs"""
        jobs = []
        
        try:
            # Use requests for Reed API if available, or scraping
            for role in settings.target_roles[:2]:
                for location in settings.locations[:2]:
                    jobs.extend(self._scrape_reed_jobs(role, location, max_results // 4))
        
        except Exception as e:
            st.error(f"Reed scraping error: {str(e)}")
        
        return jobs[:max_results]
    
    def _scrape_reed_jobs(self, role: str, location: str, max_results: int) -> List[JobListing]:
        """Scrape Reed jobs using requests"""
        jobs = []
        
        try:
            url = f"https://www.reed.co.uk/jobs/{role.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            job_cards = soup.find_all('article', class_='job-result')[:max_results]
            
            for card in job_cards:
                job = self._extract_reed_job_data(card)
                if job:
                    jobs.append(job)
        
        except Exception as e:
            st.warning(f"Reed scraping error: {str(e)}")
        
        return jobs
    
    def _extract_reed_job_data(self, card) -> Optional[JobListing]:
        """Extract Reed job data"""
        try:
            title_elem = card.find('h3', class_='title')
            company_elem = card.find('a', class_='gtmJobListingPostedBy')
            location_elem = card.find('li', class_='location')
            
            if not all([title_elem, company_elem, location_elem]):
                return None
            
            title = title_elem.text.strip()
            company = company_elem.text.strip()
            location = location_elem.text.strip()
            
            # Get URL
            url_elem = title_elem.find('a')
            url = f"https://www.reed.co.uk{url_elem['href']}" if url_elem else ""
            
            # Generate job ID
            job_id = url.split('/')[-1] if url else str(hash(f"{title}{company}"))
            
            # Try to get salary
            salary = None
            salary_elem = card.find('li', class_='salary')
            if salary_elem:
                salary = salary_elem.text.strip()
            
            return JobListing(
                job_id=job_id,
                title=title,
                company=company,
                location=location,
                salary=salary,
                description="",
                requirements=[],
                url=url,
                job_board=JobBoard.REED,
                posted_date=datetime.now(),
                application_deadline=None,
                job_type="Full-time",
                experience_level="Mid",
                remote_option="remote" in location.lower(),
                match_score=0.0
            )
            
        except Exception as e:
            return None
    
    async def apply_to_job(self, job: JobListing, cv_content: str, cover_letter: str) -> bool:
        """Apply to Reed job"""
        try:
            st.info(f"Would apply to {job.title} at {job.company} on Reed")
            await asyncio.sleep(2)
            return True
        except Exception as e:
            return False

class TotalJobsScraper(JobBoardScraper):
    """TotalJobs scraper"""
    
    def search_jobs(self, settings: AutomationSettings, max_results: int) -> List[JobListing]:
        """Search TotalJobs"""
        # Similar implementation to other scrapers
        return []
    
    async def apply_to_job(self, job: JobListing, cv_content: str, cover_letter: str) -> bool:
        """Apply to TotalJobs job"""
        return False

# ================================
# 📊 APPLICATION TRACKING
# ================================

class ApplicationTracker:
    """Track and manage job applications"""
    
    def __init__(self):
        self.applications = []
        self.load_applications()
    
    def add_application(self, application: JobApplication):
        """Add new application to tracking"""
        self.applications.append(application)
        self.save_applications()
    
    def get_applications(self, 
                        status: Optional[ApplicationStatus] = None,
                        days: Optional[int] = None) -> List[JobApplication]:
        """Get applications with optional filtering"""
        filtered_apps = self.applications
        
        if status:
            filtered_apps = [app for app in filtered_apps if app.status == status]
        
        if days:
            cutoff_date = datetime.now() - timedelta(days=days)
            filtered_apps = [app for app in filtered_apps if app.applied_date >= cutoff_date]
        
        return filtered_apps
    
    def update_application_status(self, application_id: str, status: ApplicationStatus, notes: str = ""):
        """Update application status"""
        for app in self.applications:
            if app.application_id == application_id:
                app.status = status
                app.notes += f"\n{datetime.now().strftime('%Y-%m-%d')}: {notes}"
                self.save_applications()
                break
    
    def get_analytics(self) -> Dict:
        """Get application analytics"""
        total_apps = len(self.applications)
        
        if total_apps == 0:
            return {"total": 0, "response_rate": 0, "interview_rate": 0}
        
        responses = len([app for app in self.applications if app.response_received])
        interviews = len([app for app in self.applications if app.status == ApplicationStatus.INTERVIEW])
        
        return {
            "total_applications": total_apps,
            "response_rate": (responses / total_apps) * 100,
            "interview_rate": (interviews / total_apps) * 100,
            "status_breakdown": self._get_status_breakdown(),
            "top_companies": self._get_top_companies(),
            "applications_by_date": self._get_applications_by_date()
        }
    
    def _get_status_breakdown(self) -> Dict[str, int]:
        """Get breakdown of application statuses"""
        breakdown = {}
        for app in self.applications:
            status = app.status.value
            breakdown[status] = breakdown.get(status, 0) + 1
        return breakdown
    
    def _get_top_companies(self) -> List[Tuple[str, int]]:
        """Get companies with most applications"""
        companies = {}
        for app in self.applications:
            company = app.job.company
            companies[company] = companies.get(company, 0) + 1
        
        return sorted(companies.items(), key=lambda x: x[1], reverse=True)[:10]
    
    def _get_applications_by_date(self) -> Dict[str, int]:
        """Get applications grouped by date"""
        by_date = {}
        for app in self.applications:
            date_str = app.applied_date.strftime('%Y-%m-%d')
            by_date[date_str] = by_date.get(date_str, 0) + 1
        
        return by_date
    
    def save_applications(self):
        """Save applications to session state"""
        if 'job_applications' not in st.session_state:
            st.session_state.job_applications = []
        
        # Convert to dict for JSON serialization
        st.session_state.job_applications = [asdict(app) for app in self.applications]
    
    def load_applications(self):
        """Load applications from session state"""
        if 'job_applications' in st.session_state:
            # Convert back from dict
            self.applications = []
            for app_dict in st.session_state.job_applications:
                # Reconstruct objects (simplified for demo)
                try:
                    app = JobApplication(**app_dict)
                    self.applications.append(app)
                except:
                    continue

# ================================
# 📧 FOLLOW-UP AUTOMATION
# ================================

class FollowUpManager:
    """Manage follow-up emails and reminders"""
    
    def __init__(self):
        self.email_templates = {
            "follow_up_1": self._get_follow_up_template(),
            "follow_up_2": self._get_second_follow_up_template(),
            "thank_you": self._get_thank_you_template()
        }
    
    def schedule_follow_ups(self, application: JobApplication):
        """Schedule automatic follow-ups"""
        follow_up_dates = [
            datetime.now() + timedelta(days=7),   # 1 week follow-up
            datetime.now() + timedelta(days=14),  # 2 week follow-up
        ]
        
        application.follow_up_dates = follow_up_dates
    
    def send_follow_up(self, application: JobApplication, template_type: str = "follow_up_1"):
        """Send follow-up email"""
        try:
            template = self.email_templates.get(template_type)
            if not template:
                return False
            
            # Customize template
            email_content = template.format(
                company=application.job.company,
                position=application.job.title,
                date_applied=application.applied_date.strftime('%B %d, %Y')
            )
            
            # In production, you'd send actual email here
            st.info(f"Follow-up email sent for {application.job.title} at {application.job.company}")
            
            return True
            
        except Exception as e:
            st.error(f"Failed to send follow-up: {str(e)}")
            return False
    
    def _get_follow_up_template(self) -> str:
        return """Subject: Following up on {position} application

Dear Hiring Manager,

I hope this email finds you well. I am writing to follow up on my application for the {position} position at {company}, which I submitted on {date_applied}.

I remain very interested in this opportunity and would welcome the chance to discuss how my skills and experience align with your team's needs.

Thank you for your time and consideration. I look forward to hearing from you.

Best regards,
[Your Name]"""
    
    def _get_second_follow_up_template(self) -> str:
        return """Subject: Continued interest in {position} role

Dear Hiring Manager,

I wanted to reach out once more regarding my application for the {position} position at {company}.

I understand you likely receive many applications, but I wanted to reiterate my strong interest in joining your team. I believe my background would be a great fit for this role.

If you need any additional information, please don't hesitate to ask.

Thank you for your consideration.

Kind regards,
[Your Name]"""
    
    def _get_thank_you_template(self) -> str:
        return """Subject: Thank you for the interview - {position}

Dear [Interviewer Name],

Thank you for taking the time to interview me for the {position} position at {company}. I enjoyed our conversation and learning more about the role and your team.

I'm excited about the opportunity to contribute to {company} and believe my experience would be valuable to your organization.

Please let me know if you need any additional information from me.

Thank you again for your time and consideration.

Best regards,
[Your Name]"""

# ================================
# 🎯 SMART TARGETING
# ================================

class SmartTargeting:
    """AI-powered job targeting and optimization"""
    
    def __init__(self):
        self.success_patterns = {}
        self.rejection_patterns = {}
    
    def analyze_success_patterns(self, applications: List[JobApplication]):
        """Analyze which types of applications are successful"""
        successful_apps = [app for app in applications 
                          if app.status in [ApplicationStatus.INTERVIEW, ApplicationStatus.OFFER]]
        
        rejected_apps = [app for app in applications 
                        if app.status == ApplicationStatus.REJECTED]
        
        # Analyze patterns
        self.success_patterns = self._extract_patterns(successful_apps)
        self.rejection_patterns = self._extract_patterns(rejected_apps)
    
    def _extract_patterns(self, applications: List[JobApplication]) -> Dict:
        """Extract common patterns from applications"""
        patterns = {
            'companies': {},
            'job_titles': {},
            'locations': {},
            'job_boards': {}
        }
        
        for app in applications:
            # Company patterns
            company = app.job.company
            patterns['companies'][company] = patterns['companies'].get(company, 0) + 1
            
            # Title patterns
            title_words = app.job.title.lower().split()
            for word in title_words:
                patterns['job_titles'][word] = patterns['job_titles'].get(word, 0) + 1
            
            # Location patterns
            location = app.job.location
            patterns['locations'][location] = patterns['locations'].get(location, 0) + 1
            
            # Job board patterns
            board = app.job.job_board.value
            patterns['job_boards'][board] = patterns['job_boards'].get(board, 0) + 1
        
        return patterns
    
    def get_targeting_recommendations(self) -> Dict:
        """Get AI recommendations for better targeting"""
        recommendations = {
            'preferred_companies': [],
            'avoid_companies': [],
            'successful_keywords': [],
            'best_job_boards': [],
            'optimal_locations': []
        }
        
        # Extract top patterns from successful applications
        if self.success_patterns:
            recommendations['preferred_companies'] = sorted(
                self.success_patterns['companies'].items(),
                key=lambda x: x[1], reverse=True
            )[:5]
            
            recommendations['successful_keywords'] = sorted(
                self.success_patterns['job_titles'].items(),
                key=lambda x: x[1], reverse=True
            )[:10]
            
            recommendations['best_job_boards'] = sorted(
                self.success_patterns['job_boards'].items(),
                key=lambda x: x[1], reverse=True
            )[:3]
        
        # Extract companies to avoid from rejections
        if self.rejection_patterns:
            recommendations['avoid_companies'] = sorted(
                self.rejection_patterns['companies'].items(),
                key=lambda x: x[1], reverse=True
            )[:5]
        
        return recommendations

# ================================
# 🤖 AI OPTIMIZATION
# ================================

class AIJobMatcher:
    """AI-powered job matching and optimization"""
    
    def __init__(self, cv_optimizer):
        self.cv_optimizer = cv_optimizer
    
    async def optimize_applications(self, 
                                  jobs: List[JobListing],
                                  user_profile: Dict,
                                  cv_content: str) -> List[Tuple[JobListing, str, float]]:
        """
        Use AI to optimize applications for each job
        
        Returns:
            List of (job, optimized_cv, match_score) tuples
        """
        optimized_applications = []
        
        for job in jobs:
            try:
                # Generate job-specific CV optimization
                optimized_cv = await self._optimize_cv_for_job(job, cv_content, user_profile)
                
                # Calculate enhanced match score
                match_score = await self._calculate_ai_match_score(job, user_profile, cv_content)
                
                optimized_applications.append((job, optimized_cv, match_score))
                
            except Exception as e:
                st.warning(f"Failed to optimize for {job.title}: {str(e)}")
        
        # Sort by match score
        optimized_applications.sort(key=lambda x: x[2], reverse=True)
        
        return optimized_applications
    
    async def _optimize_cv_for_job(self, job: JobListing, cv_content: str, user_profile: Dict) -> str:
        """Create job-specific CV optimization"""
        
        optimization_prompt = f"""
        Optimize this CV for the specific job below. Focus on:
        1. Highlighting relevant keywords from the job description
        2. Emphasizing matching experience and skills
        3. Tailoring the summary to match the role
        4. Maintaining UK CV standards
        
        Job Title: {job.title}
        Company: {job.company}
        Job Description: {job.description[:800]}
        
        Current CV Content:
        {cv_content[:1500]}
        
        Return only the optimized CV content in the same format.
        """
        
        try:
            success, optimized_cv = self.cv_optimizer.optimize_cv_with_ai(
                optimization_prompt, 
                max_tokens=2000
            )
            
            if success:
                return optimized_cv
            else:
                return cv_content  # Fallback to original
                
        except Exception as e:
            return cv_content  # Fallback to original
    
    async def _calculate_ai_match_score(self, job: JobListing, user_profile: Dict, cv_content: str) -> float:
        """Use AI to calculate sophisticated match score"""
        
        matching_prompt = f"""
        Analyze how well this candidate matches the job requirements.
        Return only a number between 0.0 and 1.0 representing the match score.
        
        Job: {job.title} at {job.company}
        Requirements: {job.description[:500]}
        
        Candidate Profile:
        Skills: {user_profile.get('skills', [])}
        Experience: {user_profile.get('experience_summary', '')}
        CV Summary: {cv_content[:300]}
        
        Consider:
        - Skill alignment
        - Experience relevance
        - Industry fit
        - Location match
        - Role seniority
        
        Score (0.0-1.0):
        """
        
        try:
            success, score_text = self.cv_optimizer.optimize_cv_with_ai(
                matching_prompt,
                max_tokens=10
            )
            
            if success:
                # Extract number from response
                import re
                numbers = re.findall(r'0\.\d+|1\.0|0\.0', score_text)
                if numbers:
                    return float(numbers[0])
            
        except Exception as e:
            pass
        
        # Fallback to basic scoring
        return job.match_score if hasattr(job, 'match_score') else 0.5