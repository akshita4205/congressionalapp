import streamlit as st
import re

st.set_page_config(
    page_title="Scam Detector",
    layout="centered"
)

st.title("Scam Detector")
st.write(
    "Gottt a message that feels a little off? Paste it here and "
    "we'll check it for common scam warning signs. Because apparently "
    "we have to be suspicious of everything now."
)

st.caption(
    "This tool checks for common warning signs. It can't guarantee "
    "whether a message is real or a scam."
)

message = st.text_area(
    "Paste the suspicious message here",
    placeholder="Paste the text message, email, or offer here...",
    height=180
)

st.subheader("A few quick questions")

expected = st.radio(
    "Were you expecting this message?",
    ["Yes", "No", "Not sure"],
    horizontal=True
)

asks_sensitive = st.radio(
    "Does it ask for money, your password, a verification code, "
    "or personal information?",
    ["Yes", "No", "Not sure"],
    horizontal=True
)

pressured = st.radio(
    "Does it rush you, threaten you, or make you feel like "
    "you HAVE to act right now?",
    ["Yes", "No", "Not sure"],
    horizontal=True
)

warning_categories = {
    "Urgency or pressure": [
        "act now",
        "immediately",
        "urgent",
        "limited time",
        "expires today",
        "final warning",
        "suspended",
        "locked",
        "within 24 hours",
        "don't delay"
    ],
    "Account or identity concerns": [
        "verify your account",
        "account suspended",
        "password",
        "verification code",
        "social security",
        "personal information",
        "confirm your identity",
        "login details"
    ],
    "Suspicious links": [
        "click here",
        "tap here",
        "click the link",
        "open this link",
        "verify here",
        "http://",
        "bit.ly"
    ],
    "Money or payment requests": [
        "send money",
        "wire transfer",
        "pay now",
        "payment required",
        "gift card",
        "bank account",
        "processing fee",
        "refund",
        "transfer funds"
    ],
    "Unusual payment methods": [
        "bitcoin",
        "cryptocurrency",
        "crypto",
        "prepaid card",
        "gift cards",
        "send the code",
        "payment through gift cards"
    ],
    "Unexpected prizes or offers": [
        "you won",
        "winner",
        "claim your prize",
        "free gift",
        "congratulations",
        "claim your reward",
        "you have been selected",
        "inheritance"
    ]
}

category_explanations = {
    "Urgency or pressure":
        "The message is trying to make you act quickly. Scammers "
        "sometimes do this so you don't have time to think.",

    "Account or identity concerns":
        "The message mentions account access or sensitive information. "
        "Be careful with passwords and verification codes.",

    "Suspicious links":
        "The message contains wording or a link that deserves a closer "
        "look. Don't click it just to see where it goes.",

    "Money or payment requests":
        "The message mentions money or a payment. Check the request "
        "through an official source before paying anyone.",

    "Unusual payment methods":
        "The message mentions payment methods that scammers may use "
        "because the money can be difficult to recover.",

    "Unexpected prizes or offers":
        "The message mentions a prize or offer. Be cautious if you "
        "didn't enter anything or have to pay to claim it."
}

category_advice = {
    "Urgency or pressure":
        "Take your time. A legitimate organization shouldn't require "
        "you to panic before you can verify a request.",

    "Account or identity concerns":
        "Don't share passwords or verification codes. Contact the "
        "organization using its official website or phone number.",

    "Suspicious links":
        "Avoid clicking the link. Open the organization's official "
        "website yourself instead.",

    "Money or payment requests":
        "Don't send money until you've independently confirmed "
        "who is asking and why.",

    "Unusual payment methods":
        "Pause before paying with gift cards, cryptocurrency, or "
        "other unusual methods. Verify the request independently.",

    "Unexpected prizes or offers":
        "Don't pay a fee or share sensitive information just to "
        "claim a surprise prize."
}


def find_warning_categories(message):
    message_lower = message.lower()
    found_categories = {}

    for category, phrases in warning_categories.items():
        matches = []

        for phrase in phrases:
            pattern = (
                r"(?<!\w)"
                + re.escape(phrase)
                + r"(?!\w)"
            )

            if re.search(pattern, message_lower):
                matches.append(phrase)

        if matches:
            found_categories[category] = matches

    return found_categories


def calculate_risk_score(
    found_categories,
    unexpected_message,
    asks_sensitive,
    pressured
):
    score = len(found_categories)

    if unexpected_message:
        score += 1

    if asks_sensitive:
        score += 2

    if pressured:
        score += 1

    return min(score, 8)


def get_risk_label(score):
    if score <= 1:
        return "Fewer warning signs found"

    elif score <= 3:
        return "Some warning signs found"

    elif score <= 5:
        return "Several warning signs found"

    else:
        return "Many warning signs found"


def get_risk_explanation(score):
    if score <= 1:
        return (
            "The checker found relatively few warning signs. "
            "That doesn't automatically mean the message is safe."
        )

    elif score <= 3:
        return (
            "There are some things worth checking before you respond. "
            "Don't rush into clicking links or sharing information."
        )

    elif score <= 5:
        return (
            "This message has several warning signs. Verify the sender "
            "independently before doing anything it asks."
        )

    else:
        return (
            "This message has multiple warning signs. Don't send money "
            "or share sensitive information until you've verified it."
        )


if st.button("Check this message", type="primary"):
    if not message.strip():
        st.warning("Paste a message first. I can't analyze an empty box.")

    else:
        found_categories = find_warning_categories(message)

        unexpected_message = expected == "No"
        sensitive_request = asks_sensitive == "Yes"
        pressure_reported = pressured == "Yes"

        score = calculate_risk_score(
            found_categories,
            unexpected_message,
            sensitive_request,
            pressure_reported
        )

        st.divider()
        st.subheader("Here's what I found")

        st.metric(
            "Warning signs score",
            f"{score}/8"
        )

        st.write(f"**{get_risk_label(score)}**")
        st.write(get_risk_explanation(score))

        if found_categories:
            st.subheader("What looks suspicious")

            for category, matches in found_categories.items():
                st.markdown(f"**{category}**")

                st.write(
                    "Words or phrases found: "
                    + ", ".join(f"`{phrase}`" for phrase in matches)
                )

                st.write(category_explanations[category])
                st.info(category_advice[category])

        else:
            st.write(
                "I didn't find any of the warning phrases I'm checking "
                "for. That doesn't mean the message is definitely safe. "
                "Scams can be worded in lots of different ways."
            )

        if expected == "No":
            st.warning(
                "You weren't expecting this message. That's another "
                "reason to verify who sent it."
            )

        if asks_sensitive == "Yes":
            st.warning(
                "The message asks for sensitive information or money. "
                "Don't share anything until you've verified the request."
            )

        if pressured == "Yes":
            st.warning(
                "You noticed pressure or threats. Take a step back "
                "instead of letting the message rush you."
            )

        st.divider()

        st.subheader("What you should do next")

        st.write(
            "1. Don't click suspicious links or open unexpected "
            "attachments."
        )

        st.write(
            "2. Don't share passwords, verification codes, or "
            "financial information."
        )

        st.write(
            "3. Contact the organization using a phone number or "
            "website you find independently."
        )

        st.write(
            "4. If the message claims to be from someone you know, "
            "check with them using another method."
        )

        st.caption(
            "Privacy note: This app checks the text you enter using "
            "predefined rules. Avoid pasting passwords, verification "
            "codes, or other private information."
        )

st.divider()

st.caption(
    "Made to help people spot common scam warning signs. "
    "Not every suspicious message is a scam, and not every scam "
    "looks suspicious."
)
