KB_SEED = [
    {
        "category": "Account Issues",
        "intent": "password_reset",
        "keywords": ["reset", "password", "forgot", "locked out", "can't login"],
        "problem_summary": "User cannot access account due to password issue",
        "solution_template": "Dear {{customer_name}},\nTo reset your password:\n1. Visit {{reset_url}}\n2. Enter your registered email\n3. Open the reset link\n4. Set a new password\nTicket: {{ticket_id}}",
        "variables_used": ["customer_name", "reset_url", "ticket_id"],
        "confidence_threshold": 75,
    },
    {
        "category": "Account Issues",
        "intent": "two_factor_issue",
        "keywords": ["2fa", "otp", "authenticator", "verification code"],
        "problem_summary": "User has trouble with 2FA verification",
        "solution_template": "Dear {{customer_name}},\nFor 2FA issues:\n1. Confirm device time is synced\n2. Use backup codes if available\n3. Rebind authenticator from security settings\nTicket: {{ticket_id}}",
        "variables_used": ["customer_name", "ticket_id"],
        "confidence_threshold": 72,
    },
    {
        "category": "Billing & Payments",
        "intent": "refund_request",
        "keywords": ["refund", "money back", "charge", "cancel payment"],
        "problem_summary": "Customer requests refund",
        "solution_template": "Dear {{customer_name}},\nWe can help with your refund request.\n1. Confirm order ID\n2. We review eligibility in 1 business day\n3. Refund is issued to original payment method\nTicket: {{ticket_id}}",
        "variables_used": ["customer_name", "ticket_id"],
        "confidence_threshold": 70,
    },
    {
        "category": "General Inquiry",
        "intent": "general_inquiry",
        "keywords": ["hours", "contact", "location", "support"],
        "problem_summary": "General customer question",
        "solution_template": "Dear {{customer_name}},\nThanks for contacting {{company_name}}.\nOur support team is available 24/7 via email.\nTicket: {{ticket_id}}",
        "variables_used": ["customer_name", "company_name", "ticket_id"],
        "confidence_threshold": 65,
    },
]

# Expand to 20+ realistic intents for production demo.
for i in range(5, 23):
    KB_SEED.append(
        {
            "category": "Technical Support" if i % 2 == 0 else "Order & Delivery",
            "intent": f"intent_{i}",
            "keywords": [f"keyword_{i}", "issue", "help", "support"],
            "problem_summary": f"Seeded KB article {i}",
            "solution_template": (
                "Dear {{customer_name}},\n"
                f"This is a guided solution for article {i}.\n"
                "1. Verify account details\n2. Retry the requested action\n3. Reply if issue persists\n"
                "Ticket: {{ticket_id}}"
            ),
            "variables_used": ["customer_name", "ticket_id"],
            "confidence_threshold": 68,
        }
    )
