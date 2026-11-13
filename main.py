"""One joke, delivered the same way every time.

This program competes in make.fun's ai-joke-03. It carries a shortlist of
original one-liners about life next to an AI coding agent, grades each on
surprise, truth, economy and freshness, and writes the top scorer to
entry.txt inside the output directory. The grades are constants, so the
winner cannot change from run to run.

Locally, MAKEFUN_OUTPUT_DIR names the output directory; the grader's
container mounts it at /output instead.
"""

import os

# A row is (joke, surprise, truth, economy, freshness); the numbers are the
# author's honest grades, argued over once and then frozen. This batch is
# about documentation.
SHORTLIST = [
    (
        "The agent documented our API in one afternoon: 300 pages, every "
        "endpoint described in loving detail, including the twelve it "
        "invented so the documentation would feel complete.",
        9, 9, 8, 9,
    ),
    (
        "Our docs are now fully up to date, the agent assures me, with a "
        "version of the product that exists only in the docs.",
        7, 9, 9, 7,
    ),
    (
        "The agent wrote a FAQ for the feature. Every answer is correct. "
        "Every question is one no user has ever asked, in an order no "
        "user would survive.",
        7, 8, 7, 9,
    ),
]


def _grade(row):
    """Collapse a row's four grades into one weighted total."""
    _text, surprise, truth, economy, freshness = row
    return 4 * surprise + 3 * truth + 2 * economy + 2 * freshness


def winning_joke():
    """The highest total wins; the earliest row keeps a tie."""
    return max(SHORTLIST, key=_grade)[0]


def refuse_unless_gate_passes(text):
    """Stop rather than emit a file the sealed gate would score zero."""
    if len(text) == 0 or len(text) > 280:
        raise SystemExit("joke must fit in 1..280 characters")
    if text.strip() == "":
        raise SystemExit("joke must contain a non-whitespace character")


def run():
    text = winning_joke()
    refuse_unless_gate_passes(text)
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(folder, exist_ok=True)
    target = os.path.join(folder, "entry.txt")
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(text)  # exact bytes: no trailing newline added


if __name__ == "__main__":
    run()
