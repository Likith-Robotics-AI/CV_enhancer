# fixed_reed_scraper.py
"""
Fixed and simplified Reed job scraper that actually works
Focus on Reed.co.uk since it's responding with jobs
"""

import requests
from bs4 import BeautifulSoup
import time
import random
from dataclasses import dataclass
from typing import List, Optional
import urllib.parse

@dataclass
class SimpleJob:
    title: str
    company: str
    location: str
    salary: str
    description: str
    url: str
    source: str

class WorkingReedScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-GB,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })
    
    def analyze_reed_structure(self, url: str):
        """Analyze Reed's HTML structure to find job selectors"""
        print(f"\n🔍 ANALYZING Reed structure at: {url}")
        
        try:
            response = self.session.get(url, timeout=15)
            print(f"📊 Response: {response.status_code}")
            
            if response.status_code != 200:
                return
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            print(f"\n📈 Page Statistics:")
            print(f"   - Page title: {soup.title.string if soup.title else 'No title'}")
            print(f"   - Total articles: {len(soup.find_all('article'))}")
            print(f"   - Total divs: {len(soup.find_all('div'))}")
            print(f"   - Total job-related links: {len([a for a in soup.find_all('a') if 'job' in a.get('href', '').lower()])}")
            
            print(f"\n🔍 Looking for job containers...")
            
            # Look for job-related elements
            potential_job_containers = []
            
            # Check articles (most likely)
            articles = soup.find_all('article')
            if articles:
                print(f"📋 Found {len(articles)} <article> tags")
                for i, article in enumerate(articles[:3]):  # Check first 3
                    classes = article.get('class', [])
                    id_attr = article.get('id', '')
                    print(f"   Article {i+1}: classes={classes}, id={id_attr}")
                    
                    # Look for job titles in this article
                    title_links = article.find_all('a', href=True)
                    for link in title_links:
                        href = link.get('href', '')
                        text = link.get_text(strip=True)
                        if 'job' in href and len(text) > 10 and 'python' in text.lower():
                            print(f"   🎯 FOUND JOB LINK: '{text}' -> {href}")
                            potential_job_containers.append(article)
                            break
            
            # Check divs with job-related classes
            print(f"\n🔍 Checking divs with job-related classes...")
            job_divs = soup.find_all('div', class_=lambda x: x and any(keyword in str(x).lower() for keyword in ['job', 'result', 'card', 'listing']))
            if job_divs:
                print(f"📋 Found {len(job_divs)} divs with job-related classes")
                for i, div in enumerate(job_divs[:3]):
                    classes = div.get('class', [])
                    print(f"   Div {i+1}: classes={classes}")
            
            # Look for specific patterns in HTML
            print(f"\n🔍 Looking for Reed-specific patterns...")
            
            # Check for data attributes
            data_elements = soup.find_all(attrs={'data-id': True}) or soup.find_all(attrs={'data-job-id': True})
            if data_elements:
                print(f"📋 Found {len(data_elements)} elements with data-id/data-job-id")
            
            # Check for common Reed classes
            reed_classes = [
                'job-result', 'job-card', 'job-listing', 'search-result',
                'vacancy', 'position', 'role-card', 'listing-item'
            ]
            
            for class_name in reed_classes:
                elements = soup.find_all(class_=class_name) or soup.find_all(class_=lambda x: x and class_name in str(x))
                if elements:
                    print(f"✅ Found {len(elements)} elements with class containing '{class_name}'")
                    # Show first element structure
                    first = elements[0]
                    print(f"   First element: {first.name}, classes={first.get('class', [])}")
            
            return soup
            
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            return None
    
    def extract_jobs_from_soup(self, soup: BeautifulSoup, max_jobs: int = 10) -> List[SimpleJob]:
        """Try to extract jobs using multiple strategies"""
        jobs = []
        
        print(f"\n🎯 Attempting job extraction...")
        
        # Strategy 1: Look for articles (most likely)
        print("📋 Strategy 1: Checking <article> tags...")
        articles = soup.find_all('article')
        for i, article in enumerate(articles[:max_jobs]):
            try:
                job = self.extract_job_from_element(article, f"article-{i}")
                if job and job.title != "Unknown Title":
                    jobs.append(job)
                    print(f"✅ Extracted from article {i+1}: {job.title}")
                    if len(jobs) >= max_jobs:
                        break
            except Exception as e:
                print(f"❌ Error extracting from article {i+1}: {e}")
        
        # Strategy 2: Look for divs with links that contain "job"
        if len(jobs) < max_jobs:
            print(f"📋 Strategy 2: Looking for job links...")
            job_links = soup.find_all('a', href=lambda x: x and 'job' in x)
            processed_titles = set()
            
            for link in job_links[:max_jobs*2]:  # Check more links
                try:
                    text = link.get_text(strip=True)
                    href = link.get('href')
                    
                    # Skip if too short or already processed
                    if len(text) < 10 or text in processed_titles:
                        continue
                    
                    processed_titles.add(text)
                    
                    # Find parent container for more info
                    parent = link.find_parent(['article', 'div'])
                    if parent:
                        job = self.extract_job_from_element(parent, f"link-parent", known_title=text, known_url=href)
                        if job:
                            jobs.append(job)
                            print(f"✅ Extracted from link parent: {job.title}")
                            if len(jobs) >= max_jobs:
                                break
                
                except Exception as e:
                    continue
        
        return jobs
    
    def extract_job_from_element(self, element, debug_id: str, known_title: str = None, known_url: str = None) -> Optional[SimpleJob]:
        """Extract job info from any HTML element"""
        try:
            # Get title
            title = known_title or "Unknown Title"
            if not known_title:
                title_selectors = [
                    'h1', 'h2', 'h3', 'h4',  # Headers
                    'a[href*="job"]',  # Job links
                    '.title', '.job-title', '.position',  # Common classes
                    'a'  # Any link
                ]
                
                for selector in title_selectors:
                    elem = element.select_one(selector)
                    if elem:
                        candidate_title = elem.get_text(strip=True)
                        if len(candidate_title) > 5:  # Must be meaningful
                            title = candidate_title
                            break
            
            # Get company
            company = "Unknown Company"
            # Look for text that might be company name
            all_text = element.get_text()
            lines = [line.strip() for line in all_text.split('\n') if line.strip()]
            
            for line in lines:
                # Company names are usually shorter than job titles and don't contain common job words
                if (5 < len(line) < 50 and 
                    not any(word in line.lower() for word in ['developer', 'engineer', 'manager', 'analyst', 'python', 'java', 'senior', 'junior']) and
                    line != title):
                    company = line
                    break
            
            # Get URL
            job_url = known_url or ""
            if not known_url:
                link_elem = element.find('a', href=True)
                if link_elem:
                    href = link_elem.get('href')
                    if href.startswith('/'):
                        job_url = f"https://www.reed.co.uk{href}"
                    else:
                        job_url = href
            elif known_url and known_url.startswith('/'):
                job_url = f"https://www.reed.co.uk{known_url}"
            else:
                job_url = known_url or ""
            
            # Get some description
            description = element.get_text(strip=True)[:200] + "..."
            
            # Only return if we have meaningful data
            if title != "Unknown Title" and len(title) > 5:
                return SimpleJob(
                    title=title,
                    company=company,
                    location="London",  # Default since we searched for London
                    salary="See job posting",
                    description=description,
                    url=job_url,
                    source="Reed"
                )
            
            return None
            
        except Exception as e:
            print(f"❌ Error extracting from {debug_id}: {e}")
            return None
    
    def search_reed_jobs(self, job_title: str, location: str, max_jobs: int = 10) -> List[SimpleJob]:
        """Search Reed with analysis and extraction"""
        print(f"🔍 Reed Search: '{job_title}' in '{location}' (max {max_jobs} jobs)")
        
        # Build URL
        url = f"https://www.reed.co.uk/jobs/{job_title.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}"
        
        # First analyze the structure
        soup = self.analyze_reed_structure(url)
        
        if not soup:
            return []
        
        # Then extract jobs
        jobs = self.extract_jobs_from_soup(soup, max_jobs)
        
        return jobs
    
    def print_jobs(self, jobs: List[SimpleJob]):
        """Print jobs nicely"""
        if not jobs:
            print("\n❌ No jobs extracted!")
            return
        
        print(f"\n🎯 Successfully extracted {len(jobs)} jobs:")
        print("=" * 80)
        
        for i, job in enumerate(jobs, 1):
            print(f"\n📋 Job {i}:")
            print(f"   🏢 Title: {job.title}")
            print(f"   🏭 Company: {job.company}")
            print(f"   📍 Location: {job.location}")
            print(f"   💰 Salary: {job.salary}")
            print(f"   📝 Description: {job.description[:100]}...")
            print(f"   🔗 URL: {job.url}")
            print("-" * 60)

def main():
    print("🎯 Reed Job Scraper - Fixed Version")
    print("=" * 50)
    
    scraper = WorkingReedScraper()
    
    # Test with parameters that we know Reed has
    job_title = "python developer"
    location = "london"
    max_jobs = 5
    
    jobs = scraper.search_reed_jobs(job_title, location, max_jobs)
    scraper.print_jobs(jobs)
    
    print(f"\n🏁 Complete! Found {len(jobs)} jobs from Reed.")

if __name__ == "__main__":
    main()