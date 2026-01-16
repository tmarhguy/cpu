#!/usr/bin/env python3
"""
Standard pytest-compatible test suite for 8-bit ALU
Run with: pytest test_alu.py -v
Or: python3 test_alu.py
"""

import json
from pathlib import Path
from typing import Dict, Tuple

# pytest is optional - only needed for advanced testing
try:
    import pytest
    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False
    # Mock pytest decorators for standalone mode
    class pytest:
        @staticmethod
        def fixture(*args, **kwargs):
            def decorator(func):
                return func
            return decorator
        
        class mark:
            @staticmethod
            def parametrize(*args, **kwargs):
                def decorator(func):
                    return func
                return decorator


class ALU8Bit:
    """Software simulation of 8-bit ALU"""
    
    def __init__(self):
        self.width = 8
        self.mask = (1 << self.width) - 1
        
    def execute(self, opcode: str, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """Execute ALU operation and return result with flags"""
        a = a & self.mask
        b = b & self.mask
        
        operations = {
            '00000': self.add,
            '00001': self.sub,
            '00010': self.inc_a,
            '00011': self.dec_a,
            '00100': self.lsl,
            '00101': self.lsr,
            '00110': self.asr,
            '00111': self.rev_a,
            '01000': self.nand,
            '01001': self.nor,
            '01010': self.xor,
            '01011': self.pass_a,
            '01100': self.pass_b,
            '01101': self.and_op,
            '01110': self.or_op,
            '01111': self.xnor,
            '10000': self.cmp,
            '10001': self.not_a,
            '10010': self.not_b,
        }
        
        if opcode not in operations:
            raise ValueError(f"Unknown opcode: {opcode}")
            
        return operations[opcode](a, b)
    
    def _flags(self, result: int, carry: bool = False, overflow: bool = False) -> Dict[str, bool]:
        """Calculate standard flags"""
        result_8bit = result & self.mask
        return {
            'carry': carry,
            'zero': result_8bit == 0,
            'overflow': overflow,
            'negative': bool(result_8bit & 0x80)
        }
    
    def add(self, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """ADD: A + B"""
        result = a + b
        carry = result > self.mask
        overflow = ((a & 0x80) == (b & 0x80)) and ((a & 0x80) != (result & 0x80))
        return result & self.mask, self._flags(result, carry, overflow)
    
    def sub(self, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """SUB: A - B"""
        result = a - b
        carry = result >= 0
        overflow = ((a & 0x80) != (b & 0x80)) and ((a & 0x80) != (result & 0x80))
        return result & self.mask, self._flags(result, carry, overflow)
    
    def inc_a(self, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """INC A: A + 1"""
        result = a + 1
        carry = result > self.mask
        overflow = (a == 0x7F)
        return result & self.mask, self._flags(result, carry, overflow)
    
    def dec_a(self, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """DEC A: A - 1"""
        result = a - 1
        carry = result >= 0
        overflow = (a == 0x80)
        return result & self.mask, self._flags(result, carry, overflow)
    
    def lsl(self, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """LSL: Logical shift left"""
        carry = bool(a & 0x80)
        result = (a << 1) & self.mask
        return result, self._flags(result, carry, False)
    
    def lsr(self, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """LSR: Logical shift right"""
        carry = bool(a & 0x01)
        result = (a >> 1) & self.mask
        return result, self._flags(result, carry, False)
    
    def asr(self, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """ASR: Arithmetic shift right"""
        carry = bool(a & 0x01)
        sign_bit = a & 0x80
        result = ((a >> 1) | sign_bit) & self.mask
        return result, self._flags(result, carry, False)
    
    def rev_a(self, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """REV A: Reverse bits"""
        result = 0
        for i in range(8):
            if a & (1 << i):
                result |= (1 << (7 - i))
        return result, self._flags(result, False, False)
    
    def nand(self, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """NAND"""
        result = (~(a & b)) & self.mask
        return result, self._flags(result, False, False)
    
    def nor(self, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """NOR"""
        result = (~(a | b)) & self.mask
        return result, self._flags(result, False, False)
    
    def xor(self, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """XOR"""
        result = (a ^ b) & self.mask
        return result, self._flags(result, False, False)
    
    def pass_a(self, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """PASS A"""
        return a, self._flags(a, False, False)
    
    def pass_b(self, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """PASS B"""
        return b, self._flags(b, False, False)
    
    def and_op(self, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """AND"""
        result = (a & b) & self.mask
        return result, self._flags(result, False, False)
    
    def or_op(self, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """OR"""
        result = (a | b) & self.mask
        return result, self._flags(result, False, False)
    
    def xnor(self, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """XNOR"""
        result = (~(a ^ b)) & self.mask
        return result, self._flags(result, False, False)
    
    def cmp(self, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """CMP: Compare (flags only)"""
        result = a - b
        carry = result >= 0
        overflow = ((a & 0x80) != (b & 0x80)) and ((a & 0x80) != (result & 0x80))
        return 0, self._flags(result, carry, overflow)
    
    def not_a(self, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """NOT A"""
        result = (~a) & self.mask
        return result, self._flags(result, False, False)
    
    def not_b(self, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """NOT B"""
        result = (~b) & self.mask
        return result, self._flags(result, False, False)


# Global ALU instance for tests
alu = ALU8Bit()


def load_test_vectors():
    """Load test vectors from JSON file"""
    test_file = Path(__file__).parent / 'vectors' / 'demo.json'
    with open(test_file, 'r') as f:
        data = json.load(f)
    return data.get('tests', [])


# Parametrize tests with all test vectors
@pytest.fixture(scope="module")
def test_vectors():
    """Fixture to load test vectors once"""
    return load_test_vectors()


def test_load_vectors(test_vectors):
    """Test that vectors are loaded correctly"""
    assert len(test_vectors) > 0, "No test vectors loaded"
    assert len(test_vectors) == 1900, f"Expected 1900 tests, got {len(test_vectors)}"


@pytest.mark.parametrize("test_data", load_test_vectors(), ids=lambda t: t.get('test_name', 'unknown'))
def test_alu_operation(test_data):
    """Test each ALU operation from test vectors"""
    test_name = test_data.get('test_name', 'unknown')
    opcode = test_data.get('opcode', '')
    a = int(test_data.get('A', 0))
    b = int(test_data.get('B', 0))
    expected_result = int(test_data.get('expected_result', 0))
    expected_flags = test_data.get('expected_flags', {})
    
    # Execute operation
    actual_result, actual_flags = alu.execute(opcode, a, b)
    
    # Assert result
    assert actual_result == expected_result, \
        f"Result mismatch: expected 0x{expected_result:02X}, got 0x{actual_result:02X}"
    
    # Assert flags
    for flag in ['carry', 'zero', 'overflow', 'negative']:
        expected = expected_flags.get(flag, False)
        actual = actual_flags.get(flag, False)
        assert expected == actual, \
            f"Flag '{flag}' mismatch: expected {expected}, got {actual}"


# Grouped tests by operation for better organization
class TestArithmetic:
    """Test arithmetic operations"""
    
    def test_add_simple(self):
        """Test simple addition"""
        result, flags = alu.execute('00000', 5, 3)
        assert result == 8
        assert flags['zero'] == False
        assert flags['carry'] == False
    
    def test_add_overflow(self):
        """Test addition with carry"""
        result, flags = alu.execute('00000', 255, 1)
        assert result == 0
        assert flags['carry'] == True
        assert flags['zero'] == True
    
    def test_sub_simple(self):
        """Test simple subtraction"""
        result, flags = alu.execute('00001', 10, 3)
        assert result == 7
        assert flags['carry'] == True
    
    def test_sub_underflow(self):
        """Test subtraction with underflow"""
        result, flags = alu.execute('00001', 3, 10)
        assert result == 249  # 256 - 7
        assert flags['negative'] == True
    
    def test_inc(self):
        """Test increment"""
        result, flags = alu.execute('00010', 42, 0)
        assert result == 43
    
    def test_dec(self):
        """Test decrement"""
        result, flags = alu.execute('00011', 42, 0)
        assert result == 41


class TestLogic:
    """Test logic operations"""
    
    def test_and(self):
        """Test AND operation"""
        result, flags = alu.execute('01101', 0b11110000, 0b10101010)
        assert result == 0b10100000
    
    def test_or(self):
        """Test OR operation"""
        result, flags = alu.execute('01110', 0b11110000, 0b10101010)
        assert result == 0b11111010
    
    def test_xor(self):
        """Test XOR operation"""
        result, flags = alu.execute('01010', 0b11110000, 0b10101010)
        assert result == 0b01011010
    
    def test_nand(self):
        """Test NAND operation"""
        result, flags = alu.execute('01000', 0xFF, 0xFF)
        assert result == 0x00
    
    def test_nor(self):
        """Test NOR operation"""
        result, flags = alu.execute('01001', 0x00, 0x00)
        assert result == 0xFF
    
    def test_xnor(self):
        """Test XNOR operation"""
        result, flags = alu.execute('01111', 0xFF, 0xFF)
        assert result == 0xFF


class TestShift:
    """Test shift operations"""
    
    def test_lsl(self):
        """Test logical shift left"""
        result, flags = alu.execute('00100', 0b00000001, 0)
        assert result == 0b00000010
        assert flags['carry'] == False
    
    def test_lsl_carry(self):
        """Test logical shift left with carry"""
        result, flags = alu.execute('00100', 0b10000000, 0)
        assert result == 0b00000000
        assert flags['carry'] == True
    
    def test_lsr(self):
        """Test logical shift right"""
        result, flags = alu.execute('00101', 0b10000000, 0)
        assert result == 0b01000000
    
    def test_asr(self):
        """Test arithmetic shift right"""
        result, flags = alu.execute('00110', 0b11000000, 0)
        assert result == 0b11100000  # Sign bit preserved


class TestSpecial:
    """Test special operations"""
    
    def test_pass_a(self):
        """Test PASS A"""
        result, flags = alu.execute('01011', 42, 99)
        assert result == 42
    
    def test_pass_b(self):
        """Test PASS B"""
        result, flags = alu.execute('01100', 42, 99)
        assert result == 99
    
    def test_not_a(self):
        """Test NOT A"""
        result, flags = alu.execute('10001', 0b11110000, 0)
        assert result == 0b00001111
    
    def test_not_b(self):
        """Test NOT B"""
        result, flags = alu.execute('10010', 0, 0b11110000)
        assert result == 0b00001111
    
    def test_rev_a(self):
        """Test REV A (bit reversal)"""
        result, flags = alu.execute('00111', 0b10000001, 0)
        assert result == 0b10000001  # Palindrome
        
        result, flags = alu.execute('00111', 0b10000000, 0)
        assert result == 0b00000001
    
    def test_cmp(self):
        """Test CMP (compare)"""
        result, flags = alu.execute('10000', 10, 5)
        assert result == 0  # CMP returns 0
        assert flags['carry'] == True  # A >= B
        assert flags['zero'] == False


class TestFlags:
    """Test flag generation"""
    
    def test_zero_flag(self):
        """Test zero flag"""
        result, flags = alu.execute('00000', 0, 0)
        assert flags['zero'] == True
        
        result, flags = alu.execute('00000', 1, 0)
        assert flags['zero'] == False
    
    def test_negative_flag(self):
        """Test negative flag"""
        result, flags = alu.execute('00001', 0, 1)
        assert flags['negative'] == True
    
    def test_carry_flag(self):
        """Test carry flag"""
        result, flags = alu.execute('00000', 200, 100)
        assert flags['carry'] == True
    
    def test_overflow_flag(self):
        """Test overflow flag"""
        # Adding two positive numbers resulting in negative
        result, flags = alu.execute('00000', 127, 1)
        assert flags['overflow'] == True


def main():
    """Run tests without pytest"""
    print("\n" + "="*80)
    print("Running ALU Tests (unittest mode)")
    print("="*80 + "\n")
    
    test_vectors = load_test_vectors()
    passed = 0
    failed = 0
    
    for test_data in test_vectors:
        try:
            test_alu_operation(test_data)
            passed += 1
        except AssertionError as e:
            failed += 1
            if failed <= 10:  # Only print first 10 failures
                print(f"❌ FAIL: {test_data.get('test_name')}")
                print(f"   {e}\n")
    
    print(f"\n{'='*80}")
    print(f"Results: {passed} passed, {failed} failed out of {passed+failed} total")
    print(f"Success Rate: {100*passed/(passed+failed):.1f}%")
    print(f"{'='*80}\n")
    
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    import sys
    sys.exit(main())
