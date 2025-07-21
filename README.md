# Discrete Transistor 8-bit CPU

[![CI](https://github.com/tmarhguy/cpu/workflows/CI/badge.svg)](https://github.com/tmarhguy/cpu/actions)
[![codecov](https://codecov.io/gh/tmarhguy/cpu/branch/main/graph/badge.svg)](https://codecov.io/gh/tmarhguy/cpu)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

A complete discrete-transistor 8-bit CPU implementation with toolchain, featuring a Python assembler, cycle-accurate simulator, and WebAssembly deployment for educational demonstration.

## 🎯 Project Overview

This project builds a working 8-bit CPU using discrete MOSFETs (≤800 transistors) with a complete software toolchain. The CPU executes a custom 16-instruction ISA and demonstrates computation through a Fibonacci sequence calculator with LED output visualization.

**Key Features:**

- 8-bit architecture with 16 instructions
- Discrete transistor implementation (no integrated circuits)
- 1-5 kHz clock speed for visibility and debugging
- Complete toolchain: assembler, simulator, test harness
- WebAssembly simulator for browser deployment
- Hardware verification with oscilloscope integration

## 🚀 Quick Start

```bash
# 1-click setup
brew bundle         # Install dependencies (macOS)
direnv allow        # Load environment
asdf install        # Install runtime versions
poetry install      # Install Python dependencies
poetry run dev      # Start development server
poetry run test --watch  # Run tests continuously
```

## 📁 Project Structure

```
src/           # Production code (assembler, simulator, CPU modules)
tests/         # Automated test suite
scripts/       # Utility CLI scripts
docs/          # Documentation site
examples/      # Sample programs (Fibonacci, etc.)
infra/         # Infrastructure as Code
.vscode/       # VS Code workspace configuration
.devcontainer/ # Development container setup
```

## 🛠️ Development

### Prerequisites

- Python 3.12+
- Node.js 20 LTS
- Poetry 1.8+
- Docker (optional)

### Local Development

```bash
# Install dependencies
poetry install
npm install

# Run assembler
poetry run asm examples/fibonacci.asm -o fibonacci.hex

# Run simulator
poetry run sim fibonacci.hex --cycles

# Run tests
poetry run pytest
npm test

# Format code
poetry run black .
poetry run ruff check .
npm run lint
```

### Hardware Build Phases

1. **P0-P1**: Tooling & ALU slice (10 days)
2. **P2-P4**: Registers, bus, control logic (20 days)
3. **P5-P7**: Integration & instruction set (23 days)
4. **P8-P10**: I/O, demo program, PCB (22 days)

See `literature.md` for detailed build timeline and specifications.

## 🧪 Testing

```bash
# Run all tests
poetry run pytest

# Test specific module
poetry run pytest tests/test_assembler.py

# Run with coverage
poetry run pytest --cov=src

# Hardware-in-the-loop testing
poetry run python scripts/hardware_test.py
```

## 📖 Documentation

- [CPU Specification](docs/cpu-spec.md)
- [Instruction Set Architecture](docs/isa.md)
- [Build Guide](docs/build-guide.md)
- [API Reference](docs/api.md)

## 🌐 Web Simulator

The WebAssembly simulator is deployed at: [https://tmarhguy.github.io/cpu](https://tmarhguy.github.io/cpu)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'feat: add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏆 Success Criteria

- [x] Executes Fibonacci demo end-to-end in hardware
- [x] Assembler → HEX → EEPROM → CPU workflow proven
- [x] Clock stable ±5% for 30 minutes
- [x] ALU accuracy: passes 100-vector testbench
- [x] WebAssembly simulator matches hardware output

## 📧 Contact

**Tyrone Marhguy** - [GitHub](https://github.com/tmarhguy)

Project Link: [https://github.com/tmarhguy/cpu](https://github.com/tmarhguy/cpu)
