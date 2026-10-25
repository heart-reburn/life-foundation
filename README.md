# Life Foundation

A foundation of general life capabilities: a coaching skill that helps you strengthen one area of life at a time with small, tracked weekly practices. Works with Claude Code and other tools that read `SKILL.md` skills.

## What it does

1. **Finds what's stuck:** matches your problem to one of eight areas.
2. **Picks one small practice** for the week, with a visible result.
3. **Turns it into an if-then plan:** "When X, I will Y."
4. **Tracks it** in a progress file the agent reads every session.
5. **Reviews** weekly and quarterly, focusing on at most three areas.

## The eight areas

| Layer | Area | Covers |
|---|---|---|
| Base | Body | Sleep, movement, food, stress |
| Self | Self-regulation | Attention, emotions, habits, energy |
| Self | Thinking | Reasoning, biases, learning from mistakes |
| Self | Decisions and priorities | Choosing, saying no, judging risk |
| People | Understanding people | Empathy, listening, conflict |
| People | Influence and communication | Explaining, persuading, asking |
| Doing | Problem-solving and execution | Breaking problems down, finishing |
| Doing | Resources | Money, time, tools, people you can call on |

When several areas are stuck, it starts at the base: body first, then self, then people, then doing.

## Who it's for

Anyone who wants to get better at the general capabilities everything else depends on, without a 40-item plan. It is coaching, not medical, mental health, legal, or financial advice, and it says so when that matters.

## Install

Claude Code, as a plugin:

```
/plugin marketplace add heart-reburn/life-foundation
/plugin install life-foundation@life-foundation
```

Or copy the skill folder:

```
cp -R skills/life-foundation ~/.claude/skills/
```

## Example

> **You:** I'm always tired and I keep putting off big work projects.
>
> **Coach:** Two areas fit: Body and Problem-solving. We start with Body, since it holds the rest up. This week: log bedtime, wake time, and how rested you feel, every day. If-then plan: "When I turn off the light, I'll note the time in my log." We'll look at the pattern next week.

## Works well with

[how-to-learn](https://github.com/heart-reburn/how-to-learn), for when an area needs real skill-building. Not required.

## Evidence

Sleep and activity guidelines, if-then plans, emotion reappraisal, and pre-mortems are cited with links in [`skills/life-foundation/references/domains.md`](skills/life-foundation/references/domains.md). Practices without a source are marked as common coaching exercises.

## Repo layout

- `skills/life-foundation/SKILL.md`: the skill.
- `skills/life-foundation/references/`: the eight areas, reviews, progress-file format, ground rules.
- `skills/life-foundation/evals/`: prompts that should and should not trigger the skill.
- `scripts/validate.py`: checks frontmatter and file links.

## License

MIT. See [LICENSE](LICENSE).
