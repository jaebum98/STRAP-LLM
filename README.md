# STRAP-LLM: Structured Task Allocation and Planning for Heterogeneous Robots using Large Language Models

**Intelligent Service Robot Journal**

author : Jaebum Park, and Jun-sik Kim (corresponding author)

## Structured Modules of Robot information

### Experiment for Planning Accuracy (1st Experiment)

#### robot_case1.txt 
: Robots that have the same delivery task, but with different elevator process, usable objects and places

- **Delivery-Robot-1** (Delivery Process, Elevator Process)
- **Delivery-Robot-2** (Delivery Process)
- **Delivery-Robot-3** (Delivery Process, Elevator Process)

#### robot_case2.txt 
: Robots that have various tasks different from delivery task

- **Delivery-Robot-1** (Delivery Process, Elevator Process)
- **Delivery-Robot-2** (Delivery Process)
- **Delivery-Robot-3** (Delivery Process, Elevator Process)
- **AID-Robot** (Disinfection Process, Elevator Process)
- **Clean-Robot** (Cleaning Process, Elevator Process)
- **Guide-Robot** (Guide Process, Filming Process, Elevator Process)
- **Surveillance-Robot** (Surveillance Process)

#### robot_case3.txt 
: Robots that operate in a different space from the previous cases

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
### Comparison experiment to SOTA Method (2nd Experiment)

#### compare_test_robot.txt 
 : Robots introduced in SMART-LLM

- **robot1** (Pick or Put Process, Slicing Process, Throwing Process, Break Process)
- **robot2** (Switch Process, Slicing Process, Throwing Process, Break Process)
- **robot3** (Switch Process, Pick or Put Process, Throwing Process, Break Process)
- **robot4** (Switch Process, Pick or Put Process, Slicing Process, Break Process)
- **robot5** (Switch Process, Pick or Put Process, Slicing Process, Throwing Process, Break Process)
- **robot6** (Open or Close Process, Slicing Process, Throwing Process, Break Process)
- **robot7** (Open or Close Process, Pick or Put Process, Throwing Process, Break Process)
- **robot8** (Open or Close Process, Pick or Put Process, Slicing Process, Throwing Process)
- **robot9** (Open or Close Process, Pick or Put Process, Slicing Process, Throwing Process, Break Process)
- **robot10** (Open or Close Process, Switch Process, Throwing Process, Break Process)
- **robot11** (Open or Close Process, Switch Process, Slicing Process, Break Process)
- **robot12** (Open or Close Process, Switch Process, Slicing Process, Throwing Process, Break Process)
- **robot13** (Open or Close Process)
- **robot14** (Switch Process)
- **robot15** (Pick or Put Process)
- **robot16** (Slicing Process)
- **robot17** (Throwing Process, Break Process)

: A new heterogeneous robot

- **PetCare-Robot** (Playing Process, Cleaning Process, Health Monitoring Process)

---
## System Structure (2 stages)

### Stage 1 : Task & Skill Reasoning
- **Stage1_rule** : Rules are set to prevent LLM from outputting incorrect results during the task decomposition, allocation, and planning processes.
- **Sample_of_task_decomposition_allocation_plan** : Example of chain-of-thought the process from task decomposition to allocation and planning (one-shot-prompt)
#### 

### Stage 2 : Language (ex.JSON, python function) Translation
- **Stage2_rule** : Rules for converting into a language that robots can understand
- **Sample_of_Robot_language_format_conversion** : Example of languages ​​that robots can understand (one-shot-prompt)
## Exucute Code

**You need to install the openai library before running the code.**

    pip install openai


### Experiment for Planning Accuracy test
Run from *STRAP-LLM* file

    python3 code/llm_system.py


### Comparison experiment to SOTA Method(SMART-LLM) test
Run from *STRAP-LLM* file
    
    python3 code/llm_system_compare_test.py