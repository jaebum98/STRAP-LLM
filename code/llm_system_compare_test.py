import json
import os
import argparse
from pathlib import Path
from datetime import datetime
import time
import sys
sys.path.append(".")
import openai

def LM(prompt, gpt_version, max_tokens=128, temperature=0, stop=None, logprobs=1, frequency_penalty=0, response_format = "text"):
    if response_format == "json_format":
        response = openai.ChatCompletion.create(model=gpt_version,
                                            messages=prompt,
                                            max_tokens=max_tokens,
                                            temperature=temperature,
                                            frequency_penalty = frequency_penalty,
                                            response_format = {"type":"json_object"}
                                            )
        return response, response["choices"][0]["message"]["content"].strip()
    else:
        response = openai.ChatCompletion.create(model=gpt_version,
                                            messages=prompt,
                                            max_tokens=max_tokens,
                                            temperature=temperature,
                                            frequency_penalty = frequency_penalty,
                                            )
        return response, response["choices"][0]["message"]["content"].strip()

def set_api_key():
    openai.api_key = "" # input api key


def evaluate_result(command_num, result, correct_answers, each_correct, correct_time,
                    directory, total_command, plan, pythondata, runtime, total_token, trial_num):

    if correct_answers[command_num] == result:
        correct_time += 1
        each_correct[command_num+1].append(1)
    else:
        each_correct[command_num+1].append(0)

    print(each_correct)

    # 결과 로그 저장
    log_path = f"log/{directory}/test{command_num}_{trial_num}.txt"
    with open(log_path, 'w') as d:
        d.write("\ninput = " + total_command[command_num-1])
        d.write("\n1step output = " + plan)
        d.write("\n2step output = " + pythondata)
        d.write("\nruntime = " + str(runtime))
        d.write("\ntotal_token = " + str(total_token))

    return correct_time

if __name__ == "__main__":
    set_api_key()
    plan = ""

    robot = open("robot/compare_test_robot.txt", "r").read()
    robot_include_new_robot = open("robot/compare_test_robot_include_new_robot.txt", "r").read()
    ##### 1 stage (skill sequence strategy) #####
    # 이전 방법
    # stage1_rule = open("prompt_ct/multi_robot_stage1/Compare_test_stage1_rule.txt", "r").read()
    # Sample_of_task_decomposition_allocation_plan = open("prompt_ct/multi_robot_stage1/Compare_test_Sample_of_task_decomposition_allocation_plan.txt", "r").read()
    # 새로운 방법
    stage1_rule = open("prompt/multi_robot_stage1/stage1_rule.txt", "r").read()
    Sample_of_task_decomposition_allocation_plan = open("prompt/multi_robot_stage1/Sample_of_task_decomposition_allocation_plan.txt", "r").read()

    total_command = ["Put apple in fridge and switch off the light", # Existing robot commands
                     "Play with the puppy and check its health"]

    correct_answer_1 = [
        {"Action json Sequence": [{"robot":"Delivery-Robot-1"},{"skill":"MoveTo","location":"Meeting Room1"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray1"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"Meeting Room3"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray8"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"1floorev_front"},{"skill":"CallElevator","floor":"1","direction":"Up"},{"skill":"CheckinsideElevator"},{"skill":"MoveTo","location":"1floorev_in"},{"skill":"MoveElevator","floor":"2"},{"skill":"MoveTo","location":"Laboratory2"},{"skill":"Detect","direction":"right"},{"skill":"MoveRobotArm","item":"tray9"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"Restroom2"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray6"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"2floorev_front"},{"skill":"CallElevator","floor":"2","direction":"Up"},{"skill":"CheckinsideElevator"},{"skill":"MoveTo","location":"2floorev_in"},{"skill":"MoveElevator","floor":"3"},{"skill":"MoveTo","location":"Toilet3"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray2"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"Office"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray3"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"3floorev_front"},{"skill":"CallElevator","floor":"3","direction":"Down"},{"skill":"CheckinsideElevator"},{"skill":"MoveTo","location":"3floorev_in"},{"skill":"MoveElevator","floor":"1"},{"skill":"MoveTo","location":"Meeting Room2"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray5"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"Main Hall"}]},
        ''
    ]
    correct_answer_2 = [
        {"Action json Sequence": [{"robot":"Delivery-Robot-1"},{"skill":"MoveTo","location":"Meeting Room1"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray1"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"Meeting Room3"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray8"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"1floorev_front"},{"skill":"CallElevator","floor":"1","direction":"Up"},{"skill":"CheckinsideElevator"},{"skill":"MoveTo","location":"1floorev_in"},{"skill":"MoveElevator","floor":"2"},{"skill":"MoveTo","location":"Laboratory2"},{"skill":"Detect","direction":"right"},{"skill":"MoveRobotArm","item":"tray9"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"Restroom2"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray6"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"2floorev_front"},{"skill":"CallElevator","floor":"2","direction":"Up"},{"skill":"CheckinsideElevator"},{"skill":"MoveTo","location":"2floorev_in"},{"skill":"MoveElevator","floor":"3"},{"skill":"MoveTo","location":"Toilet3"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray2"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"Office"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray3"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"3floorev_front"},{"skill":"CallElevator","floor":"3","direction":"Down"},{"skill":"CheckinsideElevator"},{"skill":"MoveTo","location":"3floorev_in"},{"skill":"MoveElevator","floor":"1"},{"skill":"MoveTo","location":"Meeting Room2"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray5"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"Main Hall"}]},
        ''
    ]
    directory = ["compare_test_scenario1_1st",
                 "compare_test_scenario2_1st"]
    correct_1 = {1 : [-1,-1,-1,-1], 2 : [-1,-1,-1,-1]}
    correct_2 = {1 : [-1,-1,-1,-1], 2 : [-1,-1,-1,-1]}
    each_correct_1 = {1 : list(), 2 : list()}
    each_correct_2 = {1 : list(), 2 : list()}
    
    trials = int(input("Specify the number of trials to test per task. : "))
    print(trials) 

    for scenario in range(0,2):
        for command_num in range(0,2):
            try_time = 0
            correct_time = 0
            process_time_entire = 0
            token_usage_entire = 0
            for trial_num in range(0,trials):
                start = time.time()
                if scenario == 0:
                    stage1_prompt = '\n' + robot
                elif scenario == 1:
                    stage1_prompt = '\n' + robot_include_new_robot
                stage1_prompt += '\n' + stage1_rule
                stage1_prompt += '\n' + Sample_of_task_decomposition_allocation_plan
                stage1_prompt += '\n user input :  ' + total_command[command_num]
                print(total_command[command_num])
                messages = [{"role": "user", "content": stage1_prompt}]
                res, text = LM(messages,"gpt-4o-2024-11-20", max_tokens=4000, frequency_penalty=0.0, response_format = "text")
                step1_token = res["usage"]["total_tokens"]
                plan = text  # Save the received result
                print(plan)
                ##### 2 stage (Convert python function format) #####
                if "CANNOT" in plan or "fail" in plan:
                    print("Task performance is impossible.")
                    step2_token = 0
                    pydata =""
                else:
                    print ("Converting to python function format...")
                    # 가존 거
                    # stage2_rule = open("prompt_ct/multi_robot_stage2/Compare_test_stage2_rule.txt", "r").read()
                    # Sample_of_Robot_language_format_conversion = open("prompt_ct/multi_robot_stage2/Compare_test_Sample_of_Robot_language_format_conversion.txt", "r").read()
                    # 새로운 거
                    stage2_rule = open("prompt/multi_robot_stage2/stage2_rule_python_test.txt", "r").read()
                    Sample_of_Robot_language_format_conversion = open("prompt/multi_robot_stage2/Sample_of_Robot_language_format_conversion_python_test.txt", "r").read()
                    stage2_prompt = stage2_rule
                    stage2_prompt += '\n' + Sample_of_Robot_language_format_conversion
                    stage2_prompt += '\n' + plan
                    messages = [{"role": "user", "content": stage2_prompt}]
                    res, text = LM(messages,"gpt-4o-2024-11-20", max_tokens=4000, frequency_penalty=0.0, response_format = "text")
                    step2_token = res["usage"]["total_tokens"]
                    pydata = text
                    print(pydata)

                end = time.time()
                runtime = end - start
                now = datetime.now() # current date and time
                date_time = now.strftime("%m-%d-%Y-%H-%M-%S")
                total_token = step1_token + step2_token
                try_time += 1
                print("token usage : ",total_token)
                print("execution time : %ds"  %(runtime))
                process_time_entire += runtime
                token_usage_entire += total_token
    #             if scenario == 0:
    #                 correct_time = evaluate_result(command_num, pydata, correct_answer_1, each_correct_1, correct_time, directory[scenario], total_command, plan, pydata, runtime, total_token, trial_num)
    #             elif scenario == 1:
    #                 correct_time = evaluate_result(command_num, pydata, correct_answer_2, each_correct_2, correct_time, directory[scenario], total_command, plan, pydata, runtime, total_token, trial_num)
    #         if scenario == 0:
    #             correct_1[command_num+1][0] = correct_time
    #             correct_1[command_num+1][1] = try_time
    #             correct_1[command_num+1][2] = process_time_entire / trials
    #             correct_1[command_num+1][3] = token_usage_entire / trials
    #         elif scenario == 1:
    #             correct_2[command_num+1][0] = correct_time
    #             correct_2[command_num+1][1] = try_time
    #             correct_2[command_num+1][2] = process_time_entire / trials
    #             correct_2[command_num+1][3] = token_usage_entire / trials
    # print(correct_1)
    # print(each_correct_1)
    # print(correct_2)
    # print(each_correct_2)