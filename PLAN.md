# DLI-Spanish-Simulator Implementation Plan

## Overview

Build a CLI-based multi-agent system that implements Defense Language Institute methodology for rapid Spanish fluency. The system uses 4 specialized AI agents powered by Claude API, YAML configuration files, and integrates with existing progress tracking.

## Architecture Summary

### Four Specialized Agents

1. **Mission Commander (Orchestrator)** - Assigns daily missions, provides 40-60 vocabulary words in context, enforces Spanish-only mode
2. **ISO-Immersion Agent (Role-Play)** - Runs scenarios (haggling, border crossing, etc.), NO grammar correction, focus on intent understanding
3. **Intelligence Analyst (Comprehension)** - Presents Spanish content, user explains intent/intelligence gathered
4. **Peel-Back Linguist (Feedback)** - Post-mission only, analyzes output, teaches patterns before rules (DLAB-style)

### Technology Stack

- **Interface:** CLI application using Click + Rich (beautiful terminal output)
- **AI:** Claude API (claude-sonnet-4-5) via Anthropic SDK
- **Configuration:** YAML for agent configs and mission templates
- **Data Storage:**
  - Existing `progress.json` (extended with DLI metrics)
  - YAML for agent configurations
  - JSON for session logs and vocabulary pools
- **Language:** Python 3.11+

### Key Design Decisions

- **Agent Communication:** Orchestrator pattern manages handoffs between agents
- **API Strategy:** One Claude API call per agent turn (not streaming)
- **State Management:** In-memory during session, persisted to `data/sessions/` on completion
- **Spanish Enforcement:** CLI-level validation + agent system prompts
- **Vocabulary Management:** Two-tier system (master pool + daily assignments)

## Project Structure

```
/Users/thesolutionarchitect/Documents/source/spanish/
│
├── cli.py                          # Main entry point
├── requirements.txt                # Python dependencies
├── .env.example                    # API key template
│
├── config/
│   ├── agents/                     # Agent YAML configs
│   │   ├── mission_commander.yaml
│   │   ├── iso_immersion.yaml
│   │   ├── intelligence_analyst.yaml
│   │   └── peel_back_linguist.yaml
│   ├── missions/                   # Mission templates
│   │   ├── business_meeting.yaml
│   │   ├── border_crossing.yaml
│   │   ├── medical_emergency.yaml
│   │   └── market_haggling.yaml
│   └── settings.yaml               # Global settings
│
├── src/
│   ├── agents/
│   │   ├── base_agent.py          # Abstract base class
│   │   ├── mission_commander.py
│   │   ├── iso_immersion.py
│   │   ├── intelligence_analyst.py
│   │   └── peel_back_linguist.py
│   │
│   ├── core/
│   │   ├── orchestrator.py        # Agent coordination
│   │   ├── session_manager.py     # Session lifecycle
│   │   ├── claude_client.py       # Claude API wrapper
│   │   └── progress_tracker.py    # progress.json integration
│   │
│   ├── data/
│   │   ├── vocabulary_pool.py     # Manages 40-60 daily words
│   │   ├── mission_loader.py      # Parses mission YAMLs
│   │   └── content_sources.py     # For Intelligence Analyst
│   │
│   ├── utils/
│   │   ├── yaml_parser.py
│   │   ├── validators.py          # Spanish-only enforcement
│   │   └── logger.py
│   │
│   └── ui/
│       ├── cli_renderer.py        # Rich formatting
│       └── prompts.py             # Input handling
│
├── data/                          # Runtime data (gitignored)
│   ├── sessions/
│   ├── recordings/
│   └── vocabulary/
│       ├── master_pool.json
│       └── daily_assignments.json
│
├── progress.json                  # PRESERVED & EXTENDED
├── vocabulary.md                  # PRESERVED as reference
│
└── tests/
    ├── test_agents.py
    ├── test_orchestrator.py
    └── test_progress_integration.py
```

## Implementation Phases

### Phase 1: Core Infrastructure (MVP)

**Goal:** Basic CLI with Mission Commander agent working

**Files to create:**
- `cli.py` - Basic Click CLI with start/stats commands
- `requirements.txt` - Python dependencies (anthropic, pyyaml, rich, click, python-dotenv, pydantic, langdetect)
- `.env.example` - Template for ANTHROPIC_API_KEY
- `src/core/claude_client.py` - Claude API wrapper with retry logic
- `src/agents/base_agent.py` - Abstract base class for all agents
- `src/agents/mission_commander.py` - First agent implementation
- `config/agents/mission_commander.yaml` - Agent configuration with system prompt
- `src/utils/yaml_parser.py` - YAML loading utilities

**Deliverable:** User can run `python cli.py start` and Mission Commander assigns a mission with 50 vocabulary words in full sentences

**Validation:**
- CLI starts without errors
- Claude API successfully called
- Vocabulary words presented in context (never isolated)

### Phase 2: Role-Play & Orchestration

**Goal:** Interactive missions with ISO-Immersion agent

**Files to create:**
- `src/agents/iso_immersion.py` - Scenario-based role-play agent
- `config/agents/iso_immersion.yaml` - Agent config
- `config/missions/market_haggling.yaml` - First mission template
- `src/core/orchestrator.py` - Agent handoff logic (Commander → ISO-Immersion)
- `src/data/mission_loader.py` - Parse mission YAML templates
- `src/utils/validators.py` - Spanish-only input validation

**Deliverable:** Complete mission flow: Commander assigns → ISO-Immersion runs scenario → Mission completion

**Validation:**
- Agent handoff works seamlessly
- ISO-Immersion NEVER corrects grammar during mission
- Spanish-only mode enforced (English input rejected)

### Phase 3: Full Agent Suite

**Goal:** All 4 agents operational

**Files to create:**
- `src/agents/intelligence_analyst.py` - Comprehension testing agent
- `src/agents/peel_back_linguist.py` - Post-mission feedback agent
- `config/agents/intelligence_analyst.yaml`
- `config/agents/peel_back_linguist.yaml`
- `src/data/content_sources.py` - Spanish content for comprehension testing
- `src/core/session_manager.py` - Full session lifecycle management

**Deliverable:** Complete session flow: Commander → ISO-Immersion → Intelligence Analyst → Peel-Back Linguist

**Validation:**
- All 4 agents execute in sequence
- Peel-Back Linguist uses pattern recognition (user deduces before explanation)
- Intent-focused assessment (not grammar-focused)

### Phase 4: Progress Integration

**Goal:** Seamless integration with existing progress tracking

**Files to create:**
- `src/core/progress_tracker.py` - Extend progress.json with DLI metrics
- `src/data/vocabulary_pool.py` - Manage master pool + daily assignments
- `data/vocabulary/master_pool.json` - Migrate from vocabulary.md + expand to 500+ words
- `config/settings.yaml` - Global settings (intensity mode, difficulty, etc.)

**Files to modify:**
- `progress.json` - Add new fields:
  ```json
  {
    "dli_metrics": {
      "daily_vocabulary_target": 50,
      "pattern_recognition_score": 0,
      "no_english_violations": 0,
      "last_mission_date": null
    },
    "stats": {
      "successful_intent_communications": 0,
      "missions_completed": 0
    }
  }
  ```

**Deliverable:** progress.json auto-updates after each session, vocabulary mastery tiers integrate with DLI system

**Validation:**
- Existing progress preserved (18 words marked as pre-training)
- New sessions add 40-60 words to daily target
- Mastery tiers (learning/familiar/mastered) work with new system

### Phase 5: UX Polish

**Goal:** Production-ready CLI with beautiful output

**Files to create:**
- `src/ui/cli_renderer.py` - Rich formatting (tables, panels, progress bars)
- `src/ui/prompts.py` - Enhanced input handling with validation
- `src/utils/logger.py` - Session recording to `data/sessions/`
- `config/missions/` - All mission templates:
  - `business_meeting.yaml`
  - `border_crossing.yaml`
  - `medical_emergency.yaml`
  - (Add 3-5 more missions at different difficulty levels)

**Update:**
- `cli.py` - Add all commands:
  ```bash
  python cli.py start          # Start daily session
  python cli.py resume         # Resume interrupted session
  python cli.py stats          # View progress
  python cli.py vocab          # Review vocabulary by tier
  python cli.py mission --type border_crossing
  python cli.py history --date 2025-01-05
  python cli.py settings --intensity brutal  # 60 words instead of 40
  ```

**Deliverable:** Polished CLI with beautiful output, all commands working, session logging enabled

**Validation:**
- CLI output uses Rich formatting (colors, panels, tables)
- All commands functional
- Session logs saved to `data/sessions/YYYY-MM-DD.json`

### Phase 6: Testing & Documentation

**Goal:** Comprehensive testing and docs

**Files to create:**
- `tests/test_agents.py` - Unit tests for all 4 agents
- `tests/test_orchestrator.py` - Test agent handoffs
- `tests/test_progress_integration.py` - Test progress.json updates
- `README.md` - Installation and usage instructions
- `ARCHITECTURE.md` - Detailed architecture documentation

**Deliverable:** Test suite passing, documentation complete

## Critical Files (Priority Order)

1. **src/core/orchestrator.py** - Agent coordination logic (the "brain")
2. **src/agents/base_agent.py** - Abstract base class for all agents
3. **src/core/claude_client.py** - Claude API wrapper
4. **config/agents/mission_commander.yaml** - Template for all agent configs
5. **src/core/progress_tracker.py** - Integration with existing progress.json

## DLI Methodology Non-Negotiables

These constraints MUST be enforced:

1. **Grammar Correction Timing**
   - ISO-Immersion: ZERO grammar corrections during mission
   - Peel-Back Linguist: ONLY source of grammar feedback
   - Validate with `grammar_correction_allowed: false` flag in agent config

2. **Vocabulary Context Requirement**
   - Mission Commander: NEVER provide isolated words
   - All 40-60 words must appear in full sentences
   - Validate in mission YAML: each word must have `context` field

3. **Intent Over Accuracy**
   - Intelligence Analyst: Measures "successful intent communication"
   - Progress metric: `successful_intent_communications` (not grammar score)
   - Claude judges: "Did I understand what you meant?" (yes/no)

4. **Pattern Recognition First**
   - Peel-Back Linguist: Shows patterns, user deduces rule
   - DLAB-style: present examples → ask for pattern → user deduction → explain rule

5. **Spanish-Only Enforcement**
   - CLI-level validation (reject English input immediately)
   - Agent system prompts reinforce Spanish-only
   - Exception: SOS command for help (in Spanish: "¿Cómo se dice...?")

## Migration of Existing Data

### vocabulary.md
- Keep as human-readable reference (no changes)
- Data imported into `data/vocabulary/master_pool.json`

### progress.json
- Extend with new fields (backward compatible)
- Map old structure to new:
  - `game_history` → `mission_history`
  - `"El Detective Raúl"` → `"ISO-Immersion Agent"`
  - `games_played` → `missions_completed`

### Existing 18 Words
- Mark as "pre-training vocabulary" in master pool
- First session introduces 42 NEW words (reaching 60 total active)
- Preserve mastery tiers (learning/familiar/mastered)

### "El Detective Raúl" Game
- Create `config/missions/detective_mystery.yaml`
- ISO-Immersion Agent roleplays as detective/suspects
- Preserves mystery game feel within DLI structure

## Example Session Flow

```
$ python cli.py start

[Mission Commander]: ¡Buenos días, agente!
Tu misión: INFILTRAR UNA REUNIÓN DE NEGOCIOS EN MADRID
Vocabulario operacional (50 palabras):
1. "Las ventas del trimestre aumentaron un 15%"
...
¿Estás listo? (sí/no)

> sí

[Mission Commander]: ⚠️ LOCKDOWN ACTIVO: Solo español ⚠️

[ISO-Immersion - Señora García]: Buenos días. Presente los
datos de ventas del último trimestre.

> las ventas aumentar mucho en trimestre

[ISO-Immersion]: ¿Cuánto exactamente?

> quince por ciento más

... [mission continues] ...

[Mission Complete ✓]
Comunicación de intención: 8/10

[Intelligence Analyst]: Analiza esta inteligencia:
"Los inversores están preocupados..."
¿Cuál era la INTENCIÓN?

> hay problema con competencia, necesitan actuar rápido

[Intelligence Analyst]: ✓ Excelente comprensión

[Peel-Back Linguist]: Mira estos patrones:
1. "las ventas aumentar mucho"
2. "necesitan hacer algo"
¿Notas un patrón?

> los verbos no están conjugados?

[Peel-Back Linguist]: ¡Exacto! Veamos...

[Session Complete]
✓ 50 palabras nuevas
✓ 1 misión completada
✓ Racha: 2 días
```

## Dependencies (requirements.txt)

```
anthropic>=0.18.0       # Claude API
pyyaml>=6.0            # YAML parsing
python-dotenv>=1.0.0   # Environment variables
rich>=13.0.0           # Beautiful CLI output
click>=8.1.0           # CLI framework
pydantic>=2.0.0        # Data validation
langdetect>=1.0.9      # Spanish-only enforcement
```

## Risk Mitigation

### Challenge: Claude API Rate Limits
- **Solution:** Exponential backoff in `claude_client.py`, cache common responses, offline mode for vocab review

### Challenge: Vocabulary Pool Exhaustion
- **Solution:** Start with 1000+ word master pool, spaced repetition algorithm

### Challenge: User Frustration (Spanish-Only)
- **Solution:** Difficulty settings in `config/settings.yaml`, SOS command for help

### Challenge: Mission Complexity Scaling
- **Solution:** Dynamic difficulty based on `successful_intent_communications` metric

## Success Metrics

- ✅ All 4 agents operational with distinct roles
- ✅ 40-60 vocabulary words per session (in context, never isolated)
- ✅ Zero grammar corrections during missions (only in Peel-Back Linguist)
- ✅ Pattern recognition before explicit grammar explanation
- ✅ Spanish-only mode enforced at CLI level
- ✅ progress.json seamlessly extended (no data loss)
- ✅ Beautiful CLI output with Rich library
- ✅ Session logging to `data/sessions/`

## Next Steps After Approval

1. Create project structure (directories)
2. Set up Python environment + install dependencies
3. Implement Phase 1: Core Infrastructure (MVP)
4. Test Mission Commander agent
5. Proceed to Phase 2: Role-Play & Orchestration
