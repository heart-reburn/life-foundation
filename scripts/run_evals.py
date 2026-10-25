#!/usr/bin/env python3
"""Run the skill's evals with the Claude CLI (needs `claude` on PATH).

  run_evals.py trigger [skill]    would the skill load for each query?
  run_evals.py behavior [skill]   does the skill behave as the checklist says?

Uses the sonnet model. Trigger results show whether the description is
too broad or too narrow. Behavior results are a model-graded smoke test,
not proof: read the failures.
"""
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def ask(prompt, system=None):
    cmd = ["claude", "-p", "--model", "sonnet", "--tools", ""]
    if system:
        cmd += ["--append-system-prompt", system]
    return subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=180).stdout.strip()


def frontmatter(skill_dir):
    text = (skill_dir / "SKILL.md").read_text()
    head = text.split("---")[1]
    return {k.strip(): v.strip() for k, _, v in (l.partition(":") for l in head.splitlines() if ":" in l)}


def trigger(skill_dir):
    fm = frontmatter(skill_dir)
    cases = json.loads((skill_dir / "evals" / "trigger-queries.json").read_text())

    def run(case):
        reply = ask(
            f"You have one skill available.\nName: {fm['name']}\nDescription: {fm['description']}\n\n"
            f"User message: {case['query']}\n\nWould you load this skill to handle the message? Answer only YES or NO."
        )
        return case, reply.upper().startswith("YES")

    with ThreadPoolExecutor(8) as pool:
        results = list(pool.map(run, cases))
    bad = [(c["query"], got) for c, got in results if got != c["should_trigger"]]
    print(f"{skill_dir.name}: {len(results) - len(bad)}/{len(results)} trigger cases correct")
    for q, got in bad:
        print(f"  WRONG ({'loaded' if got else 'not loaded'}): {q}")
    return not bad


def behavior(skill_dir):
    cases = json.loads((skill_dir / "evals" / "behavior-cases.json").read_text())
    parts = [(skill_dir / "SKILL.md").read_text()]
    for ref in sorted((skill_dir / "references").glob("*.md")):
        parts.append(f"\n\n# references/{ref.name}\n" + ref.read_text())
    system = (
        "You are an agent with this skill loaded. You cannot run tools in this test: "
        "when the skill says to read or write a file, say what you would read or write.\n\n" + "".join(parts)
    )

    def run(case):
        out = ask(case["prompt"], system)
        items = "\n".join(f"{i + 1}. {c}" for i, c in enumerate(case["checklist"]))
        verdict = ask(
            f"Reply under test:\n---\n{out}\n---\nFor each numbered requirement, answer PASS or FAIL, "
            f"one per line, in the form `N: PASS` or `N: FAIL`, with no other text.\n{items}"
        )
        fails = [line for line in verdict.splitlines() if "FAIL" in line.upper()]
        return case, fails

    with ThreadPoolExecutor(4) as pool:
        results = list(pool.map(run, cases))
    ok = 0
    for case, fails in results:
        if fails:
            print(f"  FAIL {case['name']}: " + "; ".join(case["checklist"][int(f.split(':')[0]) - 1] for f in fails if f.split(':')[0].strip().isdigit()))
        else:
            ok += 1
    print(f"{skill_dir.name}: {ok}/{len(results)} behavior cases passed")
    return ok == len(results)


def main(argv):
    if len(argv) < 2 or argv[1] not in ("trigger", "behavior"):
        print(__doc__)
        return 2
    skills = [ROOT / "skills" / argv[2]] if len(argv) > 2 else sorted((ROOT / "skills").iterdir())
    func = trigger if argv[1] == "trigger" else behavior
    return 0 if all([func(s) for s in skills]) else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
