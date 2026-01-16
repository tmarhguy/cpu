#!/usr/bin/env python3
"""
8-Bit ALU Command Line Interface

A professional CLI tool for executing ALU operations interactively.
Supports both simulation mode and future FPGA hardware integration.

Usage:
    ./alu_cli.py ADD 42 23
    ./alu_cli.py --hex XOR 0xAA 0x55
    ./alu_cli.py --binary AND 11110000 00001111
    ./alu_cli.py --list
    ./alu_cli.py --help

Author: Tyrone Marhguy
Project: 8-Bit Discrete Transistor ALU
"""

import sys
import argparse
from pathlib import Path
from typing import Dict, Tuple, Optional

# Add test directory to path
sys.path.insert(0, str(Path(__file__).parent / 'test'))

try:
    from test_alu import ALU8Bit
except ImportError:
    print("Error: Could not import ALU8Bit from test_alu.py", file=sys.stderr)
    print("Please ensure test/test_alu.py exists and is accessible.", file=sys.stderr)
    sys.exit(1)


class ALUInterface:
    """Professional interface for ALU operations"""
    
    # Operation name to opcode mapping
    OPCODE_MAP = {
        'ADD':    '00000',
        'SUB':    '00001',
        'INC':    '00010',
        'DEC':    '00011',
        'LSL':    '00100',
        'LSR':    '00101',
        'ASR':    '00110',
        'REV':    '00111',
        'NAND':   '01000',
        'NOR':    '01001',
        'XOR':    '01010',
        'PASSA':  '01011',
        'PASSB':  '01100',
        'AND':    '01101',
        'OR':     '01110',
        'XNOR':   '01111',
        'CMP':    '10000',
        'NOTA':   '10001',
        'NOTB':   '10010',
    }
    
    # Operation descriptions
    OPERATION_INFO = {
        'ADD':    ('Arithmetic', 'A + B', 'Addition'),
        'SUB':    ('Arithmetic', 'A - B', 'Subtraction (2\'s complement)'),
        'INC':    ('Arithmetic', 'A + 1', 'Increment A'),
        'DEC':    ('Arithmetic', 'A - 1', 'Decrement A'),
        'LSL':    ('Shift', 'A << 1', 'Logical shift left'),
        'LSR':    ('Shift', 'A >> 1', 'Logical shift right'),
        'ASR':    ('Shift', 'A >> 1 (sign)', 'Arithmetic shift right'),
        'REV':    ('Special', 'reverse(A)', 'Reverse bit order'),
        'NAND':   ('Logic', '~(A & B)', 'NAND gate'),
        'NOR':    ('Logic', '~(A | B)', 'NOR gate'),
        'XOR':    ('Logic', 'A ^ B', 'XOR gate'),
        'PASSA':  ('Logic', 'A', 'Pass A through'),
        'PASSB':  ('Logic', 'B', 'Pass B through'),
        'AND':    ('Logic', 'A & B', 'AND gate'),
        'OR':     ('Logic', 'A | B', 'OR gate'),
        'XNOR':   ('Logic', '~(A ^ B)', 'XNOR gate'),
        'CMP':    ('Special', 'A - B (flags)', 'Compare (flags only)'),
        'NOTA':   ('Logic', '~A', 'Invert A'),
        'NOTB':   ('Logic', '~B', 'Invert B'),
    }
    
    def __init__(self):
        self.alu = ALU8Bit()
        self.mode = 'simulation'  # 'simulation' or 'fpga'
    
    def execute(self, operation: str, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """Execute ALU operation"""
        operation = operation.upper()
        
        if operation not in self.OPCODE_MAP:
            raise ValueError(f"Unknown operation: {operation}")
        
        opcode = self.OPCODE_MAP[operation]
        
        if self.mode == 'simulation':
            return self._execute_simulation(opcode, a, b)
        elif self.mode == 'fpga':
            return self._execute_fpga(opcode, a, b)
        else:
            raise ValueError(f"Unknown mode: {self.mode}")
    
    def _execute_simulation(self, opcode: str, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """Execute on software golden model"""
        return self.alu.execute(opcode, a, b)
    
    def _execute_fpga(self, opcode: str, a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """Execute on FPGA hardware (placeholder for future implementation)"""
        raise NotImplementedError("FPGA mode not yet implemented")
    
    def format_result(self, operation: str, a: int, b: int, result: int, 
                     flags: Dict[str, bool], format_type: str = 'decimal') -> str:
        """Format execution result for display"""
        lines = []
        lines.append("=" * 70)
        lines.append(f"ALU Operation: {operation}")
        lines.append("=" * 70)
        
        # Operation info
        if operation in self.OPERATION_INFO:
            category, expr, desc = self.OPERATION_INFO[operation]
            opcode = self.OPCODE_MAP[operation]
            lines.append(f"Opcode:      {opcode} (binary: 0b{int(opcode, 2):05b}, decimal: {int(opcode, 2)})")
            lines.append(f"Category:    {category}")
            lines.append(f"Expression:  {expr}")
            lines.append(f"Description: {desc}")
            lines.append("")
        
        # Inputs
        lines.append("Inputs:")
        lines.append(f"  A = {self._format_value(a, format_type)}")
        lines.append(f"  B = {self._format_value(b, format_type)}")
        lines.append("")
        
        # Result
        lines.append("Result:")
        lines.append(f"  OUT = {self._format_value(result, format_type)}")
        lines.append("")
        
        # Flags
        lines.append("Flags:")
        lines.append(f"  Carry (C):    {self._format_flag(flags.get('carry', False))}")
        lines.append(f"  Zero (Z):     {self._format_flag(flags.get('zero', False))}")
        lines.append(f"  Negative (N): {self._format_flag(flags.get('negative', False))}")
        lines.append(f"  Overflow (V): {self._format_flag(flags.get('overflow', False))}")
        lines.append("=" * 70)
        
        return "\n".join(lines)
    
    def _format_value(self, value: int, format_type: str) -> str:
        """Format a value according to specified format"""
        value = value & 0xFF  # Ensure 8-bit
        
        if format_type == 'hex':
            return f"0x{value:02X}"
        elif format_type == 'binary':
            return f"0b{value:08b}"
        elif format_type == 'all':
            return f"{value:3d} (0x{value:02X}, 0b{value:08b})"
        else:  # decimal
            return f"{value:3d}"
    
    def _format_flag(self, flag: bool) -> str:
        """Format a flag value"""
        return "1 (SET)" if flag else "0 (CLEAR)"
    
    def list_operations(self) -> str:
        """List all available operations"""
        lines = []
        lines.append("=" * 70)
        lines.append("Available ALU Operations (19 total)")
        lines.append("=" * 70)
        lines.append("")
        
        # Group by category
        categories = {}
        for op, info in self.OPERATION_INFO.items():
            category = info[0]
            if category not in categories:
                categories[category] = []
            categories[category].append((op, info[1], info[2]))
        
        for category in ['Arithmetic', 'Logic', 'Shift', 'Special']:
            if category in categories:
                lines.append(f"{category} Operations:")
                lines.append("-" * 70)
                for op, expr, desc in categories[category]:
                    opcode = self.OPCODE_MAP[op]
                    lines.append(f"  {op:8s} [{opcode}]  {expr:20s}  {desc}")
                lines.append("")
        
        lines.append("=" * 70)
        lines.append("Usage Examples:")
        lines.append("  ./alu_cli.py ADD 42 23")
        lines.append("  ./alu_cli.py --hex XOR 0xAA 0x55")
        lines.append("  ./alu_cli.py --binary AND 11110000 00001111")
        lines.append("  ./alu_cli.py --format all SUB 100 35")
        lines.append("=" * 70)
        
        return "\n".join(lines)


def parse_value(value_str: str, input_format: Optional[str] = None) -> int:
    """Parse input value with auto-detection or specified format"""
    value_str = value_str.strip()
    
    # Auto-detect format if not specified
    if input_format is None:
        if value_str.startswith('0x') or value_str.startswith('0X'):
            return int(value_str, 16)
        elif value_str.startswith('0b') or value_str.startswith('0B'):
            return int(value_str, 2)
        else:
            return int(value_str, 10)
    
    # Use specified format
    if input_format == 'hex':
        return int(value_str, 16)
    elif input_format == 'binary':
        return int(value_str, 2)
    else:
        return int(value_str, 10)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='8-Bit ALU Command Line Interface',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s ADD 42 23                    # Decimal input
  %(prog)s --hex XOR 0xAA 0x55          # Hexadecimal input
  %(prog)s --binary AND 11110000 00001111  # Binary input
  %(prog)s --format all SUB 100 35      # Show all formats
  %(prog)s --list                       # List all operations
  %(prog)s --interactive                # Interactive mode

For more information, see: docs/OPCODE_TABLE.md
        """
    )
    
    # Positional arguments
    parser.add_argument('operation', nargs='?', type=str,
                       help='ALU operation (ADD, SUB, AND, XOR, etc.)')
    parser.add_argument('operand_a', nargs='?', type=str,
                       help='First operand (A)')
    parser.add_argument('operand_b', nargs='?', type=str,
                       help='Second operand (B)')
    
    # Input format options
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument('--hex', action='store_true',
                           help='Interpret inputs as hexadecimal')
    input_group.add_argument('--binary', action='store_true',
                           help='Interpret inputs as binary')
    
    # Output format options
    parser.add_argument('--format', choices=['decimal', 'hex', 'binary', 'all'],
                       default='decimal',
                       help='Output format (default: decimal)')
    
    # Mode options
    parser.add_argument('--mode', choices=['simulation', 'fpga'],
                       default='simulation',
                       help='Execution mode (default: simulation)')
    
    # Information options
    parser.add_argument('--list', action='store_true',
                       help='List all available operations')
    parser.add_argument('--interactive', action='store_true',
                       help='Start interactive mode')
    parser.add_argument('--quiet', action='store_true',
                       help='Minimal output (result only)')
    
    args = parser.parse_args()
    
    # Create ALU interface
    interface = ALUInterface()
    interface.mode = args.mode
    
    # Handle list operations
    if args.list:
        print(interface.list_operations())
        return 0
    
    # Handle interactive mode
    if args.interactive:
        print("Interactive mode not yet implemented.")
        print("Use: ./alu_cli.py <operation> <a> <b>")
        return 1
    
    # Validate required arguments
    if not args.operation or not args.operand_a or not args.operand_b:
        parser.print_help()
        return 1
    
    try:
        # Determine input format
        input_format = None
        if args.hex:
            input_format = 'hex'
        elif args.binary:
            input_format = 'binary'
        
        # Parse operands
        a = parse_value(args.operand_a, input_format)
        b = parse_value(args.operand_b, input_format)
        
        # Validate 8-bit range
        if not (0 <= a <= 255):
            print(f"Error: Operand A ({a}) out of 8-bit range (0-255)", file=sys.stderr)
            return 1
        if not (0 <= b <= 255):
            print(f"Error: Operand B ({b}) out of 8-bit range (0-255)", file=sys.stderr)
            return 1
        
        # Execute operation
        result, flags = interface.execute(args.operation, a, b)
        
        # Display result
        if args.quiet:
            print(result)
        else:
            output = interface.format_result(
                args.operation.upper(), a, b, result, flags, args.format
            )
            print(output)
        
        return 0
        
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
