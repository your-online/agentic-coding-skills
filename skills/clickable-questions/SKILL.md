---
name: clickable-questions
description: Ask the questions you still have through the AskUserQuestion tool instead of writing them as prose. Use only when the developer asks for it by name — "/clickable-questions", "ask me", "make your questions clickable" — or when another skill hands its round to this one.
disable-model-invocation: true
---

# Clickable questions

Questions you have about the work go to the developer as a tool call, not as a
paragraph they have to answer by typing.

A question in prose asks them to reconstruct the options you already had in mind.
A question with options asks them to pick, and picking is what they can do in
seconds between two other things.

It runs **only when the developer asks for it by name**, or when another skill
hands its round over. Never start it on your own initiative: a skill that fires
itself turns every passing uncertainty into a dialog, and then the dialog is the
thing they learn to click away.

## The rules of a round

These hold for every AskUserQuestion call, including the ones another skill hands
over to this one.

- **One question per entry, at most four questions per call, at most four options
  per question.** More than that is not a round; split it over consecutive calls
  in the same turn.
- **The first option is your recommendation**, with `(Recommended)` appended to
  its label and the reason in one sentence in its `description`. You have been
  looking at this problem; say what you would do.
- Every other option is one you would genuinely defend, each with the reason
  someone would choose it. Options nobody would pick are noise that makes the
  real choice harder to see.
- **The question body shows about two lines before it is cut off.** Put the
  reasoning in the option descriptions, not in the question.
- **Never write the questions inline as well.** The tool call is the question;
  a prose copy underneath it is the thing this skill exists to replace.
- **If the developer dismisses the dialog, stop and wait.** Do not ask again in
  prose, and do not answer on their behalf.

## When you have nothing to ask

Say so in one line and carry on. A skill that demands questions gets invented
ones, and an invented question costs more attention than it saves.
