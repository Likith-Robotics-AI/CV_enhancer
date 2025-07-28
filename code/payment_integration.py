"""
Integration module to connect payment processing with your existing CV optimizer app
"""

import streamlit as st
from payment_processor import PaymentProcessor, PaymentUI, PlanType
from typing import Dict, Optional

# ================================
# 🔧 USER SUBSCRIPTION MANAGEMENT
# ================================

class UserSubscriptionManager:
    """Manage user subscription state and access control"""
    
    def __init__(self, payment_processor: PaymentProcessor):
        self.processor = payment_processor
        self.init_user_session()
    
    def init_user_session(self):
        """Initialize user subscription session state"""
        if 'user_subscription' not in st.session_state:
            st.session_state.user_subscription = PlanType.FREE.value
        
        if 'cv_usage_count' not in st.session_state:
            st.session_state.cv_usage_count = 0
        
        if 'user_email' not in st.session_state:
            st.session_state.user_email = None
        
        if 'subscription_id' not in st.session_state:
            st.session_state.subscription_id = None
    
    def get_user_plan(self) -> PlanType:
        """Get user's current plan"""
        try:
            return PlanType(st.session_state.user_subscription)
        except ValueError:
            return PlanType.FREE
    
    def has_access_to_feature(self, feature: str) -> bool:
        """Check if user has access to a specific feature"""
        user_plan = st.session_state.user_subscription
        return self.processor.validate_user_access(user_plan, feature)
    
    def can_optimize_cv(self) -> tuple[bool, str]:
        """Check if user can optimize another CV"""
        user_plan = self.get_user_plan()
        plan_details = self.processor.get_plan_details(user_plan)
        
        # Unlimited for Pro and Enterprise
        if plan_details.cv_limit == -1:
            return True, "Unlimited optimizations available"
        
        # Check usage for Free plan
        if st.session_state.cv_usage_count >= plan_details.cv_limit:
            return False, f"You've reached your limit of {plan_details.cv_limit} CV optimization(s). Upgrade to Pro for unlimited access."
        
        remaining = plan_details.cv_limit - st.session_state.cv_usage_count
        return True, f"{remaining} optimization(s) remaining"
    
    def increment_cv_usage(self):
        """Increment CV usage counter"""
        st.session_state.cv_usage_count += 1
    
    def upgrade_user_plan(self, new_plan: PlanType, subscription_id: str = None):
        """Upgrade user to a new plan"""
        st.session_state.user_subscription = new_plan.value
        if subscription_id:
            st.session_state.subscription_id = subscription_id
        
        # Reset usage counter for new plans
        if new_plan != PlanType.FREE:
            st.session_state.cv_usage_count = 0

# ================================
# 🎨 ENHANCED UI COMPONENTS
# ================================

def render_subscription_status():
    """Render user's current subscription status"""
    user_plan = PlanType(st.session_state.user_subscription)
    plan_details = st.session_state.payment_processor.get_plan_details(user_plan)
    
    # Create status badge
    if user_plan == PlanType.FREE:
        badge_color = "var(--neutral-500)"
        badge_text = "Free Plan"
    elif user_plan == PlanType.PRO:
        badge_color = "var(--primary)"
        badge_text = "Pro Plan"
    else:
        badge_color = "var(--accent)"
        badge_text = "Enterprise Plan"
    
    st.markdown(f"""
    <div style="
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: var(--bg-secondary);
        padding: var(--space-4) var(--space-6);
        border-radius: var(--radius-lg);
        border: 1px solid var(--border-light);
        margin-bottom: var(--space-6);
    ">
        <div style="display: flex; align-items: center; gap: var(--space-3);">
            <div style="
                background: {badge_color};
                color: white;
                padding: var(--space-1) var(--space-3);
                border-radius: var(--radius-full);
                font-size: 0.75rem;
                font-weight: 600;
            ">{badge_text}</div>
            <span style="color: var(--text-secondary); font-size: 0.875rem;">
                CV Optimizations: {st.session_state.cv_usage_count}
                {f"/{plan_details.cv_limit}" if plan_details.cv_limit != -1 else " (Unlimited)"}
            </span>
        </div>
        <div>
            {'<span style="color: var(--success);">✅ Priority Support</span>' if plan_details.priority_support else ''}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_upgrade_prompt():
    """Render upgrade prompt for free users"""
    user_plan = PlanType(st.session_state.user_subscription)
    
    if user_plan == PlanType.FREE:
        can_optimize, message = st.session_state.subscription_manager.can_optimize_cv()
        
        if not can_optimize:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, var(--warning-glow), var(--bg-secondary));
                border: 1px solid var(--warning);
                padding: var(--space-6);
                border-radius: var(--radius-xl);
                text-align: center;
                margin: var(--space-6) 0;
            ">
                <div style="font-size: 2rem; margin-bottom: var(--space-3);">⭐</div>
                <h4 style="color: var(--text-primary); margin-bottom: var(--space-3);">
                    Upgrade to Continue Optimizing
                </h4>
                <p style="color: var(--text-secondary); margin-bottom: var(--space-5);">
                    {message}
                </p>
                <div style="
                    background: var(--bg-primary);
                    padding: var(--space-4);
                    border-radius: var(--radius-lg);
                    margin-bottom: var(--space-5);
                ">
                    <strong style="color: var(--text-primary);">Pro Plan Benefits:</strong>
                    <ul style="color: var(--text-secondary); margin: var(--space-2) 0 0 0; text-align: left;">
                        <li>✅ Unlimited CV optimizations</li>
                        <li>✅ Premium templates</li>
                        <li>✅ Priority support</li>
                        <li>✅ Advanced ATS optimization</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🚀 Upgrade to Pro", type="primary", use_container_width=True):
                    st.session_state.active_nav = 'Pricing'
                    st.rerun()
            with col2:
                if st.button("📧 Contact Sales", use_container_width=True):
                    st.session_state.show_contact_form = True
            
            return False  # Block further actions
    
    return True  # Allow actions to continue

def render_feature_access_check(feature: str, feature_name: str = None):
    """Render feature access check and upgrade prompt if needed"""
    if not feature_name:
        feature_name = feature.replace('_', ' ').title()
    
    has_access = st.session_state.subscription_manager.has_access_to_feature(feature)
    
    if not has_access:
        st.markdown(f"""
        <div style="
            background: var(--bg-secondary);
            border: 1px solid var(--border-primary);
            padding: var(--space-5);
            border-radius: var(--radius-lg);
            text-align: center;
            margin: var(--space-4) 0;
        ">
            <div style="font-size: 1.5rem; margin-bottom: var(--space-2);">🔒</div>
            <h5 style="color: var(--text-primary); margin-bottom: var(--space-2);">
                {feature_name} - Pro Feature
            </h5>
            <p style="color: var(--text-secondary); font-size: 0.875rem;">
                Upgrade to Pro to unlock this feature
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"🚀 Upgrade for {feature_name}", type="primary", key=f"upgrade_{feature}"):
            st.session_state.active_nav = 'Pricing'
            st.rerun()
        
        return False
    
    return True

# ================================
# 🔄 MODIFIED APP FUNCTIONS
# ================================

def enhanced_optimize_cv():
    """Enhanced CV optimization with subscription checks"""
    # Check if user can optimize
    can_optimize, message = st.session_state.subscription_manager.can_optimize_cv()
    
    if not can_optimize:
        st.error(f"❌ {message}")
        render_upgrade_prompt()
        return
    
    # Show remaining optimizations for free users
    user_plan = st.session_state.subscription_manager.get_user_plan()
    if user_plan == PlanType.FREE:
        st.info(f"ℹ️ {message}")
    
    # Proceed with original optimization logic
    try:
        # Your existing optimize_cv() function code here
        # ... (same as before)
        
        # After successful optimization, increment usage
        st.session_state.subscription_manager.increment_cv_usage()
        
        # Show success message with upgrade prompt for free users
        if user_plan == PlanType.FREE:
            remaining = st.session_state.subscription_manager.can_optimize_cv()[1]
            if "0 optimization" in remaining:
                st.balloons()
                st.success("🎉 CV optimized successfully!")
                render_upgrade_prompt()
            else:
                st.success(f"🎉 CV optimized successfully! {remaining}")
    
    except Exception as e:
        st.error(f"❌ Optimization failed: {str(e)}")

def enhanced_template_selection():
    """Enhanced template selection with access control"""
    st.markdown("### 🎨 Choose Your Template")
    
    user_plan = st.session_state.subscription_manager.get_user_plan()
    has_advanced = st.session_state.subscription_manager.has_access_to_feature("advanced_templates")
    
    # Basic templates (available to all)
    basic_templates = ['professional', 'modern']
    
    # Premium templates (Pro and Enterprise only)
    premium_templates = ['executive', 'creative']
    
    # Render basic templates
    st.markdown("#### ✅ Available Templates")
    cols = st.columns(len(basic_templates))
    for idx, template in enumerate(basic_templates):
        with cols[idx]:
            if st.button(f"{template.title()}", key=f"basic_{template}", use_container_width=True):
                st.session_state.selected_template = template
                st.session_state.template_selected = True
                st.success(f"✅ {template.title()} template selected")
    
    # Render premium templates
    st.markdown("#### ⭐ Premium Templates")
    if has_advanced:
        cols = st.columns(len(premium_templates))
        for idx, template in enumerate(premium_templates):
            with cols[idx]:
                if st.button(f"{template.title()}", key=f"premium_{template}", use_container_width=True):
                    st.session_state.selected_template = template
                    st.session_state.template_selected = True
                    st.success(f"✅ {template.title()} template selected")
    else:
        cols = st.columns(len(premium_templates))
        for idx, template in enumerate(premium_templates):
            with cols[idx]:
                st.button(
                    f"🔒 {template.title()} (Pro)",
                    disabled=True,
                    use_container_width=True,
                    help="Upgrade to Pro to access premium templates"
                )
        
        st.markdown("""
        <div style="text-align: center; margin-top: var(--space-4);">
            <small style="color: var(--text-tertiary);">
                Premium templates available with Pro subscription
            </small>
        </div>
        """, unsafe_allow_html=True)

def enhanced_pricing_page():
    """Enhanced pricing page with current plan indication"""
    user_plan = st.session_state.subscription_manager.get_user_plan()
    
    st.markdown("## 💰 Pricing Plans")
    render_subscription_status()
    
    # Show current plan
    if user_plan != PlanType.FREE:
        st.markdown(f"""
        <div style="
            background: var(--success-glow);
            border: 1px solid var(--success);
            padding: var(--space-4);
            border-radius: var(--radius-lg);
            text-align: center;
            margin-bottom: var(--space-6);
        ">
            <span style="color: var(--success);">
                ✅ You're currently on the {user_plan.value.title()} plan
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    # Render pricing cards with current plan indication
    st.session_state.payment_ui.render_pricing_cards()

# ================================
# 📱 PAYMENT STATUS HANDLERS
# ================================

def handle_payment_callback():
    """Handle payment success/failure callbacks"""
    query_params = st.experimental_get_query_params()
    
    if 'payment' in query_params:
        status = query_params['payment'][0]
        
        if status == 'success':
            # Payment successful - upgrade user
            if 'plan' in query_params and 'subscription_id' in query_params:
                try:
                    plan_type = PlanType(query_params['plan'][0])
                    subscription_id = query_params['subscription_id'][0]
                    
                    st.session_state.subscription_manager.upgrade_user_plan(
                        plan_type, subscription_id
                    )
                    
                    st.session_state.payment_ui.render_payment_success()
                    return True
                except:
                    pass
            
            st.session_state.payment_ui.render_payment_success()
            return True
            
        elif status == 'cancelled':
            st.session_state.payment_ui.render_payment_cancelled()
            return True
    
    return False

# ================================
# 🔗 MAIN INTEGRATION FUNCTION
# ================================

def integrate_payments_with_main_app():
    """
    Main integration function to add to your existing app.py
    Call this in your main() function before other page renders
    """
    
    # Initialize payment system
    if 'payment_processor' not in st.session_state:
        st.session_state.payment_processor = PaymentProcessor()
    
    if 'payment_ui' not in st.session_state:
        st.session_state.payment_ui = PaymentUI(st.session_state.payment_processor)
    
    if 'subscription_manager' not in st.session_state:
        st.session_state.subscription_manager = UserSubscriptionManager(
            st.session_state.payment_processor
        )
    
    # Handle payment callbacks first
    if handle_payment_callback():
        return  # Stop here if handling payment callback
    
    # Add subscription status to all pages
    if st.session_state.get('active_nav') == 'Home':
        render_subscription_status()

# ================================
# 🛠️ EXAMPLE USAGE
# ================================

def example_modified_main():
    """
    Example of how to modify your main() function
    """
    
    def main():
        configure_page()
        load_modern_css()
        initialize_session_state()
        
        # 🔥 ADD THIS LINE - Initialize payment system
        integrate_payments_with_main_app()
        
        render_top_navbar()
        
        active_page = st.session_state.get("active_nav", "Home")
        
        if active_page == "About":
            render_about_page()
        elif active_page == "Help":
            render_help_page()
        elif active_page == "Pricing":
            enhanced_pricing_page()  # 🔥 REPLACE with enhanced version
        elif active_page == "My Account":
            render_account_page()
        else:
            render_home_page()

# ================================
# 🔄 REPLACEMENTS FOR EXISTING FUNCTIONS
# ================================

"""
Replace these functions in your existing app.py:

1. Replace optimize_cv() with enhanced_optimize_cv()
2. Replace render_template_section() content with enhanced_template_selection()
3. Replace render_pricing_page() with enhanced_pricing_page()
4. Add integrate_payments_with_main_app() to your main() function
5. Add render_subscription_status() to your home page

Add these to your requirements.txt:
- stripe>=7.0.0
"""

# ================================
# 🔐 SECRETS CONFIGURATION
# ================================

secrets_example = """
# Add these to your .streamlit/secrets.toml file:

[default]
STRIPE_SECRET_KEY = "sk_test_..."  # Your Stripe secret key
STRIPE_PUBLISHABLE_KEY = "pk_test_..."  # Your Stripe publishable key  
STRIPE_WEBHOOK_SECRET = "whsec_..."  # Your webhook endpoint secret
APP_URL = "https://your-app.streamlit.app"  # Your app URL

# For production, use live keys:
# STRIPE_SECRET_KEY = "sk_live_..."
# STRIPE_PUBLISHABLE_KEY = "pk_live_..."
"""