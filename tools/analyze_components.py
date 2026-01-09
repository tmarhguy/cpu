#!/usr/bin/env python3
"""
Analyze Logisim circuit file and extract all components with their sizes.
"""

import xml.etree.ElementTree as ET
from collections import defaultdict
import sys

def get_attr(comp, name, default=None):
    """Get attribute value from component."""
    for attr in comp.findall('a'):
        if attr.get('name') == name:
            return attr.get('val')
    return default

def analyze_logisim_circuit(filename):
    """Analyze a Logisim circuit file and return component statistics."""
    
    tree = ET.parse(filename)
    root = tree.getroot()
    
    # Component categories
    gates = defaultdict(lambda: defaultdict(int))
    muxes = defaultdict(lambda: defaultdict(int))
    other = defaultdict(int)
    
    # Find all components in the main circuit
    circuit = root.find(".//circuit[@name='main']")
    if circuit is None:
        print("Warning: Could not find main circuit")
        return
    
    for comp in circuit.findall('comp'):
        lib = comp.get('lib')
        name = comp.get('name')
        
        if lib == '1':  # Gates library
            # NOT gates don't have inputs attribute
            if 'NOT' in name or name == 'NOT Gate':
                width = get_attr(comp, 'width', '1')
                key = f"{name}"
                gates[key][f"width={width}"] += 1
            else:
                inputs = get_attr(comp, 'inputs', '2')  # Default is 2 for gates
                width = get_attr(comp, 'width', '1')  # Default is 1 bit
                
                # Create key: "GateType (inputs=X, width=Y)"
                key = f"{name}"
                if inputs != '2' or width != '1':
                    if width != '1':
                        gates[key][f"width={width}"] += 1
                    if inputs != '2':
                        gates[key][f"inputs={inputs}"] += 1
                else:
                    gates[key]["inputs=2, width=1"] += 1
                
        elif lib == '2':  # Multiplexers library
            select = get_attr(comp, 'select', '1')  # Default select bits
            width = get_attr(comp, 'width', '1')
            num_inputs = 2 ** int(select) if select else 2
            
            key = f"{name}"
            muxes[key][f"{num_inputs}:1 MUX, select={select}, width={width}"] += 1
            
        elif lib == '3':  # Arithmetic library
            width = get_attr(comp, 'width', '1')
            key = f"{name} (width={width})"
            other[key] += 1
            
        else:
            # Other components
            width = get_attr(comp, 'width', None)
            fanout = get_attr(comp, 'fanout', None)
            incoming = get_attr(comp, 'incoming', None)
            
            key = name
            if width:
                key += f" (width={width})"
            if fanout:
                key += f" (fanout={fanout})"
            if incoming:
                key += f" (incoming={incoming})"
                
            other[key] += 1
    
    return gates, muxes, other

def print_results(gates, muxes, other):
    """Print analysis results in a formatted way."""
    
    print("=" * 80)
    print("COMPONENT ANALYSIS - ALU TOP CIRCUIT")
    print("=" * 80)
    print()
    
    # Print Gates
    print("GATES:")
    print("-" * 80)
    
    # Detailed breakdown by input size and width
    gate_details = defaultdict(lambda: defaultdict(int))
    
    for gate_name, variations in sorted(gates.items()):
        for variant, count in sorted(variations.items()):
            # Parse inputs and width
            if 'NOT' in gate_name:
                # NOT gates are unary - no inputs attribute
                width = '1'  # default
                if 'width=' in variant:
                    width = variant.split('width=')[1].split(',')[0].split(')')[0]
                key = f"{gate_name} ({width}-bit)"
            else:
                inputs = '2'  # default
                width = '1'   # default
                
                if 'inputs=' in variant:
                    inputs = variant.split('inputs=')[1].split(',')[0].split(')')[0]
                if 'width=' in variant:
                    width = variant.split('width=')[1].split(',')[0].split(')')[0]
                
                key = f"{gate_name} ({inputs}-input, {width}-bit)"
            gate_details[gate_name][key] += count
    
    for gate_name in sorted(gate_details.keys()):
        print(f"  {gate_name}:")
        for variant, count in sorted(gate_details[gate_name].items()):
            print(f"    {variant}: {count}")
        print(f"    Subtotal: {sum(gate_details[gate_name].values())}")
        print()
    
    print()
    print("MULTIPLEXERS:")
    print("-" * 80)
    
    mux_types = defaultdict(lambda: defaultdict(int))
    for mux_name, variations in sorted(muxes.items()):
        for variant, count in sorted(variations.items()):
            mux_types[mux_name][variant] += count
    
    for mux_name in sorted(mux_types.keys()):
        print(f"  {mux_name}")
        for variant, count in sorted(mux_types[mux_name].items()):
            print(f"    {variant}: {count}")
        print()
    
    print()
    print("OTHER COMPONENTS:")
    print("-" * 80)
    
    for comp_name, count in sorted(other.items()):
        print(f"  {comp_name}: {count}")
    
    print()
    print("=" * 80)
    
    # Summary statistics
    print()
    print("SUMMARY:")
    print("-" * 80)
    
    total_gates = sum(sum(v.values()) for v in gates.values())
    total_muxes = sum(sum(v.values()) for v in muxes.values())
    total_other = sum(other.values())
    
    print(f"Total Gates: {total_gates}")
    print(f"Total Multiplexers: {total_muxes}")
    print(f"Total Other Components: {total_other}")
    print(f"Grand Total: {total_gates + total_muxes + total_other}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = '/Users/tmarhguy/Documents/cpu/logisim/top/alu_top.circ'
    
    gates, muxes, other = analyze_logisim_circuit(filename)
    print_results(gates, muxes, other)

