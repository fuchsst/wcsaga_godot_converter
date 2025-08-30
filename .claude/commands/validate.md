---
description: "Comprehensive validation of migration tasks with quality gates, performance testing, and integration verification"
allowed-tools: ["Bash", "Write", "Read", "Task"]
---

# Validation Agent Orchestration

You are orchestrating comprehensive validation following the **AI-Orchestrated Development** methodology. Use the **qa_engineer** agent for systematic quality assurance.

## Agent Assignment
- **Primary Agent**: qa_engineer
- **Task**: Validate implementation of: "$ARGUMENTS"

## Validation Execution Checklist

### Phase 1: Context Loading & Analysis
- [ ] Read task/story file: `.workflow/tasks/$ARGUMENTS.md` or `.workflow/stories/$ARGUMENTS.md`
- [ ] Extract validation requirements and acceptance criteria
- [ ] Identify modified files and affected systems
- [ ] Review implementation completeness against requirements
- [ ] Load current project state context from `project_state.json`

### Phase 2: Code Quality Gates
- [ ] **GDScript Formatting**: `uv run gdformat --check .`
- [ ] **GDScript Linting**: `uv run gdlint .`
- [ ] **Python Code Quality**: `uv run ruff check .`
- [ ] **Type Checking**: `uv run mypy converter/ data_converter/` (if applicable)
- [ ] **Security Scanning**: Static analysis for common vulnerabilities

### Phase 3: Testing Gates
- [ ] **Unit Tests**: `uv run pytest tests/unit/ -v --cov`
- [ ] **Integration Tests**: `uv run pytest tests/integration/ -v`
- [ ] **Migration Tests**: `uv run pytest tests/migration/ -v`
- [ ] **Regression Tests**: Validate existing functionality unchanged

### Phase 4: Godot-Specific Validation
- [ ] **Project Structure**: Validate Godot project integrity
- [ ] **Scene Loading**: Test all .tscn files load without errors
- [ ] **Resource References**: Check for broken asset references
- [ ] **Signal Connections**: Validate signal wiring correctness
- [ ] **Node Hierarchy**: Verify scene tree structure is optimal

### Phase 5: Migration-Specific Validation
- [ ] **Behavioral Compatibility**: Verify functionality matches C++ original
- [ ] **Asset Quality**: Validate converted assets render correctly
- [ ] **Integration Points**: Test system interactions work properly
- [ ] **Data Migration**: Verify data structures convert correctly

### Phase 6: Documentation & Reporting
- [ ] Generate comprehensive validation report
- [ ] Update task/story status based on results
- [ ] Update `project_state.json` with validation metadata and results
- [ ] Document any issues for remediation in `.workflow/logs/`
- [ ] Provide recommendations for improvements

## Quality Gate Definitions

### **PASS Criteria**
- All automated checks pass (exit code 0)
- All acceptance criteria validated successfully
- All integration points function correctly
- Documentation is complete and accurate

### **FAIL Criteria**
- Any critical quality check fails
- Core functionality is broken or missing
- Integration failures block other systems
- Security vulnerabilities detected

### **WARNING Criteria**
- Non-critical linting warnings present
- Optional features not fully implemented
- Documentation gaps identified
- Technical debt introduced

## Validation Command Sequences

### **Core Quality Checks**
```bash
echo "=== GDScript Quality Gates ==="
uv run gdformat --check . || echo "FORMATTING_FAILED"
uv run gdlint . || echo "LINTING_FAILED"

echo "=== Python Quality Gates ==="
uv run ruff check . || echo "RUFF_FAILED"
uv run mypy converter/ data_converter/ || echo "TYPING_FAILED"

echo "=== Security Scanning ==="
uv run bandit -r converter/ data_converter/ || echo "SECURITY_ISSUES"
```

### **Testing Gates**
```bash
echo "=== Unit Testing ==="
uv run pytest tests/unit/ -v --cov --cov-report=term-missing || echo "UNIT_TESTS_FAILED"

echo "=== Integration Testing ==="
uv run pytest tests/integration/ -v || echo "INTEGRATION_TESTS_FAILED"

echo "=== Migration Testing ==="
uv run pytest tests/migration/ -v || echo "MIGRATION_TESTS_FAILED"
```

### **Godot Project Validation**
```bash
echo "=== Project Structure ==="
test -f project.godot && echo "✓ project.godot found" || echo "✗ project.godot missing"
test -f export_presets.cfg && echo "✓ export_presets.cfg found" || echo "⚠ export_presets.cfg missing"

echo "=== Scene Validation ==="
find . -name "*.tscn" -exec echo "Validating scene: {}" \;
# Add Godot scene validation commands

echo "=== Resource Validation ==="
find . -name "*.tres" -exec echo "Validating resource: {}" \;
# Add resource integrity checks
```

## Performance Validation

### **Benchmarking**
```bash
echo "=== Performance Benchmarks ==="
# Migration-specific performance tests
uv run pytest tests/performance/test_combat_performance.py -v
uv run pytest tests/performance/test_asset_loading.py -v
uv run pytest tests/performance/test_rendering_performance.py -v
```

### **Memory Usage**
```bash
echo "=== Memory Profiling ==="
# Memory usage validation for Godot systems
uv run pytest tests/performance/test_memory_usage.py -v
```

## Migration-Specific Validation

### **Asset Pipeline Validation**
- Verify converted models load in Godot
- Check texture compression and quality
- Validate audio format conversion

### **Gameplay System Validation**
- Compare behavior with C++ original
- Validate physics interactions
- Verify combat mechanics accuracy

### **UI System Validation**
- Test Control node functionality
- Validate theme application
- Check input handling
- Verify responsive design

## Error Handling & Reporting

### **Success Path**
```bash
# Update validation status to PASSED
# Update project_state.json with success metadata
# Generate success summary report in .workflow/logs/
# Mark all quality gates as completed
```

### **Failure Path**
```bash
# Capture complete stdout/stderr of failing commands
# Save detailed logs to .workflow/logs/$ARGUMENTS-validation-failure.log
# Update status to VALIDATION_FAILED in task/story file
# Update project_state.json with failure metadata
# Generate comprehensive failure analysis
# Provide specific remediation steps
```

## Validation Report Template

```markdown
# Validation Report: $ARGUMENTS

## Executive Summary
- **Overall Status**: PASS/FAIL/WARNING
- **Validation Date**: $(date)
- **Total Checks**: X
- **Passed**: Y  
- **Failed**: Z
- **Warnings**: W

## Quality Gates Results
- [ ] GDScript Formatting: PASS/FAIL
- [ ] GDScript Linting: PASS/FAIL
- [ ] Python Quality: PASS/FAIL
- [ ] Unit Tests: PASS/FAIL (X% coverage)
- [ ] Integration Tests: PASS/FAIL
- [ ] Project Structure: PASS/FAIL

## Migration-Specific Results
- [ ] Asset Validation: PASS/FAIL
- [ ] Behavioral Compatibility: PASS/FAIL
- [ ] Integration Points: PASS/FAIL

## Critical Issues
[List any critical issues that must be resolved]

## Warnings & Recommendations
[List non-blocking issues and improvement suggestions]

## Next Steps
[Provide clear action items for remediation]
```

## State-Aware Execution

Use the **Task tool** to invoke the qa_engineer agent with:
- Complete validation context and requirements
- Current project state information from `project_state.json`
- Quality gate definitions and thresholds
- Error handling and reporting procedures
- Migration-specific validation criteria

After validation is complete, ensure that:
1. The `project_state.json` file is updated with validation results, metadata, and statistics
2. Task or story status is updated in the respective markdown file
3. All validation logs are saved to `.workflow/logs/` with appropriate naming
4. Any failed validations generate automated feedback as described in the error handling procedures
5. Validation metrics and trends are tracked for project analytics

**Critical**: Validation should be thorough but not create unnecessary development friction. Focus on ensuring quality while maintaining velocity toward Wing Commander Saga migration goals. All validation activities should update the project state for progress tracking.