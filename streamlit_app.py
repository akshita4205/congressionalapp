import re
import streamlit as st

st.set_page_config(
    page_title="Scam Detector",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --bg: #0b1120;
    --panel: #121c30;
    --panel-light: #18253b;
    --teal: #42e8c5;
    --text: #edf3ff;
    --muted: #9aabc5;
}

.stApp {
    background:
        radial-gradient(ellipse at 10% 0%, #142b3c 0%, transparent 40%),
        linear-gradient(180deg, #0b1120 0%, #0d1424 100%);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stToolbar"] {
    right: 1rem;
}

.block-container {
    max-width: 1050px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

h1, h2, h3, h4 {
    font-family: 'Space Grotesk', sans-serif !important;
    letter-spacing: -0.5px;
}

h1 {
    color: #f4f7ff !important;
    font-size: 2.7rem !important;
    font-weight: 700 !important;
}

h2, h3 {
    color: #f0f5ff !important;
}

p, label, li {
    color: #d4deef;
}

small, [data-testid="stCaptionContainer"] {
    color: var(--muted) !important;
}

.hero {
    background: linear-gradient(135deg, #14283a 0%, #132039 60%, #19233b 100%);
    border: 1px solid #294459;
    border-radius: 22px;
    padding: 30px 32px;
    margin-bottom: 26px;
    position: relative;
    overflow: hidden;
}

.hero:after {
    content: "";
    position: absolute;
    width: 190px;
    height: 190px;
    border-radius: 50%;
    background: #42e8c5;
    opacity: 0.06;
    right: -40px;
    top: -65px;
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
    font-size: 1.02rem;
    line-height: 1.7;
    max-width: 650px;
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

div[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
    background: #42e8c5;
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

div[data-testid="stRadio"] label {
    color: #d5dfef;
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

div.stButton > button:focus {
    box-shadow: 0 0 0 2px #0b1120, 0 0 0 4px #42e8c5;
}

div[data-testid="stMetric"] {
    background: #121e31;
    border: 1px solid #2a3b54;
    padding: 18px;
    border-radius: 15px;
}

div[data-testid="stMetricLabel"] {
    color: #a8b8d0;
}

div[data-testid="stMetricValue"] {
    color: #55ebcb;
    font-family: 'Space Grotesk', sans-serif;
}

div[data-testid="stProgressBar"] > div {
    background: #24334a;
    border-radius: 20px;
}

div[data-testid="stProgressBar"] > div > div {
    background: #42e8c5;
    border-radius: 20px;
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(18, 28, 48, 0.72);
    border-color: #283951;
    border-radius: 16px;
}

div[data-testid="stCode"] {
    border: 1px solid #2a3c55;
    border-radius: 10px;
}

hr {
    border-color: #24334a;
}

.footer {
    text-align: center;
    color: #7f91ad;
    font-size: 0.83rem;
    padding: 24px 0 0;
    line-height: 1.8;
}

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

</style>
""", unsafe_allow_html=True)


# Scam warning phrases

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
        "security code", "one-time passcode", "one time passcode",
        "ssn", "bank details"
    ],
    "Suspicious links": [
        "click here", "tap here", "click the link",
        "open this link", "verify here", "bit.ly",
        "tinyurl.com", "t.co", "free-gift", "claim your reward"
    ],
    "Money or payment requests": [
        "send money", "wire transfer", "pay now",
        "payment required", "gift card", "bank account",
        "processing fee", "transfer funds", "pay a fee",
        "send payment", "outstanding balance",
        "refund", "overdue payment"
    ],
    "Unusual payment methods": [
        "bitcoin", "cryptocurrency", "crypto",
        "prepaid card", "gift cards", "send the code",
        "payment through gift cards", "crypto wallet"
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
        "police department", "gift card code",
        "keep this confidential", "don't tell anyone",
        "do not tell anyone", "i am stranded",
        "urgent favor", "send me the code"
    ]
}

category_explanations = {
    "Urgency or pressure":
        "This message may be trying to rush you into acting before you "
        "have time to think. That is a common scam tactic.",

    "Account or identity concerns":
        "This mentions an account or personal information. Be careful with "
        "passwords and verification codes, even if the message looks real.",

    "Suspicious links":
        "This message contains a link or wording related to links. That "
        "doesn't automatically make it dangerous, but don't click it to find out.",

    "Money or payment requests":
        "This mentions money or a payment. Double-check who's asking "
        "before sending anything.",

    "Unusual payment methods":
        "Scammers sometimes ask for gift cards or cryptocurrency because "
        "getting that money back can be difficult.",

    "Unexpected prizes or offers":
        "This mentions a prize or offer. If you never entered anything "
        "or have to pay to claim it, that's a warning sign.",

    "Possible impersonation":
        "Someone could be pretending to be a person or organization you "
        "trust. Check with them through a separate contact method."
}

category_advice = {
    "Urgency or pressure":
        "Take a second. You don't need to panic just because a message "
        "acts like the world ends in five minutes.",

    "Account or identity concerns":
        "Don't share passwords or verification codes. Visit the official "
        "website yourself or call the number on your bank card.",

    "Suspicious links":
        "Don't click random links. Find the organization's official "
        "website yourself instead.",

    "Money or payment requests":
        "Don't send money until you've checked who's asking and why.",

    "Unusual payment methods":
        "Pause before paying with gift cards or crypto. Verify the request "
        "through another trusted source.",

    "Unexpected prizes or offers":
        "Don't pay a random fee or give away personal information just "
        "to claim a prize.",

    "Possible impersonation":
        "Contact the person or organization another way. Don't rely on "
        "contact details in the suspicious message."
}


def find_warning_categories(message):
    found_categories = {}
    message_lower = message.lower()

    for category, phrases in warning_categories.items():
        matches = []
        seen = set()

        for phrase in phrases:
            if phrase in ("bit.ly", "tinyurl.com", "t.co"):
                pattern = re.escape(phrase)
            else:
                pattern = r"(?<!\w)" + re.escape(phrase) + r"(?!\w)"

            match = re.search(pattern, message_lower)

            if match and phrase not in seen:
                start = max(0, match.start() - 45)
                end = min(len(message), match.end() + 45)

                matches.append({
                    "phrase": message[match.start():match.end()],
                    "context": message[start:end].replace("\n", " ")
                })

                seen.add(phrase)

        if category == "Suspicious links":
            url_match = re.search(r"https?://\S+", message)

            if url_match:
                url = url_match.group().rstrip(".,!?;:)")

                if url.lower() not in seen:
                    start = max(0, url_match.start() - 45)
                    end = min(len(message), url_match.end() + 45)

                    matches.append({
                        "phrase": url,
                        "context": message[start:end].replace("\n", " ")
                    })

        if matches:
            found_categories[category] = matches

    return found_categories


def calculate_risk_score(
    found_categories,
    expected,
    asks_sensitive,
    pressured
):
    score = len(found_categories)

    # Context answers add points only when the message has detected
    # warning signs, so unrelated gibberish doesn't score highly.
    if found_categories:
        if expected == "Unexpected":
            score += 1

        if asks_sensitive == "Yes":
            score += 2

        if pressured == "Yes":
            score += 2

    return min(score, 10)


def get_risk_label(score):
    if score <= 2:
        return "Few warning signs detected"
    elif score <= 4:
        return "Some warning signs detected"
    elif score <= 7:
        return "Several warning signs detected"
    return "Many warning signs detected"


def get_risk_explanation(score):
    if score <= 2:
        return (
            "We didn't find many warning signs. That doesn't prove the "
            "message is safe, so check who sent it before trusting it."
        )
    elif score <= 4:
        return (
            "There are a few things worth checking. Make sure you know "
            "who sent the message before clicking anything or sharing info."
        )
    elif score <= 7:
        return (
            "This message has several warning signs. Be careful and verify "
            "the sender before doing anything."
        )
    return (
        "This message has many warning signs. Don't send money or share "
        "private information until you've independently verified the request."
    )


def show_analysis(message, expected, asks_sensitive, pressured):
    found_categories = find_warning_categories(message)

    score = calculate_risk_score(
        found_categories,
        expected,
        asks_sensitive,
        pressured
    )

    st.markdown('<div class="section-heading">Your results</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Here are the warning signs '
        'we found in your message.</div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):
        left, right = st.columns([1, 2])

        with left:
            st.metric("Warning signs score", f"{score}/10")
            st.progress(score / 10)

        with right:
            st.markdown(f"### {get_risk_label(score)}")
            st.write(get_risk_explanation(score))

            if score >= 5:
                st.warning("Pause and verify the message before taking action.")
            elif score >= 3:
                st.info("Double-check the sender and the request.")
            else:
                st.success(
                    "Few warning signs detected. This is not proof "
                    "that the message is safe."
                )

    if found_categories:
        st.markdown("### What stood out")

        for category, matches in found_categories.items():
            with st.container(border=True):
                st.markdown(f"**{category}**")
                st.write(category_explanations[category])

                for item in matches:
                    st.caption(f"Matched phrase: {item['phrase']}")
                    st.code(item["context"], language=None)

                st.info(category_advice[category])
    else:
        with st.container(border=True):
            st.markdown("### No matching warning phrases")
            st.write(
                "We didn't find any of the phrases this app checks for. "
                "That doesn't mean the message is safe. Scams can be worded "
                "in many different ways, and this detector won't catch every one."
            )

    if expected == "Unexpected":
        st.warning(
            "You weren't expecting this message. Double-check who sent it."
        )

    if asks_sensitive == "Yes":
        st.warning(
            "You indicated that it asks for money or sensitive information. "
            "Verify the request before sharing anything."
        )

    if pressured == "Yes":
        st.warning(
            "You noticed pressure or threats. Take your time instead of "
            "letting the message rush you."
        )

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
        "This score is based on simple rules and your answers. It is not "
        "a percentage chance that the message is a scam."
    )


# Main header

st.markdown("""
<div class="hero">
    <div class="eyebrow">Digital safety, made simpler</div>
    <div class="hero-title">Think twice.<br>Click smarter.</div>
    <div class="hero-description">
        Got a message that feels a little off? Check it for common scam
        warning signs before you reply, click, or share anything.
    </div>
    <span class="pill">Rule-based detection</span>
    <span class="pill">Privacy-conscious design</span>
    <span class="pill">Built for real-world awareness</span>
</div>
""", unsafe_allow_html=True)

tab_check, tab_learn, tab_about = st.tabs([
    "Check a message",
    "Learn to spot scams",
    "How it works"
])


# Check a message

with tab_check:
    st.markdown(
        '<div class="section-heading">Check a suspicious message</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-subtitle">Paste the message below, '
        'then answer three quick questions for more context.</div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):
        message = st.text_area(
            "Message to check",
            placeholder=(
                "Paste a text message, email, or offer here..."
            ),
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


# Learn to spot scams

with tab_learn:
    st.markdown(
        '<div class="section-heading">Could you spot the scam?</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-subtitle">Practice with made-up examples. '
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
                "It asks for money and tries to get you to use a link. "
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
                "An unexpected prize that requires an upfront payment is "
                "a major warning sign. Verify the contest independently."
            )
        },
        "The account warning": {
            "message": (
                "We noticed unusual activity on your account. "
                "Use our official app or website to review your security."
            ),
            "answer": "Not enough information",
            "explanation": (
                "It could be legitimate, but scammers can copy these messages. "
                "Open the official app or website yourself."
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
        "The library reminder": {
            "message": (
                "Reminder: your library book is due Friday. "
                "You can renew it through the library website."
            ),
            "answer": "Not enough information",
            "explanation": (
                "There are few obvious warning signs, but that doesn't prove "
                "it's real. Visit the library's official website yourself."
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
        '<div class="section-subtitle">The app looks for warning signs '
        'and explains what you should pay attention to.</div>',
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
                problems, suspicious links, payments, prizes, and impersonation.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <div class="feature-number">03</div>
            <div class="feature-title">Warning score</div>
            <div class="feature-text">
                Detected categories and your answers contribute to a score
                out of 10. It is a simple rule-based score, not a probability.
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
                and pressure help add context to the analysis.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <div class="feature-number">04</div>
            <div class="feature-title">Practical advice</div>
            <div class="feature-text">
                Instead of just showing a number, the app highlights matched
                phrases and suggests safer next steps.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### What it can't do")

    st.write(
        "This is a rule-based prototype, not an AI scam detector. It can't "
        "confirm who sent a message, verify a website, or catch every scam. "
        "It can also flag harmless messages that happen to contain certain phrases."
    )

    st.markdown("### Privacy")

    st.write(
        "This code does not intentionally save your message to a database "
        "or send it to an AI service. The hosting platform may have its own "
        "logging policies, so don't enter sensitive personal information."
    )


st.markdown("""
<div class="footer">
    Built to help people recognize scam warning signs.<br>
    Not every suspicious message is a scam, and not every scam looks suspicious.
</div>
""", unsafe_allow_html=True)
