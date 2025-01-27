# TaiScript Documentation

## Overview

TaiScript is a playful, pseudo-code-inspired programming language that integrates programming concepts with humorous real-world references (like bribes for execution). Its syntax is designed to be simple yet expressive, catering to an audience who wants a light-hearted approach to learning programming.

---

## Features

- **Flexible Syntax**: Inspired by natural language with a touch of humor.
- **Profiles (`parichay`)**: Affects how much "bribe" is required to run code efficiently.
- **Bribe Mechanism**: Adds a playful layer of execution cost.
- **Loop, Conditionals, and Variables**: Implements basic programming constructs.
- **File Operations**: Includes operations like opening, writing to, and closing files.
- **Nested Loops**: Supports multiple nested loop scenarios.
- **Custom Error Messages**: Errors like insufficient bribes are presented humorously.

---

## Language Components

### 1. Program Structure
A program starts with `yojna shuru` and ends with `yojna band`.

```plaintext
yojna shuru "ProgramName"
    // Statements
yojna band
```

### 2. Profiles (`parichay`)
Define your profile at the start of the program. Profiles impact bribe requirements and execution speed.


| **Profile**           | **Reduction Factor** | **Description**                                                                |
|------------------------|----------------------|-------------------------------------------------------------------------------|
| `JANTA`               | 1.0 (No discount)   | Ordinary citizen. Slow execution with maximum bribes                            |
| `STUDENT`             | 0.5 (50% discount)  | Students get a discount, but there may still be a delay in execution.           |
| `CHACHA VIDHAYAK HAI` | 0.0 (Free)          | No bribes needed. Instant execution, as "you know someone in power."            |
| `BABU SAHEB`          | 0.0 (Free)          | No bribes needed. But equivalent black money will be credited.                  |
| `NETA JI`             | 0.0 (Free)          | No bribes required, but at the end, an extra print is added praising Neta Ji    |

Example:
```plaintext
parichay "JANTA"
```

---

### 3. Bribes (`ghoos lo`)
Here every operation has a "bribe cost" associated with it. This cost, or "ghoos," must be paid to ensure the smooth execution of your program. Without providing sufficient ghoos, your program execution halts with a humorous error message.

The `ghoos lo` statement allows you to **add a specific amount of bribe** to a pool that will be consumed as your program executes.

---

**Syntax**

```plaintext
ghoos lo <amount>
```

- `<amount>`: The amount of bribe you are adding to the pool.

Example:
```plaintext
ghoos lo 500
```
This statement adds 500 to the bribe pool.

---

#### **How `ghoos` Works**

**Base Bribe Amount**

The base bribe amount is calculated based on the **current year** and a starting year (`2025`). The bribe increases every year due to inflation, calculated as follows:

#### **Formula**:
Base Bribe Amount = Initial Amount x (1.5 ^ (Year since 2025))

- **Initial Amount**: 500
- **Growth Factor**: Bribe increases by 1.5× every year.

#### **Example Calculations**:
- **In 2025**: Base Bribe = 500
- **In 2026**: Base Bribe = 500 × 1.5 = 750
- **In 2027**: Base Bribe = 750 × 1.5 = 1125

---

#### **Adjusted Bribe Formula**:
Effective Bribe = Base Bribe Amount x Reduction Factor

---

#### **When is `ghoos` Consumed?**

Bribe is consumed at key points in the program:
1. **Variable Declaration (`likho`)**: A small amount of bribe may be consumed.
2. **Loops (`ginti karo`)**: Loops consume a significant bribe depending on the number of loops and nesting.
3. **Conditionals (`agar`)**: Minor bribe consumption for executing conditional logic.
4. **File Operations**: Operations like opening, writing to, or closing a file require bribes.

---

#### **How to Calculate Bribe?**

To ensure smooth execution of your program, follow these steps:

1. **Identify Base Bribe**:
   - Use the formula for base bribe considering the current year.
   - Example: If the year is 2025, the base bribe is 500.

2. **Consider Profile Discount**:
   - Adjust the base bribe using the reduction factor for your profile (`parichay`).

3. **Estimate Complexity**:
   - The complexity of your code (e.g., nested loops, large conditionals) will increase the bribe required. (For time complexity 1 - n: ghoos lo is n, for n^2 it is 2 x n, for n^3 it is 3 x n and so on)
   - **Example**: A simple program may require 500, while nested loops may require 2000+.

4. **Add Sufficient `ghoos` at Key Points**:
   - Add bribe at the beginning (`ghoos lo`) and before major operations like loops or conditionals.
   - Example:
     ```plaintext
     ghoos lo 1000
     ginti karo i 1 se 10 tak {
         ginti karo j 1 se i tak {
             ghoshna "*"
         }
         ginti band
         ghoshna ""
     }
     ginti band
     ```

---

#### Code:
```plaintext
yojna shuru "PatternPrinter"

parichay "JANTA"

ghoos lo 500
likho n 10
ghoshna "Starting Pattern"

ghoos lo 1000
ginti karo i 1 se n tak {
    ginti karo j 1 se i tak {
        ghoshna "*" lagatar
    }
    ginti band
    ghoshna ""
}
ginti band

yojna band
```

#### Execution:

1. **Profile**: `JANTA` → No discount.
2. **Base Bribe in 2025**: 500.
3. **Bribes Added**:
   - **500** for initial variable declaration and print statements.
   - **1000** for nested loops.
4. **Complexity**:
   - Outer Loop: 1–10 (10 iterations).
   - Inner Loop: Nested (1 + 2 + ... + 10 = 55 iterations).

5. **Bribe Consumption**:
   - Initial `500` consumed for variable declaration and `ghoshna`.
   - `1000` consumed for nested loops.

---

#### **Error Handling**

If sufficient bribe is not provided, the program halts with an error:

```plaintext
Runtime exception: Itne me kya hoga! Thoda aur adjust karo, tabhi file aage badhegi.
Pass <shortfall> more under the table.
```

To avoid errors:
- Calculate bribe requirements in advance.
- Provide bribes before complex operations like loops or file operations.

---

#### **Note**

`ghoos lo` is not just a fun addition but a core concept in TaiScript that:
- Simulates real-world bureaucracy.
- Adds complexity management to your programs.
- Challenges you to think ahead and calculate requirements.

Use it wisely to ensure smooth execution of your TaiScript programs!

### 4. Variable Declaration (`likho`)
Declare variables using `likho`.

```plaintext
likho <variableName> <value>
```

Example:
```plaintext
likho n 10
```

---

### 5. Input (`pucho`)
Take input from the user and store it in a variable.

```plaintext
pucho <variableName>
```

Example:
```plaintext
pucho c
```

---

### 6. Print (`ghoshna`)
Print values to the console. Use `lagatar` to print without a newline.

```plaintext
ghoshna <expression> [lagatar]
```

Example:
```plaintext
ghoshna "Hello, World!"
ghoshna "*" lagatar
```

---

### 7. Loops (`ginti karo`)
Run a loop using `ginti karo`. Loops require start, end, and optional increment values.

```plaintext
ginti karo <variable> <start> se <end> tak <badhao/ghatao> <increment/decrement value> {
    // Loop body
}
ginti band
```

Example:
```plaintext
ginti karo i 1 se n tak badhao 2 {
    ghoshna i
}
ginti band
```

---

### 8. Conditionals (`agar` and `warna`)
Use `agar` for `if` conditions and `warna` for `else`.

```plaintext
agar <condition> {
    // If block
} warna {
    // Else block
}
```

Example:
```plaintext
agar n barabar hai 10 {
    ghoshna "It's ten!"
} warna {
    ghoshna "Not ten!"
}
```

---

### 9. Arithmetic Operations
Perform arithmetic with keywords.

| **Operator**          | **Meaning**      |
|-----------------------|------------------|
| `me jodo`             | Addition         |
| `se ghatao`           | Subtraction      |
| `me guna karo`        | Multiplication   |
| `ka bhag karo`        | Division         |
| `ka shesh bhag karo`  | Modulus          |

Example:
```plaintext
likho sum 5 me jodo 10
```

---

### 10. File Operations
Perform operations on files.

- **Open a file**:
```plaintext
file kholo "<fileName>" aur naam do <alias>
```

- **Write to a file**:
```plaintext
<alias> me likho <expression>
```

- **Close a file**:
```plaintext
band karo <alias>
```

Example:
```plaintext
file kholo "report.txt" aur naam do report
report me likho "Final salary is: 5000"
band karo report
```

---

## Error Handling

TaiScript provides humorous error messages when things go wrong:
- **Insufficient Bribes**: `"Itne me kya hoga! Thoda aur adjust karo."`
- **Syntax Errors**: `"Unexpected token: '...'."`

---

## Example Program

```plaintext
yojna shuru "PatternPrinter"

parichay "JANTA"

ghoos lo 500
likho n 10
ghoshna "Yaaaaayyyyy"

ghoos lo 1000
ginti karo i 1 se n tak {
    ginti karo j 1 se i tak {
        ghoshna "*" lagatar
    }
    ginti band
    ghoshna ""
}
ginti band

yojna band
```

**Output**:
```plaintext
Yaaaaayyyyy
*
**
***
****
*****
******
*******
********
*********
**********
```

---

## Execution Flow

1. **Lexing**: Converts TaiScript code into tokens.
2. **Parsing**: Generates an Abstract Syntax Tree (AST) from tokens.
3. **Interpreting**: Executes the AST while managing bribes and handling loops, conditionals, etc.

---

## Limitations

- TaiScript is not suitable for large-scale applications.
- Heavy reliance on "bribes" may confuse some users.

---

## Future Improvements

- Better Error Handling
- Add more datatypes (boolean, list/arrays, dictionaries, maps, etc.)
- Add custom data types and functions.
- Built in library supports (Math, String manipulation, File I/O)
- Enhance file operation capabilities.
- Introduce modular programming to include other scripts or programs.
- Build plugin for VSCode, add syntax highlighting and auto completion.
- Add some Easter eggs for fun

---