import os
import stripe
import streamlit as st
import hashlib
import hmac
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum

# ================================
# 🏗️ PAYMENT CONFIGURATION
# ================================

class PlanType(Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"

@dataclass
class PricingPlan:
    """Pricing plan configuration"""
    plan_id: str
    name: str
    price_monthly: float
    price_yearly: float
    currency: str
    stripe_price_id_monthly: str
    stripe_price_id_yearly: str
    features: list
    cv_limit: int  # -1 for unlimited
    priority_support: bool
    advanced_templates: bool

# ================================
# 💳 PAYMENT PROCESSOR CLASS
# ================================

class PaymentProcessor:
    """
    Comprehensive payment processing class using Stripe
    Handles subscriptions, one-time payments, and webhook processing
    """
    
    def __init__(self):
        """Initialize the payment processor with Stripe configuration"""
        # Initialize Stripe
        self.stripe_secret_key = self._get_stripe_secret_key()
        self.stripe_publishable_key = self._get_stripe_publishable_key()
        self.webhook_secret = self._get_webhook_secret()
        
        if self.stripe_secret_key:
            stripe.api_key = self.stripe_secret_key
        
        # Define pricing plans
        self.plans = {
            PlanType.FREE: PricingPlan(
                plan_id="free",
                name="Free",
                price_monthly=0.0,
                price_yearly=0.0,
                currency="gbp",
                stripe_price_id_monthly="",
                stripe_price_id_yearly="",
                features=[
                    "1 CV optimization",
                    "Basic templates",
                    "ATS optimization", 
                    "PDF download"
                ],
                cv_limit=1,
                priority_support=False,
                advanced_templates=False
            ),
            PlanType.PRO: PricingPlan(
                plan_id="pro",
                name="Pro",
                price_monthly=9.99,
                price_yearly=99.99,
                currency="gbp",
                stripe_price_id_monthly="price_pro_monthly_id",  # Replace with actual Stripe price ID
                stripe_price_id_yearly="price_pro_yearly_id",    # Replace with actual Stripe price ID
                features=[
                    "Unlimited CV optimizations",
                    "Premium templates",
                    "Advanced ATS optimization",
                    "Multiple formats (PDF, Word)",
                    "Priority support",
                    "Cover letter templates"
                ],
                cv_limit=-1,
                priority_support=True,
                advanced_templates=True
            ),
            PlanType.ENTERPRISE: PricingPlan(
                plan_id="enterprise",
                name="Enterprise",
                price_monthly=0.0,  # Custom pricing
                price_yearly=0.0,   # Custom pricing
                currency="gbp",
                stripe_price_id_monthly="",
                stripe_price_id_yearly="",
                features=[
                    "Everything in Pro",
                    "Team management",
                    "Analytics dashboard",
                    "API access",
                    "Custom branding",
                    "Dedicated support"
                ],
                cv_limit=-1,
                priority_support=True,
                advanced_templates=True
            )
        }
    
    def _get_stripe_secret_key(self) -> str:
        """Get Stripe secret key from environment or Streamlit secrets"""
        try:
            # Try environment variable first
            key = os.getenv('STRIPE_SECRET_KEY')
            if key:
                return key
            
            # Try Streamlit secrets
            return st.secrets.get("STRIPE_SECRET_KEY", "")
        except:
            return ""
    
    def _get_stripe_publishable_key(self) -> str:
        """Get Stripe publishable key from environment or Streamlit secrets"""
        try:
            # Try environment variable first
            key = os.getenv('STRIPE_PUBLISHABLE_KEY')
            if key:
                return key
            
            # Try Streamlit secrets
            return st.secrets.get("STRIPE_PUBLISHABLE_KEY", "")
        except:
            return ""
    
    def _get_webhook_secret(self) -> str:
        """Get Stripe webhook secret from environment or Streamlit secrets"""
        try:
            # Try environment variable first
            secret = os.getenv('STRIPE_WEBHOOK_SECRET')
            if secret:
                return secret
            
            # Try Streamlit secrets
            return st.secrets.get("STRIPE_WEBHOOK_SECRET", "")
        except:
            return ""
    
    def is_configured(self) -> bool:
        """Check if Stripe is properly configured"""
        return bool(self.stripe_secret_key and self.stripe_publishable_key)
    
    def create_checkout_session(self, 
                              plan_type: PlanType, 
                              billing_cycle: str = "monthly",
                              customer_email: str = None,
                              success_url: str = None,
                              cancel_url: str = None,
                              metadata: Dict[str, str] = None) -> Tuple[bool, str]:
        """
        Create a Stripe Checkout session for subscription
        
        Args:
            plan_type: The pricing plan type
            billing_cycle: "monthly" or "yearly"
            customer_email: Customer's email address
            success_url: URL to redirect after successful payment
            cancel_url: URL to redirect after cancelled payment
            metadata: Additional metadata to store with the session
            
        Returns:
            Tuple of (success: bool, session_url_or_error: str)
        """
        try:
            if not self.is_configured():
                return False, "Payment system not configured. Please contact support."
            
            plan = self.plans[plan_type]
            
            # Free plan doesn't need payment
            if plan_type == PlanType.FREE:
                return False, "Free plan doesn't require payment"
            
            # Get the appropriate price ID
            if billing_cycle == "yearly":
                price_id = plan.stripe_price_id_yearly
            else:
                price_id = plan.stripe_price_id_monthly
            
            if not price_id:
                return False, f"Price ID not configured for {plan.name} {billing_cycle} plan"
            
            # Default URLs
            if not success_url:
                success_url = f"{st.secrets.get('APP_URL', 'http://localhost:8501')}?payment=success"
            if not cancel_url:
                cancel_url = f"{st.secrets.get('APP_URL', 'http://localhost:8501')}?payment=cancelled"
            
            # Create session parameters
            session_params = {
                'payment_method_types': ['card'],
                'line_items': [{
                    'price': price_id,
                    'quantity': 1,
                }],
                'mode': 'subscription',
                'success_url': success_url,
                'cancel_url': cancel_url,
                'metadata': metadata or {},
            }
            
            # Add customer email if provided
            if customer_email:
                session_params['customer_email'] = customer_email
            
            # Create the checkout session
            session = stripe.checkout.Session.create(**session_params)
            
            return True, session.url
            
        except stripe.error.StripeError as e:
            return False, f"Stripe error: {str(e)}"
        except Exception as e:
            return False, f"Payment error: {str(e)}"
    
    def create_one_time_payment(self,
                               amount: float,
                               currency: str = "gbp",
                               description: str = "CV Optimization",
                               customer_email: str = None,
                               success_url: str = None,
                               cancel_url: str = None,
                               metadata: Dict[str, str] = None) -> Tuple[bool, str]:
        """
        Create a one-time payment session
        
        Args:
            amount: Payment amount in the currency's smallest unit (pence for GBP)
            currency: Currency code (gbp, usd, eur)
            description: Payment description
            customer_email: Customer's email
            success_url: Success redirect URL
            cancel_url: Cancel redirect URL
            metadata: Additional metadata
            
        Returns:
            Tuple of (success: bool, session_url_or_error: str)
        """
        try:
            if not self.is_configured():
                return False, "Payment system not configured. Please contact support."
            
            # Convert amount to smallest currency unit (pence for GBP)
            amount_in_smallest_unit = int(amount * 100)
            
            # Default URLs
            if not success_url:
                success_url = f"{st.secrets.get('APP_URL', 'http://localhost:8501')}?payment=success"
            if not cancel_url:
                cancel_url = f"{st.secrets.get('APP_URL', 'http://localhost:8501')}?payment=cancelled"
            
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': currency,
                        'product_data': {
                            'name': description,
                        },
                        'unit_amount': amount_in_smallest_unit,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
                customer_email=customer_email,
                metadata=metadata or {},
            )
            
            return True, session.url
            
        except stripe.error.StripeError as e:
            return False, f"Stripe error: {str(e)}"
        except Exception as e:
            return False, f"Payment error: {str(e)}"
    
    def get_customer_subscriptions(self, customer_id: str) -> Tuple[bool, list]:
        """
        Get all subscriptions for a customer
        
        Args:
            customer_id: Stripe customer ID
            
        Returns:
            Tuple of (success: bool, subscriptions_list_or_error: list/str)
        """
        try:
            if not self.is_configured():
                return False, "Payment system not configured"
            
            subscriptions = stripe.Subscription.list(customer=customer_id)
            return True, subscriptions.data
            
        except stripe.error.StripeError as e:
            return False, f"Stripe error: {str(e)}"
        except Exception as e:
            return False, f"Error retrieving subscriptions: {str(e)}"
    
    def cancel_subscription(self, subscription_id: str) -> Tuple[bool, str]:
        """
        Cancel a subscription
        
        Args:
            subscription_id: Stripe subscription ID
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            if not self.is_configured():
                return False, "Payment system not configured"
            
            subscription = stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=True
            )
            
            return True, "Subscription will be cancelled at the end of the billing period"
            
        except stripe.error.StripeError as e:
            return False, f"Stripe error: {str(e)}"
        except Exception as e:
            return False, f"Error cancelling subscription: {str(e)}"
    
    def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        """
        Verify Stripe webhook signature
        
        Args:
            payload: Raw request payload
            signature: Stripe signature header
            
        Returns:
            bool: True if signature is valid
        """
        try:
            if not self.webhook_secret:
                return False
            
            stripe.Webhook.construct_event(payload, signature, self.webhook_secret)
            return True
            
        except stripe.error.SignatureVerificationError:
            return False
        except Exception:
            return False
    
    def handle_webhook_event(self, event_data: dict) -> Tuple[bool, str]:
        """
        Handle Stripe webhook events
        
        Args:
            event_data: Stripe event data
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            event_type = event_data.get('type')
            
            if event_type == 'checkout.session.completed':
                return self._handle_checkout_completed(event_data['data']['object'])
            elif event_type == 'customer.subscription.created':
                return self._handle_subscription_created(event_data['data']['object'])
            elif event_type == 'customer.subscription.updated':
                return self._handle_subscription_updated(event_data['data']['object'])
            elif event_type == 'customer.subscription.deleted':
                return self._handle_subscription_cancelled(event_data['data']['object'])
            elif event_type == 'invoice.payment_succeeded':
                return self._handle_payment_succeeded(event_data['data']['object'])
            elif event_type == 'invoice.payment_failed':
                return self._handle_payment_failed(event_data['data']['object'])
            else:
                return True, f"Unhandled event type: {event_type}"
                
        except Exception as e:
            return False, f"Error handling webhook: {str(e)}"
    
    def _handle_checkout_completed(self, session: dict) -> Tuple[bool, str]:
        """Handle successful checkout completion"""
        try:
            customer_id = session.get('customer')
            customer_email = session.get('customer_email')
            subscription_id = session.get('subscription')
            
            # Log successful payment
            print(f"Checkout completed for customer {customer_email} (ID: {customer_id})")
            
            # Here you would typically:
            # 1. Update user's subscription status in your database
            # 2. Send welcome email
            # 3. Grant access to premium features
            
            return True, "Checkout completed successfully"
            
        except Exception as e:
            return False, f"Error handling checkout completion: {str(e)}"
    
    def _handle_subscription_created(self, subscription: dict) -> Tuple[bool, str]:
        """Handle new subscription creation"""
        try:
            customer_id = subscription.get('customer')
            subscription_id = subscription.get('id')
            status = subscription.get('status')
            
            print(f"New subscription created: {subscription_id} for customer {customer_id}")
            
            # Update user's subscription in database
            # Grant premium access
            
            return True, "Subscription created successfully"
            
        except Exception as e:
            return False, f"Error handling subscription creation: {str(e)}"
    
    def _handle_subscription_updated(self, subscription: dict) -> Tuple[bool, str]:
        """Handle subscription updates"""
        try:
            subscription_id = subscription.get('id')
            status = subscription.get('status')
            
            print(f"Subscription updated: {subscription_id}, status: {status}")
            
            # Update subscription status in database
            
            return True, "Subscription updated successfully"
            
        except Exception as e:
            return False, f"Error handling subscription update: {str(e)}"
    
    def _handle_subscription_cancelled(self, subscription: dict) -> Tuple[bool, str]:
        """Handle subscription cancellation"""
        try:
            subscription_id = subscription.get('id')
            customer_id = subscription.get('customer')
            
            print(f"Subscription cancelled: {subscription_id} for customer {customer_id}")
            
            # Revoke premium access
            # Send cancellation email
            
            return True, "Subscription cancelled successfully"
            
        except Exception as e:
            return False, f"Error handling subscription cancellation: {str(e)}"
    
    def _handle_payment_succeeded(self, invoice: dict) -> Tuple[bool, str]:
        """Handle successful payment"""
        try:
            customer_id = invoice.get('customer')
            amount_paid = invoice.get('amount_paid')
            
            print(f"Payment succeeded: {amount_paid} for customer {customer_id}")
            
            # Update payment history
            # Send receipt email
            
            return True, "Payment processed successfully"
            
        except Exception as e:
            return False, f"Error handling successful payment: {str(e)}"
    
    def _handle_payment_failed(self, invoice: dict) -> Tuple[bool, str]:
        """Handle failed payment"""
        try:
            customer_id = invoice.get('customer')
            
            print(f"Payment failed for customer {customer_id}")
            
            # Send payment failure notification
            # Potentially downgrade account after grace period
            
            return True, "Payment failure handled"
            
        except Exception as e:
            return False, f"Error handling payment failure: {str(e)}"
    
    def get_plan_details(self, plan_type: PlanType) -> PricingPlan:
        """Get pricing plan details"""
        return self.plans[plan_type]
    
    def validate_user_access(self, user_subscription: str, feature: str) -> bool:
        """
        Validate if user has access to a specific feature
        
        Args:
            user_subscription: User's current subscription type
            feature: Feature to check access for
            
        Returns:
            bool: True if user has access
        """
        try:
            plan_type = PlanType(user_subscription)
            plan = self.plans[plan_type]
            
            # Define feature access logic
            if feature == "unlimited_cv":
                return plan.cv_limit == -1
            elif feature == "priority_support":
                return plan.priority_support
            elif feature == "advanced_templates":
                return plan.advanced_templates
            elif feature == "basic_cv":
                return True  # All plans have basic CV access
            else:
                return False
                
        except (ValueError, KeyError):
            return False

# ================================
# 🎨 STREAMLIT PAYMENT UI
# ================================

class PaymentUI:
    """Streamlit UI components for payment processing"""
    
    def __init__(self, payment_processor: PaymentProcessor):
        self.processor = payment_processor
    
    def render_pricing_cards(self):
        """Render interactive pricing cards with payment buttons"""
        
        if not self.processor.is_configured():
            st.error("❌ Payment system not configured. Please contact support.")
            return
        
        st.markdown("### 💳 Choose Your Plan")
        
        col1, col2, col3 = st.columns(3)
        
        # Free Plan
        with col1:
            plan = self.processor.get_plan_details(PlanType.FREE)
            self._render_plan_card(plan, PlanType.FREE, is_free=True)
        
        # Pro Plan
        with col2:
            plan = self.processor.get_plan_details(PlanType.PRO)
            self._render_plan_card(plan, PlanType.PRO, is_popular=True)
        
        # Enterprise Plan
        with col3:
            plan = self.processor.get_plan_details(PlanType.ENTERPRISE)
            self._render_plan_card(plan, PlanType.ENTERPRISE, is_enterprise=True)
    
    def _render_plan_card(self, plan: PricingPlan, plan_type: PlanType, 
                         is_free: bool = False, is_popular: bool = False, 
                         is_enterprise: bool = False):
        """Render a single pricing plan card"""
        
        # Card styling
        card_style = "border: 1px solid var(--border-light);"
        if is_popular:
            card_style = "border: 2px solid var(--primary); box-shadow: 0 0 20px var(--primary-glow);"
        
        st.markdown(f"""
        <div style="
            background: var(--bg-secondary);
            {card_style}
            border-radius: var(--radius-xl);
            padding: var(--space-8);
            text-align: center;
            height: 500px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            position: relative;
        ">
        """, unsafe_allow_html=True)
        
        # Popular badge
        if is_popular:
            st.markdown("""
            <div style="
                position: absolute;
                top: -10px;
                left: 50%;
                transform: translateX(-50%);
                background: var(--primary);
                color: white;
                padding: 4px 16px;
                border-radius: 12px;
                font-size: 0.75rem;
                font-weight: 600;
            ">MOST POPULAR</div>
            """, unsafe_allow_html=True)
        
        # Plan content
        st.markdown(f"### {plan.name}")
        
        if is_free:
            st.markdown("# £0")
            st.markdown("Perfect for trying out Tailor")
        elif is_enterprise:
            st.markdown("# Custom")
            st.markdown("For teams and organizations")
        else:
            # Monthly/Yearly toggle for Pro plan
            billing_cycle = st.radio(
                "Billing Cycle",
                ["Monthly", "Yearly"],
                key=f"billing_{plan.plan_id}",
                horizontal=True
            )
            
            if billing_cycle == "Monthly":
                st.markdown(f"# £{plan.price_monthly}")
                st.markdown("per month")
            else:
                st.markdown(f"# £{plan.price_yearly}")
                st.markdown("per year")
                discount = int((1 - (plan.price_yearly / (plan.price_monthly * 12))) * 100)
                st.markdown(f"<small style='color: var(--success);'>Save {discount}%</small>", 
                           unsafe_allow_html=True)
        
        # Features list
        st.markdown("---")
        for feature in plan.features:
            st.markdown(f"✅ {feature}")
        
        # Action button
        if is_free:
            if st.button("Get Started Free", key=f"btn_{plan.plan_id}", use_container_width=True):
                st.session_state.active_nav = 'Home'
                st.rerun()
        elif is_enterprise:
            if st.button("Contact Sales", key=f"btn_{plan.plan_id}", use_container_width=True):
                self._handle_enterprise_contact()
        else:
            billing = "yearly" if billing_cycle == "Yearly" else "monthly"
            if st.button(f"Upgrade to {plan.name}", key=f"btn_{plan.plan_id}_{billing}", 
                        use_container_width=True, type="primary"):
                self._handle_subscription_purchase(plan_type, billing)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    def _handle_subscription_purchase(self, plan_type: PlanType, billing_cycle: str):
        """Handle subscription purchase"""
        try:
            # Get user email (you might want to collect this)
            user_email = st.session_state.get('user_email', 'customer@example.com')
            
            # Create checkout session
            success, result = self.processor.create_checkout_session(
                plan_type=plan_type,
                billing_cycle=billing_cycle,
                customer_email=user_email,
                metadata={
                    'source': 'cv_optimizer_app',
                    'plan': plan_type.value,
                    'billing': billing_cycle
                }
            )
            
            if success:
                # Redirect to Stripe Checkout
                st.markdown(f"""
                <script>
                    window.open('{result}', '_blank');
                </script>
                """, unsafe_allow_html=True)
                
                st.success("🎉 Redirecting to secure checkout...")
                st.info("💳 You'll be redirected to Stripe's secure payment page.")
            else:
                st.error(f"❌ {result}")
                
        except Exception as e:
            st.error(f"❌ Error initiating payment: {str(e)}")
    
    def _handle_enterprise_contact(self):
        """Handle enterprise contact form"""
        st.info("📧 Our sales team will contact you within 24 hours!")
        
        # You could add a contact form here
        with st.form("enterprise_contact"):
            st.markdown("### 📞 Enterprise Contact")
            
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name*")
                company = st.text_input("Company*")
            with col2:
                email = st.text_input("Email*")
                phone = st.text_input("Phone")
            
            team_size = st.selectbox("Team Size", 
                                   ["1-10", "11-50", "51-200", "201-500", "500+"])
            message = st.text_area("Tell us about your requirements")
            
            if st.form_submit_button("Contact Sales", type="primary"):
                # Here you would typically send this to your CRM or email
                st.success("✅ Thank you! We'll be in touch soon.")
    
    def render_payment_success(self):
        """Render payment success page"""
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, var(--success), var(--success-dark));
            color: white;
            padding: var(--space-12);
            border-radius: var(--radius-2xl);
            text-align: center;
            margin: var(--space-8);
        ">
            <div style="font-size: 4rem; margin-bottom: var(--space-6);">🎉</div>
            <h2 style="color: white; margin-bottom: var(--space-4);">Payment Successful!</h2>
            <p style="font-size: 1.25rem; opacity: 0.9; margin-bottom: var(--space-6);">
                Welcome to Tailor Pro! Your subscription is now active.
            </p>
            <div style="
                background: rgba(255, 255, 255, 0.1);
                padding: var(--space-6);
                border-radius: var(--radius-lg);
                margin-top: var(--space-6);
            ">
                <h4 style="color: white; margin-bottom: var(--space-3);">What's Next?</h4>
                <ul style="text-align: left; max-width: 400px; margin: 0 auto;">
                    <li>✅ Unlimited CV optimizations</li>
                    <li>✅ Access to premium templates</li>
                    <li>✅ Priority support</li>
                    <li>✅ Advanced ATS optimization</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Start Optimizing", type="primary", use_container_width=True):
            st.session_state.active_nav = 'Home'
            st.rerun()
    
    def render_payment_cancelled(self):
        """Render payment cancelled page"""
        st.markdown("""
        <div style="
            background: var(--bg-secondary);
            border: 1px solid var(--border-light);
            padding: var(--space-10);
            border-radius: var(--radius-2xl);
            text-align: center;
            margin: var(--space-8);
        ">
            <div style="font-size: 3rem; margin-bottom: var(--space-4);">😔</div>
            <h3 style="color: var(--text-primary); margin-bottom: var(--space-3);">Payment Cancelled</h3>
            <p style="color: var(--text-secondary); margin-bottom: var(--space-6);">
                No worries! You can still use our free plan or try upgrading again later.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Try Again", type="primary", use_container_width=True):
                st.session_state.active_nav = 'Pricing'
                st.rerun()
        with col2:
            if st.button("🏠 Back to Home", use_container_width=True):
                st.session_state.active_nav = 'Home'
                st.rerun()

# ================================
# 🔗 INTEGRATION EXAMPLE
# ================================

def integrate_payments_with_app():
    """Example of how to integrate payments with your existing app"""
    
    # Initialize payment processor
    if 'payment_processor' not in st.session_state:
        st.session_state.payment_processor = PaymentProcessor()
    
    if 'payment_ui' not in st.session_state:
        st.session_state.payment_ui = PaymentUI(st.session_state.payment_processor)
    
    # Check for payment status in URL parameters
    query_params = st.experimental_get_query_params()
    
    if 'payment' in query_params:
        if query_params['payment'][0] == 'success':
            st.session_state.payment_ui.render_payment_success()
            return
        elif query_params['payment'][0] == 'cancelled':
            st.session_state.payment_ui.render_payment_cancelled()
            return
    
    # Normal pricing page
    st.session_state.payment_ui.render_pricing_cards()

# ================================
# 🔧 WEBHOOK HANDLER (SEPARATE ENDPOINT)
# ================================

def create_webhook_handler():
    """
    Example webhook handler for Flask/FastAPI
    This should be deployed as a separate endpoint
    """
    webhook_code = '''
import stripe
from flask import Flask, request, jsonify
from payment_processor import PaymentProcessor

app = Flask(__name__)
processor = PaymentProcessor()

@app.route('/stripe-webhook', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhook events"""
    payload = request.get_data()
    signature = request.headers.get('Stripe-Signature')
    
    # Verify webhook signature
    if not processor.verify_webhook_signature(payload, signature):
        return jsonify({'error': 'Invalid signature'}), 400
    
    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
        
        # Handle the event
        success, message = processor.handle_webhook_event(event)
        
        if success:
            return jsonify({'status': 'success', 'message': message}), 200
        else:
            return jsonify({'status': 'error', 'message': message}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
    '''
    
    return webhook_code