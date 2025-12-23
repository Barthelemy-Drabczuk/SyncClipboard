# Contributing to SyncClipboard

Thank you for your interest in contributing to SyncClipboard! We welcome contributions from the community while maintaining the project's commercial viability.

## 🔒 Contributor License Agreement

By contributing to this project, you agree that:

1. **You grant the project maintainers** a perpetual, worldwide, non-exclusive, royalty-free, irrevocable license to use, reproduce, modify, distribute, and commercialize your contributions
2. **Your contributions are your original work** or you have the right to submit them
3. **You understand** that your contributions may be used in both open-source and commercial versions of this software
4. **You retain copyright** to your contributions, but grant us the rights described above

This dual-licensing approach allows us to:
- Keep the project open source for the community
- Potentially develop commercial features or offerings
- Ensure long-term sustainability of the project

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- MongoDB (for local development)
- Git

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/syncclipboard.git
   cd syncclipboard
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   Using pyproject.toml:
   ```bash
   pip install -e ".[dev]"
   ```

4. **Set Up MongoDB**

   Using Docker:
   ```bash
   docker-compose up -d mongodb
   ```

   Or install locally (see [SETUP.md](SETUP.md))

## 📝 Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions or fixes

### 2. Make Your Changes

- Write clean, readable code
- Follow existing code style and conventions
- Add or update tests for your changes
- Update documentation as needed

### 3. Code Style

We follow PEP 8 with modifications defined in `pyproject.toml`.

**Format your code:**
```bash
black src/
```

**Check linting:**
```bash
flake8 src/
```

**Type checking (optional but encouraged):**
```bash
mypy src/
```

### 4. Testing

**Run all tests:**
```bash
cd src
python -m pytest tests/ -v
```

**Run with coverage:**
```bash
pytest --cov=. --cov-report=html
```

**Test in Docker:**
```bash
docker-compose exec webapp pytest tests/ -v
```

All tests must pass before submitting a PR.

### 5. Commit Your Changes

Use clear, descriptive commit messages:

```bash
git commit -m "Add feature: brief description"
```

**Commit message format:**
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Fix bug" not "Fixes bug")
- First line: 50 characters or less
- Reference issues: "Fix #123: description"

**Examples:**
```
Add WebSocket reconnection logic
Fix clipboard sync on Windows 11
Update Docker setup documentation
Refactor user authentication flow
```

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a PR on GitHub with:
- Clear description of what changed
- Why the change is needed
- How it was tested
- Screenshots (if UI changes)
- References to related issues

## ✅ Pull Request Guidelines

### Before Submitting

- [ ] Code follows project style guidelines
- [ ] All tests pass locally
- [ ] New tests added for new features
- [ ] Documentation updated (if needed)
- [ ] No unnecessary dependencies added
- [ ] Commit messages are clear and descriptive

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How was this tested?

## Checklist
- [ ] Tests pass
- [ ] Code formatted with black
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

## 🎯 What We Accept

### ✅ Encouraged Contributions

- **Bug fixes** - Especially with test cases
- **Performance improvements** - With benchmarks
- **Documentation improvements** - Clarifications, examples, typos
- **Test coverage** - Additional test cases
- **Security fixes** - Responsibly disclosed
- **Accessibility improvements**
- **Cross-platform compatibility fixes**

### ⚠️ Discuss First

Please open an issue before working on:
- **Major features** - May not align with project direction
- **Breaking changes** - Need careful consideration
- **Architecture changes** - Should be discussed with maintainers
- **New dependencies** - Should be justified

### ❌ Won't Accept

- Code that doesn't pass tests
- Changes without documentation
- Contributions that violate our license
- Malicious code or security vulnerabilities
- Plagiarized code

## 🧪 Testing Guidelines

### Writing Tests

- Place tests in `src/tests/`
- Name files: `*_test.py` or `test_*.py`
- Name functions: `test_*`
- Use descriptive test names
- Mock external dependencies

**Example:**
```python
import pytest
from unittest.mock import Mock, patch

def test_clipboard_sync_sends_to_server(mock_db):
    """Test that clipboard changes are sent to server"""
    # Arrange
    client = Client(user_id=123)
    observer = ServerClipboardObserver("http://localhost:5000")
    client.attach(observer)

    # Act
    client.notify(123, "test content")

    # Assert
    # Verify server was called
```

### Test Categories

Mark tests appropriately:
```python
@pytest.mark.unit
def test_user_creation():
    pass

@pytest.mark.integration
def test_database_connection():
    pass

@pytest.mark.slow
def test_large_clipboard_history():
    pass
```

## 📚 Documentation

Update documentation when:
- Adding new features
- Changing APIs or interfaces
- Modifying setup/deployment procedures
- Fixing bugs that affect documented behavior

Documentation locations:
- `README.md` - Overview and quick start
- `SETUP.md` - Installation and setup
- `DOCKER.md` - Docker deployment
- Code comments - Complex logic
- Docstrings - All public functions/classes

## 🐛 Reporting Bugs

Create an issue with:
- **Clear title** - Summarize the bug
- **Steps to reproduce** - Minimal example
- **Expected behavior** - What should happen
- **Actual behavior** - What actually happens
- **Environment** - OS, Python version, etc.
- **Screenshots** - If applicable

## 💡 Suggesting Features

Open an issue with:
- **Use case** - Why is this needed?
- **Proposed solution** - How should it work?
- **Alternatives considered** - Other approaches?
- **Impact** - Who benefits from this?

## 🔐 Security Issues

**DO NOT** open public issues for security vulnerabilities.

Instead:
1. Email security concerns privately (add your email here)
2. Include detailed information
3. Allow reasonable time for a fix before disclosure

## 📜 Code of Conduct

### Our Standards

- Be respectful and inclusive
- Accept constructive criticism
- Focus on what's best for the project
- Show empathy toward others

### Unacceptable Behavior

- Harassment or discriminatory comments
- Trolling or insulting remarks
- Personal or political attacks
- Publishing others' private information

## 📞 Getting Help

- 📖 Read the documentation first
- 💬 Check existing issues
- 🆕 Open a new issue if needed
- 💡 Discuss in issue comments

## 🎓 Learning Resources

New to contributing? Check out:
- [First Contributions Guide](https://github.com/firstcontributions/first-contributions)
- [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/)
- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

By contributing, you agree that your contributions will be licensed under the same license, with the additional terms described in the Contributor License Agreement above.

---

**Thank you for contributing to SyncClipboard!** 🎉

Your contributions help make this project better for everyone while supporting its sustainable development.
