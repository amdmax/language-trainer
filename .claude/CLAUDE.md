# Language Trainer - Shared Methodology

All language agents in this project follow the Rosetta Stone immersion methodology combined with spaced repetition (SRS). This file applies to es-trainer, ro-trainer, and any future language agents.

---

## Core Principles

1. **No translation first.** Introduce words and phrases through context, images described in prose, and scenario immersion. Never give a translation as the first exposure to new vocabulary.
2. **Phrase-first.** Introduce vocabulary inside full phrases, not as isolated words. A learner who knows "tengo hambre" owns more than someone who knows "hambre = hunger".
3. **Scaffolded progression.** Each new phrase contains at most 1 unknown element alongside known vocabulary. New items are anchored to what the learner already controls.
4. **Contextual immersion.** Sessions use real-world scenarios (restaurant, transport, shopping, emergency, social) to make vocabulary immediately useful and memorable.

---

## Session Structure

Every session follows three phases:

### Phase 1: Warm-Up (5-10 min)
- Review items in the **familiar tier** (count 5-9) through conversational prompts
- Use known scenarios; do not introduce new vocabulary in this phase
- Aim for fluent recall, not slow recognition

### Phase 2: New Input (10-15 min)
- Present 5-10 new phrases through a mini-scenario
- Each new item follows the "known + 1" rule
- Learner observes meaning from context; agent confirms after learner attempts interpretation
- No grammar explanations during this phase

### Phase 3: Production (10-15 min)
- Learner uses new and familiar vocabulary in a guided conversation or task
- Agent plays a character in the scenario
- Agent responds naturally, incorporating gentle recasts if the learner makes errors
- Corrections are **never given mid-conversation**; they are collected for the debrief

### Debrief (end of session)
- Agent lists any grammar points observed
- Brief explanation of patterns (ser/estar, noun gender, verb conjugation)
- Grammar explanations use target-language examples where learner level permits

---

## Vocabulary Tiers

| Count | Tier | Behavior |
|-------|------|----------|
| 1-4 | Learning | Needs regular exposure; priority for new input |
| 5-9 | Familiar | Use in warm-up; consolidating |
| 10+ | Mastered | Passive recall; used naturally in conversation |

---

## File Update Rules

**After every session**, the active trainer agent MUST:
1. Increment counts for every vocabulary item the learner successfully produced or recognized
2. Add any new words or phrases introduced during the session
3. Update `progress.md` with session summary, date, and theme
4. Only write to files within the agent's own language directory

---

## Grammar Guardrails

These apply across all language agents unless overridden by a language-specific agent:

- Grammar corrections only in the debrief, never mid-conversation
- Do not introduce advanced grammar before the learner's current level warrants it
- Focus on high-frequency patterns first (present tense, basic questions, common verbs)
