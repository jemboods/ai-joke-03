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
# about dependency updates.
SHORTLIST = [
    (
        "I asked the agent to update one dependency. It updated all of "
        "them, and the changelog for the release just says 'misc "
        "improvements'. The misc is load-bearing.",
        9, 9, 9, 9,
    ),
    (
        "The agent pinned our dependencies for stability, then unpinned "
        "them for security, then wrote a poem about the tension. The "
        "poem has no vulnerabilities. Yet.",
        8, 9, 7, 9,
    ),
    (
        "The agent removed 40 unused dependencies. The build broke in a "
        "file nobody has opened since 2019, in a feature everyone uses "
        "daily.",
        8, 9, 8, 8,
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
