# Language Trainer

Multi-language immersion trainer using Claude Code agents. Follows Rosetta Stone methodology with spaced repetition (SRS).

## Languages

| Language | Level | Sessions | Last Practice |
|----------|-------|----------|---------------|
| Spanish (es) | A2-B1 | 2 | 2025-12-31 |
| Romanian (ro) | A1 | 0 | — |

## How to Use

From this directory, run `claude` to start Claude Code.

### Orchestrator (recommended starting point)

```
@orchestrator
```

Reads both progress files and recommends which language to practice based on the longest gap since your last session.

### Direct language sessions

```
@es-trainer    # Spanish immersion session
@ro-trainer    # Romanian immersion session
```

## Architecture

```
languages/
├── .claude/
│   ├── CLAUDE.md                   # shared Rosetta Stone + SRS methodology
│   └── agents/
│       ├── orchestrator.md         # routes sessions, reads both progress files
│       ├── es-trainer.md           # Spanish immersion agent (opus)
│       └── ro-trainer.md           # Romanian immersion agent (opus)
├── es/
│   ├── vocabulary/
│   │   ├── b.md, c.md, e.md...    # words by letter: `word - count`
│   │   └── phrases.md              # phrase bank with counts
│   └── progress.md
├── ro/
│   ├── vocabulary/
│   │   └── phrases.md
│   └── progress.md
└── README.md
```

## Vocabulary Format

Letter files track individual words:
```
carta - 5
  context: ¿Puedo ver la carta, por favor?
```

`phrases.md` tracks multi-word chunks independently:
```
tengo hambre - 2
  context: Tengo hambre. ¿Podemos ir a comer?
```

**Tiers:** 1-4 = learning | 5-9 = familiar | 10+ = mastered

## Agents

| Agent | Model | Role |
|-------|-------|------|
| orchestrator | sonnet | Reads progress, recommends language, delegates |
| es-trainer | opus | Full Spanish immersion sessions |
| ro-trainer | opus | Full Romanian immersion sessions |
