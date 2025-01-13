# Modular Approach to Heterogeneous Robot Information and Efficient Framework for Multi-Robot Task Allocation using Large Language Models

**Intelligent Service Robot Journal**

author : Jaebum Park, and Jun-sik Kim

## Prompt Description

### Robot information
---
#### robot_case1.txt 
: Robots with similar purposes, differing in detailed process and specification

- **Delivery-Robot-1** (Delivery Process, Elevator Process)
- **Delivery-Robot-2** (Delivery Process)
- **Delivery-Robot-3** (Delivery Process, Elevator Process)
---
#### robot_case2.txt 
: Robots offering building-wide services, categorized by scope

- **Delivery-Robot-1** (Delivery Process, Elevator Process)
- **Delivery-Robot-2** (Delivery Process)
- **Delivery-Robot-3** (Delivery Process, Elevator Process)
- **AID-Robot** (Disinfection Process, Elevator Process)
- **Clean-Robot** (Cleaning Process, Elevator Process)
- **Guide-Robot** (Guide Process, Filming Process, Elevator Process)
- **Surveillance-Robot** (Surveillance Process)
---
#### robot_case3.txt 
: All robots, including home and library services, were included

- **Delivery-Robot-1** (Delivery Process, Elevator Process)
- **Delivery-Robot-2** (Delivery Process)
- **Delivery-Robot-3** (Delivery Process, Elevator Process)
- **AID-Robot** (Disinfection Process, Elevator Process)
- **Clean-Robot** (Cleaning Process, Elevator Process)
- **Guide-Robot** (Guide Process, Filming Process, Elevator Process)
- **Surveillance-Robot** (Surveillance Process)
- **Library-Robot** (Drawer Process, Elevator Process)
- **Home-Service-Robot-1** (Slicing Process)
- **Home-Service-Robot-2** (Washing Process, Switching Process)
- **Home-Service-Robot-3** (Throwing Process)
---
#### compare_test_robot.txt 
 : Robots for comparison with SMART-LLM

---
### Stage 1 : Task Decomposition & Allocation
- **Stage1_rule** : Rules are set to prevent LLM from outputting incorrect results during the task decomposition, allocation, and planning processes.
- **Sample_of_task_decomposition_allocation_plan** : Example to fix the form of the process from task decomposition to allocation and planning (one-shot-prompt)
Compare_test_
#### 

### Stage 2 : Robot language (ex.JSON, python function) Format Conversion
- **Stage2_rule** : Rules for converting into a language that robots can understand
- **Sample_of_Robot_language_format_conversion** : Example of languages ​​that robots can understand (one-shot-prompt)
## Exucute Code

**You need to install the openai library before running the code.**

    pip install openai
### Comparison test with other LLMs systems(SMART-LLM)
Run from *Robot-Task-Planning-LLM* file
    
    python3 code/llm_system_compare_test.py

### LLMs system performance test
Run from *Robot-Task-Planning-LLM* file

    python3 code/llm_system.py
