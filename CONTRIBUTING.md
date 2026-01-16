# Contributing to 8-Bit Transistor CPU

Thank you for your interest in contributing to this project! This document provides guidelines for contributing to the 8-Bit Transistor CPU project.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Requirements](#testing-requirements)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Areas for Contribution](#areas-for-contribution)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of background or experience level.

### Expected Behavior

- Be respectful and constructive in all interactions
- Welcome newcomers and help them get started
- Focus on what is best for the project and community
- Show empathy towards other community members

### Unacceptable Behavior

- Harassment, discrimination, or offensive comments
- Trolling, insulting, or derogatory remarks
- Publishing others' private information
- Any conduct that would be inappropriate in a professional setting

---

## Getting Started

### Prerequisites

Before contributing, ensure you have:

1. **Git** installed and configured
2. **Python 3.7+** for testing
3. **Logisim Evolution** for simulation work
4. **KiCad** for hardware design contributions
5. **ngspice** for SPICE simulations (optional)

### Setup Your Development Environment

```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/YOUR_USERNAME/cpu.git
cd cpu

# Add upstream remote
git remote add upstream https://github.com/tmarhguy/cpu.git

# Create a development branch
git checkout -b feature/your-feature-name

# Run tests to verify setup
./run_tests.sh
```

---

## How to Contribute

### Types of Contributions

We welcome contributions in several areas:

1. **Hardware Design**
   - Gate optimizations
   - New operations
   - PCB improvements
   - Component selection

2. **Simulation**
   - Logisim circuit improvements
   - SPICE models
   - Test benches
   - Timing analysis

3. **Software**
   - Test vector generation
   - Verification scripts
   - Firmware improvements
   - Build automation

4. **Documentation**
   - Tutorials and guides
   - Architecture explanations
   - Build instructions
   - Troubleshooting guides

5. **Testing**
   - Additional test vectors
   - Hardware verification
   - Performance benchmarks
   - Edge case discovery

---

## Development Workflow

### 1. Find or Create an Issue

- Check existing [issues](https://github.com/tmarhguy/cpu/issues)
- Comment on an issue to claim it
- Or create a new issue describing your contribution

### 2. Create a Branch

```bash
# Update your fork
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/descriptive-name
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `test/` - Test additions
- `refactor/` - Code refactoring

### 3. Make Your Changes

- Write clear, concise code
- Follow existing code style
- Add tests for new features
- Update documentation as needed

### 4. Test Your Changes

```bash
# Run test suite
./run_tests.sh

# Or with pytest
cd test && pytest test_alu.py -v

# Verify Logisim simulation (if applicable)
# Open circuit in Logisim Evolution and test
```

### 5. Commit Your Changes

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: add carry-lookahead adder optimization

- Implement 4-bit carry-lookahead blocks
- Reduce propagation delay by 40%
- Add comprehensive test coverage
- Update documentation"
```

### Commit Message Format

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions or modifications
- `refactor:` - Code refactoring
- `perf:` - Performance improvements
- `chore:` - Build process or auxiliary tool changes

**Examples:**
```
feat(alu): add carry-lookahead adder

fix(flags): correct overflow flag calculation

docs(readme): update build instructions

test(alu): add edge case tests for subtraction
```

### 6. Push and Create Pull Request

```bash
# Push to your fork
git push origin feature/descriptive-name

# Go to GitHub and create a Pull Request
```

---

## Coding Standards

### Hardware Design (KiCad)

1. **Schematic Standards:**
   - Use hierarchical design
   - Label all nets clearly
   - Add component values and part numbers
   - Include design notes

2. **PCB Standards:**
   - Follow 2-layer design rules
   - Maintain 0.2mm minimum trace width
   - Use proper ground planes
   - Add mounting holes

3. **Component Selection:**
   - Prefer through-hole for educational builds
   - Use standard 5V logic families
   - Document all part numbers
   - Provide alternative components

### Simulation (Logisim)

1. **Circuit Design:**
   - Use subcircuits for modularity
   - Label all inputs and outputs
   - Add comments for complex logic
   - Use consistent naming

2. **Testing:**
   - Verify all input combinations
   - Test edge cases
   - Document expected behavior
   - Provide test vectors

### Software (Python)

1. **Code Style:**
   - Follow PEP 8
   - Use type hints where appropriate
   - Write docstrings for functions
   - Keep functions focused and small

2. **Testing:**
   - Write tests for new features
   - Maintain 100% pass rate
   - Test edge cases
   - Use descriptive test names

**Example:**
```python
def execute_alu_operation(opcode: str, a: int, b: int) -> tuple[int, dict]:
    """
    Execute ALU operation and return result with flags.
    
    Args:
        opcode: 5-bit operation code (e.g., "00000" for ADD)
        a: 8-bit operand A (0-255)
        b: 8-bit operand B (0-255)
    
    Returns:
        Tuple of (result, flags) where flags is a dict with Z, N, C, V
    
    Example:
        >>> execute_alu_operation("00000", 5, 3)
        (8, {'zero': False, 'negative': False, 'carry': False, 'overflow': False})
    """
    # Implementation
    pass
```

### Documentation (Markdown)

1. **Style:**
   - Use clear, concise language
   - Include code examples
   - Add diagrams where helpful
   - Link to related documentation

2. **Structure:**
   - Use proper heading hierarchy
   - Include table of contents for long docs
   - Add navigation links
   - Use tables for structured data

3. **Media:**
   - Place all media in `/media/` directory
   - Use relative paths
   - Add alt text for images
   - Include captions

---

## Testing Requirements

### All Contributions Must:

1. **Pass existing tests:**
   ```bash
   ./run_tests.sh
   # All 1,900 tests must pass
   ```

2. **Add new tests for new features:**
   - Unit tests for components
   - Integration tests for systems
   - Edge case coverage

3. **Maintain test coverage:**
   - Aim for 100% coverage
   - Test all code paths
   - Verify error handling

### Hardware Contributions

1. **Simulation verification:**
   - SPICE simulation for transistor-level
   - Logisim verification for gate-level
   - Test all operations

2. **Documentation:**
   - Schematic capture
   - Bill of materials
   - Assembly instructions

---

## Documentation

### Documentation Requirements

All contributions should include appropriate documentation:

1. **Code Documentation:**
   - Inline comments for complex logic
   - Docstrings for functions/classes
   - README updates for new features

2. **Hardware Documentation:**
   - Schematics (KiCad format)
   - PCB layouts
   - Component datasheets
   - Assembly notes

3. **User Documentation:**
   - Update relevant guides
   - Add tutorials if needed
   - Include examples
   - Update changelog

### Documentation Style

- Use clear, simple language
- Provide examples
- Include diagrams
- Link to related docs
- Keep it up-to-date

---

## Pull Request Process

### Before Submitting

- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] Branch is up-to-date with main

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
- [ ] All existing tests pass
- [ ] New tests added
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes (or documented)

## Related Issues
Closes #123
```

### Review Process

1. **Automated Checks:**
   - Tests must pass
   - No linting errors
   - Documentation builds successfully

2. **Code Review:**
   - At least one approval required
   - Address reviewer feedback
   - Maintain respectful discussion

3. **Merge:**
   - Squash and merge (typically)
   - Clear commit message
   - Delete branch after merge

---

## Areas for Contribution

### High Priority

1. **Carry-Lookahead Adder:**
   - Implement 4-bit CLA blocks
   - Reduce propagation delay
   - Maintain compatibility

2. **Additional Operations:**
   - Multiply (iterative or combinational)
   - Divide
   - Rotate operations

3. **Hardware Testing:**
   - Complete REV A operation testing
   - Performance characterization
   - Long-term reliability testing

### Medium Priority

4. **Documentation:**
   - Video tutorials
   - Build guide improvements
   - Troubleshooting expansion

5. **Optimization:**
   - Transistor count reduction
   - Power consumption optimization
   - Layout improvements

6. **Tooling:**
   - Automated testing scripts
   - PCB generation tools
   - BOM management

### Low Priority

7. **Extended Features:**
   - 16-bit ALU variant
   - Pipelining
   - Additional flags

8. **Alternative Implementations:**
   - FPGA port
   - ASIC design
   - Different logic families

---

## Questions?

### Getting Help

- **Documentation:** Check [docs/](docs/) directory
- **Issues:** Search [existing issues](https://github.com/tmarhguy/cpu/issues)
- **Discussions:** Use [GitHub Discussions](https://github.com/tmarhguy/cpu/discussions)
- **Email:** tmarhguy@gmail.com | tmarhguy@seas.upenn.edu
- **Twitter:** [@marhguy_tyrone](https://twitter.com/marhguy_tyrone)
- **Instagram:** [@tmarhguy](https://instagram.com/tmarhguy)
- **Substack:** [@tmarhguy](https://tmarhguy.substack.com)

### Resources

- [Getting Started Guide](docs/GETTING_STARTED.md)
- [Architecture Documentation](docs/ARCHITECTURE.md)
- [Verification Guide](docs/VERIFICATION.md)
- [Test Suite Documentation](test/README.md)

---

## Recognition

Contributors will be:
- Listed in project README
- Credited in release notes
- Acknowledged in documentation

Thank you for contributing to the 8-Bit Transistor CPU project!

---

## 👨‍💻 Project Maintainer

**Tyrone Marhguy**  
Sophomore, Computer Engineering  
University of Pennsylvania, School of Engineering and Applied Science  
Expected Graduation: May 2028

### Connect with Me

- 🌐 [tmarhguy.com](https://tmarhguy.com)
- 📧 tmarhguy@gmail.com | tmarhguy@seas.upenn.edu
- 💼 [LinkedIn](https://linkedin.com/in/tmarhguy)
- 🐦 [Twitter](https://twitter.com/marhguy_tyrone)
- 📷 [Instagram](https://instagram.com/tmarhguy)
- 📝 [Substack](https://tmarhguy.substack.com)
- 🐦 [Twitter: @marhguy_tyrone](https://twitter.com/marhguy_tyrone)
- 📸 [Instagram: @tmarhguy](https://instagram.com/tmarhguy)

---

**Last Updated:** 2026-01-16  
**Version:** 1.0
