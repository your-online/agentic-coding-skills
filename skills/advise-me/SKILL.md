---
name: advise-me
description: Read how the current session is working against the agentic coding rubric and say what to do differently from here, in chat, from the transcript and whatever code exists. Use only when the developer asks about their own approach while the work is still going on, including before any code exists — "how am I doing so far", "feedback on my approach", "am I going about this the right way". It answers in chat and writes no file; a written verdict on finished work is what the review-my-work skill is for.
---

# Advise me

The criteria live in `references/rubric.md` — the `references` directory that sits
beside this skill's own directory, in the same skills directory. It is material to
read, not a skill: there is nothing to invoke. Read that file whole before you start,
the file itself and not a summary of it, and follow the rules it sets out for judging
work against it. Beside it sits `learning-materials.md`, reading for a developer who
wants to get better at a criterion; point at it when that is what would help, do not
load it to advise.

It runs only when the developer asks for it by name. Never start it on your own
initiative, and never infer from the state of the work that feedback is due.

The other half of this pair is `review-my-work`: reviewer plus falsifier plus one
Markdown report, for a verdict on finished work. This route answers in chat, writes
no file, and runs while the work is still going on.

## Sources

Always both, as far as they exist:

- The whole transcript of this session — what was asked, what was tried, what was
  verified, what was assumed.
- The code produced so far, as a diff, on the basis the rubric's judging rules
  derive and ask you to name. Before any code exists there is no diff, and the
  transcript alone carries the answer.

Look at both yourself. Do not advise from memory of what you did — read the diff.

## Run it

**1. Send off the second opinion first.** Spawn one judging subagent, in the
background and non-blocking, under the rules the rubric sets out for that role. Its
job is the same as yours: judge this work against the rubric and say what to do
better, every point carrying its remedy the way the rubric's judging rules ask.
Send it off before you write your own answer, so it is not shaped by it, and
in the background so the developer waits for neither.

Hand it the raw sources by path, never as a retelling: the session transcript where
this platform stores it, the diff written out to a file with its basis named, and
`references/rubric.md`. A subagent that reads the sources itself is the point; one
that reads your account of them is you again, with a delay.

If no isolated subagent can be spawned, say so in one line and give your own read
anyway — it is worth less alone, and the developer should know which of the two they
are holding.

**2. Then answer yourself, in the main context**, from the rubric, the transcript
and the diff. Where does this work meet the criteria, where does it not, and what
would you do differently from here. Say it straight.

**3. Report the subagent's judgement when it lands**, including — especially — where
it contradicts yours. Do not smooth the two into one voice. It saw the same sources
without having made the choices, which is exactly why its disagreement is the most
useful part of this skill.

**4. Offer a falsifier over the advice — never start one.** Once both answers are on
the table, close with a single short line offering one more round: a fresh agent that
gets the same sources and this advice, and is asked to knock it down — a wrong
diagnosis, a heavier remedy than the work needs, something both readers walked past —
and to say what is missing. Strongly recommended after every advice that anything
hangs on, because half of it came from the session that made the choices being judged
and that is the half most likely to be gentle. Skip the offer when nothing much rests
on the answer.

Say what it buys, not what it is called: this route is for a developer who has never
heard the word falsifier, and "shall I have a falsifier check this" tells them
nothing. Nothing runs until the developer says yes. Never spawn it on your own
initiative, never make it the default, and never turn the offer into a question the
developer has to answer before they get their advice.

## The answer

Open with the substance. No preamble about which model this runs on, no explanation
of what this route can or cannot do, no note that the rubric has been loaded, no
disclaimer about judging your own work — the developer knows, and the second opinion
is on its way. Only when something is genuinely off does it get a line: the strongest
model was unavailable, no subagent could be spawned, there is no diff to look at.

Name the few things that matter most, each tied to a criterion and to the concrete
place in the transcript or the diff where you saw it. Each one carries its remedy,
the way the rubric's judging rules ask, and takes the shape those same rules ask for
— concrete enough to start on. Short enough to read in the middle of the work.

You are judging choices you made yourself, and that is softer than a judgement from
outside — which is what the background agent is for, and why its report gets the last
word rather than a footnote.
