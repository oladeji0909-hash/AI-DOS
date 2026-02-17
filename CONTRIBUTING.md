# Contributing to AI-DOS

Thank you for your interest in contributing to AI-DOS! This document provides guidelines and instructions for contributing.

## Code of Conduct

### Our Pledge
We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in all interactions.

### Our Standards
- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce**
- **Expected behavior**
- **Actual behavior**
- **Screenshots** (if applicable)
- **Environment details** (OS, Docker version, etc.)
- **Logs** (relevant error messages)

**Bug Report Template:**
```markdown
**Description**
A clear description of the bug.

**To Reproduce**
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**
- OS: [e.g., Windows 11]
- Docker Version: [e.g., 24.0.0]
- AI-DOS Version: [e.g., 1.0.0]

**Logs**
```
Paste relevant logs here
```

**Screenshots**
If applicable, add screenshots.
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title and description**
- **Use case** (why is this needed?)
- **Proposed solution**
- **Alternatives considered**
- **Additional context**

### Pull Requests

1. **Fork the repository**
2. **Create a branch** from `main`
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Write/update tests**
5. **Update documentation**
6. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
7. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```
8. **Open a Pull Request**

## Development Process

### Setting Up Development Environment

1. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-dos.git
   cd ai-dos
   ```

2. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/ai-dos/ai-dos.git
   ```

3. **Run setup script**
   ```bash
   ./scripts/setup.bat  # Windows
   ./scripts/setup.sh   # Linux/Mac
   ```

4. **Start development environment**
   ```bash
   docker-compose up -d
   ```

### Coding Standards

#### Python
- Follow PEP 8
- Use type hints
- Write docstrings (Google style)
- Maximum line length: 100 characters
- Use meaningful variable names

**Example:**
```python
def process_dataset(
    dataset_id: str,
    options: Dict[str, Any]
) -> ProcessingResult:
    """Process a dataset with given options.
    
    Args:
        dataset_id: Unique identifier of the dataset
        options: Processing options including:
            - batch_size: Number of samples per batch
            - num_workers: Number of parallel workers
            
    Returns:
        ProcessingResult containing status and metrics
        
    Raises:
        DatasetNotFoundError: If dataset doesn't exist
        ProcessingError: If processing fails
    """
    pass
```

#### TypeScript
- Use TypeScript for all new code
- Follow Airbnb style guide
- Use functional components
- Prefer const over let
- Use async/await

**Example:**
```typescript
interface Dataset {
  id: string;
  name: string;
  ownerId: string;
}

const fetchDataset = async (id: string): Promise<Dataset> => {
  const response = await fetch(`/api/datasets/${id}`);
  if (!response.ok) {
    throw new Error('Failed to fetch dataset');
  }
  return response.json();
};
```

#### Go
- Follow official Go style guide
- Use gofmt
- Handle all errors
- Write table-driven tests

**Example:**
```go
func ProcessJob(ctx context.Context, jobID string) error {
    job, err := fetchJob(ctx, jobID)
    if err != nil {
        return fmt.Errorf("failed to fetch job: %w", err)
    }
    
    if err := job.Execute(ctx); err != nil {
        return fmt.Errorf("failed to execute job: %w", err)
    }
    
    return nil
}
```

### Testing

#### Unit Tests
- Write tests for all new code
- Aim for >80% code coverage
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)

**Example:**
```python
def test_create_dataset_success():
    # Arrange
    dataset = Dataset(name="test", owner_id="user123")
    
    # Act
    result = create_dataset(dataset)
    
    # Assert
    assert result.id is not None
    assert result.name == "test"
    assert result.owner_id == "user123"

def test_create_dataset_duplicate_name():
    # Arrange
    dataset = Dataset(name="existing", owner_id="user123")
    create_dataset(dataset)
    
    # Act & Assert
    with pytest.raises(DuplicateNameError):
        create_dataset(dataset)
```

#### Integration Tests
- Test service interactions
- Use test database
- Clean up after tests

#### End-to-End Tests
- Test complete workflows
- Use realistic data
- Test error scenarios

### Documentation

#### Code Documentation
- Document all public APIs
- Include examples
- Explain complex logic
- Keep docs up to date

#### User Documentation
- Write clear, concise guides
- Include screenshots
- Provide code examples
- Cover common use cases

#### API Documentation
- Use OpenAPI/Swagger
- Document all endpoints
- Include request/response examples
- Document error codes

### Commit Messages

Follow conventional commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

**Examples:**
```
feat(dataforge): add dataset versioning

Implement Git-like versioning for datasets with commit history
and diff capabilities.

Closes #123
```

```
fix(modelhub): resolve race condition in experiment tracking

Add mutex lock to prevent concurrent writes to experiment state.

Fixes #456
```

### Pull Request Process

1. **Update documentation**
2. **Add tests**
3. **Ensure CI passes**
4. **Request review**
5. **Address feedback**
6. **Squash commits** (if requested)
7. **Merge** (maintainers only)

### Pull Request Template

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests pass locally
- [ ] Dependent changes merged

## Related Issues
Closes #(issue number)

## Screenshots
If applicable, add screenshots.
```

## Community

### Communication Channels

- **Discord**: Real-time chat and support
- **GitHub Discussions**: Long-form discussions
- **GitHub Issues**: Bug reports and feature requests
- **Twitter**: Announcements and updates
- **Blog**: Technical articles and tutorials

### Community Calls

- **Frequency**: Bi-weekly
- **Format**: Video call
- **Topics**: Roadmap, demos, Q&A
- **Recording**: Available on YouTube

### Recognition

Contributors are recognized in:
- README contributors section
- Release notes
- Annual contributor awards
- Conference speaking opportunities

## Getting Help

### Resources
- [Documentation](https://docs.ai-dos.org)
- [API Reference](https://api.ai-dos.org)
- [Examples](./examples/)
- [FAQ](./docs/faq.md)

### Support Channels
1. Check documentation
2. Search existing issues
3. Ask in Discord
4. Create GitHub issue
5. Email support (for sensitive issues)

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

## Recognition

### Top Contributors
We recognize top contributors monthly based on:
- Code contributions
- Documentation improvements
- Community support
- Bug reports
- Feature suggestions

### Contributor Levels
- **Contributor**: 1+ merged PR
- **Regular Contributor**: 5+ merged PRs
- **Core Contributor**: 20+ merged PRs
- **Maintainer**: Trusted with merge access

## Thank You!

Your contributions make AI-DOS better for everyone. We appreciate your time and effort! 🙏

---

**Questions?** Join our [Discord](https://discord.gg/ai-dos) or open a [Discussion](https://github.com/ai-dos/ai-dos/discussions).
