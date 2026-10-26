import re
from urllib.parse import urlparse

import streamlit as st

st.set_page_config(
    page_title="Scam Detector",
    page_icon="SD",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

.stApp {
    background: radial-gradient(ellipse at 10% 0%, #142b3c 0%, transparent 40%),
                linear-gradient(180deg, #0b1120 0%, #0d1424 100%);
    color: #edf3ff;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] { background: transparent; }

.block-container {
    max-width: 1050px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3, h4 {
    font-family: 'Space Grotesk', sans-serif !important;
    letter-spacing: -0.4px;
}

h1 { color: #f4f7ff !important; }

p, label, li { color: #d4deef; }

[data-testid="stCaptionContainer"] { color: #9aabc5 !important; }

.hero {
    background: linear-gradient(135deg, #14283a, #132039 60%, #19233b);
    border: 1px solid #294459;
    border-radius: 22px;
    padding: 30px 32px;
    margin-bottom: 26px;
}

.eyebrow {
    color: #42e8c5;
    text-transform: uppercase;
    font-size: 0.76rem;
    font-weight: 700;
    letter-spacing: 2px;
    margin-bottom: 12px;
}

.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.5rem;
    line-height: 1.12;
    font-weight: 700;
    color: #f4f7ff;
    margin-bottom: 13px;
}

.hero-description {
    color: #b8c8df;
    font-size: 1rem;
    line-height: 1.7;
    max-width: 680px;
    margin-bottom: 18px;
}

.pill {
    display: inline-block;
    border: 1px solid #326657;
    color: #79f1d5;
    background: #173b3a;
    border-radius: 100px;
    padding: 6px 12px;
    font-size: 0.78rem;
    font-weight: 600;
    margin-right: 7px;
    margin-top: 4px;
}

.section-heading {
    font-family: 'Space Grotesk', sans-serif;
    color: #f1f5ff;
    font-size: 1.45rem;
    font-weight: 600;
    margin-top: 12px;
    margin-bottom: 5px;
}

.section-subtitle {
    color: #9aabc5;
    font-size: 0.93rem;
    margin-bottom: 18px;
    line-height: 1.6;
}

div[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 8px;
    background: #101a2b;
    border: 1px solid #24334a;
    border-radius: 13px;
    padding: 7px;
    margin-bottom: 22px;
}

div[data-testid="stTabs"] button[data-baseweb="tab"] {
    background: transparent;
    color: #9aabc5;
    border-radius: 9px;
    border: none;
    padding: 11px 17px;
    font-weight: 600;
}

div[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"] {
    background: #1b3444;
    color: #55ebcb;
}

div[data-testid="stTextArea"] textarea {
    background: #101a2b;
    color: #f0f5ff;
    border: 1px solid #2b3c55;
    border-radius: 13px;
    padding: 16px;
    font-size: 0.98rem;
}

div[data-testid="stTextArea"] textarea:focus {
    border-color: #42e8c5;
    box-shadow: 0 0 0 1px #42e8c5;
}

div.stButton > button {
    background: #42e8c5;
    color: #08201e;
    border: none;
    border-radius: 11px;
    padding: 0.65rem 1.2rem;
    font-weight: 700;
    min-height: 44px;
    transition: 0.2s ease;
}

div.stButton > button:hover {
    background: #73f3d8;
    color: #08201e;
    border: none;
    transform: translateY(-1px);
}

div[data-testid="stMetric"] {
    background: #121e31;
    border: 1px solid #2a3b54;
    padding: 18px;
    border-radius: 15px;
}

div[data-testid="stMetricLabel"] { color: #a8b8d0; }

div[data-testid="stMetricValue"] {
    color: #55ebcb;
    font-family: 'Space Grotesk', sans-serif;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(18, 28, 48, 0.72);
    border-color: #283951;
    border-radius: 16px;
}

hr { border-color: #24334a; }

.feature-card {
    background: #121e31;
    border: 1px solid #2a3b54;
    border-radius: 15px;
    padding: 18px;
    height: 100%;
}

.feature-number {
    color: #42e8c5;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 8px;
}

.feature-title {
    color: #f0f5ff;
    font-weight: 700;
    margin-bottom: 7px;
}

.feature-text {
    color: #9aabc5;
    font-size: 0.9rem;
    line-height: 1.6;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background: #101a2b;
    border-color: #2b3c55;
    border-radius: 10px;
}

.footer {
    text-align: center;
    color: #7f91ad;
    font-size: 0.83rem;
    padding: 24px 0 0;
    line-height: 1.8;
}
</style>
""", unsafe_allow_html=True)


# Warning phrases are grouped by category.
# Each category contributes at most one point to the base score.

warning_categories = {
    "Urgency or pressure": [
        "act now", "immediately", "urgent", "limited time",
        "expires today", "final warning", "account suspended",
        "account locked", "within 24 hours", "don't delay",
        "do not delay", "last chance", "act immediately",
        "your account will be closed"
    ],
    "Account or identity concerns": [
        "verify your account", "password", "verification code",
        "social security", "personal information",
        "confirm your identity", "login details",
        "security code", "one-time passcode",
        "one time passcode", "ssn", "bank details"
    ],
    "Suspicious links": [
        "click here", "tap here", "click the link",
        "open this link", "verify here"
    ],
    "Money or payment requests": [
        "send money", "wire transfer", "pay now",
        "payment required", "bank account",
        "processing fee", "transfer funds", "pay a fee",
        "send payment", "outstanding balance",
        "refund", "overdue payment"
    ],
    "Unusual payment methods": [
        "bitcoin", "cryptocurrency", "crypto",
        "prepaid card", "gift card", "gift cards",
        "send the code", "payment through gift cards",
        "crypto wallet", "gift card code"
    ],
    "Unexpected prizes or offers": [
        "you won", "winner", "claim your prize",
        "free gift", "congratulations", "claim your reward",
        "you have been selected", "inheritance",
        "you have won", "cash prize", "claim your winnings"
    ],
    "Possible impersonation": [
        "pretending to be", "this is your bank",
        "your account has been compromised",
        "we detected unusual activity", "government agency",
        "police department", "keep this confidential",
        "don't tell anyone", "do not tell anyone",
        "i am stranded", "urgent favor"
    ]
}

category_explanations = {
    "Urgency or pressure":
        "This may be trying to rush you into acting before you have "
        "time to think. That is a common scam tactic.",

    "Account or identity concerns":
        "This mentions an account or personal information. Be careful "
        "with passwords and verification codes, even if the message looks real.",

    "Suspicious links":
        "This contains wording that encourages you to use a link. "
        "Check the destination independently before opening it.",

    "Money or payment requests":
        "This mentions a payment or financial request. Verify who is "
        "asking and why before sending anything.",

    "Unusual payment methods":
        "Gift cards and cryptocurrency can be difficult to recover "
        "once sent. Treat requests to pay this way with caution.",

    "Unexpected prizes or offers":
        "This mentions a prize or offer. Unexpected prizes that require "
        "upfront payments deserve extra scrutiny.",

    "Possible impersonation":
        "Someone could be pretending to be a person or organization "
        "you trust. Verify the request using a separate contact method."
}

category_advice = {
    "Urgency or pressure":
        "Take a second. A message trying to rush you doesn't mean "
        "you have to act immediately.",

    "Account or identity concerns":
        "Don't share passwords or verification codes. Visit the official "
        "website yourself or call the number on your bank card.",

    "Suspicious links":
        "Don't blindly trust links in messages. Find the organization's "
        "official website yourself.",

    "Money or payment requests":
        "Verify the person, organization, and reason for the payment first.",

    "Unusual payment methods":
        "Pause before paying with gift cards or crypto. Verify the request "
        "through another trusted source.",

    "Unexpected prizes or offers":
        "Don't pay a random fee or share private information just to claim "
        "a prize.",

    "Possible impersonation":
        "Contact the person or organization another way. Don't rely on "
        "contact details in the suspicious message."
}

known_shorteners = {
    "bit.ly",
    "t.co",
    "tinyurl.com",
    "is.gd",
    "ow.ly",
    "buff.ly",
    "rebrand.ly",
    "cutt.ly",
    "shorturl.at",
    "rb.gy"
}


def get_urls(message):
    return re.findall(r"https?://[^\s<>\"']+", message, flags=re.IGNORECASE)


def get_hostname(url):
    cleaned_url = url.rstrip(".,!?;:)]}")

    try:
        parsed = urlparse(cleaned_url)
        hostname = parsed.hostname

        if hostname:
            return hostname.lower().rstrip(".")

    except ValueError:
        pass

    return None


def is_known_shortener(hostname):
    if not hostname:
        return False

    return any(
        hostname == domain or hostname.endswith("." + domain)
        for domain in known_shorteners
    )


def find_warning_categories(message):
    found_categories = {}
    message_lower = message.lower()

    for category, phrases in warning_categories.items():
        matches = []
        seen_phrases = set()

        for phrase in phrases:
            pattern = r"(?<!\w)" + re.escape(phrase) + r"(?!\w)"
            match = re.search(pattern, message_lower)

            if match and phrase not in seen_phrases:
                start = max(0, match.start() - 45)
                end = min(len(message), match.end() + 45)

                matches.append({
                    "phrase": message[match.start():match.end()],
                    "context": message[start:end].replace("\n", " ")
                })

                seen_phrases.add(phrase)

        if category == "Suspicious links":
            for url in get_urls(message):
                hostname = get_hostname(url)

                if is_known_shortener(hostname):
                    matches.append({
                        "phrase": url.rstrip(".,!?;:)]}"),
                        "context": url.rstrip(".,!?;:)]}")
                    })

        if matches:
            unique_matches = []
            seen = set()

            for item in matches:
                key = item["phrase"].lower()

                if key not in seen:
                    unique_matches.append(item)
                    seen.add(key)

            found_categories[category] = unique_matches

    return found_categories


def calculate_risk_score(
    found_categories,
    expected,
    asks_sensitive,
    pressured
):
    # Category points and user-reported concerns both contribute.
    # Each category is counted only once.
    score = len(found_categories)

    if expected == "Unexpected":
        score += 1

    if asks_sensitive == "Yes":
        score += 2

    if pressured == "Yes":
        score += 2

    return min(score, 10)


def get_risk_label(score):
    if score <= 2:
        return "Few warning signs reported"
    elif score <= 4:
        return "Some warning signs reported"
    elif score <= 7:
        return "Several warning signs reported"
    return "Many warning signs reported"


def get_risk_explanation(score, found_categories):
    if not found_categories:
        return (
            "No matching warning phrases were found. Your answers may "
            "still point to concerns worth checking. The detector can "
            "miss scams that use different wording."
        )

    if score <= 2:
        return (
            "We found a small number of warning signs. This doesn't prove "
            "the message is safe, so check who sent it before trusting it."
        )

    if score <= 4:
        return (
            "There are things worth checking. Verify the sender and "
            "the request before clicking anything or sharing information."
        )

    if score <= 7:
        return (
            "Several warning signs or concerning circumstances were reported. "
            "Be careful and verify the request independently."
        )

    return (
        "Many warning signs or concerning circumstances were reported. "
        "Don't send money or share private information until you've "
        "independently verified the request."
    )


def show_analysis(message, expected, asks_sensitive, pressured):
    found_categories = find_warning_categories(message)

    score = calculate_risk_score(
        found_categories,
        expected,
        asks_sensitive,
        pressured
    )

    st.markdown("### Your results")
    st.caption("The score combines detected phrases with your answers.")

    with st.container(border=True):
        left, right = st.columns([1, 2])

        with left:
            st.metric("Warning signs score", f"{score}/10")
            st.progress(score / 10)

        with right:
            st.markdown(f"### {get_risk_label(score)}")
            st.write(get_risk_explanation(score, found_categories))

            if score >= 5:
                st.warning("Pause and verify the message before taking action.")
            elif score >= 3:
                st.info("Double-check the sender and the request.")
            else:
                st.info(
                    "A low score is not proof that a message is safe."
                )

    st.markdown("### What the message matched")

    if found_categories:
        for category, matches in found_categories.items():
            with st.container(border=True):
                st.markdown(f"**{category}**")
                st.write(category_explanations[category])

                for item in matches:
                    st.caption("Matched phrase")
                    st.text(item["phrase"])

                st.info(category_advice[category])
    else:
        st.write(
            "No phrases from our warning lists matched this message. "
            "That doesn't prove it is safe."
        )

    st.markdown("### What you told us")

    answers = [
        ("Expected message", expected),
        ("Sensitive information or money requested", asks_sensitive),
        ("Pressure or threats", pressured)
    ]

    for question, answer in answers:
        st.write(f"**{question}:** {answer}")

    st.markdown("### What to do next")

    advice = [
        "Don't click suspicious links or open unexpected attachments.",
        "Never share passwords or verification codes with someone who asks for them.",
        "Find the organization's official contact details yourself.",
        "If the message claims to be from someone you know, contact them another way."
    ]

    for item in advice:
        st.markdown(f"- {item}")

    st.caption(
        "This is a rule-based score, not a percentage chance that the "
        "message is a scam. 'Not sure' answers add no points."
    )


# Header

st.markdown("""
<div class="hero">
    <div class="eyebrow">Digital safety, made simpler</div>
    <div class="hero-title">Think twice.<br>Click smarter.</div>
    <div class="hero-description">
        For anyone who wants to check a suspicious text, email, or offer.
        Spot common scam warning signs before replying, clicking, or sharing information.
    </div>
    <span class="pill">Rule-based detection</span>
    <span class="pill">Interactive learning</span>
    <span class="pill">Practical safety tips</span>
</div>
""", unsafe_allow_html=True)

tab_check, tab_learn, tab_about = st.tabs([
    "Check a message",
    "Learn to spot scams",
    "How it works"
])


# Message checker

with tab_check:
    st.markdown(
        '<div class="section-heading">Check a suspicious message</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-subtitle">Paste the message and answer '
        'three quick questions for more context.</div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):
        message = st.text_area(
            "Message to check",
            placeholder="Paste a text message, email, or offer here...",
            height=180,
            key="message_input"
        )

        st.caption(
            "Don't include real passwords, verification codes, or other "
            "private information."
        )

        st.markdown("#### A little context")

        expected = st.radio(
            "Were you expecting this message?",
            ["Expected", "Unexpected", "Not sure"],
            horizontal=True,
            key="expected_input"
        )

        asks_sensitive = st.radio(
            "Does it ask for money, a password, a verification code, "
            "or personal information?",
            ["Yes", "No", "Not sure"],
            horizontal=True,
            key="sensitive_input"
        )

        pressured = st.radio(
            "Does it rush you, threaten you, or make you feel like "
            "you have to act right now?",
            ["Yes", "No", "Not sure"],
            horizontal=True,
            key="pressure_input"
        )

        analyze = st.button(
            "Analyze message",
            type="primary",
            use_container_width=True
        )

    if analyze:
        if not message.strip():
            st.warning("Paste a message first so there's something to check.")
        else:
            show_analysis(
                message,
                expected,
                asks_sensitive,
                pressured
            )


# Learning quiz

with tab_learn:
    st.markdown(
        '<div class="section-heading">Could you spot the scam?</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-subtitle">Practice with made-up messages. '
        'Some are obvious, and some need a closer look.</div>',
        unsafe_allow_html=True
    )

    examples = {
        "The fake delivery fee": {
            "message": (
                "Your package is on hold. Pay a small delivery fee now "
                "using this link to receive your package."
            ),
            "answer": "Likely scam",
            "explanation": (
                "It asks for money and encourages you to use a link. "
                "Check your delivery through the courier's official website."
            )
        },
        "The unexpected prize": {
            "message": (
                "Congratulations! You have won a $2,000 prize. "
                "Pay a processing fee to claim your reward."
            ),
            "answer": "Likely scam",
            "explanation": (
                "An unexpected prize requiring an upfront payment is a "
                "major warning sign. Verify the contest independently."
            )
        },
        "The account warning": {
            "message": (
                "We noticed unusual activity on your account. "
                "Open our official app to review your security."
            ),
            "answer": "Not enough information",
            "explanation": (
                "It could be legitimate, but scammers can copy these messages. "
                "Open the official app yourself instead of trusting a message link."
            )
        },
        "The gift card request": {
            "message": (
                "I need you to buy gift cards urgently and send me the codes. "
                "Please don't tell anyone."
            ),
            "answer": "Likely scam",
            "explanation": (
                "Urgency, gift card codes, and secrecy are major warning signs. "
                "Contact the person another way before doing anything."
            )
        },
        "The real library reminder": {
            "message": (
                "Reminder from Evergreen Valley Public Library: your borrowed "
                "book is due Friday. You can check your loan details by opening "
                "the library website you normally use."
            ),
            "answer": "Probably legitimate",
            "explanation": (
                "This message gives a routine reminder without asking for "
                "payment, passwords, or urgent action. In real life, the text "
                "alone can't prove who sent it, so check your library account "
                "through its usual official website if you're unsure."
            )
        }
    }

    selected_example = st.selectbox(
        "Choose a practice message",
        list(examples.keys())
    )

    example = examples[selected_example]

    with st.container(border=True):
        st.caption("EXAMPLE MESSAGE")
        st.markdown(f"**{selected_example}**")
        st.write(example["message"])

    answer = st.radio(
        "What do you think?",
        [
            "Likely scam",
            "Probably legitimate",
            "Not enough information"
        ],
        horizontal=True,
        key="learning_answer"
    )

    if st.button("Check my answer", use_container_width=True):
        if answer == example["answer"]:
            st.success("Correct! You picked the best answer for this example.")
        else:
            st.info(f"The best answer is: {example['answer']}.")

        st.write(example["explanation"])


# About the app

with tab_about:
    st.markdown(
        '<div class="section-heading">How it works</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-subtitle">A simple way to learn about '
        'common scam warning signs.</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-number">01</div>
            <div class="feature-title">Phrase detection</div>
            <div class="feature-text">
                The app checks for phrases linked to urgency, account
                problems, links, payments, prizes, and impersonation.
            </div>
        </div>
        <br>
        <div class="feature-card">
            <div class="feature-number">03</div>
            <div class="feature-title">Warning score</div>
            <div class="feature-text">
                Detected categories and your answers contribute to a score
                out of 10. This is a simple rule-based score, not a probability.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-number">02</div>
            <div class="feature-title">Context matters</div>
            <div class="feature-text">
                Your answers about unexpected messages, sensitive requests,
                and pressure add context to the results.
            </div>
        </div>
        <br>
        <div class="feature-card">
            <div class="feature-number">04</div>
            <div class="feature-title">Practical advice</div>
            <div class="feature-text">
                The app shows matched phrases and suggests safer next steps
                instead of giving you a number with no explanation.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Who is this for?")

    st.write(
        "Scam Detector is designed for everyday users, including teens, "
        "families, and older adults who want help recognizing common scam "
        "warning signs in messages."
    )

    st.markdown("### What it can't do")

    st.write(
        "This is a rule-based prototype, not an AI scam detector. It can't "
        "confirm who sent a message, verify a website, or catch every scam. "
        "It may also flag harmless messages that contain certain phrases."
    )

    st.markdown("### Privacy")

    st.write(
        "This code does not intentionally save messages to a database or "
        "send them to an AI service. The hosting platform may have its own "
        "logging policies, so don't enter sensitive personal information."
    )

    st.markdown("### A note about the score")

    st.write(
        "The score combines detected warning categories with the answers "
        "provided by the user. 'Not sure' answers add no points. The score "
        "is not a probability that the message is a scam."
    )


st.markdown("""
<div class="footer">
    Built to help people recognize scam warning signs.<br>
    Not every suspicious message is a scam, and not every scam looks suspicious.
</div>
""", unsafe_allow_html=True)
