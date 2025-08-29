---
description: "Creates and manages project planning artifacts (PRDs, Epics, Stories) following AI-Orchestrated Development methodology"
allowed-tools: ["Write", "Read", "Edit", "Bash", "Task"]
---

# Project Planning Agent Orchestration

You are orchestrating project planning following the **AI-Orchestrated Development** methodology. Use specialized agents based on planning level.

## Planning Level Detection
Analyze `$ARGUMENTS` to determine planning level:
- **PRD Level**: Contains broad business/technical requirements
- **Epic Level**: Contains feature-set or system-level scope  
- **Story Level**: Contains specific, implementable tasks

## Agent Assignment by Level

### **PRD Planning**
- **Agent**: migration-architect
- **Trigger**: Broad requirements, business goals, system-wide migration
- **Output**: `.workflow/prds/PRD-{ID}-{slug}.md`

### **Epic Planning** 
- **Agent**: lead-developer
- **Trigger**: Feature breakdown, component migration, system phases
- **Output**: `.workflow/epics/EPIC-{ID}-{slug}.md`

### **Story Planning**
- **Agent**: godot-systems-designer
- **Trigger**: Specific implementation tasks, "As a..." statements
- **Output**: `.workflow/stories/STORY-{ID}-{slug}.md`

## Execution Workflow

### Phase 1: Context Analysis
- [ ] Read `project_state.json` for current project state
- [ ] Analyze `$ARGUMENTS` to determine planning level and scope
- [ ] Identify parent artifacts (PRD → Epic → Story hierarchy)
- [ ] Check for dependencies and conflicts

### Phase 2: Agent Delegation
- [ ] Select appropriate specialized agent based on detected level
- [ ] Provide complete context including project state
- [ ] Include relevant templates and patterns
- [ ] Specify Wing Commander Saga migration context

### Phase 3: Artifact Creation
- [ ] Generate unique ID: `{TYPE}-NNN`
- [ ] Create structured markdown file in appropriate `.workflow/` directory
- [ ] Follow hierarchical linkage (Stories → Epics → PRDs)
- [ ] Include all required sections per artifact type

### Phase 4: State Management
- [ ] Update `project_state.json` with new artifact
- [ ] Link to parent artifacts and dependencies
- [ ] Set appropriate initial status
- [ ] Record metadata and relationships

## Planning Templates

### **PRD Template Structure**
```markdown
# PRD-{ID}: {Title}

## Business Context
Why this migration is needed for Wing Commander Saga

## Technical Scope  
Specific C++ → Godot migration areas covered

## Success Criteria
Measurable completion outcomes

## Dependencies
Other PRDs or external requirements

## Risk Assessment
Migration-specific challenges and mitigation strategies
```

### **Epic Template Structure**
```markdown
# EPIC-{ID}: {Title}

## PRD Reference
Link to parent PRD

## Technical Scope
Specific systems/components this epic addresses

## Implementation Phases
3-7 development phases with clear milestones

## Acceptance Criteria
What defines epic completion

## Agent Assignments
Which specialized agents handle each phase
```

### **Story Template Structure**
```markdown
# STORY-{ID}: {Title}

## User Story
"As a [role], I want [goal] so that [benefit]"

## Epic Reference
Link to parent epic

## Godot Implementation
Specific nodes, systems, and patterns to use

## Acceptance Criteria
- [ ] Functional requirements
- [ ] Quality gates (tests, format, integration)
- [ ] Documentation requirements

## Definition of Done
Technical completion checklist

## Agent Assignment
Which specialized agent implements this story
```

## Migration-Specific Planning Guidance

### **System Categories**
- **Gameplay Systems**: Combat, navigation, AI, physics
- **Asset Pipeline**: Models, textures, audio conversion
- **UI/UX Systems**: Interface migration to Godot scenes
- **Data Systems**: Save games, configuration, persistence
- **Rendering**: Graphics, shaders, visual effects
- **Audio**: 3D audio, music, sound effects

### **Godot Architecture Patterns**
- **Scene Tree Design**: Hierarchical node organization
- **Signal Communication**: Event-driven interactions
- **Resource Management**: Asset loading and caching
- **Component Composition**: Node-based functionality

## State-Aware Execution

Use the **Task tool** to invoke the appropriate agent with:
- Complete project context from `project_state.json`
- Detected planning level and requirements
- Migration-specific templates and patterns
- Quality standards and validation criteria

**Remember**: Each artifact should fit within the hierarchical structure and support the overall Wing Commander Saga → Godot migration strategy.