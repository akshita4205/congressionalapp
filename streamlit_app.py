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
        "This message may be trying to rush you so you don't have time "
        "to think things through. Scammers do this because a panicked "
        "person is more likely to act without checking.",

    "Account or identity concerns":
        "This brings up your account or personal information. That isn't "
        "automatically a scam, but be especially careful with passwords "
        "and verification codes. Those are not things to hand over just "
        "because a message asks.",

    "Suspicious links":
        "This wording encourages you to open a link. The link might be "
        "harmless, but don't assume that. Go to the organization's "
        "official website yourself instead.",

    "Money or payment requests":
        "This message mentions money or a payment. Before sending anything, "
        "check who is asking and whether the request actually makes sense.",

    "Unusual payment methods":
        "Gift cards and cryptocurrency are difficult or sometimes "
        "impossible to recover once sent. If someone insists you pay "
        "this way, take a step back and check the request.",

    "Unexpected prizes or offers":
        "This mentions a prize or an offer. If you supposedly won something "
        "you never entered, especially if you have to pay first, be careful.",

    "Possible impersonation":
        "Someone could be pretending to be a person or organization you "
        "trust. A familiar name or official-sounding message doesn't prove "
        "it's real. Check through a separate contact method."
}

category_advice = {
    "Urgency or pressure":
        "Take a second before doing anything. A message saying 'right now' "
        "doesn't mean you actually have to act right now.",

    "Account or identity concerns":
        "Don't share passwords or verification codes. If you're worried "
        "about your account, visit the official website yourself or call "
        "the number on your bank card.",

    "Suspicious links":
        "Don't blindly trust a link just because it looks convincing. "
        "Find the organization's official website yourself.",

    "Money or payment requests":
        "Check who is asking, why they need the money, and whether you "
        "can confirm the request another way.",

    "Unusual payment methods":
        "Pause before paying with gift cards or crypto. Check the request "
        "with someone you trust or contact the organization directly.",

    "Unexpected prizes or offers":
        "Don't pay a random fee or share private information just to claim "
        "a prize. A message promising free money can still cost you.",

    "Possible impersonation":
        "Contact the person or organization another way. Don't rely on "
        "the phone number or link in the message you're checking."
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
        return "A few warning signs"
    elif score <= 4:
        return "Some things look suspicious"
    elif score <= 7:
        return "Several warning signs"
    return "A lot of warning signs"


def get_risk_explanation(score, found_categories):
    if not found_categories:
        return (
            "We didn't find any of the warning phrases we're looking for. "
            "That doesn't automatically make the message safe, though. "
            "Scammers can word things in all sorts of ways, and your "
            "answers may still point to something worth checking."
        )

    if score <= 2:
        return (
            "We found a couple of things worth noticing. This doesn't prove "
            "the message is a scam, but don't trust it just because the "
            "score is low. Check who sent it first."
        )

    if score <= 4:
        return (
            "There are a few things here worth checking. Before clicking "
            "anything or sharing information, make sure the sender and "
            "the request are actually legitimate."
        )

    if score <= 7:
        return (
            "Several warning signs showed up, either in the message itself "
            "or in your answers. Don't rush into anything. Check the "
            "request through a source you know you can trust."
        )

    return (
        "There are quite a few reasons to be careful here. Don't send money "
        "or share private information until you've checked the request "
        "independently. It's better to spend an extra minute checking "
        "than to regret trusting the message."
    )


def show_analysis(message, expected, asks_sensitive, pressured):
    found_categories = find_warning_categories(message)

    score = calculate_risk_score(
        found_categories,
        expected,
        asks_sensitive,
        pressured
    )

    st.markdown("### Here's what we found")
    st.caption(
        "Your score combines phrases in the message with the answers you gave."
    )

    with st.container(border=True):
        left, right = st.columns([1, 2])

        with left:
            st.metric("Warning signs score", f"{score}/10")
            st.progress(score / 10)

        with right:
            st.markdown(f"### {get_risk_label(score)}")
            st.write(get_risk_explanation(score, found_categories))

            if score >= 5:
                st.warning(
                    "Pause before doing anything. Check the message first."
                )
            elif score >= 3:
                st.info(
                    "A couple of things deserve a closer look. Check the sender."
                )
            else:
                st.info(
                    "The score is low, but that doesn't guarantee the "
                    "message is safe."
                )

    st.markdown("### What caught our attention")

    if found_categories:
        for category, matches in found_categories.items():
            with st.container(border=True):
                st.markdown(f"**{category}**")
                st.write(category_explanations[category])

                for item in matches:
                    st.caption("What we noticed")
                    st.text(item["phrase"])

                st.info(category_advice[category])
    else:
        st.write(
            "Nothing from our warning lists matched the message. That can "
            "be reassuring, but it isn't proof that everything is fine. "
            "A scam can still slip through if it uses different wording."
        )

    st.markdown("### Your answers")

    answers = [
        ("Were you expecting this message?", expected),
        ("Did it ask for money or private information?", asks_sensitive),
        ("Did it pressure or threaten you?", pressured)
    ]

    for question, answer in answers:
        st.write(f"**{question}** {answer}")

    st.markdown("### What you can do next")

    advice = [
        "Don't click links or open attachments if something feels off.",
        "Never give someone your password or verification code just because they ask.",
        "If a message claims to be from a company, visit its official website yourself.",
        "If it supposedly came from someone you know, check with them another way.",
        "If you're still unsure, ask someone you trust before doing anything."
    ]

    for item in advice:
        st.markdown(f"- {item}")

    st.caption(
        "This is a rule-based score, not a percentage chance that the "
        "message is a scam. 'Not sure' answers don't add points."
    )


st.markdown("""
<div class="hero">
    <div class="eyebrow">Digital safety, without the guesswork</div>
    <div class="hero-title">Think twice.<br>Click smarter.</div>
    <div class="hero-description">
        Got a message that feels a little off? Paste it here and let's
        look at it. Scam Detector checks for common warning signs and
        helps you figure out what to look out for before you click,
        reply, or share anything.
    </div>
    <span class="pill">Checks common warning signs</span>
    <span class="pill">Explains what it finds</span>
    <span class="pill">Helps you learn as you go</span>
</div>
""", unsafe_allow_html=True)

tab_check, tab_learn, tab_about = st.tabs([
    "Check a message",
    "Learn to spot scams",
    "How it works"
])


with tab_check:
    st.markdown(
        '<div class="section-heading">Something seem off?</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-subtitle">Paste the message below. '
        "We'll check for common warning signs, and your answers will "
        'help put things into context.</div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):
        message = st.text_area(
            "Message to check",
            placeholder="Paste a suspicious text, email, or offer here...",
            height=180,
            key="message_input"
        )

        st.caption(
            "Quick reminder: leave out real passwords, verification codes, "
            "and other private information."
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
            "Check this message",
            type="primary",
            use_container_width=True
        )

    if analyze:
        if not message.strip():
            st.warning("Paste a message first. We need something to check.")
        else:
            show_analysis(
                message,
                expected,
                asks_sensitive,
                pressured
            )


with tab_learn:
    st.markdown(
        '<div class="section-heading">Can you spot the scam?</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-subtitle">Try a few made-up messages. '
        "Some are pretty obvious. Others need a little more thought. "
        'That is kind of the point.</div>',
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
                "This asks you to pay a fee and pushes you toward a link. "
                "Don't use the link to check your delivery. Go to the "
                "courier's official website yourself and see if anything "
                "actually needs your attention."
            )
        },
        "The unexpected prize": {
            "message": (
                "Congratulations! You have won a $2,000 prize. "
                "Pay a processing fee to claim your reward."
            ),
            "answer": "Likely scam",
            "explanation": (
                "You supposedly won money, but first you have to pay money. "
                "That should make you suspicious. Check whether the contest "
                "is real, and don't pay a fee just to claim an unexpected prize."
            )
        },
        "The account warning": {
            "message": (
                "We noticed unusual activity on your account. "
                "Open our official app to review your security."
            ),
            "answer": "Not enough information",
            "explanation": (
                "This one could be legitimate. Companies really do send "
                "security alerts, but scammers can copy them too. Open the "
                "app you normally use yourself instead of trusting a link "
                "in a message."
            )
        },
        "The gift card request": {
            "message": (
                "I need you to buy gift cards urgently and send me the codes. "
                "Please don't tell anyone."
            ),
            "answer": "Likely scam",
            "explanation": (
                "The urgency, gift card codes, and request for secrecy are "
                "all warning signs. Someone who asks you to pay this way "
                "could be trying to make the money difficult to recover. "
                "Check with the person another way before doing anything."
            )
        },
        "The library reminder": {
            "message": (
                "Reminder from Evergreen Valley Public Library: your borrowed "
                "book is due Friday. You can check your loan details by opening "
                "the library website you normally use."
            ),
            "answer": "Probably legitimate",
            "explanation": (
                "This looks like a routine reminder. It doesn't demand money, "
                "ask for a password, or threaten you. In real life, though, "
                "a normal-sounding message can still be copied by a scammer. "
                "If you're unsure, check your library account through its "
                "usual official website."
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
        "What's your best guess?",
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
            st.success(
                "Correct! You picked the best answer for this example."
            )
        else:
            st.info(
                f"The best answer here is: {example['answer']}."
            )

        st.write(example["explanation"])


with tab_about:
    st.markdown(
        '<div class="section-heading">So, how does this work?</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        "<div class='section-subtitle'>Here's what the app checks, "
        'what the score means, and where its limits are.</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-number">01</div>
            <div class="feature-title">Looks for warning signs</div>
            <div class="feature-text">
                The app checks the message for phrases linked to pressure,
                account problems, suspicious links, payment requests,
                unexpected prizes, and possible impersonation.
            </div>
        </div>
        <br>
        <div class="feature-card">
            <div class="feature-number">03</div>
            <div class="feature-title">Gives you a score</div>
            <div class="feature-text">
                The detected categories and your answers contribute to
                a score out of 10. It helps summarize the warning signs,
                but it is not a probability that the message is a scam.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-number">02</div>
            <div class="feature-title">Takes your answers into account</div>
            <div class="feature-text">
                Whether you expected the message, whether it asks for
                sensitive information, and whether it pressures you can
                all change the result. Context matters.
            </div>
        </div>
        <br>
        <div class="feature-card">
            <div class="feature-number">04</div>
            <div class="feature-title">Explains what to look out for</div>
            <div class="feature-text">
                Instead of just giving you a number and leaving you to
                figure out what it means, the app explains the warning
                signs it found and what you can do next.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Who is this for?")

    st.write(
        "Scam Detector is for everyday people who want a little help "
        "figuring out whether a message seems suspicious. That includes "
        "teens, families, and older adults. You don't need to know anything "
        "about cybersecurity to use it."
    )

    st.markdown("### What it can't do")

    st.write(
        "This is a rule-based prototype, not an AI scam detector. It looks "
        "for specific phrases and known shortened-link domains, so it can "
        "miss scams that use different wording. It can also flag a perfectly "
        "harmless message just because it contains a suspicious-sounding "
        "phrase. It can't confirm who sent a message or prove that a website "
        "is safe. Use the result as a starting point, not a final verdict."
    )

    st.markdown("### What about privacy?")

    st.write(
        "The code doesn't intentionally save messages to a database or send "
        "them to an AI service. However, the platform hosting the app may "
        "have its own logging policies. To be safe, don't paste real "
        "passwords, verification codes, or other sensitive information."
    )

    st.markdown("### How should I read the score?")

    st.write(
        "The score combines the warning categories found in the message "
        "with the answers you give. Each category counts once, even if "
        "several phrases from that category appear. Answering 'Not sure' "
        "doesn't add points. The score is not a percentage chance that "
        "the message is a scam, and a low score doesn't guarantee safety."
    )


st.markdown("""
<div class="footer">
    A little caution can go a long way.<br>
    Not every suspicious message is a scam, and not every scam looks suspicious.
</div>
""", unsafe_allow_html=True)
