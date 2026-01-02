---
name: code-review
description: Comprehensive code review following industry best practices
tags: [code-review, quality, security, performance]
version: 1.0.0
author: standard-syntax
---

# Code Review Skill

This skill provides comprehensive code review capabilities following industry best practices.

## Review Checklist

### Security

1. **Input Validation**
   - All user inputs are validated
   - Type checking is enforced
   - SQL injection prevention (parameterized queries)
   - XSS prevention (output encoding)

2. **Authentication & Authorization**
   - Proper authentication mechanisms
   - Authorization checks on all endpoints
   - Secure password handling (hashing, salting)
   - Session management

3. **Data Protection**
   - Sensitive data encryption
   - Secure communication (HTTPS)
   - Proper error messages (no sensitive info leakage)
   - Secure file uploads

4. **Dependencies**
   - No known vulnerable dependencies
   - Dependencies are up to date
   - Minimal dependency footprint

### Performance

1. **Database Operations**
   - Efficient queries (no N+1 problems)
   - Proper indexing
   - Connection pooling
   - Query optimization

2. **Resource Management**
   - Proper resource cleanup (files, connections)
   - Memory efficiency
   - Caching where appropriate
   - Async operations for I/O

3. **Scalability**
   - Stateless design where possible
   - Rate limiting implementation
   - Load balancing considerations

### Code Quality

1. **Readability**
   - Clear, descriptive names
   - Appropriate comments
   - Consistent formatting (PEP 8 for Python)
   - Logical code organization

2. **Maintainability**
   - DRY principle (Don't Repeat Yourself)
   - Single Responsibility Principle
   - Proper error handling
   - Comprehensive logging

3. **Testing**
   - Unit tests present
   - Integration tests where needed
   - Edge cases covered
   - >80% code coverage

4. **Documentation**
   - API documentation
   - Inline docstrings
   - README with setup/usage
   - Architecture diagrams if complex

### Python-Specific

1. **Type Hints**
   - All function signatures have type hints
   - Return types specified
   - Complex types properly annotated

2. **Error Handling**
   - Specific exception types
   - Proper exception hierarchy
   - Context managers for resources
   - Graceful degradation

3. **Best Practices**
   - Using context managers (with statements)
   - List/dict comprehensions where appropriate
   - Generator expressions for large datasets
   - Proper use of standard library

## Review Process

When conducting a code review:

1. **First Pass - High Level**
   - Understand the purpose
   - Check architecture/design
   - Identify major issues

2. **Second Pass - Detailed**
   - Line-by-line review
   - Check all items in checklist
   - Note specific issues

3. **Third Pass - Testing**
   - Verify test coverage
   - Check test quality
   - Run tests if possible

4. **Report**
   - Categorize issues (Critical, Major, Minor)
   - Provide specific examples
   - Suggest fixes with code snippets
   - Give overall assessment

## Output Format

Provide reviews in this structure:

```
## Security Issues
- [CRITICAL/MAJOR/MINOR] Issue description
  Location: file:line
  Fix: Specific recommendation

## Performance Issues
- [CRITICAL/MAJOR/MINOR] Issue description
  Location: file:line
  Fix: Specific recommendation

## Code Quality Issues
- [CRITICAL/MAJOR/MINOR] Issue description
  Location: file:line
  Fix: Specific recommendation

## Strengths
- What was done well

## Recommendations
- High-level suggestions for improvement

## Overall Assessment
Score: X/10
Production Ready: Yes/No
Summary: Brief overview
```

## Example Usage

```python
from pydantic_deep import create_deep_agent

agent = create_deep_agent(
    skill_directories=[{"path": "./skills", "recursive": True}],
)

# Agent will load this skill and use it when reviewing code
result = await agent.run(
    "Review the code in src/api.py using code-review skill",
    deps=deps,
)
```
