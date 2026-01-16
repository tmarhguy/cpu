#!/usr/bin/env python3
"""
Generate exhaustive test vectors for 8-bit ALU
Creates 256×256 test combinations for each operation (19 operations × 65,536 tests = 1,245,184 tests)
"""

import json
import sys
from pathlib import Path
from typing import Dict, Tuple


class ALU8Bit:
    """Software simulation of 8-bit ALU"""
    
    def __init__(self):
        self.width = 8
        self.mask = (1 << self.width) - 1
        
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


def generate_exhaustive_tests(output_file: Path, chunk_size: int = 10000):
    """
    Generate exhaustive test vectors
    For operations that use B: 256×256 = 65,536 tests per operation
    For operations that don't use B: 256 tests per operation (B=0)
    """
    
    print("=" * 80)
    print("EXHAUSTIVE ALU TEST VECTOR GENERATOR")
    print("=" * 80)
    print()
    
    alu = ALU8Bit()
    
    operations = [
        ("00000", "ADD", alu.add, True),
        ("00001", "SUB", alu.sub, True),
        ("00010", "INC_A", alu.inc_a, False),
        ("00011", "DEC_A", alu.dec_a, False),
        ("00100", "LSL", alu.lsl, False),
        ("00101", "LSR", alu.lsr, False),
        ("00110", "ASR", alu.asr, False),
        ("00111", "REV_A", alu.rev_a, False),
        ("01000", "NAND", alu.nand, True),
        ("01001", "NOR", alu.nor, True),
        ("01010", "XOR", alu.xor, True),
        ("01011", "PASS_A", alu.pass_a, False),
        ("01100", "PASS_B", alu.pass_b, True),
        ("01101", "AND", alu.and_op, True),
        ("01110", "OR", alu.or_op, True),
        ("01111", "XNOR", alu.xnor, True),
        ("10000", "CMP", alu.cmp, True),
        ("10001", "NOT_A", alu.not_a, False),
        ("10010", "NOT_B", alu.not_b, True),
    ]
    
    # Calculate total tests: 256×256 for ALL 19 operations
    total_operations = len(operations)
    total_tests = total_operations * 256 * 256
    
    print(f"Total operations:                {total_operations}")
    print(f"Tests per operation:             256×256 = 65,536")
    print(f"Total test vectors to generate:  {total_tests:,} ({total_operations} × 65,536)")
    print(f"Estimated JSON file size:        ~{total_tests * 200 / (1024*1024):.1f} MB")
    print()
    
    response = input("This will generate a LARGE file. Continue? (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        print("Cancelled.")
        return
    
    print()
    print("Generating test vectors...")
    print()
    
    all_tests = []
    test_count = 0
    
    for opcode, op_name, op_func, uses_b in operations:
        print(f"Generating: {opcode} {op_name:10s}", end=" ", flush=True)
        op_tests = 0
        
        for a in range(256):
            # Generate all 256×256 combinations for EVERY operation
            # Even if the operation doesn't use B, we test all B values
            for b in range(256):
                result, flags = op_func(a, b)
                
                test = {
                    "test_name": f"{op_name}_{a:02X}_{b:02X}",
                    "opcode": opcode,
                    "A": a,
                    "B": b,
                    "expected_result": result,
                    "expected_flags": flags
                }
                all_tests.append(test)
                op_tests += 1
                test_count += 1
            
            # Progress indicator
            if (a + 1) % 64 == 0:
                print(".", end="", flush=True)
        
        print(f" {op_tests:,} tests")
    
    print()
    print(f"Total tests generated: {test_count:,}")
    print()
    print(f"Writing to {output_file}...")
    
    # Write to file
    with open(output_file, 'w') as f:
        json.dump({"tests": all_tests}, f, indent=2)
    
    # Get file size
    file_size = output_file.stat().st_size
    print(f"✅ Complete! File size: {file_size / (1024*1024):.2f} MB")
    print()
    
    # Print summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Output file:     {output_file}")
    print(f"Total tests:     {test_count:,}")
    print(f"File size:       {file_size / (1024*1024):.2f} MB")
    print(f"Lines:           {sum(1 for _ in open(output_file)):,}")
    print()
    print("Test distribution:")
    
    for opcode, op_name, _, uses_b in operations:
        print(f"  {opcode} {op_name:10s}: 65,536 tests (256×256)")
    
    print()
    print("=" * 80)
    print()


def main():
    """Main entry point"""
    
    # Output file path
    output_file = Path(__file__).parent.parent / 'vectors' / 'exhaustive.json'
    
    if len(sys.argv) > 1:
        output_file = Path(sys.argv[1])
    
    try:
        generate_exhaustive_tests(output_file)
    except KeyboardInterrupt:
        print("\n\n❌ Interrupted by user")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
