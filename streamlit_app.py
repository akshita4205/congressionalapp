import streamlit as st
import re

st.set_page_config(
    page_title="Scam Detector",
    layout="centered"
)

st.title("Scam Detector")
st.write(
    "Found a message that feels a little off? Paste it here and "
    "let's check it for common scam warning signs so we don't get scammed."
)

st.caption(
    "This tool checks for common warning signs. It can't guarantee "
    "whether a message is real or a scam, so take it with a grain of salt. "
)

message = st.text_area(
    "Paste the suspicious message here",
    placeholder="Paste the text message, email, or offer here...",
    height=180
)

st.subheader("Your Input")

expected = st.radio(
    "Was this a message you saw coming?",
    ["Yeah", "Definetely not", "I don't know"],
    horizontal=True
)

asks_sensitive = st.radio(
    "Does it ask for something specific like money, a password, a verification code, "
    "or some form of personal information?",
    ["Yeah", "Definetly not", "I don't know"],
    horizontal=True
)

pressured = st.radio(
    "Does it rush you, threaten you, or make you feel like "
    "you HAVE to act right now or else the world ends?",
    ["Yeah", "Definetely not", "I don't know"],
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
        "The message is pressuring you to act quickly. Scammers "
        "sometimes do this so you don't have time to think and make a hasty decision.",

    "Account or identity concerns":
        "The message mentions account access or sensitive information. "
        "In this situation be careful with passwords and verification codes.",

    "Suspicious links":
        "The message contains wording or a link that you should keep an eye on, "
        " so don't click it just to see where it goes.",

    "Money or payment requests":
        "The message mentions some form of money or a payment. Make sure to check the request "
        "through an official source or bank before paying anyone.",

    "Unusual payment methods":
        "The message mentions payment methods that scammers may use "
        "because sometimes the money can be difficult to recover.",

    "Unexpected prizes or offers":
        "The message mentions a prize or offer. If it's too good to be true, be cautious if you "
        "didn't enter anything or have to pay to claim it."
}

category_advice = {
    "Urgency or pressure":
        "Take your time. An actual organization won't make you stress  "
        "before you can verify a request, it's not a bomb you're holding.",

    "Account or identity concerns":
        "Don't share any passwords or verification codes. Contact the "
        "organization using its OFFICIAL website or phone number and report the issue.",

    "Suspicious links":
        "Try and avoidclicking the link. Open the organization's official "
        "website yourself instead which you can find by typing it out on google. Normally, if the brand is legit, the first couple of websites shouldn't be fake.",

    "Money or payment requests":
        "Do NOT send money until you've 100% confirmed "
        "who is asking and why they'er asking",

    "Unusual payment methods":
        "Pause before paying with gift cards, cryptocurrency, or "
        "any other unusual methods. Verify such a request by either asking for assistance or going in-person.",

    "Unexpected prizes or offers":
        "Don't pay an unecessary fee or share any form of sensitive information just to "
        "claim a 'surprise' prize. (You probably won't get the prize)"
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
        return "Few warning signs found"

    elif score <= 3:
        return "Some warning signs found"

    elif score <= 5:
        return "Several warning signs found"

    else:
        return "Many warning signs found"


def get_risk_explanation(score):
    if score <= 1:
        return (
            "After looking through the message, there were relatively few warning signs. "
            "However that doesn't automatically mean the message is safe."
        )

    elif score <= 3:
        return (
            "There are some things worth checking before you respond, and watch what you press. "
            "Don't rush into clicking links or sharing information blidnly."
        )

    elif score <= 5:
        return (
            "This message has several warning signs. Definetely verify who's sending this "
            "by yourself before doing anything it asks."
        )

    else:
        return (
            "This message has many warning signs. This is HIGHLY likely to be a scam. Don't send money "
            "or share any sensitive information until you've actually verified it."
        )


if st.button("Check this message", type="primary"):
    if not message.strip():
        st.warning("You have to actually say something. Unfortunately, we can't analyze an empty box.")

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
        st.subheader("Here's what we found")

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
                "Okay. So we didn't find any of the warning phrases that we were looking "
                "for. That doesn't necessarily mean the message is fully safe. "
                "Scams can be worded in lots of different ways, they're usually pretty creative about it."
            )

        if expected == "No":
            st.warning(
                "You weren't expecting this message. That's another "
                "reason to dobule check who sent it. (Unknown Number/ Well-known Brand?)"
            )

        if asks_sensitive == "Yes":
            st.warning(
                "If the message starts asking for sensitive information or money, be wary. Most legit organizations don't do things like this. "
                "Don't share anything until you've verified the request."
            )

        if pressured == "Yes":
            st.warning(
                "You noticed any sort of pressure or threats? Take a step back, and just keep in mind this is HIGHLY likely  "
                "a scam. Act rationally instead of letting the message rush you."
            )

        st.divider()

        st.subheader("What you should do next")

        st.write(
            "1) Don't click suspicious links or open unexpected "
            "attachments."
        )

        st.write(
            "2) Don't share any passwords, verification codes, or "
            "financial information."
        )

        st.write(
            "3) Contact the organization using a phone number or "
            "website you find on the google. (Cross-check that too)"
        )

        st.write(
            "4) If the message claims to be from someone you know, "
            "check with them using another method (Their other socials)"
        )

        st.caption(
            "Privacy note: This app checks the text you enter using "
            "pre-written rules. Avoid pasting passwords, verification "
            "codes, or other private information you wouldn't want us to see."
        )

st.divider()

st.caption(
    "Made to help out on spotting common scam warning signs. "
    "Not every suspicious message is a scam, and not every scam "
    "looks suspicious."
)
