
## Page 1

**The page is titled "1 - bit half adder"**^1^.

**It displays a circuit diagram with two vertical input lines, 'A' **^2^^2^and 'B'^3^^3^. The diagram shows two logic gates:

* **An AND gate with inputs A and B, producing an output labeled 'out'**^4^^4^.
* **An XOR gate with inputs A and B, producing an output labeled 'carry out'**^5^.

The page also contains scattered text fragments, including:

* (A+B) **A AND B **^6^
* **A XOR B **^7^
* **A **^8^^8^^8^^8^
* **D **^9^
* **out **^10^^10^^10^^10^
* **B **^11^^11^^11^^11^
* **Carry-out **^12^
* **Carry **^13^
* **Fragments of a truth table, including "0" **^14^^14^^14^^14^^14^^14^^14^^14^^14^^14^^14^^14^^14^^14^^14^, "1" ^15^^15^^15^^15^^15^^15^^15^^15^^15^, "00" ^16^, "01" ^17^^17^^17^^17^, "11" ^18^, and "10"^19^.

---

## Page 2

**This page is titled "1 bit full adder"**^20^.

**It contains a table with truth table and K-map information**^21^:

* **Headers:** A, B, Cin, A+B+Cin, k-map, k-map^22^.
* **Content:** The table shows inputs and outputs for a full adder, with K-maps used to derive the logic expressions.
* **Derived Formulas:**
  * **Sum: "**$=A\oplus B\oplus C$**"**^23^.
  * **Carry: "ABC + ABC + ABC + ABC"**^24^.

**A second table lists "Transistor Cost Finding"**^25^:

* **Gate Costs:**
  * **NOT: 2 **^26^
  * **NOR: 4 **^27^
  * **NAND: 4 **^28^
  * **OR: 6 **^29^
  * **AND: 6 **^30^
  * **XOR: 12 **^31^
  * **XNOR **^32^
* **Carry Formula:** "**$Cary=AB+BC+AC$**"^33^.
* **Notes:** "best design Gen: (n-1) mosfets for n input" ^34^and "n- AND = (n-1) NAND + n-OR = (n-1) OR NOT"^35^.

---

## Page 3

**This page displays images of three logic gates: "AND" **^36^, "OR" ^37^, and "XOR"^38^.

**It includes "Design cost" **^39^ calculations for a full adder:

**Calculation 1 (Standard Carry):**

* **Formula: "AB + BC + AC" **^40^
* **Implementation: "**$3~AND+1~OR$**" **^41^
* **Cost: "**$\Rightarrow3\cdot6+2\cdot6=30T$**" **^42^

**Calculation 2 (Optimized Carry):**

* **Formula: "**$AB+C(A\oplus B)$**" **^43^
* **Implementation: "**$2~AND+1~OR+1~XOR$**" **^44^
* **Cost: "**$2\cdot6+6+12=30T$**" **^45^

**Calculation 3 (Sum):**

* **"3-12" **^46^
* **"36 T" **^47^

**Total Cost:**

* **"**$Final=36+30=66T$**" **^48^

**Other labels on the page include "A" **^49^, "B" ^50^, "carry-in" ^51^, "out" ^52^, and "carry-out"^53^.

---

## Page 4

**This page shows the "Designing" **^54^and "Simulation" ^55^of the "Carry - Circuit"^56^.

* **The circuit implements the "AB + BC + AC" **^57^ carry logic.
* **It shows a simulation "for Carry" **^58^with the inputs set to "101" ^59^ (A=1, B=0, C=1).
* **The circuit path is highlighted, showing the final "Carry" **^60^output is "1"^61^.

---

## Page 5

**This page shows the "Designing" **^62^and "Simulation of" ^63^the "Sum" ^64^^64^circuit (written as "sun" ^65^).

* The circuit consists of two XOR gates, implementing **$A \oplus B \oplus C$**.
* **It shows a simulation with the inputs set to "100" **^66^ (A=1, B=0, C=0).
* **The circuit path is highlighted, showing the final "Sum" **^67^output is "1"^68^.
* **Other text includes "2" **^69^and "ABAC"^70^.

---

## Page 6

**This page discusses "Scaling" **^71^from a 1-bit full adder to an "8-bit full - adder"^72^.

* **Current implementation:** ^73^"adds" ^74^"two 1-bits."^75^.
* **New Design:** Use the "1 bit" ^76^"full adder" ^77^"as" ^78^ "a" **"black box"**^79^.
* **Inputs/Outputs:**
  * **"8-bit Input **$A[7:0]$**" **^80^
  * **"8-bit input **$B[7:0]$**" **^81^
  * **"8- bit output" **^82^"S[7:0]" ^83^
  * **"carry," **^84^"1 bit" ^85^("1 if overflow else" ^86^"will address" ^87^"later" ^88^).

**A diagram shows an 8-bit ripple-carry adder, chaining the carry-out from one stage (**$C_0$** **^89^, **$C_1$** ^90^, etc.) to the carry-in of the next, producing "S[0]" ^91^through "S[7]" ^92^and a final carry-out "**$C_8$**" ^93^or "**$C_{final}$**"^94^.

The page notes that "Currently," 95"ADD is the" 96"only operation."97.

The goal is "Improving" 98 "to" "support" 99"subtraction" 100("SUB" 101101101101101101101101101).

* **ADD:** "A" ^102^ + **"B" **^103^"=>" ^104^"A + B"^105^.
* **SUB:** "A" ^106^ - **"B" **^107^"=>" ^108^"**$A+(-B)$**"^109^.
* **This is implemented using "2's complement,"**^110^.
* **A note says to "* Ignore storage register specs" **^111^ "in" **"assembly."**^112^.

---

## Page 7

This page discusses how to implement subtraction.

* **A table demonstrates 2's complement: "NOT (B)" **^113^"+" ^114^"1"^115^.
* **"ALU must know when to add / subtract."**^116^.
* **"A control line is" **^117^"Created."^118^.

**The page notes that the current design only supports "2" **^119^"operations" ^120^but "will be improved to support" ^121^"MUL (multiplication) and" ^122^"DIV (divide)"^123^. **The "Same ALU will handle logical operations,"**^124^.

A "4 bit" 125"control signal" 126is proposed, allowing "$2^{4}=16$" 127"possible operations"128.

The implementation will use a "selector" 129"mux"130.

---

## Page 8

**This page shows a block diagram for "Logic with control signal"**^131^.

* **Inputs: "A" **^132^, "B" ^133^, "Control sign-" ^134^, "Cin"^135^.
* **Outputs: "Sum" **^136^, "carry-out"^137^.

**To perform subtraction ("Given A-B" **^138^):

* **The "Control line" is set to "1 if Sub else 0"**^139^.
* **Setting "SUB" **^140^to "1" ^141^will "supply adder with" ^142^"first NOT (B)" and also "adds" ^143^the "1" ^144^ (as **$C_{in}$**) **which "completes 2's complement"**^145^.

**"Cons of Design"**^146^:

* **"It requires at least" **^147^"8 of 3 input AND gates and" ^148^"OR" ^149^"gates" ^150^ (likely for a multiplexer).
* **Cost: "**$(16+7)\cdot6T=\sim138T$**" **^151^, "excluding NOT" ^152^"gates"^153^.

---

## Page 9

**This page proposes a "Different approach"**^154^.

* **"Instead of dedicated mux" **^155^, "Implement" ^156^"the logic circuit switched" ^157^"using" ^158^"XOR"^159^.
* **A truth table for "A XOR B" **^160^ is shown.
* **The "beautiful" **^161^"logic" ^162^ is that:

  * B XOR 0 = B
  * B XOR 1 = NOT B
* **The "control" **^163^"signal" ^164^ will be an 8-bit value:

  * **ADD:** "00000000" ^165^
  * **SUB:** "1111111" ^166^
* **The input "B is" **^167^"always passed through" ^168^"an" ^169^"XOR" ^170^gate "with that" ^171^ control signal.
* **The "control (1bit) feeds the ALU" **^172^ (as **$C_{in}$**) **"to complete" **^173^ the 2's complement.

---

## Page 10

**This page lists the "Advantage;" **^174^ of the XOR design.

* **Cost:** "8 bit" ^175^"XOR" ^176^ gates.
* **"8 * 12" **^177^"=" ^178^"96T"^179^^179^^179^^179^.
* **This is cheaper than the "138T" **^180^ MUX design.

**A diagram for the "Logic with" **^181^"XOR design" ^182^ is shown.

* **Inputs: "A" **^183^, "B" ^184^, "Control sign-"^185^.
* **A "blackbox" **^186^ (control unit) **takes the "4 bits" **^187^ "CT. Sig" (control signal).
* **The control unit "sends"**^188^:
  1. **A "1 bit to adder" **^189^ (as **$C_{in}$**).
  2. **An "8 bit" **^190^signal of "1s" ^191^or "0s" ^192^to the "XOR" ^193^ gates.
* **The adder then outputs "Sum" **^194^and "Carry-out"^195^.

**Conclusion:** "With the growing operations, it is obvious" ^196^ "a" **"control unit is" **^197^"needed with its decoder to" ^198^"process for the diff operators."^199^.

---

## Page 11

**This page has a concluding title: "Building Control Unit" **^200^followed by a "}"^201^.
