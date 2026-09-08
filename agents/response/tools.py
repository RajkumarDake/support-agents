"""Response Agent tools: reply templates and a tone checker."""

import re

TEMPLATES = {
    "billing": ("Hi{name},\n\nThanks for flagging this. Here is what I found on your billing "
                "record:\n\n{facts}\n\n{next_step}\n\nBest,\nSupport"),
    "refund": ("Hi{name},\n\nThanks for getting in touch about this charge. Here is what I can "
               "see:\n\n{facts}\n\n{next_step}\n\nBest,\nSupport"),
    "technical": ("Hi{name},\n\nSorry for the trouble. Here is what is going on and how to fix "
                  "it:\n\n{facts}\n\n{next_step}\n\nBest,\nSupport"),
    "account": ("Hi{name},\n\nHappy to help with this. Here is what applies to your "
                "workspace:\n\n{facts}\n\n{next_step}\n\nBest,\nSupport"),
    "unclear": ("Hi{name},\n\nThanks for reaching out. I want to make sure I point you at the "
                "right thing:\n\n{facts}\n\n{next_step}\n\nBest,\nSupport"),
}

BLAME = ["your fault", "you should have", "you failed to", "you clearly", "you must have",
         "as I already said", "obviously", "you did not read"]
OVERPROMISE = ["guarantee", "guaranteed", "immediately refunded", "will never happen again",
               "100% certain", "instantly", "right away, no matter what", "always works",
               "we will refund"]
GREETINGS = ["hi", "hello", "hey", "good morning", "good afternoon", "thanks for"]


def get_template(category: str) -> str:
    return TEMPLATES.get(category, TEMPLATES["unclear"])


def check_tone(draft: str) -> list[str]:
    """Returns a list of tone problems. Empty list means the draft reads fine."""
    low = draft.lower()
    flags = []
    flags += [f"blame: '{p}'" for p in BLAME if p in low]
    flags += [f"over-promising: '{p}'" for p in OVERPROMISE if p in low]

    first_line = low.strip().split("\n", 1)[0]
    if not any(first_line.startswith(g) for g in GREETINGS):
        flags.append("missing greeting")
    if len(re.findall(r"!", draft)) > 2:
        flags.append("too many exclamation marks")
    if len(draft.split()) > 400:
        flags.append("reply is too long for a support answer")
    return flags
