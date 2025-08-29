---
description: "Breaks down user stories into detailed implementation tasks with Godot migration patterns and agent assignments"
allowed-tools: ["Read", "Write", "Glob", "Grep", "Task"]
---

# Task Breakdown Agent Orchestration

You are orchestrating task breakdown following the **AI-Orchestrated Development** methodology. Use the **godot-architect** agent for technical analysis and decomposition.

## Agent Assignment
- **Primary Agent**: godot-architect
- **Task**: Break down story into implementation tasks: "$ARGUMENTS"

## Breakdown Execution Checklist

### Phase 1: Story Analysis
- [ ] Read `project_state.json` to understand project context
- [ ] Locate story file: `.workflow/stories/$ARGUMENTS.md`
- [ ] Extract acceptance criteria and technical requirements
- [ ] Identify parent Epic and PRD for broader context
- [ ] Analyze complexity and scope

### Phase 2: Codebase Analysis
- [ ] Examine relevant C++ source code and architecture
- [ ] Identify current implementation patterns and dependencies
- [ ] Map existing data structures and algorithms
- [ ] Understand integration points with other systems

### Phase 3: Godot Architecture Design
- [ ] Plan scene tree structure and node hierarchy
- [ ] Define signal-based communication patterns
- [ ] Map C++ classes to GDScript equivalents
- [ ] Design resource management approach

### Phase 4: Task Decomposition
- [ ] Break story into 3-8 atomic implementation tasks
- [ ] Order tasks by logical dependencies
- [ ] Assign specialized agents to each task
- [ ] Define validation criteria per task

### Phase 5: Task Documentation
- [ ] Create task files in `.workflow/tasks/`
- [ ] Generate structured JSON breakdown plan
- [ ] Update story with task references
- [ ] Update project state with task metadata

## Task Categories & Agent Assignments

### **Code Migration Tasks**
- **Agent**: gdscript-engineer
- **Focus**: C++ → GDScript algorithm conversion
- **Pattern**: Analysis → Design → Implementation → Testing

### **Asset Pipeline Tasks**
- **Agent**: asset-pipeline-engineer
- **Focus**: Format conversion and import workflows
- **Pattern**: Format analysis → Converter → Pipeline → Validation

### **System Architecture Tasks**
- **Agent**: godot-systems-designer
- **Focus**: Node composition and scene design
- **Pattern**: Architecture → Components → Integration → Testing

### **UI/UX Tasks**
- **Agent**: gdscript-engineer + godot-systems-designer
- **Focus**: Control nodes and interface logic
- **Pattern**: Layout → Theme → Logic → UX Testing

### **Quality Assurance Tasks**
- **Agent**: qa-engineer
- **Focus**: Testing, validation, performance
- **Pattern**: Test design → Implementation → Automation → Reporting

## Task Template Structure

```json
{
  "id": "task-{story-id}-{seq}",
  "title": "Specific implementation task",
  "description": "Detailed task description with context",
  "story_id": "$ARGUMENTS",
  "dependencies": ["task-{story-id}-{prev}"],
  "agent": "specialized-agent-name",
  "complexity": "low|medium|high",
  "files_to_modify": ["path/to/file.gd", "scenes/Scene.tscn"],
  "validation_criteria": [
    "Specific testable outcome",
    "Quality gate requirement"
  ],
  "godot_patterns": [
    "Node composition pattern used",
    "Signal communication approach"
  ],
  "estimated_hours": 2-8
}
```

## Migration-Specific Task Patterns

### **Gameplay System Migration**
1. **C++ Analysis**: Study original implementation
2. **GDScript Design**: Plan equivalent Godot approach
3. **Core Implementation**: Convert algorithms and logic
4. **Integration**: Connect with Godot systems

### **Asset Conversion Pipeline**
1. **Format Analysis**: Understand source asset structure
2. **Converter Development**: Build conversion tools
3. **Import Pipeline**: Integrate with Godot import system
4. **Quality Validation**: Verify converted assets
5. **Batch Processing**: Enable bulk conversion

### **UI System Migration**
1. **Layout Analysis**: Study original UI structure
2. **Control Node Design**: Plan Godot Control hierarchy
3. **Theme Development**: Create consistent styling
4. **Logic Implementation**: Port interaction code
5. **Responsive Testing**: Validate across screen sizes

## JSON Output Format

```json
{
  "story_id": "$ARGUMENTS",
  "breakdown_date": "2025-08-29",
  "total_tasks": 5,
  "estimated_hours": 24,
  "critical_path": ["task-001", "task-003", "task-005"],
  "tasks": [
    {
      "id": "task-{story-id}-001",
      "title": "Analyze C++ [system] implementation",
      "description": "Study existing code and document architecture",
      "dependencies": [],
      "agent": "godot-architect",
      "complexity": "medium",
      "files_to_modify": ["analysis/system_review.md"],
      "validation_criteria": ["Architecture documented", "Dependencies mapped"],
      "estimated_hours": 4
    }
  ]
}
```

## Quality Gates

### **Task Definition Quality**
- Each task is atomic and testable
- Clear agent assignment with appropriate skills
- Well-defined acceptance criteria
- Realistic time estimates
- Proper dependency ordering

### **Technical Quality**
- Godot best practices incorporated
- Integration points identified
- Error handling planned

## State-Aware Execution

Use the **Task tool** to invoke the godot-architect agent with:
- Complete story context and requirements
- Current project state information
- Codebase analysis findings
- Godot architecture guidelines
- Task decomposition templates

**Output**: Structured JSON breakdown ready for implementation phase.