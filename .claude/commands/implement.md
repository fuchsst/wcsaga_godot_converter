---
description: "Implements migration tasks using specialized agents with automated quality gates and state management"
allowed-tools: ["Read", "Write", "Edit", "MultiEdit", "Bash", "Task"]
---

# Implementation Agent Orchestration

You are orchestrating task implementation following the **AI-Orchestrated Development** methodology. Use specialized agents based on task type and complexity.

## Agent Selection by Task Type
- **Code Migration**: gdscript-engineer
- **Asset Pipeline**: asset-pipeline-engineer
- **System Architecture**: godot-systems-designer
- **UI/UX Development**: gdscript-engineer + godot-systems-designer
- **Quality Assurance**: qa-engineer

## Implementation Execution Checklist

### Phase 1: Task Context Loading
- [ ] Read task file: `.workflow/tasks/$ARGUMENTS.md`
- [ ] Update task status to 'in_progress' in frontmatter
- [ ] Extract implementation requirements and acceptance criteria
- [ ] Identify assigned agent and complexity level
- [ ] Load parent story and epic context

### Phase 2: Feedback Processing
- [ ] **CRITICAL**: Check for "## Feedback" section in task file
- [ ] If feedback exists, prioritize addressing it above all instructions
- [ ] Incorporate human feedback into implementation approach
- [ ] Document feedback resolution strategy

### Phase 3: Implementation Environment Setup
- [ ] Read `project_state.json` for current project context
- [ ] Analyze files to be modified and their dependencies
- [ ] Understand current Godot project structure
- [ ] Prepare development environment and tools

### Phase 4: Specialized Agent Execution
- [ ] Invoke appropriate agent via Task tool
- [ ] Provide complete context and requirements
- [ ] Follow Godot architecture patterns and conventions
- [ ] Implement all acceptance criteria systematically

### Phase 5: Automated Quality Gates
- [ ] **Code Formatting**: `uv run gdformat .`
- [ ] **Code Linting**: `uv run gdlint .`
- [ ] **Python Quality**: `uv run ruff check .`
- [ ] **Unit Testing**: `uv run pytest tests/unit/`
- [ ] **Integration Testing**: `uv run pytest tests/integration/`

### Phase 6: Completion Documentation
- [ ] Mark all acceptance criteria as `[x]` completed
- [ ] Update task status to 'completed' in frontmatter
- [ ] Update `project_state.json` with completion metadata
- [ ] Generate implementation summary and lessons learned

## Implementation Patterns by Task Type

### **GDScript Code Implementation**
```gd
# Follow Godot conventions:
# - Signal-based communication
# - Proper node lifecycle management
# - Type hints and static typing
# - Documentation comments
# - Error handling

extends Node

signal system_ready
signal system_error(message: String)

@export var config: SystemConfig
var _initialized: bool = false

func _ready() -> void:
    await _initialize_system()
    
func _initialize_system() -> void:
    # Implementation with proper error handling
    pass
```

### **Asset Pipeline Implementation**
```python
# Asset conversion patterns:
# - Robust error handling
# - Progress reporting
# - Batch processing
# - Quality validation

class AssetConverter:
    def convert_asset(self, source_path: Path, target_path: Path) -> bool:
        try:
            # Conversion logic
            return self._validate_conversion(target_path)
        except Exception as e:
            logger.error(f"Conversion failed: {e}")
            return False
```

### **Scene Architecture Implementation**
```
# Godot scene structure patterns:
# - Clear hierarchy
# - Single responsibility nodes
# - Proper signal connections
# - Resource management

MainSystem (Node)
├── SystemManager (Node)
├── UIController (Control)
│   ├── MainPanel (Panel)
│   └── StatusBar (HBoxContainer)
└── AudioManager (Node)
    ├── MusicPlayer (AudioStreamPlayer)
    └── SFXPlayer (AudioStreamPlayer)
```

## Error Handling Protocols

### **Recoverable Errors**
- Document in task file "## Issues" section
- Attempt alternative implementation approach
- Update acceptance criteria if scope adjustment needed
- Continue with partial implementation
- Request human guidance if needed

### **Blocking Errors**
- Set task status to 'failed' in frontmatter
- Document failure in "## Failure Analysis" section
- Update `project_state.json` with failure metadata
- Generate detailed error report for human review
- Suggest remediation steps and alternatives

## Quality Assurance Integration

### **Automated Checks**
```bash
# Pre-commit quality gates
echo "=== Code Formatting ==="
uv run gdformat . || echo "FORMATTING_ISSUES"

echo "=== Code Linting ==="
uv run gdlint . || echo "LINTING_ISSUES"

echo "=== Python Quality ==="
uv run ruff check . || echo "PYTHON_ISSUES"

echo "=== Unit Tests ==="
uv run pytest tests/unit/ -v || echo "UNIT_TEST_FAILURES"

echo "=== Integration Tests ==="
uv run pytest tests/integration/ -v || echo "INTEGRATION_FAILURES"
```

### **Migration-Specific Validation**
- **Behavior**: Validate functionality matches original implementation
- **Integration**: Confirm proper interaction with existing systems
- **Assets**: Verify converted assets load and render correctly

## Task Status Management

### **Status Progression**
1. **pending** → Task created, not started
2. **in_progress** → Implementation underway
3. **testing** → Implementation complete, validation in progress
4. **completed** → All acceptance criteria met, quality gates passed
5. **failed** → Blocking issues prevent completion

### **State Updates**
```json
{
  "task_id": "$ARGUMENTS",
  "status": "completed",
  "completion_date": "2025-08-29T15:30:00Z",
  "agent_used": "gdscript-engineer",
  "quality_gates": {
    "formatting": "passed",
    "linting": "passed", 
    "unit_tests": "passed",
    "integration_tests": "passed"
  },
  "files_modified": ["scripts/System.gd", "scenes/MainSystem.tscn"],
  "lessons_learned": ["Signal pattern worked well", "Performance optimization needed"]
}
```

## State-Aware Execution

Use the **Task tool** to invoke the appropriate specialized agent with:
- Complete task context and implementation requirements
- Current project state and dependency information
- Quality standards and validation criteria
- Error handling protocols and escalation paths

**Remember**: Each task represents atomic, testable progress that moves the Wing Commander Saga migration forward while maintaining high quality standards.