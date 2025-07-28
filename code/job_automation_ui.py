# job_automation_ui.py
"""
Streamlit UI components for job application automation
"""

import asyncio
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time

from job_automation import (
    JobAutomationEngine,
    ApplicationTracker,
    FollowUpManager,
    SmartTargeting,
    AIJobMatcher,
    AutomationSettings,
    JobBoard,
    ApplicationStatus,
    JobListing,
    JobApplication
)
from payment_processor import PlanType

# ================================
# 🎯 JOB AUTOMATION UI COMPONENTS
# ================================

class JobAutomationUI:
    """Streamlit UI for job automation features"""
    
    def __init__(self):
        self.automation_engine = JobAutomationEngine()
        self.tracker = ApplicationTracker()
        self.follow_up_manager = FollowUpManager()
        self.smart_targeting = SmartTargeting()
        
        # Initialize session state
        self._init_session_state()
    
    def _init_session_state(self):
        """Initialize automation-specific session state"""
        if 'automation_active' not in st.session_state:
            st.session_state.automation_active = False
        
        if 'job_search_results' not in st.session_state:
            st.session_state.job_search_results = []
        
        if 'automation_settings' not in st.session_state:
            st.session_state.automation_settings = None
        
        if 'selected_jobs' not in st.session_state:
            st.session_state.selected_jobs = []
    
    def render_automation_dashboard(self):
        """Render the main automation dashboard"""
        
        # Check subscription access
        if not self._check_automation_access():
            return
        
        st.markdown("""
        <div class="section-card">
            <div class="section-header">
                <div class="section-title">
                    🤖 Job Application Automation
                </div>
                <div class="section-subtitle">
                    Automatically find and apply to jobs that match your profile
                </div>
            </div>
            <div class="section-content">
        """, unsafe_allow_html=True)
        
        # Dashboard tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🎯 Setup", "📊 Dashboard", "🔍 Job Search", "📋 Applications", "⚙️ Settings"
        ])
        
        with tab1:
            self._render_automation_setup()
        
        with tab2:
            self._render_automation_dashboard()
        
        with tab3:
            self._render_job_search()
        
        with tab4:
            self._render_application_tracking()
        
        with tab5:
            self._render_automation_settings()
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    def _check_automation_access(self) -> bool:
        """Check if user has access to automation features"""
        user_plan = st.session_state.subscription_manager.get_user_plan()
        
        if user_plan == PlanType.FREE:
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, var(--primary-glow), var(--bg-secondary));
                border: 2px solid var(--primary);
                padding: var(--space-8);
                border-radius: var(--radius-xl);
                text-align: center;
                margin: var(--space-6) 0;
            ">
                <div style="font-size: 3rem; margin-bottom: var(--space-4);">🤖</div>
                <h3 style="color: var(--text-primary); margin-bottom: var(--space-3);">
                    Unlock Job Application Automation
                </h3>
                <p style="color: var(--text-secondary); margin-bottom: var(--space-5); font-size: 1.125rem;">
                    Automatically apply to hundreds of relevant jobs with AI-optimized applications
                </p>
                
                <div style="
                    background: var(--bg-primary);
                    padding: var(--space-5);
                    border-radius: var(--radius-lg);
                    margin-bottom: var(--space-5);
                ">
                    <h4 style="color: var(--text-primary); margin-bottom: var(--space-3);">Automation Features:</h4>
                    <ul style="color: var(--text-secondary); text-align: left; max-width: 500px; margin: 0 auto;">
                        <li>🔍 Smart job discovery across multiple platforms</li>
                        <li>🎯 AI-powered job matching and filtering</li>
                        <li>📝 Custom cover letter generation</li>
                        <li>⚡ Bulk application submission</li>
                        <li>📊 Application tracking and analytics</li>
                        <li>📧 Automated follow-up emails</li>
                        <li>🧠 Machine learning optimization</li>
                    </ul>
                </div>
                
                <div style="display: flex; gap: var(--space-4); justify-content: center;">
                    <div style="
                        background: var(--bg-tertiary);
                        padding: var(--space-4);
                        border-radius: var(--radius-lg);
                        border: 1px solid var(--border-light);
                    ">
                        <strong style="color: var(--primary);">Pro Plan</strong><br>
                        <span style="color: var(--text-secondary); font-size: 0.875rem;">
                            50 applications/day
                        </span>
                    </div>
                    <div style="
                        background: var(--bg-tertiary);
                        padding: var(--space-4);
                        border-radius: var(--radius-lg);
                        border: 1px solid var(--border-light);
                    ">
                        <strong style="color: var(--accent);">Enterprise</strong><br>
                        <span style="color: var(--text-secondary); font-size: 0.875rem;">
                            Unlimited applications
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("🚀 Upgrade to Unlock Automation", type="primary", use_container_width=True):
                    st.session_state.active_nav = 'Pricing'
                    st.rerun()
            
            return False
        
        return True
    
    def _render_automation_setup(self):
        """Render automation setup wizard"""
        st.markdown("### 🎯 Automation Setup")
        
        # Check if CV is optimized
        if not st.session_state.get('optimized_cv'):
            st.warning("⚠️ Please optimize your CV first before setting up automation")
            if st.button("🔙 Go to CV Optimization"):
                st.session_state.active_nav = 'Home'
                st.rerun()
            return
        
        # Step 1: Target Roles
        st.markdown("#### 1. Target Job Roles")
        target_roles = st.multiselect(
            "What roles are you looking for?",
            options=[
                "Software Developer", "Data Scientist", "Product Manager",
                "Marketing Manager", "Sales Representative", "Business Analyst",
                "DevOps Engineer", "UX Designer", "Project Manager",
                "Financial Analyst", "HR Manager", "Operations Manager"
            ],
            default=st.session_state.get('target_roles', []),
            help="Select all relevant job titles you're interested in"
        )
        st.session_state.target_roles = target_roles
        
        # Step 2: Locations
        st.markdown("#### 2. Target Locations")
        locations = st.multiselect(
            "Where do you want to work?",
            options=[
                "London", "Manchester", "Birmingham", "Edinburgh", "Glasgow",
                "Bristol", "Leeds", "Liverpool", "Newcastle", "Remote"
            ],
            default=st.session_state.get('target_locations', ['London']),
            help="Select preferred work locations"
        )
        st.session_state.target_locations = locations
        
        # Step 3: Job Preferences
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 3. Job Preferences")
            job_types = st.multiselect(
                "Job Types",
                options=["Full-time", "Part-time", "Contract", "Freelance"],
                default=["Full-time"]
            )
            
            experience_levels = st.multiselect(
                "Experience Levels",
                options=["Entry", "Mid", "Senior", "Executive"],
                default=["Mid"]
            )
            
            remote_only = st.checkbox("Remote jobs only", value=False)
        
        with col2:
            st.markdown("#### 4. Salary Expectations")
            salary_min = st.number_input("Minimum Salary (£)", min_value=0, value=30000, step=5000)
            salary_max = st.number_input("Maximum Salary (£)", min_value=0, value=80000, step=5000)
            
            st.markdown("#### 5. Daily Limits")
            user_plan = st.session_state.subscription_manager.get_user_plan()
            
            if user_plan == PlanType.PRO:
                max_daily = 50
            elif user_plan == PlanType.ENTERPRISE:
                max_daily = 200
            else:
                max_daily = 5
            
            daily_limit = st.slider(
                "Applications per day",
                min_value=1,
                max_value=max_daily,
                value=min(10, max_daily),
                help=f"Your {user_plan.value.title()} plan allows up to {max_daily} applications per day"
            )
        
        # Step 6: Company Exclusions
        st.markdown("#### 6. Company Exclusions (Optional)")
        exclude_companies = st.text_area(
            "Companies to avoid (one per line)",
            placeholder="Enter company names you don't want to apply to...",
            help="List companies where you don't want to apply"
        )
        
        excluded_list = [company.strip() for company in exclude_companies.split('\n') if company.strip()]
        
        # Step 7: Advanced Settings
        with st.expander("🔧 Advanced Settings"):
            auto_follow_up = st.checkbox("Enable automatic follow-up emails", value=True)
            custom_cover_letter = st.checkbox("Generate custom cover letters", value=True)
            
            job_boards = st.multiselect(
                "Job Boards to Search",
                options=["LinkedIn", "Indeed", "Reed", "TotalJobs", "Glassdoor"],
                default=["LinkedIn", "Indeed", "Reed"]
            )
        
        # Save Settings
        if st.button("💾 Save Automation Settings", type="primary"):
            settings = AutomationSettings(
                target_roles=target_roles,
                locations=locations,
                salary_min=salary_min if salary_min > 0 else None,
                salary_max=salary_max if salary_max > 0 else None,
                job_types=job_types,
                experience_levels=experience_levels,
                remote_only=remote_only,
                exclude_companies=excluded_list,
                max_applications_per_day=daily_limit,
                auto_follow_up=auto_follow_up,
                custom_cover_letter=custom_cover_letter
            )
            
            st.session_state.automation_settings = settings
            st.success("✅ Automation settings saved!")
            
            # Validation
            if not target_roles:
                st.error("❌ Please select at least one target role")
            elif not locations:
                st.error("❌ Please select at least one location")
            else:
                st.info("🎯 Ready to start job automation! Go to the Job Search tab.")
    
    def _render_automation_dashboard(self):
        """Render automation dashboard with analytics"""
        st.markdown("### 📊 Automation Dashboard")
        
        # Get analytics
        analytics = self.tracker.get_analytics()
        
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Applications",
                analytics.get('total_applications', 0),
                delta="+12 this week" if analytics.get('total_applications', 0) > 0 else None
            )
        
        with col2:
            response_rate = analytics.get('response_rate', 0)
            st.metric(
                "Response Rate",
                f"{response_rate:.1f}%",
                delta=f"+{response_rate-15:.1f}%" if response_rate > 15 else f"{response_rate-15:.1f}%"
            )
        
        with col3:
            interview_rate = analytics.get('interview_rate', 0)
            st.metric(
                "Interview Rate",
                f"{interview_rate:.1f}%",
                delta=f"+{interview_rate-8:.1f}%" if interview_rate > 8 else f"{interview_rate-8:.1f}%"
            )
        
        with col4:
            today_count = len([app for app in self.tracker.get_applications(days=1)])
            st.metric(
                "Applied Today",
                today_count,
                delta=f"Limit: {st.session_state.automation_settings.max_applications_per_day if st.session_state.automation_settings else 'Not set'}"
            )
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Application Status Pie Chart
            status_breakdown = analytics.get('status_breakdown', {})
            if status_breakdown:
                fig = px.pie(
                    values=list(status_breakdown.values()),
                    names=list(status_breakdown.keys()),
                    title="Application Status Breakdown"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Applications Over Time
            apps_by_date = analytics.get('applications_by_date', {})
            if apps_by_date:
                dates = list(apps_by_date.keys())
                counts = list(apps_by_date.values())
                
                fig = px.line(
                    x=dates,
                    y=counts,
                    title="Applications Over Time"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Recent Activity
        st.markdown("### 📈 Recent Activity")
        recent_apps = self.tracker.get_applications(days=7)
        
        if recent_apps:
            activity_data = []
            for app in recent_apps[-10:]:  # Show last 10
                activity_data.append({
                    "Date": app.applied_date.strftime('%Y-%m-%d'),
                    "Company": app.job.company,
                    "Role": app.job.title,
                    "Status": app.status.value.title(),
                    "Job Board": app.job.job_board.value.title()
                })
            
            df = pd.DataFrame(activity_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No recent applications found. Start your automation to see activity here!")
        
        # Quick Actions
        st.markdown("### ⚡ Quick Actions")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🔍 Search New Jobs", use_container_width=True):
                st.session_state.active_tab = "🔍 Job Search"
                st.rerun()
        
        with col2:
            if st.button("📧 Send Follow-ups", use_container_width=True):
                self._send_follow_ups()
        
        with col3:
            if st.button("📊 Export Data", use_container_width=True):
                self._export_application_data()
        
        with col4:
            automation_status = "🟢 Active" if st.session_state.automation_active else "🔴 Inactive"
            if st.button(f"Automation: {automation_status}", use_container_width=True):
                st.session_state.automation_active = not st.session_state.automation_active
                st.rerun()
    
    def _render_job_search(self):
        """Render job search and application interface"""
        st.markdown("### 🔍 Smart Job Search")
        
        if not st.session_state.automation_settings:
            st.warning("⚠️ Please configure your automation settings first!")
            return
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### Search Configuration")
            
            # Override search parameters
            search_roles = st.multiselect(
                "Override target roles (optional)",
                options=st.session_state.automation_settings.target_roles,
                help="Leave empty to use all configured roles"
            )
            
            search_locations = st.multiselect(
                "Override locations (optional)",
                options=st.session_state.automation_settings.locations,
                help="Leave empty to use all configured locations"
            )
            
            max_results = st.slider("Maximum jobs to find", 10, 200, 50)
        
        with col2:
            st.markdown("#### Search Status")
            
            if st.session_state.job_search_results:
                st.success(f"✅ Found {len(st.session_state.job_search_results)} jobs")
            else:
                st.info("🔍 Click 'Search Jobs' to find opportunities")
            
            # Search button
            if st.button("🚀 Search Jobs", type="primary", use_container_width=True):
                self._run_job_search(search_roles, search_locations, max_results)
        
        # Display search results
        if st.session_state.job_search_results:
            self._display_job_results()
    
    def _run_job_search(self, override_roles: List[str], override_locations: List[str], max_results: int):
        """Execute job search"""
        settings = st.session_state.automation_settings
        
        # Use overrides if provided
        if override_roles:
            settings.target_roles = override_roles
        if override_locations:
            settings.locations = override_locations
        
        with st.spinner("🔍 Searching for jobs across multiple platforms..."):
            try:
                # Run job search
                jobs = self.automation_engine.search_jobs(settings, max_results)
                
                # Use AI to enhance job matching if available
                if st.session_state.get('cv_optimizer'):
                    ai_matcher = AIJobMatcher(st.session_state.cv_optimizer)
                    
                    # Get user profile
                    user_profile = {
                        'name': 'User',  # Would get from actual profile
                        'skills': ['Python', 'Data Analysis'],  # Would extract from CV
                        'experience_summary': 'Experienced professional'  # Would extract from CV
                    }
                    
                    # This would be async in real implementation
                    # For demo, just sort by existing match score
                    jobs.sort(key=lambda x: x.match_score, reverse=True)
                
                st.session_state.job_search_results = jobs
                
                if jobs:
                    st.success(f"✅ Found {len(jobs)} relevant job opportunities!")
                else:
                    st.warning("⚠️ No jobs found matching your criteria. Try adjusting your settings.")
                    
            except Exception as e:
                st.error(f"❌ Job search failed: {str(e)}")
    
    def _display_job_results(self):
        """Display job search results with application options"""
        st.markdown("### 📋 Job Search Results")
        
        jobs = st.session_state.job_search_results
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            min_match_score = st.slider("Minimum Match Score", 0.0, 1.0, 0.5, 0.1)
        
        with col2:
            company_filter = st.selectbox(
                "Filter by Company",
                options=["All"] + list(set([job.company for job in jobs])),
                index=0
            )
        
        with col3:
            location_filter = st.selectbox(
                "Filter by Location",
                options=["All"] + list(set([job.location for job in jobs])),
                index=0
            )
        
        # Apply filters
        filtered_jobs = jobs
        filtered_jobs = [job for job in filtered_jobs if job.match_score >= min_match_score]
        
        if company_filter != "All":
            filtered_jobs = [job for job in filtered_jobs if job.company == company_filter]
        
        if location_filter != "All":
            filtered_jobs = [job for job in filtered_jobs if job.location == location_filter]
        
        st.write(f"Showing {len(filtered_jobs)} of {len(jobs)} jobs")
        
        # Bulk actions
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✅ Select All High Matches (>0.7)", use_container_width=True):
                st.session_state.selected_jobs = [
                    job for job in filtered_jobs if job.match_score > 0.7
                ]
                st.rerun()
        
        with col2:
            if st.button("🚀 Apply to Selected Jobs", type="primary", use_container_width=True):
                if st.session_state.selected_jobs:
                    self._bulk_apply_jobs()
                else:
                    st.warning("No jobs selected!")
        
        with col3:
            selected_count = len(st.session_state.selected_jobs)
            st.metric("Selected Jobs", selected_count)
        
        # Job cards
        for i, job in enumerate(filtered_jobs):
            self._render_job_card(job, i)
    
    def _render_job_card(self, job: JobListing, index: int):
        """Render individual job card"""
        
        # Match score color
        if job.match_score >= 0.8:
            score_color = "var(--success)"
        elif job.match_score >= 0.6:
            score_color = "var(--warning)"
        else:
            score_color = "var(--danger)"
        
        # Check if job is selected
        is_selected = job in st.session_state.selected_jobs
        card_border = "2px solid var(--primary)" if is_selected else "1px solid var(--border-light)"
        
        st.markdown(f"""
        <div style="
            background: var(--bg-secondary);
            border: {card_border};
            border-radius: var(--radius-lg);
            padding: var(--space-5);
            margin-bottom: var(--space-4);
            transition: all 0.2s ease;
        ">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: var(--space-3);">
                <div>
                    <h4 style="color: var(--text-primary); margin-bottom: var(--space-2);">
                        {job.title} at {job.company}
                    </h4>
                    <p style="color: var(--text-secondary); margin: 0;">
                        📍 {job.location} • 🏢 {job.job_board.value.title()} • 
                        {job.posted_date.strftime('%Y-%m-%d') if job.posted_date else 'Recently posted'}
                    </p>
                </div>
                <div style="text-align: center;">
                    <div style="
                        background: {score_color};
                        color: white;
                        padding: var(--space-2) var(--space-3);
                        border-radius: var(--radius-full);
                        font-size: 0.875rem;
                        font-weight: 600;
                    ">
                        {job.match_score:.0%} Match
                    </div>
                </div>
            </div>
            
            <div style="margin-bottom: var(--space-3);">
                <p style="color: var(--text-secondary); font-size: 0.875rem; margin: 0;">
                    {job.description[:200] if job.description else 'No description available'}...
                </p>
            </div>
            
            <div style="display: flex; gap: var(--space-2); margin-bottom: var(--space-3);">
                <span style="
                    background: var(--bg-primary);
                    color: var(--text-secondary);
                    padding: var(--space-1) var(--space-3);
                    border-radius: var(--radius-full);
                    font-size: 0.75rem;
                ">
                    {job.job_type}
                </span>
                <span style="
                    background: var(--bg-primary);
                    color: var(--text-secondary);
                    padding: var(--space-1) var(--space-3);
                    border-radius: var(--radius-full);
                    font-size: 0.75rem;
                ">
                    {job.experience_level}
                </span>
                {f'<span style="background: var(--success-glow); color: var(--success); padding: var(--space-1) var(--space-3); border-radius: var(--radius-full); font-size: 0.75rem;">Remote</span>' if job.remote_option else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("👁️ View Details", key=f"view_{index}", use_container_width=True):
                self._show_job_details(job)
        
        with col2:
            select_text = "✅ Selected" if is_selected else "➕ Select"
            if st.button(select_text, key=f"select_{index}", use_container_width=True):
                if is_selected:
                    st.session_state.selected_jobs.remove(job)
                else:
                    st.session_state.selected_jobs.append(job)
                st.rerun()
        
        with col3:
            if st.button("🚀 Apply Now", key=f"apply_{index}", type="primary", use_container_width=True):
                self._apply_to_single_job(job)
        
        with col4:
            if st.button("🔗 Open Job", key=f"open_{index}", use_container_width=True):
                st.markdown(f'<a href="{job.url}" target="_blank">Open in new tab</a>', unsafe_allow_html=True)
    
    def _show_job_details(self, job: JobListing):
        """Show detailed job information in modal"""
        with st.expander(f"📋 {job.title} at {job.company} - Full Details", expanded=True):
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                **Company:** {job.company}  
                **Location:** {job.location}  
                **Job Type:** {job.job_type}  
                **Experience:** {job.experience_level}  
                **Remote:** {'Yes' if job.remote_option else 'No'}
                """)
            
            with col2:
                st.markdown(f"""
                **Job Board:** {job.job_board.value.title()}  
                **Posted:** {job.posted_date.strftime('%Y-%m-%d') if job.posted_date else 'Unknown'}  
                **Salary:** {job.salary if job.salary else 'Not specified'}  
                **Match Score:** {job.match_score:.0%}
                """)
            
            st.markdown("**Full Description:**")
            st.markdown(job.description if job.description else "No detailed description available.")
            
            if job.requirements:
                st.markdown("**Requirements:**")
                for req in job.requirements:
                    st.markdown(f"• {req}")
            
            st.markdown(f"**Apply directly:** [View on {job.job_board.value.title()}]({job.url})")
    
    def _bulk_apply_jobs(self):
        """Apply to multiple selected jobs"""
        selected_jobs = st.session_state.selected_jobs
        
        if not selected_jobs:
            st.warning("No jobs selected for application!")
            return
        
        # Check daily limits
        settings = st.session_state.automation_settings
        applications_today = len(self.tracker.get_applications(days=1))
        
        remaining_today = settings.max_applications_per_day - applications_today
        
        if remaining_today <= 0:
            st.error(f"❌ Daily application limit reached ({settings.max_applications_per_day})")
            return
        
        jobs_to_apply = selected_jobs[:remaining_today]
        
        if len(selected_jobs) > remaining_today:
            st.warning(f"⚠️ Can only apply to {remaining_today} more jobs today. {len(selected_jobs) - remaining_today} jobs will be skipped.")
        
        # Get user profile and CV
        cv_content = st.session_state.get('optimized_cv', '')
        if not cv_content:
            st.error("❌ No optimized CV found! Please optimize your CV first.")
            return
        
        user_profile = {
            'name': 'User Name',
            'email': 'user@email.com',
            'skills': ['Python', 'Data Analysis', 'Project Management'],
            'experience_summary': 'Experienced professional with strong background'
        }
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        successful_applications = 0
        failed_applications = 0
        
        for i, job in enumerate(jobs_to_apply):
            try:
                status_text.text(f"Applying to {job.title} at {job.company}...")
                
                # Simulate application process
                time.sleep(2)  # Realistic delay
                
                # Create application record
                application = JobApplication(
                    application_id=f"app_{int(time.time())}_{i}",
                    job=job,
                    applied_date=datetime.now(),
                    status=ApplicationStatus.APPLIED,
                    cv_version="optimized_v1",
                    cover_letter="Generated cover letter" if settings.custom_cover_letter else None,
                    follow_up_dates=[],
                    notes=f"Applied via automation on {datetime.now().strftime('%Y-%m-%d')}",
                    response_received=False,
                    interview_scheduled=None
                )
                
                # Add to tracker
                self.tracker.add_application(application)
                
                # Schedule follow-ups if enabled
                if settings.auto_follow_up:
                    self.follow_up_manager.schedule_follow_ups(application)
                
                successful_applications += 1
                
            except Exception as e:
                st.error(f"❌ Failed to apply to {job.title}: {str(e)}")
                failed_applications += 1
            
            # Update progress
            progress = (i + 1) / len(jobs_to_apply)
            progress_bar.progress(progress)
        
        # Clear progress
        progress_bar.empty()
        status_text.empty()
        
        # Show results
        if successful_applications > 0:
            st.success(f"✅ Successfully applied to {successful_applications} jobs!")
            st.balloons()
        
        if failed_applications > 0:
            st.warning(f"⚠️ {failed_applications} applications failed")
        
        # Clear selected jobs
        st.session_state.selected_jobs = []
        
        # Update automation metrics
        st.session_state.applications_sent_today = applications_today + successful_applications
    
    def _apply_to_single_job(self, job: JobListing):
        """Apply to a single job"""
        st.session_state.selected_jobs = [job]
        self._bulk_apply_jobs()
    
    def _render_application_tracking(self):
        """Render application tracking interface"""
        st.markdown("### 📋 Application Tracking")
        
        applications = self.tracker.get_applications()
        
        if not applications:
            st.info("No applications tracked yet. Start applying to jobs to see them here!")
            return
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status_filter = st.selectbox(
                "Filter by Status",
                options=["All"] + [status.value.title() for status in ApplicationStatus],
                index=0
            )
        
        with col2:
            days_filter = st.selectbox(
                "Time Period",
                options=["All Time", "Last 7 days", "Last 30 days", "Last 90 days"],
                index=1
            )
        
        with col3:
            sort_by = st.selectbox(
                "Sort by",
                options=["Date Applied", "Company", "Status", "Job Title"],
                index=0
            )
        
        # Apply filters
        filtered_apps = applications
        
        if status_filter != "All":
            status_enum = ApplicationStatus(status_filter.lower())
            filtered_apps = [app for app in filtered_apps if app.status == status_enum]
        
        if days_filter != "All Time":
            days_map = {"Last 7 days": 7, "Last 30 days": 30, "Last 90 days": 90}
            days = days_map[days_filter]
            cutoff_date = datetime.now() - timedelta(days=days)
            filtered_apps = [app for app in filtered_apps if app.applied_date >= cutoff_date]
        
        # Sort applications
        if sort_by == "Date Applied":
            filtered_apps.sort(key=lambda x: x.applied_date, reverse=True)
        elif sort_by == "Company":
            filtered_apps.sort(key=lambda x: x.job.company)
        elif sort_by == "Status":
            filtered_apps.sort(key=lambda x: x.status.value)
        elif sort_by == "Job Title":
            filtered_apps.sort(key=lambda x: x.job.title)
        
        st.write(f"Showing {len(filtered_apps)} applications")
        
        # Applications list
        for app in filtered_apps:
            self._render_application_card(app)
    
    def _render_application_card(self, app: JobApplication):
        """Render individual application card"""
        
        # Status colors
        status_colors = {
            ApplicationStatus.PENDING: "var(--neutral-500)",
            ApplicationStatus.APPLIED: "var(--info)",
            ApplicationStatus.VIEWED: "var(--warning)",
            ApplicationStatus.INTERVIEW: "var(--success)",
            ApplicationStatus.REJECTED: "var(--danger)",
            ApplicationStatus.OFFER: "var(--success)",
            ApplicationStatus.WITHDRAWN: "var(--neutral-400)"
        }
        
        status_color = status_colors.get(app.status, "var(--neutral-500)")
        
        st.markdown(f"""
        <div style="
            background: var(--bg-secondary);
            border: 1px solid var(--border-light);
            border-radius: var(--radius-lg);
            padding: var(--space-5);
            margin-bottom: var(--space-4);
        ">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: var(--space-3);">
                <div>
                    <h4 style="color: var(--text-primary); margin-bottom: var(--space-2);">
                        {app.job.title} at {app.job.company}
                    </h4>
                    <p style="color: var(--text-secondary); margin: 0; font-size: 0.875rem;">
                        📍 {app.job.location} • 📅 Applied: {app.applied_date.strftime('%Y-%m-%d')} • 
                        🌐 {app.job.job_board.value.title()}
                    </p>
                </div>
                <div style="
                    background: {status_color};
                    color: white;
                    padding: var(--space-2) var(--space-3);
                    border-radius: var(--radius-full);
                    font-size: 0.875rem;
                    font-weight: 600;
                ">
                    {app.status.value.title()}
                </div>
            </div>
            
            {f'<p style="color: var(--text-secondary); font-size: 0.875rem; margin-bottom: var(--space-3);"><strong>Notes:</strong> {app.notes}</p>' if app.notes.strip() else ''}
            
            <div style="display: flex; gap: var(--space-2);">
                <span style="
                    background: var(--bg-primary);
                    color: var(--text-secondary);
                    padding: var(--space-1) var(--space-3);
                    border-radius: var(--radius-full);
                    font-size: 0.75rem;
                ">
                    CV: {app.cv_version}
                </span>
                {f'<span style="background: var(--success-glow); color: var(--success); padding: var(--space-1) var(--space-3); border-radius: var(--radius-full); font-size: 0.75rem;">Cover Letter</span>' if app.cover_letter else ''}
                {f'<span style="background: var(--warning-glow); color: var(--warning); padding: var(--space-1) var(--space-3); border-radius: var(--radius-full); font-size: 0.75rem;">Follow-up Scheduled</span>' if app.follow_up_dates else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("✏️ Update Status", key=f"update_{app.application_id}"):
                self._update_application_status(app)
        
        with col2:
            if st.button("📧 Send Follow-up", key=f"follow_{app.application_id}"):
                self._send_follow_up(app)
        
        with col3:
            if st.button("📝 Add Notes", key=f"notes_{app.application_id}"):
                self._add_application_notes(app)
        
        with col4:
            if st.button("🔗 View Job", key=f"job_{app.application_id}"):
                st.markdown(f'<a href="{app.job.url}" target="_blank">Open job posting</a>', unsafe_allow_html=True)
    
    def _update_application_status(self, app: JobApplication):
        """Update application status"""
        with st.form(f"status_update_{app.application_id}"):
            st.markdown(f"**Update Status for {app.job.title} at {app.job.company}**")
            
            new_status = st.selectbox(
                "New Status",
                options=[status.value.title() for status in ApplicationStatus],
                index=[status.value for status in ApplicationStatus].index(app.status.value)
            )
            
            notes = st.text_area("Additional Notes", placeholder="Add any notes about this update...")
            
            if st.form_submit_button("Update Status"):
                status_enum = ApplicationStatus(new_status.lower())
                self.tracker.update_application_status(app.application_id, status_enum, notes)
                st.success("✅ Status updated!")
                st.rerun()
    
    def _send_follow_up(self, app: JobApplication):
        """Send follow-up email for application"""
        success = self.follow_up_manager.send_follow_up(app, "follow_up_1")
        if success:
            st.success(f"✅ Follow-up sent for {app.job.title}!")
        else:
            st.error("❌ Failed to send follow-up")
    
    def _add_application_notes(self, app: JobApplication):
        """Add notes to application"""
        with st.form(f"notes_{app.application_id}"):
            st.markdown(f"**Add Notes for {app.job.title} at {app.job.company}**")
            
            new_notes = st.text_area("Notes", placeholder="Add your notes here...")
            
            if st.form_submit_button("Add Notes"):
                self.tracker.update_application_status(
                    app.application_id, 
                    app.status, 
                    new_notes
                )
                st.success("✅ Notes added!")
                st.rerun()
    
    def _render_automation_settings(self):
        """Render automation settings and controls"""
        st.markdown("### ⚙️ Automation Settings")
        
        if not st.session_state.automation_settings:
            st.warning("⚠️ No automation settings configured. Please complete the setup first!")
            return
        
        settings = st.session_state.automation_settings
        
        # Current settings display
        with st.expander("📋 Current Settings", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                **Target Roles:** {', '.join(settings.target_roles)}  
                **Locations:** {', '.join(settings.locations)}  
                **Job Types:** {', '.join(settings.job_types)}  
                **Experience Levels:** {', '.join(settings.experience_levels)}
                """)
            
            with col2:
                st.markdown(f"""
                **Salary Range:** £{settings.salary_min or 0:,} - £{settings.salary_max or 0:,}  
                **Daily Limit:** {settings.max_applications_per_day} applications  
                **Remote Only:** {'Yes' if settings.remote_only else 'No'}  
                **Auto Follow-up:** {'Enabled' if settings.auto_follow_up else 'Disabled'}
                """)
        
        # Automation Controls
        st.markdown("### 🎛️ Automation Controls")
        
        col1, col2 = st.columns(2)
        
        with col1:
            automation_status = st.session_state.automation_active
            status_text = "🟢 Active" if automation_status else "🔴 Inactive"
            
            st.markdown(f"**Current Status:** {status_text}")
            
            if st.button("🔄 Toggle Automation", type="primary", use_container_width=True):
                st.session_state.automation_active = not automation_status
                new_status = "activated" if not automation_status else "deactivated"
                st.success(f"✅ Automation {new_status}!")
                st.rerun()
        
        with col2:
            st.markdown("**Today's Progress:**")
            applications_today = len(self.tracker.get_applications(days=1))
            progress = applications_today / settings.max_applications_per_day
            st.progress(progress)
            st.text(f"{applications_today}/{settings.max_applications_per_day} applications sent")
        
        # Advanced Controls
        st.markdown("### 🔧 Advanced Controls")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Export Applications", use_container_width=True):
                self._export_application_data()
        
        with col2:
            if st.button("🗑️ Clear Application History", use_container_width=True):
                if st.confirm("Are you sure you want to clear all application history?"):
                    st.session_state.job_applications = []
                    self.tracker.applications = []
                    st.success("✅ Application history cleared!")
                    st.rerun()
        
        with col3:
            if st.button("🔄 Reset Settings", use_container_width=True):
                if st.confirm("Are you sure you want to reset all automation settings?"):
                    st.session_state.automation_settings = None
                    st.session_state.automation_active = False
                    st.success("✅ Settings reset!")
                    st.rerun()
        
        # AI Recommendations
        if len(self.tracker.applications) >= 10:  # Only show if enough data
            st.markdown("### 🧠 AI Recommendations")
            
            self.smart_targeting.analyze_success_patterns(self.tracker.applications)
            recommendations = self.smart_targeting.get_targeting_recommendations()
            
            if recommendations['successful_keywords']:
                st.markdown("**Successful Keywords in Job Titles:**")
                keywords = [kw[0] for kw in recommendations['successful_keywords'][:5]]
                st.info(f"Consider targeting roles with: {', '.join(keywords)}")
            
            if recommendations['best_job_boards']:
                st.markdown("**Best Performing Job Boards:**")
                boards = [board[0] for board in recommendations['best_job_boards'][:3]]
                st.info(f"Focus your search on: {', '.join(boards)}")
    
    def _send_follow_ups(self):
        """Send follow-up emails for applications"""
        applications = self.tracker.get_applications()
        
        # Find applications that need follow-up
        follow_up_needed = []
        for app in applications:
            if app.status == ApplicationStatus.APPLIED:
                days_since_applied = (datetime.now() - app.applied_date).days
                if days_since_applied >= 7 and not app.follow_up_dates:
                    follow_up_needed.append(app)
        
        if not follow_up_needed:
            st.info("No applications need follow-up at this time.")
            return
        
        st.info(f"Sending follow-up emails for {len(follow_up_needed)} applications...")
        
        success_count = 0
        for app in follow_up_needed:
            if self.follow_up_manager.send_follow_up(app):
                success_count += 1
        
        st.success(f"✅ Sent {success_count} follow-up emails!")
    
    def _export_application_data(self):
        """Export application data as CSV"""
        applications = self.tracker.get_applications()
        
        if not applications:
            st.warning("No application data to export!")
            return
        
        # Prepare data for export
        export_data = []
        for app in applications:
            export_data.append({
                'Application Date': app.applied_date.strftime('%Y-%m-%d'),
                'Company': app.job.company,
                'Job Title': app.job.title,
                'Location': app.job.location,
                'Status': app.status.value.title(),
                'Job Board': app.job.job_board.value.title(),
                'Salary': app.job.salary or 'Not specified',
                'Job Type': app.job.job_type,
                'Remote': 'Yes' if app.job.remote_option else 'No',
                'Response Received': 'Yes' if app.response_received else 'No',
                'Notes': app.notes,
                'Job URL': app.job.url
            })
        
        df = pd.DataFrame(export_data)
        csv = df.to_csv(index=False)
        
        st.download_button(
            label="📥 Download Application Data",
            data=csv,
            file_name=f"job_applications_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

# ================================
# 🔗 INTEGRATION WITH MAIN APP
# ================================

def add_job_automation_to_main_app():
    """Add job automation as a new page to the main app"""
    
    # Add to navigation items in main app
    nav_items = {
        'Home': '🏠',
        'Automation': '🤖',  # NEW
        'About': '📘', 
        'Help': '❓',
        'Pricing': '💰',
        'My Account': '👤'
    }
    
    # In main app routing:
    """
    elif active_page == "Automation":
        job_automation_ui = JobAutomationUI()
        job_automation_ui.render_automation_dashboard()
    """

def render_automation_teaser():
    """Show automation teaser for free users on home page"""
    user_plan = st.session_state.subscription_manager.get_user_plan()
    
    if user_plan == PlanType.FREE:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, var(--primary-glow), var(--bg-secondary));
            border: 1px solid var(--primary);
            border-radius: var(--radius-xl);
            padding: var(--space-6);
            margin: var(--space-6) 0;
            text-align: center;
        ">
            <div style="font-size: 2rem; margin-bottom: var(--space-3);">🤖</div>
            <h4 style="color: var(--text-primary); margin-bottom: var(--space-3);">
                Automate Your Job Search
            </h4>
            <p style="color: var(--text-secondary); margin-bottom: var(--space-4);">
                Let AI apply to hundreds of relevant jobs while you focus on interviews
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🚀 Unlock Automation", type="primary", use_container_width=True):
                st.session_state.active_nav = 'Pricing'
                st.rerun()