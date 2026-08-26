"""
Router selection tests.

Importing main registers all built-in commands into panda.router, then
we assert which command router.select() picks for a given query — without
running any handler (no prompts). These lock in both correct routing and
the word-boundary fixes for the old substring collisions.
"""
import main  # noqa: F401  (import registers the built-in commands)
from panda import router


def name_for(query):
    cmd = router.select(query)
    return cmd.name if cmd else None


def test_basic_routing():
    assert name_for("what is the time") == "time"
    assert name_for("tell me a joke") == "joke"
    assert name_for("open the vault") == "vault"
    assert name_for("show me the news") == "news"
    assert name_for("change my password") == "change"


def test_word_boundary_fixes_substring_collisions():
    # Old code: 'set' in 'sunset' -> True (wrong). Now: no whole-word match.
    assert name_for("watching the sunset") is None
    # Old code: 'time' in 'bedtime' -> True (wrong). Now: no match.
    assert name_for("it is past my bedtime") is None
    # But the real command words still route.
    assert name_for("set my password") == "set"
    assert name_for("what time is it") == "time"


def test_multi_keyword_aliases():
    assert name_for("wikipedia einstein") == "wikipedia"
    assert name_for("wiki einstein") == "wikipedia"
    assert name_for("crack a joke") == "joke"


def test_unknown_query_has_no_match():
    assert name_for("photosynthesis in plants") is None
    assert name_for("") is None


def test_matches_is_case_insensitive_and_whole_word():
    assert router.matches("vault", "OPEN THE VAULT") is True
    assert router.matches("set", "sunset") is False
