#!/usr/bin/env python3
"""
ALU Test Runner - Runs tests from JSON test vectors
Simulates the 8-bit ALU with all 19 operations
"""

import json
import sys
from pathlib import Path
from typing import Dict, Tuple

class ALU8Bit:
    """Software simulation of 8-bit ALU with all 19 operations"""
    
    def __init__(self):
        self.width = 8
        self.mask = (1 << self.width) - 1
        
    def execute(self, opcode: str, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """Execute ALU operation and return result with flags"""
        a = a & self.mask
        b = b & self.mask
        
        # Map opcode to operation
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
        # Overflow: same sign inputs, different sign output
        overflow = ((a & 0x80) == (b & 0x80)) and ((a & 0x80) != (result & 0x80))
        return result & self.mask, self._flags(result, carry, overflow)
    
    def sub(self, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """SUB: A - B"""
        result = a - b
        carry = result >= 0  # In subtraction, carry=1 means no borrow
        # Overflow: different sign inputs, result different from A
        overflow = ((a & 0x80) != (b & 0x80)) and ((a & 0x80) != (result & 0x80))
        return result & self.mask, self._flags(result, carry, overflow)
    
    def inc_a(self, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """INC A: A + 1"""
        result = a + 1
        carry = result > self.mask
        overflow = (a == 0x7F)  # Overflow when incrementing max positive signed
        return result & self.mask, self._flags(result, carry, overflow)
    
    def dec_a(self, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """DEC A: A - 1"""
        result = a - 1
        carry = result >= 0
        overflow = (a == 0x80)  # Overflow when decrementing min negative signed
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
        """ASR: Arithmetic shift right (preserves sign)"""
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
        """NAND: ~(A & B)"""
        result = (~(a & b)) & self.mask
        return result, self._flags(result, False, False)
    
    def nor(self, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """NOR: ~(A | B)"""
        result = (~(a | b)) & self.mask
        return result, self._flags(result, False, False)
    
    def xor(self, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """XOR: A ^ B"""
        result = (a ^ b) & self.mask
        return result, self._flags(result, False, False)
    
    def pass_a(self, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """PASS A: Output A"""
        return a, self._flags(a, False, False)
    
    def pass_b(self, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """PASS B: Output B"""
        return b, self._flags(b, False, False)
    
    def and_op(self, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """AND: A & B"""
        result = (a & b) & self.mask
        return result, self._flags(result, False, False)
    
    def or_op(self, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """OR: A | B"""
        result = (a | b) & self.mask
        return result, self._flags(result, False, False)
    
    def xnor(self, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """XNOR: ~(A ^ B)"""
        result = (~(a ^ b)) & self.mask
        return result, self._flags(result, False, False)
    
    def cmp(self, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """CMP: Compare A and B (flags only, result is 0)"""
        result = a - b
        carry = result >= 0
        overflow = ((a & 0x80) != (b & 0x80)) and ((a & 0x80) != (result & 0x80))
        # CMP returns 0 as result, only flags matter
        return 0, self._flags(result, carry, overflow)
    
    def not_a(self, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """NOT A: ~A"""
        result = (~a) & self.mask
        return result, self._flags(result, False, False)
    
    def not_b(self, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """NOT B: ~B"""
        result = (~b) & self.mask
        return result, self._flags(result, False, False)


def run_tests(json_file: Path) -> Tuple[int, int, int]:
    """Run tests from JSON file and return (passed, failed, total)"""
    
    import time
    
    # Load test vectors
    print(f"\nLoading test vectors from: {json_file.name}...")
    load_start = time.time()
    with open(json_file, 'r') as f:
        data = json.load(f)
    load_time = time.time() - load_start
    
    tests = data.get('tests', [])
    if not tests:
        print(f"❌ No tests found in {json_file}")
        return 0, 0, 0
    
    print(f"✅ Loaded {len(tests):,} tests in {load_time:.2f}s")
    
    alu = ALU8Bit()
    passed = 0
    failed = 0
    
    print(f"\n{'='*80}")
    print(f"Running tests from: {json_file.name}")
    print(f"{'='*80}\n")
    
    # Start timing test execution
    test_start = time.time()
    
    # Track tests per operation
    op_stats = {}
    
    for i, test in enumerate(tests):
        test_name = test.get('test_name', f'Test_{i}')
        opcode = test.get('opcode', '')
        a = int(test.get('A', 0))
        b = int(test.get('B', 0))
        expected_result = int(test.get('expected_result', 0))
        expected_flags = test.get('expected_flags', {})
        
        # Track operation
        if opcode not in op_stats:
            op_stats[opcode] = {'passed': 0, 'failed': 0}
        
        try:
            # Execute ALU operation
            actual_result, actual_flags = alu.execute(opcode, a, b)
            
            # Check result
            result_match = (expected_result == actual_result)
            
            # Check flags
            flags_match = all(
                expected_flags.get(flag, False) == actual_flags.get(flag, False)
                for flag in ['carry', 'zero', 'overflow', 'negative']
            )
            
            if result_match and flags_match:
                passed += 1
                op_stats[opcode]['passed'] += 1
                # Only print first few passes to avoid clutter
                if passed <= 10 or not result_match or not flags_match:
                    print(f"✅ [PASS] {test_name}")
            else:
                failed += 1
                op_stats[opcode]['failed'] += 1
                print(f"❌ [FAIL] {test_name}")
                print(f"   Opcode: {opcode}, A: 0x{a:02X}, B: 0x{b:02X}")
                if not result_match:
                    print(f"   Result: Expected 0x{expected_result:02X}, Got 0x{actual_result:02X}")
                if not flags_match:
                    print(f"   Expected Flags: {expected_flags}")
                    print(f"   Actual Flags:   {actual_flags}")
                print()
        
        except Exception as e:
            failed += 1
            op_stats[opcode]['failed'] += 1
            print(f"❌ [ERROR] {test_name}: {e}\n")
    
    # Calculate elapsed time
    test_end = time.time()
    test_time = test_end - test_start
    total_time = test_end - load_start
    
    # Print summary
    print(f"\n{'='*80}")
    print(f"TEST SUMMARY")
    print(f"{'='*80}")
    print(f"Total Tests:  {passed + failed:,}")
    print(f"✅ Passed:    {passed:,} ({100*passed/(passed+failed):.1f}%)")
    print(f"❌ Failed:    {failed:,} ({100*failed/(passed+failed) if failed else 0:.1f}%)")
    print(f"{'='*80}")
    print(f"⏱️  Test Execution Time:  {test_time:.3f}s")
    print(f"📊 Load + Test Time:      {total_time:.3f}s")
    print(f"⚡ Test Speed:            {int((passed+failed)/test_time):,} tests/sec")
    print(f"{'='*80}\n")
    
    # Print per-operation statistics
    print(f"{'='*80}")
    print(f"PER-OPERATION RESULTS")
    print(f"{'='*80}")
    
    opcode_names = {
        '00000': 'ADD',
        '00001': 'SUB',
        '00010': 'INC A',
        '00011': 'DEC A',
        '00100': 'LSL',
        '00101': 'LSR',
        '00110': 'ASR',
        '00111': 'REV A',
        '01000': 'NAND',
        '01001': 'NOR',
        '01010': 'XOR',
        '01011': 'PASS A',
        '01100': 'PASS B',
        '01101': 'AND',
        '01110': 'OR',
        '01111': 'XNOR',
        '10000': 'CMP',
        '10001': 'NOT A',
        '10010': 'NOT B',
    }
    
    for opcode in sorted(op_stats.keys()):
        stats = op_stats[opcode]
        total_op = stats['passed'] + stats['failed']
        pass_rate = 100 * stats['passed'] / total_op if total_op > 0 else 0
        op_name = opcode_names.get(opcode, 'Unknown')
        status = "✅" if stats['failed'] == 0 else "❌"
        print(f"{status} {opcode} | {op_name:10s} | {stats['passed']:3d}/{total_op:3d} passed ({pass_rate:5.1f}%)")
    
    print(f"{'='*80}\n")
    
    return passed, failed, passed + failed


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        json_file = Path(sys.argv[1])
    else:
        # Default to demo.json in test/vectors
        json_file = Path(__file__).parent.parent / 'vectors' / 'demo.json'
    
    if not json_file.exists():
        print(f"❌ Error: File not found: {json_file}")
        return 1
    
    passed, failed, total = run_tests(json_file)
    
    # Return 0 if all tests passed, 1 otherwise
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
