import re
import streamlit as st

st.set_page_config(
    page_title="Scam Detector",
    page_icon="🔎",
    layout="centered"
)

st.title("Scam Detector")

st.write(
    "Found a message that feels a little off? Paste it here and "
    "let's see if anything looks suspicious before you accidentally get scammed."
)

st.caption(
    "This checks for common scam warning signs, but it can't tell you "
    "for sure if something is a scam. Scammers can be pretty creative, unfortunately."
)

st.divider()

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
        "open this link", "verify here", "http://",
        "https://", "bit.ly", "tinyurl.com", "t.co",
        "free-gift", "claim your reward"
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
        "They're trying to rush you into doing something. Scammers do this "
        "because you're less likely to stop and think if you feel pressured.",

    "Account or identity concerns":
        "This mentions your account or personal information. Be careful with "
        "passwords and verification codes, even if the message looks legit.",

    "Suspicious links":
        "There's a link or wording related to links here. That doesn't "
        "automatically mean it's dangerous, but don't click it just to find out.",

    "Money or payment requests":
        "This mentions money or some kind of payment. Double-check who's "
        "asking before sending anything. Losing money over a fake message is not it.",

    "Unusual payment methods":
        "Scammers sometimes ask for gift cards or crypto because getting "
        "that money back can be really difficult.",

    "Unexpected prizes or offers":
        "This mentions a prize or offer. If you never entered anything or "
        "have to pay money to claim it, that's a pretty big red flag.",

    "Possible impersonation":
        "Someone might be pretending to be a person or organization you trust. "
        "Check with them another way instead of just trusting the message."
}

category_advice = {
    "Urgency or pressure":
        "Take a second. You don't need to panic just because some random "
        "message is acting like the world ends in five minutes.",

    "Account or identity concerns":
        "Don't share passwords or verification codes. Go to the official "
        "website yourself or call the number on your bank card.",

    "Suspicious links":
        "Don't click random links. Find the organization's actual website "
        "yourself instead of trusting whatever link they sent you.",

    "Money or payment requests":
        "Don't send money until you've actually checked who's asking and why.",

    "Unusual payment methods":
        "Pause before paying with gift cards or crypto. If something feels "
        "off, ask someone you trust before doing anything.",

    "Unexpected prizes or offers":
        "Don't pay some random fee or give away personal information just "
        "to claim a prize. That prize might not even exist.",

    "Possible impersonation":
        "Contact the person or organization another way. Don't use the "
        "phone number or contact details from the suspicious message itself."
}


def find_warning_categories(message):
    found_categories = {}
    message_lower = message.lower()

    for category, phrases in warning_categories.items():
        matches = []

        for phrase in phrases:
            pattern = r"(?<!\w)" + re.escape(phrase) + r"(?!\w)"

            for match in re.finditer(pattern, message_lower):
                start = max(0, match.start() - 45)
                end = min(len(message), match.end() + 45)

                matches.append({
                    "phrase": message[match.start():match.end()],
                    "context": message[start:end].replace("\n", " ")
                })

                break

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

    if expected == "Unexpected":
        score += 1

    if asks_sensitive == "Yes":
        score += 2

    if pressured == "Yes":
        score += 2

    return min(score, 10)


def get_risk_label(score):
    if score <= 2:
        return "Not many warning signs found"
    elif score <= 4:
        return "Some warning signs found"
    elif score <= 7:
        return "Quite a few warning signs found"
    return "A lot of warning signs found"


def get_risk_explanation(score):
    if score <= 2:
        return (
            "We didn't find many warning signs, but that doesn't mean "
            "the message is automatically safe. Don't let the low score "
            "make you trust it without checking."
        )
    elif score <= 4:
        return (
            "There's some stuff worth checking here. Make sure you know "
            "who sent the message before clicking anything or sharing info."
        )
    elif score <= 7:
        return (
            "This message has quite a few warning signs. I'd be careful "
            "and definitely check who's behind it before doing anything."
        )
    return (
        "This message has a lot of warning signs. Don't send money or "
        "share private information until you've checked that the request "
        "is actually real."
    )


def show_analysis(message, expected, asks_sensitive, pressured):
    found_categories = find_warning_categories(message)

    score = calculate_risk_score(
        found_categories,
        expected,
        asks_sensitive,
        pressured
    )

    st.divider()
    st.subheader("Here's what we found")

    st.metric("Warning signs score", f"{score}/10")
    st.write(f"**{get_risk_label(score)}**")
    st.write(get_risk_explanation(score))

    if found_categories:
        st.subheader("What looks suspicious")

        for category, matches in found_categories.items():
            st.markdown(f"**{category}**")
            st.write(category_explanations[category])

            for item in matches:
                st.caption(f"Phrase found: {item['phrase']}")
                st.code(item["context"], language=None)

            st.info(category_advice[category])

    else:
        st.write(
            "Okay, we didn't find any of the warning phrases we were "
            "looking for. That doesn't mean the message is safe, though. "
            "Scams can be worded in all sorts of ways, and our detector "
            "won't catch every single one."
        )

    if expected == "Unexpected":
        st.warning(
            "You weren't expecting this message, so double-check who sent "
            "it before replying or clicking anything."
        )

    if asks_sensitive == "Yes":
        st.warning(
            "It's asking for money or sensitive information. Don't hand "
            "over anything until you've checked that the request is real."
        )

    if pressured == "Yes":
        st.warning(
            "You noticed pressure or threats. Take a step back and think "
            "it through instead of letting some message rush you."
        )

    st.divider()
    st.subheader("What you should do next")

    advice = [
        "Don't click suspicious links or open random attachments.",
        "Don't share passwords, verification codes, or financial information.",
        "Find the organization's official contact details yourself and check with them.",
        "If the message claims to be from someone you know, contact them another way."
    ]

    for i, item in enumerate(advice, start=1):
        st.write(f"{i}. {item}")

    st.caption(
        "The score is based on the rules in this app. It's not an actual "
        "percentage chance that the message is a scam."
    )


tab_check, tab_learn, tab_about = st.tabs([
    "Check a message",
    "Learn to spot scams",
    "How it works"
])


with tab_check:
    message = st.text_area(
        "Paste the suspicious message here",
        placeholder="Paste the text message, email, or offer here...",
        height=180,
        key="message_input"
    )

    st.subheader("A few quick questions")

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
        "you HAVE to do something right now?",
        ["Yes", "No", "Not sure"],
        horizontal=True,
        key="pressure_input"
    )

    if st.button("Check this message", type="primary"):
        if not message.strip():
            st.warning(
                "You have to actually paste something first. "
                "We can't analyze an empty box."
            )
        else:
            show_analysis(
                message,
                expected,
                asks_sensitive,
                pressured
            )

    st.caption(
        "Privacy note: This version checks the text using rules built into "
        "the app. Don't paste passwords, verification codes, or other "
        "private information here."
    )


with tab_learn:
    st.subheader("Learn to spot scams")

    st.write(
        "Think you can spot a scam? Try these made-up examples and see "
        "what you catch. Some messages aren't that obvious, which is the point."
    )

    examples = {
        "The fake delivery fee": {
            "message": (
                "Your package is on hold. Pay a small delivery fee now "
                "using this link to receive your package."
            ),
            "answer": "Likely scam",
            "explanation": (
                "It's rushing you, asking for money, and sending you a link. "
                "Check your delivery through the courier's official website "
                "instead of clicking the link."
            )
        },
        "The unexpected prize": {
            "message": (
                "Congratulations! You have won a $2,000 prize. "
                "Pay a processing fee to claim your reward."
            ),
            "answer": "Likely scam",
            "explanation": (
                "A random prize that requires you to pay first is a major "
                "warning sign. Don't pay until you've independently checked "
                "whether the contest is real."
            )
        },
        "The account warning": {
            "message": (
                "We noticed unusual activity on your account. "
                "Use our official app or website to review your security."
            ),
            "answer": "Not enough information",
            "explanation": (
                "This could be a real warning, but scammers can copy these "
                "messages too. Open the official app or website yourself "
                "instead of trusting a link in an unexpected message."
            )
        },
        "The gift card request": {
            "message": (
                "I need you to buy gift cards urgently and send me the codes. "
                "Please don't tell anyone."
            ),
            "answer": "Likely scam",
            "explanation": (
                "Urgency, gift card codes, and secrecy are all major warning "
                "signs. Contact the person another way before doing anything."
            )
        },
        "The library reminder": {
            "message": (
                "Reminder: your library book is due Friday. "
                "You can renew it through the library website."
            ),
            "answer": "Not enough information",
            "explanation": (
                "This doesn't have many obvious warning signs, but that "
                "doesn't prove it's real. If you're unsure, visit the "
                "library's official website yourself."
            )
        }
    }

    selected_example = st.selectbox(
        "Choose an example",
        list(examples.keys())
    )

    example = examples[selected_example]

    st.markdown("**Here's the message:**")
    st.code(example["message"], language=None)

    answer = st.radio(
        "What do you think?",
        [
            "Likely scam",
            "Probably legitimate",
            "Not enough information"
        ],
        key="learning_answer"
    )

    if st.button("Check my answer"):
        if answer == example["answer"]:
            st.success("Correct! You're actually looking at the warning signs.")
        else:
            st.info(
                f"The best answer is: {example['answer']}. "
                "Not every message is obvious, so look at the whole situation "
                "instead of judging it based on one word."
            )

        st.write(example["explanation"])


with tab_about:
    st.subheader("How does this thing work?")

    st.markdown(
        """
        1. It looks for suspicious phrases

        The app checks your message for phrases linked to urgency, account
        problems, links, payments, unexpected prizes, and possible scams.

        2. Your answers matter too

        It also looks at whether you expected the message, whether it asks
        for sensitive information, and whether it's trying to rush you.

        3. It gives you a warning score

        The app combines the categories it finds with your answers. The score
        goes up to 10, but it's not a real percentage chance of getting scammed.

        4. It explains what it found

        Instead of just throwing a number at you and calling it a day, the
        app shows the phrases it picked up and gives you advice on what to do.
        """
    )

    st.subheader("What it can't do")

    st.write(
        "It can't confirm who sent a message, check whether a website is safe, "
        "or catch every possible scam. It might miss a scam or flag a message "
        "that's completely fine. Basically, use it as a warning system, "
        "not as proof that something is safe or dangerous."
    )

    st.subheader("What about privacy?")

    st.write(
        "This code doesn't intentionally save your message to a database "
        "or send it to an AI service. It checks the text using Python rules. "
        "The hosting platform may have its own logging policies, though, "
        "so don't paste private information into the app."
    )


st.divider()

st.caption(
    "Made to help people spot scam warning signs. Not every suspicious "
    "message is a scam, and not every scam looks suspicious."
)
```
