---
description: "Provides comprehensive project status report with validation of project_state.json and migration progress analytics"
allowed-tools: ["Read", "Bash", "Task"]
---

# Project Status Agent Orchestration

You are orchestrating project status reporting following the **AI-Orchestrated Development** methodology. Use the **migration-architect** agent for strategic status analysis.

## Agent Assignment
- **Primary Agent**: migration-architect
- **Task**: Generate comprehensive project status report

## Status Analysis Execution Checklist

### Phase 1: State Validation
- [ ] Read and validate `project_state.json` schema and integrity
- [ ] Verify all referenced artifacts exist in `.workflow/` directories
- [ ] Check for orphaned or missing dependencies
- [ ] Validate status transitions and timestamps
- [ ] Identify data inconsistencies or corruption

### Phase 2: Progress Analysis
- [ ] Calculate completion percentages by hierarchy level
- [ ] Analyze velocity and throughput metrics
- [ ] Identify blocked or stalled items
- [ ] Assess resource allocation and utilization

### Phase 3: Quality Metrics Assessment
- [ ] Review recent validation results and trends
- [ ] Analyze code quality metrics over time
- [ ] Evaluate technical debt accumulation
- [ ] Assess test coverage and stability

### Phase 4: Risk & Blockers Identification
- [ ] Identify high-risk items and dependencies
- [ ] Analyze blockers and impediments
- [ ] Review failed validation patterns
- [ ] Assess resource constraints and bottlenecks
- [ ] Evaluate timeline and scope risks

### Phase 5: Strategic Recommendations
- [ ] Provide prioritization recommendations
- [ ] Suggest process improvements
- [ ] Identify optimization opportunities
- [ ] Recommend resource reallocation
- [ ] Propose timeline adjustments

### Phase 6: Report Generation
- [ ] Generate executive summary with key metrics
- [ ] Provide detailed progress breakdown
- [ ] Include actionable recommendations
- [ ] Document critical path and dependencies
- [ ] Output formatted status report

## Status Report Structure

### **Executive Summary**
```markdown
# Wing Commander Saga Migration Status Report
**Generated**: $(date)
**Schema Version**: 2.0.0

## Key Metrics
- **Overall Progress**: X% complete
- **Active PRDs**: X (Y% complete)
- **Active Epics**: X (Y% complete) 
- **Active Stories**: X (Y% complete)
- **Quality Score**: X/10
- **Velocity**: X stories/week
- **Critical Issues**: X blocking items
```

### **Progress Breakdown**
```markdown
## PRD Progress
| PRD ID | Title | Status | Progress | Epic Count | Risk Level |
|--------|-------|--------|----------|------------|------------|
| PRD-001 | Core Systems | In Progress | 65% | 8 | Medium |
| PRD-002 | Asset Pipeline | Planning | 15% | 3 | Low |

## Epic Progress  
| Epic ID | PRD | Title | Status | Progress | Story Count | Blockers |
|---------|-----|-------|--------|----------|-------------|----------|
| EPIC-001 | PRD-001 | Combat System | Active | 80% | 12 | 1 |
| EPIC-002 | PRD-001 | Navigation | Complete | 100% | 8 | 0 |

## Story Progress
| Story ID | Epic | Title | Status | Agent | Quality Gates |
|----------|------|-------|--------|-------|---------------|
| STORY-101 | EPIC-001 | Weapon Systems | Testing | gdscript-engineer | 4/5 Pass |
| STORY-102 | EPIC-001 | Damage Model | Failed | gdscript-engineer | 2/5 Pass |
```

### **Quality Metrics**
```markdown
## Quality Dashboard
- **Code Quality**: 8.5/10 (↑ 0.3 from last week)
- **Test Coverage**: 85% (↑ 2% from last week)
- **Technical Debt**: Medium (↓ improving)

## Recent Quality Trends
- Linting issues: 12 (↓ from 18)
- Failed tests: 3 (↓ from 7)
- Performance regressions: 0 (→ stable)
- Security issues: 0 (→ stable)
```

### **Critical Issues & Blockers**
```markdown
## Critical Issues (Immediate Attention Required)
1. **STORY-102**: Combat damage calculation failing validation
   - **Impact**: Blocks EPIC-001 completion
   - **Assigned**: gdscript-engineer
   - **Recommendation**: Pair programming session needed

2. **Asset Pipeline**: POF model converter performance issues
   - **Impact**: Delays PRD-002 timeline by 2 weeks
   - **Assigned**: asset-pipeline-engineer
   - **Recommendation**: Optimize batch processing algorithm

## Blockers & Dependencies
- **External Dependencies**: 2 pending
- **Cross-team Dependencies**: 1 waiting for approval
- **Technical Blockers**: 3 requiring architecture decisions
```

### **Strategic Recommendations**
```markdown
## Immediate Actions (Next Sprint)
1. **Priority 1**: Resolve STORY-102 validation failures
2. **Priority 2**: Optimize asset pipeline performance
3. **Priority 3**: Complete EPIC-001 final integration testing

## Process Improvements
2. **Velocity**: Consider story size standardization
3. **Risk Management**: Implement earlier dependency tracking

## Resource Optimization
1. **Agent Utilization**: gdscript-engineer at 120% capacity
2. **Skill Gaps**: Need additional asset-pipeline expertise
3. **Bottlenecks**: QA validation becoming constraint
```

## Status Calculation Logic

### **Progress Calculation**
```python
def calculate_progress(artifacts: List[Artifact]) -> float:
    """Calculate weighted progress based on artifact hierarchy."""
    total_weight = 0
    completed_weight = 0
    
    for artifact in artifacts:
        weight = artifact.complexity_weight
        completion = artifact.calculate_completion_percentage()
        
        total_weight += weight
        completed_weight += weight * completion
    
    return completed_weight / total_weight if total_weight > 0 else 0.0
```

### **Quality Score Calculation**
```python
def calculate_quality_score(validation_results: Dict) -> float:
    """Calculate overall quality score from validation metrics."""
    scores = {
        'code_quality': validation_results.get('linting_score', 0),
        'test_coverage': validation_results.get('coverage_percentage', 0) / 100,
        'security': 1.0 if validation_results.get('security_issues', 0) == 0 else 0.5,
        'documentation': validation_results.get('docs_score', 0)
    }
    
    return sum(scores.values()) / len(scores) * 10
```

### **Velocity Calculation**
```python
def calculate_velocity(completed_stories: List[Story], days: int) -> float:
    """Calculate story completion velocity."""
    recent_completions = [
        story for story in completed_stories 
        if (datetime.now() - story.completion_date).days <= days
    ]
    
    return len(recent_completions) / (days / 7)  # stories per week
```

## Validation Commands

### **State Integrity Checks**
```bash
echo "=== Project State Validation ==="
python scripts/validate_project_state.py

echo "=== Artifact Consistency Check ==="
python scripts/check_artifact_links.py

echo "=== Dependency Validation ==="
python scripts/validate_dependencies.py
```

### **Metrics Collection**
```bash
echo "=== Quality Metrics Collection ==="
uv run python scripts/collect_quality_metrics.py

echo "=== Progress Calculation ==="
uv run python scripts/calculate_progress.py
```

## Output Formats

### **Console Summary**
- Concise status overview for quick checking
- Key metrics and immediate actions
- Color-coded status indicators

### **Detailed Report**
- Comprehensive markdown report
- Saved to `.workflow/reports/status-YYYYMMDD.md`
- Suitable for stakeholder review

### **JSON Export**
- Machine-readable status data
- For integration with external tools
- Supports automated reporting

## State-Aware Execution

Use the **Task tool** to invoke the migration-architect agent with:
- Current project state context
- Historical progress data
- Quality metrics and trends
- Risk assessment criteria
- Strategic reporting requirements

**Remember**: Status reporting should provide actionable insights that help maintain project velocity and quality while supporting informed decision-making.