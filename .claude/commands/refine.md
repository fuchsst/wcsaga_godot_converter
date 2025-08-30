---
description: "Refinement and optimization of implemented features with performance tuning, code review, and iterative improvements. Updates project_state.json with refinement results."
allowed-tools: ["Read", "Write", "Edit", "Bash", "Task"]
---

# Refinement Agent Orchestration

You are orchestrating feature refinement following the **AI-Orchestrated Development** methodology. Use specialized agents based on refinement type and scope. This command works with stories or tasks in the `.workflow/` directory structure.

## Agent Selection by Refinement Type
- **Code Quality Improvement**: cpp-code-analyst + gdscript-engineer
- **Architecture Refinement**: godot_architect + godot-systems-designer
- **Asset Optimization**: asset-pipeline-engineer
- **User Experience Enhancement**: godot-systems-designer

## Refinement Execution Checklist

### Phase 1: Refinement Scope Analysis
- [ ] Read `project_state.json` to understand current implementation status
- [ ] Analyze `$ARGUMENTS` to determine refinement scope (story/epic/system)
- [ ] Review validation reports and identified improvement areas
- [ ] Identify specific refinement objectives
- [ ] Locate relevant files in `.workflow/stories/` or `.workflow/tasks/` based on scope

### Phase 2: Current State Assessment
- [ ] Analyze implemented code for optimization opportunities
- [ ] Assess code quality metrics and technical debt
- [ ] Evaluate user experience and interface effectiveness
- [ ] Check integration points for optimization potential

### Phase 3: Refinement Planning
- [ ] Define specific improvement goals and success metrics
- [ ] Plan optimization approaches and techniques
- [ ] Identify risks and potential breaking changes
- [ ] Select appropriate specialized agents for each improvement
- [ ] Create refinement task breakdown in `.workflow/tasks/` if needed

### Phase 4: Iterative Improvement Execution
- [ ] Execute planned optimizations using specialized agents
- [ ] Refactor code for better maintainability
- [ ] Enhance user experience and interface design
- [ ] Optimize asset loading and rendering

### Phase 5: Validation & Measurement
- [ ] Validate improvements meet defined goals
- [ ] Ensure no regressions introduced
- [ ] Update documentation and code comments
- [ ] Record lessons learned and best practices

### Phase 6: State Update & Documentation
- [ ] Update `project_state.json` with refinement results and metrics
- [ ] Document optimization techniques used
- [ ] Provide recommendations for future improvements
- [ ] Update relevant story/task files with refinement outcomes

## Refinement Categories

### **Code Quality Enhancement**
- **Focus**: Maintainability, readability, modularity
- **Techniques**: Refactoring, design patterns, documentation
- **Metrics**: Cyclomatic complexity, code coverage, maintainability index
- **Agent**: cpp-code-analyst + gdscript-engineer

### **Architecture Refinement**
- **Focus**: System design, scalability, extensibility
- **Techniques**: Component composition, signal optimization, scene restructuring
- **Metrics**: Coupling, cohesion, extensibility
- **Agent**: godot_architect + godot-systems-designer

### **Asset Optimization**
- **Focus**: File sizes, loading performance, quality
- **Techniques**: Compression, LOD, streaming, format optimization
- **Metrics**: Asset size, loading time, visual quality
- **Agent**: asset-pipeline-engineer

### **User Experience Enhancement**
- **Focus**: Interface responsiveness, usability, accessibility
- **Techniques**: UI optimization, input handling, visual polish
- **Metrics**: Response time, usability scores, accessibility compliance
- **Agent**: godot-systems-designer

## Optimization Techniques by Domain

### **GDScript Performance Optimization**
```gd
# Performance-optimized patterns:

# 1. Object pooling for frequently created objects
var projectile_pool: Array[Projectile] = []

func get_projectile() -> Projectile:
    if projectile_pool.is_empty():
        return Projectile.new()
    return projectile_pool.pop_back()

# 2. Efficient signal connections
signal health_changed(new_health: int)

func _ready() -> void:
    # Use one-shot connections for temporary listeners
    health_changed.connect(_on_health_changed, CONNECT_ONE_SHOT)

# 3. Batch operations and reduce calls in _process
var _update_timer: float = 0.0
const UPDATE_INTERVAL: float = 0.1

func _process(delta: float) -> void:
    _update_timer += delta
    if _update_timer >= UPDATE_INTERVAL:
        _batch_update_systems()
        _update_timer = 0.0
```

### **Asset Optimization**
```python
# Asset optimization techniques:

class AssetOptimizer:
    def optimize_texture(self, texture_path: Path) -> bool:
        """Optimize texture for Godot with appropriate compression."""
        # Implement texture compression based on usage
        # - UI textures: lossy compression
        # - Normal maps: lossless compression
        # - Albedo textures: lossy with quality preservation
        
    def create_lod_chain(self, model_path: Path) -> List[Path]:
        """Generate LOD chain for 3D models."""
        # Create multiple detail levels for distance-based rendering
        
    def optimize_audio(self, audio_path: Path) -> bool:
        """Optimize audio files for streaming and memory usage."""
        # Convert to appropriate format and bitrate for usage context
```

### **Scene Tree Optimization**
```
# Optimized scene hierarchy patterns:

# Before: Deep nesting with performance issues
Ship (RigidBody3D)
├── Model (Node3D)
│   ├── Hull (MeshInstance3D)
│   ├── Weapons (Node3D)
│   │   ├── Gun1 (Node3D)
│   │   │   ├── Mesh (MeshInstance3D)
│   │   │   └── Muzzle (Node3D)
│   │   └── Gun2 (Node3D)
│   │       ├── Mesh (MeshInstance3D)
│   │       └── Muzzle (Node3D)

# After: Flattened hierarchy with component composition
Ship (RigidBody3D)
├── HullMesh (MeshInstance3D)
├── WeaponSystem (Node3D)
├── EffectManager (Node3D)
└── AudioManager (Node3D)
```

## Refinement Measurement & Validation

### **Performance Metrics**
```bash
# Automated performance benchmarking
echo "=== Performance Baseline ==="
uv run pytest tests/performance/baseline/ -v

echo "=== Post-Optimization Performance ==="
uv run pytest tests/performance/optimized/ -v

echo "=== Performance Comparison ==="
python scripts/compare_performance_metrics.py
```

### **Code Quality Metrics**
```bash
# Code quality assessment
echo "=== Code Complexity Analysis ==="
uv run radon cc converter/ data_converter/

echo "=== Code Coverage ==="
uv run pytest --cov --cov-report=html

echo "=== Technical Debt Assessment ==="
uv run ruff check . --statistics
```

### **Memory Profiling**
```bash
# Memory usage analysis
echo "=== Memory Profiling ==="
uv run python -m memory_profiler scripts/profile_memory.py

echo "=== Godot Memory Usage ==="
# Add Godot-specific memory profiling commands
```

## Iterative Refinement Process

### **1. Identify Bottlenecks**
- Profile application to find performance hotspots
- Analyze code metrics to identify complexity issues
- Review user feedback for UX pain points

### **2. Plan Optimizations**
- Prioritize improvements by impact vs effort
- Design optimization approach
- Identify potential risks and mitigation strategies

### **3. Implement Improvements**
- Apply optimizations incrementally
- Maintain test coverage during refactoring
- Document changes and reasoning

### **4. Validate Results**
- Measure improvement against baseline
- Ensure no functionality regressions
- Validate user experience improvements

### **5. Document & Share**
- Record optimization techniques used
- Update performance baselines
- Share learnings with team

## Refinement Report Template

```markdown
# Refinement Report: $ARGUMENTS

## Objectives
- [List specific improvement goals]

## Baseline Metrics
- **Performance**: [Before measurements]
- **Code Quality**: [Quality metrics before]
- **User Experience**: [UX metrics before]

## Improvements Applied
### Performance Optimizations
- [List specific optimizations]

### Code Quality Enhancements
- [List refactoring and cleanup]

### User Experience Improvements
- [List UX enhancements]

## Results Achieved
- **Performance Gains**: [Measured improvements]
- **Quality Improvements**: [Quality metric improvements]
- **User Experience**: [UX improvement validation]

## Lessons Learned
- [Key insights and techniques]

## Future Optimization Opportunities
- [Identified areas for future improvement]
```

## State-Aware Execution

Use the **Task tool** to invoke the appropriate specialized agent with:
- Current implementation state and metrics from `project_state.json`
- Specific refinement objectives and scope
- Performance baselines and target improvements
- Quality standards and optimization techniques
- Validation criteria and success metrics
- References to relevant files in `.workflow/stories/` or `.workflow/tasks/`

After successful refinement and validation, ensure that:
1. The `project_state.json` file is updated with refinement results, metrics, and improvement data
2. Relevant story or task files are updated with refinement outcomes
3. Documentation is updated to reflect optimizations and improvements
4. Lessons learned and best practices are recorded for future reference

**Remember**: Refinement is an iterative process focused on measurable improvements while maintaining system stability and functionality. All refinement activities should be tracked in the project state for progress monitoring.