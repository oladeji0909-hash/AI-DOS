# Contributing to AI-DOS

Thank you for your interest in contributing to AI-DOS! 🎉

This document provides guidelines for contributing to the project.

---

## 📋 Table of Contents

- [Code of Conduct](#-code-of-conduct)
- [How Can I Contribute?](#-how-can-i-contribute)
- [Getting Started](#-getting-started)
- [Development Workflow](#-development-workflow)
- [Pull Request Process](#-pull-request-process)
- [Coding Standards](#-coding-standards)
- [Testing Guidelines](#-testing-guidelines)
- [Documentation](#-documentation)
- [Community](#-community)

---

## 📜 Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

**Key Points:**
- ✅ Be respectful and professional
- ✅ Follow contribution guidelines
- ✅ No malicious code or spam
- ✅ Respect intellectual property
- ❌ No harassment or discrimination

**Read the full [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.**

---

## 🤝 How Can I Contribute?

### 1. Report Bugs 🐛

Found a bug? Help us fix it!

**Before Reporting:**
- Check if the bug is already reported in [Issues](https://github.com/oladeji0909-hash/AI-DOS/issues)
- Make sure you're using the latest version
- Try to reproduce the bug

**When Reporting:**
- Use the bug report template
- Provide clear title and description
- Include steps to reproduce
- Add error messages and logs
- Specify your environment (OS, Docker version, etc.)

**Example:**
```markdown
**Bug:** Deploy service fails to start

**Steps to Reproduce:**
1. Run `docker-compose up -d`
2. Check logs: `docker-compose logs deploy`
3. See error: "Port 8005 already in use"

**Environment:**
- OS: Windows 10
- Docker: 20.10.8
- AI-DOS: v1.2.0

**Expected:** Service starts successfully
**Actual:** Service fails with port conflict
```

---

### 2. Suggest Features 💡

Have an idea? We'd love to hear it!

**Before Suggesting:**
- Check if it's already suggested in [Issues](https://github.com/oladeji0909-hash/AI-DOS/issues)
- Make sure it aligns with AI-DOS goals
- Consider if it benefits most users

**When Suggesting:**
- Use the feature request template
- Explain the problem it solves
- Describe your proposed solution
- Provide examples or mockups
- Discuss alternatives you've considered

---

### 3. Improve Documentation 📚

Documentation is crucial! Help make it better.

**What to Improve:**
- Fix typos and grammar
- Add missing information
- Clarify confusing sections
- Add code examples
- Update outdated content

**Where to Contribute:**
- README.md
- GETTING_STARTED.md
- Code comments
- API documentation
- Tutorials and guides

---

### 4. Write Code 💻

Ready to code? Awesome!

**What to Work On:**
- Check [Issues](https://github.com/oladeji0909-hash/AI-DOS/issues) labeled `good first issue`
- Look for `help wanted` issues
- Propose new features (open an issue first!)
- Fix bugs
- Improve performance
- Add tests

---

## 🚀 Getting Started

### Prerequisites

- Git installed
- Docker Desktop installed
- Python 3.8+ (for SDK development)
- Code editor (VS Code recommended)

### Setup Development Environment

```bash
# 1. Fork the repository on GitHub
# Click "Fork" button on https://github.com/oladeji0909-hash/AI-DOS

# 2. Clone YOUR fork
git clone https://github.com/YOUR-USERNAME/AI-DOS.git
cd AI-DOS

# 3. Add upstream remote
git remote add upstream https://github.com/oladeji0909-hash/AI-DOS.git

# 4. Create a branch
git checkout -b feature/your-feature-name

# 5. Start services
docker-compose -f docker-compose-minimal.yml up -d

# 6. Make your changes
# Edit files, add features, fix bugs

# 7. Test your changes
python comprehensive_test.py

# 8. Commit your changes
git add .
git commit -m "✨ Add your feature description"

# 9. Push to your fork
git push origin feature/your-feature-name

# 10. Create Pull Request on GitHub
```

---

## 🔄 Development Workflow

### Branch Naming

Use descriptive branch names:

- `feature/add-new-service` - New features
- `fix/deploy-port-conflict` - Bug fixes
- `docs/update-readme` - Documentation
- `test/add-unit-tests` - Tests
- `refactor/improve-performance` - Code improvements

### Commit Messages

Write clear, meaningful commit messages:

**Format:**
```
<emoji> <type>: <description>

[optional body]

[optional footer]
```

**Types:**
- ✨ `feat:` - New feature
- 🐛 `fix:` - Bug fix
- 📚 `docs:` - Documentation
- 🎨 `style:` - Code style (formatting)
- ♻️ `refactor:` - Code refactoring
- ✅ `test:` - Adding tests
- ⚡ `perf:` - Performance improvement
- 🔧 `chore:` - Maintenance tasks

**Examples:**
```bash
✨ feat: Add AutoScale service with smart scaling
🐛 fix: Resolve port conflict in Deploy service
📚 docs: Update Getting Started guide with troubleshooting
✅ test: Add unit tests for Analytics service
```

### Keep Your Fork Updated

```bash
# Fetch upstream changes
git fetch upstream

# Merge upstream main into your branch
git checkout main
git merge upstream/main

# Push to your fork
git push origin main
```

---

## 🔀 Pull Request Process

### Before Submitting

- ✅ Test your changes thoroughly
- ✅ Update documentation if needed
- ✅ Add tests for new features
- ✅ Ensure all tests pass
- ✅ Follow coding standards
- ✅ Rebase on latest main branch

### Submitting a Pull Request

1. **Go to GitHub** - Visit your fork
2. **Click "New Pull Request"**
3. **Select branches:**
   - Base: `oladeji0909-hash/AI-DOS` `main`
   - Compare: `YOUR-USERNAME/AI-DOS` `your-branch`
4. **Fill out the template:**
   - Clear title
   - Description of changes
   - Related issues (if any)
   - Screenshots (if UI changes)
   - Testing done
5. **Submit!**

### Pull Request Template

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Related Issues
Fixes #123

## Changes Made
- Added X feature
- Fixed Y bug
- Updated Z documentation

## Testing Done
- [ ] All existing tests pass
- [ ] Added new tests
- [ ] Tested manually
- [ ] Tested on multiple environments

## Screenshots (if applicable)
[Add screenshots here]

## Checklist
- [ ] Code follows project style
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests passing
- [ ] No breaking changes (or documented)
```

### Review Process

1. **Automated Checks** - CI/CD runs tests
2. **Maintainer Review** - Code review by maintainers
3. **Feedback** - Address any requested changes
4. **Approval** - Maintainer approves PR
5. **Merge** - PR merged into main branch

**Be patient!** Maintainers review PRs as time allows.

---

## 💻 Coding Standards

### Python Code Style

Follow PEP 8 and these guidelines:

```python
# Good: Clear, descriptive names
def create_deployment(experiment_id: str, name: str) -> dict:
    """Create a new deployment from an experiment.
    
    Args:
        experiment_id: ID of the experiment to deploy
        name: Name for the deployment
        
    Returns:
        dict: Deployment information
    """
    deployment = {
        "id": generate_id(),
        "experiment_id": experiment_id,
        "name": name,
        "status": "running"
    }
    return deployment

# Bad: Unclear, no types, no docstring
def create(e, n):
    d = {"id": gen(), "e": e, "n": n, "s": "r"}
    return d
```

**Key Points:**
- ✅ Use type hints
- ✅ Write docstrings
- ✅ Descriptive variable names
- ✅ Keep functions small and focused
- ✅ Handle errors properly
- ✅ No hardcoded credentials

### FastAPI Best Practices

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class DeploymentCreate(BaseModel):
    experiment_id: str
    name: str
    description: str = ""

@app.post("/deploy/create")
async def create_deployment(deployment: DeploymentCreate):
    """Create a new deployment."""
    try:
        result = deploy_service.create(deployment)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Docker Best Practices

```dockerfile
# Good: Specific version, minimal layers
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Bad: Latest tag, many layers
FROM python:latest
RUN mkdir /app
WORKDIR /app
COPY . .
RUN pip install fastapi
RUN pip install uvicorn
RUN pip install pydantic
CMD python -m uvicorn main:app
```

---

## ✅ Testing Guidelines

### Running Tests

```bash
# Run all tests
python comprehensive_test.py

# Test specific service
curl http://localhost:8001/health

# Check Docker logs
docker-compose logs -f dataforge
```

### Writing Tests

```python
def test_create_deployment():
    """Test deployment creation."""
    # Arrange
    experiment_id = "exp_123"
    name = "Test Deployment"
    
    # Act
    result = deploy.create(experiment_id, name)
    
    # Assert
    assert result["experiment_id"] == experiment_id
    assert result["name"] == name
    assert result["status"] == "running"
    assert "deployment_id" in result
```

### Test Coverage

- ✅ Test happy paths
- ✅ Test error cases
- ✅ Test edge cases
- ✅ Test integrations
- ✅ Aim for 80%+ coverage

---

## 📚 Documentation

### Code Comments

```python
# Good: Explain WHY, not WHAT
# Use exponential backoff to avoid overwhelming the API
retry_delay = 2 ** attempt

# Bad: Obvious comment
# Set retry delay to 2 to the power of attempt
retry_delay = 2 ** attempt
```

### API Documentation

Use FastAPI's automatic docs:

```python
@app.post("/deploy/create", summary="Create deployment")
async def create_deployment(
    deployment: DeploymentCreate
) -> DeploymentResponse:
    """
    Create a new deployment from an experiment.
    
    - **experiment_id**: ID of the experiment to deploy
    - **name**: Name for the deployment
    - **description**: Optional description
    
    Returns deployment information including endpoint URL.
    """
    pass
```

---

## 🌍 Community

### Communication Channels

- 💬 **Discord** - [Join our server](https://discord.gg/ai-dos)
- 🐛 **GitHub Issues** - Bug reports and features
- 📧 **Email** - team@ai-dos.io
- 🐦 **Twitter** - [@ai_dos](https://twitter.com/ai_dos)

### Getting Help

- Read [Getting Started](GETTING_STARTED.md)
- Check [existing issues](https://github.com/oladeji0909-hash/AI-DOS/issues)
- Ask in Discord
- Email the team

### Recognition

Contributors are recognized in:
- README.md contributors section
- Release notes
- Social media shoutouts
- Contributor badge

---

## 🎯 What Makes a Good Contribution?

### ✅ Good Contributions

- Fixes a real bug
- Adds a requested feature
- Improves performance
- Enhances documentation
- Adds useful tests
- Follows guidelines
- Well-tested and documented

### ❌ Poor Contributions

- Breaks existing functionality
- No tests or documentation
- Doesn't follow code style
- Duplicates existing work
- Adds unnecessary complexity
- Contains malicious code

---

## 🚫 What We Don't Accept

- ❌ Malicious code or backdoors
- ❌ Plagiarized code
- ❌ Code that violates licenses
- ❌ Spam or low-quality PRs
- ❌ Breaking changes without discussion
- ❌ Code with security vulnerabilities

---

## 📞 Questions?

Have questions about contributing?

- 📧 Email: team@ai-dos.io
- 💬 Discord: [Join our server](https://discord.gg/ai-dos)
- 🐛 GitHub: [Open an issue](https://github.com/oladeji0909-hash/AI-DOS/issues)

---

## 🙏 Thank You!

Every contribution, no matter how small, makes AI-DOS better. Thank you for being part of this journey! 🚀

---

<div align="center">

**[Code of Conduct](CODE_OF_CONDUCT.md)** • **[Getting Started](GETTING_STARTED.md)** • **[Back to README](README.md)**

Made with ❤️ by the AI-DOS community

</div>
