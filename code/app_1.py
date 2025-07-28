# streamlit_app.py
import streamlit as st
from job_automation import (
    JobAutomationEngine,
    ApplicationTracker,
    FollowUpManager,
    SmartTargeting,
    AIJobMatcher,
    AutomationSettings,
    JobListing,
    ApplicationStatus
)
import asyncio
from datetime import datetime

# ======================================
# Initialize State
# ======================================
if 'engine' not in st.session_state:
    st.session_state.engine = JobAutomationEngine()

if 'tracker' not in st.session_state:
    st.session_state.tracker = ApplicationTracker()

if 'follow_up' not in st.session_state:
    st.session_state.follow_up = FollowUpManager()

if 'cv_content' not in st.session_state:
    st.session_state.cv_content = "Experienced Python developer with skills in ML, backend, and automation."

if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {
        "name": "John Doe",
        "skills": ["Python", "Machine Learning", "Streamlit"],
        "experience_summary": "3+ years experience in backend and AI-driven applications."
    }

# ======================================
# Streamlit UI
# ======================================
st.title("🤖 Job Application Automation Demo")

with st.sidebar:
    st.header("Automation Settings")
    roles = st.multiselect("Target Roles", ["Software Developer", "ML Engineer"], default=["Software Developer"])
    locations = st.multiselect("Preferred Locations", ["London", "Remote"], default=["Remote"])
    daily_limit = st.slider("Max Applications/Day", 1, 50, 5)

    settings = AutomationSettings(
        target_roles=roles,
        locations=locations,
        salary_min=None,
        salary_max=None,
        job_types=["Full-time"],
        experience_levels=["Mid"],
        remote_only=True,
        exclude_companies=[],
        max_applications_per_day=daily_limit,
        auto_follow_up=True,
        custom_cover_letter=True
    )

st.subheader("1. 🔍 Search Jobs")

if st.button("Search Jobs"):
    with st.spinner("Searching..."):
        jobs = st.session_state.engine.search_jobs(settings, max_results=10)
        st.session_state.search_results = jobs

if 'search_results' in st.session_state:
    for i, job in enumerate(st.session_state.search_results):
        with st.expander(f"{job.title} at {job.company} ({job.match_score:.2f} match)"):
            st.write(f"📍 {job.location} | {job.job_board.value}")
            st.write(job.description or "*No description available*")
            if st.button("Apply", key=f"apply_{i}"):
                async def apply_job():
                    apps = await st.session_state.engine.apply_to_jobs(
                        [job],
                        settings,
                        st.session_state.cv_content,
                        st.session_state.user_profile
                    )
                    for app in apps:
                        st.session_state.tracker.add_application(app)
                        st.success(f"✅ Applied to {app.job.title} at {app.job.company}")
                asyncio.run(apply_job())

st.subheader("2. 📋 Tracked Applications")

apps = st.session_state.tracker.get_applications()
if apps:
    for app in apps:
        st.markdown(f"**{app.job.title}** at *{app.job.company}* - `{app.status.value}`")
else:
    st.info("No applications tracked yet.")

st.subheader("3. 📧 Send Follow-Up Emails")

if st.button("Send Follow-Ups"):
    count = 0
    for app in apps:
        if app.status == ApplicationStatus.APPLIED:
            st.session_state.follow_up.schedule_follow_ups(app)
            st.session_state.follow_up.send_follow_up(app)
            count += 1
    st.success(f"✅ Sent follow-ups for {count} applications.")
