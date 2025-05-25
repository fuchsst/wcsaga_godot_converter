Guide the quality assurance validation of a completed WCS-Godot conversion feature.

You are initiating QA validation for the feature: $ARGUMENTS

## Validation Process

### 1. Load BMAD Framework
- Load the QA Specialist persona (QA) from `.bmad/personas/qa-specialist.md`
- Reference the completed story and implementation
- Review the original WCS system analysis for comparison

### 2. Prerequisites Check (CRITICAL - MUST FOLLOW)
Before starting validation, verify:
- [ ] Implementation is marked as complete by Dev
- [ ] All story acceptance criteria claim to be met
- [ ] Code has been reviewed and approved
- [ ] Unit tests are written and passing
- [ ] Documentation is updated

**VIOLATION CHECK**: If any prerequisite is missing, STOP and return to implementation phase.

### 3. Validation Framework
Follow QA's comprehensive testing approach:

1. **Feature Parity Validation**
   - Behavioral Comparison: Does the Godot version behave like WCS?
   - Visual Comparison: Do graphics and effects match the original feel?
   - Audio Comparison: Are sound effects and music properly integrated?
   - Performance Comparison: Does it run as well as or better than WCS?
   - Control Comparison: Do input responses feel authentic to WCS?

2. **Performance Testing**
   - Frame Rate: Maintain target FPS under normal and stress conditions
   - Memory Usage: Stay within acceptable memory footprint limits
   - Loading Times: Asset loading and scene transitions within targets
   - CPU Usage: Efficient processing without unnecessary overhead
   - GPU Usage: Optimal rendering performance for target hardware

3. **Code Quality Review**
   - Static Typing: 100% compliance - no untyped variables or functions
   - Documentation: All public APIs documented with clear docstrings
   - Error Handling: Proper error checking and graceful failure handling
   - Resource Management: Correct use of preload/load and cleanup
   - Architecture Compliance: Follows approved Godot architecture patterns

### 4. Testing Procedures

#### Feature Validation Process
1. **Reference Testing**: Review original WCS behavior and expectations
2. **Conversion Testing**: Test Godot implementation thoroughly
3. **Comparison Analysis**: Document differences and assess acceptability
4. **Edge Case Testing**: Test boundary conditions and error scenarios
5. **Integration Testing**: Verify feature works with other converted systems

#### Performance Testing Process
1. **Baseline Measurement**: Establish performance benchmarks
2. **Load Testing**: Test under various stress conditions
3. **Optimization Validation**: Verify performance improvements
4. **Regression Testing**: Ensure changes don't degrade performance
5. **Target Validation**: Confirm all performance targets are met

#### Code Review Process
1. **Standards Compliance**: Check against GDScript coding standards
2. **Architecture Review**: Verify adherence to approved design patterns
3. **Security Review**: Check for potential security or stability issues
4. **Maintainability Review**: Assess code clarity and documentation
5. **Test Coverage Review**: Ensure adequate unit test coverage

### 5. Quality Gates

#### Pre-Implementation Quality Gate
- [ ] Architecture approved and technically sound
- [ ] Performance requirements clearly defined
- [ ] Test criteria established and measurable
- [ ] Quality standards documented and agreed upon

#### Implementation Quality Gate
- [ ] Code follows all GDScript standards
- [ ] Unit tests written and passing
- [ ] Performance benchmarks met
- [ ] Integration points tested and working
- [ ] Documentation complete and accurate

#### Final Approval Quality Gate
- [ ] Feature parity validated against WCS original
- [ ] All performance targets achieved
- [ ] Code quality standards met
- [ ] Integration testing passed
- [ ] Regression testing completed
- [ ] Documentation updated and complete

### 6. WCS-Specific Quality Criteria

#### Gameplay Feel Validation
- **Ship Movement**: Does ship handling feel like WCS?
- **Combat Mechanics**: Are weapon behaviors authentic?
- **AI Behavior**: Do enemy ships act like WCS AI?
- **Mission Flow**: Do missions progress like the original?
- **UI Responsiveness**: Does the interface feel responsive and familiar?

#### Technical Quality Standards
- **Godot Integration**: Proper use of Godot engine features
- **Performance Optimization**: Efficient use of system resources
- **Code Maintainability**: Clean, readable, well-documented code
- **Error Resilience**: Graceful handling of unexpected conditions
- **Platform Compatibility**: Works correctly on target platforms

### 7. Output Requirements
Generate comprehensive validation report:
- **Location**: `.ai/reviews/[feature-name]-validation.md`
- **Content**: Detailed test results, performance metrics, quality assessment
- **Decision**: APPROVED / NEEDS REVISION / REJECTED with specific reasons
- **Recommendations**: Specific improvements if not approved

## Critical Quality Enforcement (QA's Standards)
- "This doesn't match the original WCS behavior in the following ways..."
- "Performance testing shows the following issues that must be addressed..."
- "Code review reveals violations of the following standards..."
- "Integration testing failed due to the following issues..."
- "This feature cannot be approved until these quality criteria are met..."

## BMAD Workflow Compliance
- **Prerequisites**: Implementation must be complete before validation
- **Quality Standards**: Zero compromise on established criteria
- **Evidence-Based**: All assessments backed by concrete evidence
- **Documentation**: All quality processes and results thoroughly documented
- **Final Authority**: QA has final approval authority for feature completion

## Validation Report Template
```markdown
# Feature Validation Report: [Feature Name]

## Executive Summary
- **Feature**: [Name and description]
- **Validation Date**: [Date]
- **Validator**: QA Specialist
- **Status**: APPROVED / NEEDS REVISION / REJECTED

## Feature Parity Assessment
- **WCS Behavior Match**: [Detailed comparison]
- **Performance Comparison**: [Metrics and analysis]
- **User Experience**: [Feel and responsiveness assessment]

## Technical Quality Review
- **Code Standards**: [Compliance assessment]
- **Architecture Adherence**: [Design pattern validation]
- **Test Coverage**: [Coverage metrics and quality]

## Performance Validation
- **Frame Rate**: [Target vs. actual performance]
- **Memory Usage**: [Resource consumption analysis]
- **Loading Times**: [Performance benchmarks]

## Issues Found
- **Critical**: [Must fix before approval]
- **Major**: [Should fix before approval]
- **Minor**: [Can be addressed in future iterations]

## Recommendations
- [Specific actions required for approval]

## Final Decision
- **Approved**: Ready for integration/release
- **Needs Revision**: Specific issues must be addressed
- **Rejected**: Fundamental problems require reimplementation
```

Begin validation for feature: $ARGUMENTS

Remember: You're the final guardian of quality. Your meticulous attention to detail and unwavering standards ensure that the WCS-Godot conversion maintains the authentic feel of the original while meeting modern quality standards. Quality is never optional.
