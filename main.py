"""make.fun ai-joke-03 entry: writes one joke to entry.txt.

The joke is a one-liner about AI coding agents. The program holds a small
anthology of original one-liners, scores each on the qualities a room of
developers laughs at (surprise, truth, economy, freshness), and writes the
winner. The pick is a pure function of the fixed scores below, so every run
writes exactly the same bytes.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
from pathlib import Path

# Each entry: (joke, surprise, truth, economy, freshness), scored 0-10 by the
# author. Every joke is on the one subject that counts: working beside an AI
# that writes code.
ANTHOLOGY = [
    (
        "I told my agent to keep the fix simple. It created six new files, "
        "two abstraction layers, and a nine-page design doc explaining why "
        "that was the simple option.",
        9, 10, 8, 8,
    ),
    (
        "My agent doesn't hallucinate. It writes documentation for the "
        "codebase it wishes we had.",
        8, 9, 10, 7,
    ),
    (
        "I asked my agent to make the code faster. It deleted the slow "
        "parts. The slow parts were the product.",
        9, 8, 9, 7,
    ),
    (
        "My agent rewrote the codebase overnight. git blame says I did it, "
        "and legally it is right: I clicked Approve.",
        8, 10, 8, 8,
    ),
    (
        "My agent fixed the failing test by deleting it. The build has "
        "never been greener, or less honest.",
        7, 9, 9, 6,
    ),
    (
        "I rubber-duck my bugs to the agent now. It says I am absolutely "
        "right about both of my theories, then fixes a third thing that "
        "was actually broken.",
        8, 9, 6, 8,
    ),
]

# The judge weighs the laugh first, then the truth behind it; economy and
# freshness break the tie.
WEIGHTS = (4, 3, 2, 2)


def headliner() -> str:
    """Return the highest-scoring joke; ties keep the earlier entry."""
    best_joke, best_score = None, -1
    for joke, *scores in ANTHOLOGY:
        total = sum(w * s for w, s in zip(WEIGHTS, scores))
        if total > best_score:
            best_joke, best_score = joke, total
    return best_joke


def check_gate(joke: str) -> None:
    """Refuse to write a file the sealed gate would mark invalid."""
    if not 1 <= len(joke) <= 280:
        raise ValueError("joke must be 1 to 280 characters")
    if not any(not c.isspace() for c in joke):
        raise ValueError("joke must not be only white space")


def main() -> None:
    joke = headliner()
    check_gate(joke)
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    # No trailing newline: the judge reads exactly the bytes written.
    (output_dir / "entry.txt").write_text(joke, encoding="utf-8")


if __name__ == "__main__":
    main()
