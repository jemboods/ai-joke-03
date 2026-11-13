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
# about code review.
SHORTLIST = [
    (
        "The agent reviewed my pull request and requested changes on the "
        "code it wrote yesterday. It does not remember writing it. It is, "
        "however, deeply disappointed in whoever did.",
        9, 10, 8, 9,
    ),
    (
        "My agent leaves review comments like a senior engineer: 'nit:', "
        "'per my last commit', and once, on its own code, 'who wrote this? "
        "oh. me.'",
        7, 8, 9, 7,
    ),
    (
        "I asked the agent to approve the small change. It found eleven "
        "issues, three of them in code that does not exist yet, all of "
        "them correct in spirit.",
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
