
from oncall_slackbot.integrations.nlp import spacy as nlp_spacy
from typing import Optional


def _noop_generate_label(message_text: str) -> Optional[str]:
    return None


if nlp_spacy.is_configured():
    from oncall_slackbot.integrations.nlp.spacy import generate_label
else:
    # Install a noop version as the label generator
    generate_label = _noop_generate_label


def is_backend_present() -> bool:
    """
    Returns whether an NLP backend is actually configured.
    :return: True if a backend is configured, false otherwise
    """
    return generate_label != _noop_generate_label
