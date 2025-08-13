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


def evaluate_result(command_num, result, correct_answers, each_correct, correct_time,
                    directory, total_command, plan, jsondata, runtime, total_token, trial_num):

    if correct_answers[command_num-1] == result:
        correct_time += 1
        each_correct[command_num].append(1)
    else:
        if result == {"Action json Sequence": []}:
            correct_time += 1
            each_correct[command_num].append(1)
        else:
            each_correct[command_num].append(0)

    print(each_correct)

    # 결과 로그 저장
    log_path = f"log/{directory}/test{command_num}_{trial_num}.txt"
    with open(log_path, 'w') as d:
        d.write("\ninput = " + total_command[command_num-1])
        d.write("\n1step output = " + plan)
        d.write("\n2step output = " + jsondata)
        d.write("\nruntime = " + str(runtime))
        d.write("\ntotal_token = " + str(total_token))

    return correct_time

def set_api_key():
    openai.api_key = "" # input api key

if __name__ == "__main__":
    set_api_key()
    plan = ""
    robot_case1 = open("robot/robot_case1.txt", "r").read()
    robot_case2 = open("robot/robot_case2.txt", "r").read()
    robot_case3 = open("robot/robot_case3.txt", "r").read()

    ##### 1 stage (skill sequence strategy) #####
    stage1_rule = open("prompt/multi_robot_stage1/stage1_rule.txt", "r").read()
    stage1_rule_no_strict = open("prompt/multi_robot_stage1/stage1_rule_no_strict.txt", "r").read()
    Sample_of_task_decomposition_allocation_plan = open("prompt/multi_robot_stage1/Sample_of_task_decomposition_allocation_plan.txt", "r").read()


## experiment user input ##
    total_command = ["Deliver tray 1 to Meeting Room1, tray 8 to Meeting Room3, tray 9 to Laboratory2, tray 6 to Restroom2, tray 2 to Toilet3, and tray 3 to Office , tray 5 to Meeting Room2 in that order.",
            "Send tray 1 to Dining Room, tray 3 to Bedroom, tray 2 to Laundry room in that order.",
            "Deliver TV to Office.",
            "Can you disinfect Toilet3?",
            "I want to take a picture, can you take a picture and send it to 010-1234-5678?",
            "Can you clean Restroom2 and bring Icecream to the same place?",
            "Can you guide me to Classroom?",
            "Can you patrol to Restricted Area?",
            "Place the laptop on bed.",
            "Slice the lettuce, trash the mug and switch off the light switch",
            "Give me the Harry Potter book from the drawer and patrol to Storage Room."
    ]
## predicted correct answer
    correct_answer_1 = [
        {"Action json Sequence": [{"robot":"Delivery-Robot-1"},{"skill":"MoveTo","location":"Meeting Room1"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray1"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"Meeting Room3"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray8"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"1floorev_front"},{"skill":"CallElevator","floor":"1","direction":"Up"},{"skill":"CheckinsideElevator"},{"skill":"MoveTo","location":"1floorev_in"},{"skill":"MoveElevator","floor":"2"},{"skill":"MoveTo","location":"Laboratory2"},{"skill":"Detect","direction":"right"},{"skill":"MoveRobotArm","item":"tray9"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"Restroom2"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray6"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"2floorev_front"},{"skill":"CallElevator","floor":"2","direction":"Up"},{"skill":"CheckinsideElevator"},{"skill":"MoveTo","location":"2floorev_in"},{"skill":"MoveElevator","floor":"3"},{"skill":"MoveTo","location":"Toilet3"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray2"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"Office"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray3"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"3floorev_front"},{"skill":"CallElevator","floor":"3","direction":"Down"},{"skill":"CheckinsideElevator"},{"skill":"MoveTo","location":"3floorev_in"},{"skill":"MoveElevator","floor":"1"},{"skill":"MoveTo","location":"Meeting Room2"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray5"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"Main Hall"}]},
        {"Action json Sequence": [{"robot":"Delivery-Robot-2"},{"skill":"MoveTo","location":"Dining Room"},{"skill":"MoveRobotArm","item":"tray1"},{"skill":"MoveTo","location":"Bedroom"},{"skill":"MoveRobotArm","item":"tray3"},{"skill":"MoveTo","location":"Laundry room"},{"skill":"MoveRobotArm","item":"tray2"},{"skill":"MoveTo","location":"Living Room"}]},
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        ''
    ]
    correct_answer_2 = [
        {"Action json Sequence": [{"robot":"Delivery-Robot-1"},{"skill":"MoveTo","location":"Meeting Room1"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray1"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"Meeting Room3"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray8"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"1floorev_front"},{"skill":"CallElevator","floor":"1","direction":"Up"},{"skill":"CheckinsideElevator"},{"skill":"MoveTo","location":"1floorev_in"},{"skill":"MoveElevator","floor":"2"},{"skill":"MoveTo","location":"Laboratory2"},{"skill":"Detect","direction":"right"},{"skill":"MoveRobotArm","item":"tray9"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"Restroom2"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray6"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"2floorev_front"},{"skill":"CallElevator","floor":"2","direction":"Up"},{"skill":"CheckinsideElevator"},{"skill":"MoveTo","location":"2floorev_in"},{"skill":"MoveElevator","floor":"3"},{"skill":"MoveTo","location":"Toilet3"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray2"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"Office"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray3"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"3floorev_front"},{"skill":"CallElevator","floor":"3","direction":"Down"},{"skill":"CheckinsideElevator"},{"skill":"MoveTo","location":"3floorev_in"},{"skill":"MoveElevator","floor":"1"},{"skill":"MoveTo","location":"Meeting Room2"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray5"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"Main Hall"}]},
        {"Action json Sequence": [{"robot":"Delivery-Robot-2"},{"skill":"MoveTo","location":"Dining Room"},{"skill":"MoveRobotArm","item":"tray1"},{"skill":"MoveTo","location":"Bedroom"},{"skill":"MoveRobotArm","item":"tray3"},{"skill":"MoveTo","location":"Laundry room"},{"skill":"MoveRobotArm","item":"tray2"},{"skill":"MoveTo","location":"Living Room"}]},
        '',
        {"Action json Sequence": [{"robot":"AID-Robot"},{"skill":"DriveTo","location":"1floorev_front"},{"skill":"CallElevator","floor":"1","direction":"Up"},{"skill":"CheckinsideElevator"},{"skill":"DriveTo","location":"1floorev_in"},{"skill":"MoveElevator","floor":"3"},{"skill":"DriveTo","location":"Toilet3"},{"skill":"Spray"},{"skill":"DriveTo","location":"3floorev_front"},{"skill":"CallElevator","floor":"3","direction":"Down"},{"skill":"CheckinsideElevator"},{"skill":"DriveTo","location":"3floorev_in"},{"skill":"MoveElevator","floor":"1"},{"skill":"DriveTo","location":"Main Hall"}]},
        {"Action json Sequence": [{"robot":"Guide-Robot"},{"skill":"VoiceOutput","messages":"I will take a picture in 5 seconds."},{"skill":"TakePicture"},{"skill":"SendPicture","address":"010-1234-5678"},{"skill":"VoiceOutput","messages":"Transmission is complete."}]},
        {"Action json Sequence": [{"robot":"Clean-Robot"},{"skill":"MoveTo","location":"Restroom2"},{"skill":"CleanUp"},{"skill":"MoveTo","location":"Storage Room"},{"robot":"Delivery-Robot-3"},{"skill":"MoveTo","location":"1floorev_front"},{"skill":"CallElevator","floor":"1","direction":"Up"},{"skill":"CheckinsideElevator"},{"skill":"MoveTo","location":"1floorev_in"},{"skill":"MoveElevator","floor":"2"},{"skill":"MoveTo","location":"Restroom2"},{"skill":"Detect"},{"skill":"MoveRobotArm","item":"Icecream"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"2floorev_front"},{"skill":"CallElevator","floor":"2","direction":"Down"},{"skill":"CheckinsideElevator"},{"skill":"MoveTo","location":"2floorev_in"},{"skill":"MoveElevator","floor":"1"},{"skill":"MoveTo","location":"Main Hall"}]},
        '',
        '',
        '',
        '',
        ''
    ]
    correct_answer_3 = [
        {"Action json Sequence": [{"robot":"Delivery-Robot-1"},{"skill":"MoveTo","location":"Meeting Room1"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray1"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"Meeting Room3"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray8"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"1floorev_front"},{"skill":"CallElevator","floor":"1","direction":"Up"},{"skill":"CheckinsideElevator"},{"skill":"MoveTo","location":"1floorev_in"},{"skill":"MoveElevator","floor":"2"},{"skill":"MoveTo","location":"Laboratory2"},{"skill":"Detect","direction":"right"},{"skill":"MoveRobotArm","item":"tray9"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"Restroom2"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray6"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"2floorev_front"},{"skill":"CallElevator","floor":"2","direction":"Up"},{"skill":"CheckinsideElevator"},{"skill":"MoveTo","location":"2floorev_in"},{"skill":"MoveElevator","floor":"3"},{"skill":"MoveTo","location":"Toilet3"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray2"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"Office"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray3"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"3floorev_front"},{"skill":"CallElevator","floor":"3","direction":"Down"},{"skill":"CheckinsideElevator"},{"skill":"MoveTo","location":"3floorev_in"},{"skill":"MoveElevator","floor":"1"},{"skill":"MoveTo","location":"Meeting Room2"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray5"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"Main Hall"}]},
        {"Action json Sequence": [{"robot":"Delivery-Robot-2"},{"skill":"MoveTo","location":"Dining Room"},{"skill":"MoveRobotArm","item":"tray1"},{"skill":"MoveTo","location":"Bedroom"},{"skill":"MoveRobotArm","item":"tray3"},{"skill":"MoveTo","location":"Laundry room"},{"skill":"MoveRobotArm","item":"tray2"},{"skill":"MoveTo","location":"Living Room"}]},
        '',
        {"Action json Sequence": [{"robot":"AID-Robot"},{"skill":"DriveTo","location":"1floorev_front"},{"skill":"CallElevator","floor":"1","direction":"Up"},{"skill":"CheckinsideElevator"},{"skill":"DriveTo","location":"1floorev_in"},{"skill":"MoveElevator","floor":"3"},{"skill":"DriveTo","location":"Toilet3"},{"skill":"Spray"},{"skill":"DriveTo","location":"3floorev_front"},{"skill":"CallElevator","floor":"3","direction":"Down"},{"skill":"CheckinsideElevator"},{"skill":"DriveTo","location":"3floorev_in"},{"skill":"MoveElevator","floor":"1"},{"skill":"DriveTo","location":"Main Hall"}]},
        {"Action json Sequence": [{"robot":"Guide-Robot"},{"skill":"VoiceOutput","messages":"I will take a picture in 5 seconds."},{"skill":"TakePicture"},{"skill":"SendPicture","address":"010-1234-5678"},{"skill":"VoiceOutput","messages":"Transmission is complete."}]},
        {"Action json Sequence": [{"robot":"Clean-Robot"},{"skill":"MoveTo","location":"Restroom2"},{"skill":"CleanUp"},{"skill":"MoveTo","location":"Storage Room"},{"robot":"Delivery-Robot-3"},{"skill":"MoveTo","location":"1floorev_front"},{"skill":"CallElevator","floor":"1","direction":"Up"},{"skill":"CheckinsideElevator"},{"skill":"MoveTo","location":"1floorev_in"},{"skill":"MoveElevator","floor":"2"},{"skill":"MoveTo","location":"Restroom2"},{"skill":"Detect"},{"skill":"MoveRobotArm","item":"Icecream"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"2floorev_front"},{"skill":"CallElevator","floor":"2","direction":"Down"},{"skill":"CheckinsideElevator"},{"skill":"MoveTo","location":"2floorev_in"},{"skill":"MoveElevator","floor":"1"},{"skill":"MoveTo","location":"Main Hall"}]},
        '',
        '',
        {"Action json Sequence": [{"robot":"Home-Service-Robot-1"},{"skill":"GoTo","object":"laptop"},{"skill":"Pickup","object":"laptop"},{"skill":"GoTo","object":"bed"},{"skill":"Put","object":"laptop"},{"skill":"ReturnHome"}]},
        {"Action json Sequence": [{"robot":"Home-Service-Robot-1"},{"skill":"GoTo","object":"Lettuce"},{"skill":"Pickup","object":"Lettuce"},{"skill":"GoTo","object":"CounterTop"},{"skill":"Put","object":"Lettuce"},{"skill":"GoTo","object":"Knife"},{"skill":"Pickup","object":"Knife"},{"skill":"GoTo","object":"CounterTop"},{"skill":"Slice","object":"Lettuce"},{"skill":"Put","object":"Knife"},{"skill":"ReturnHome"},{"robot":"Home-Service-Robot-3"},{"skill":"GoTo","object":"Mug"},{"skill":"Pickup","object":"Mug"},{"skill":"GoTo","object":"GarbageCan"},{"skill":"Throw","object":"Mug"},{"skill":"ReturnHome"},{"robot":"Home-Service-Robot-2"},{"skill":"GoTo","object":"LightSwitch"},{"skill":"Switchoff","object":"LightSwitch"},{"skill":"ReturnHome"}]},
        {"Action json Sequence": [{"robot":"Library-Robot"},{"skill":"StartCollabot"},{"skill":"OpenDrawer","book":"Harry Potter"}, {"skill":"ExecuteDrawerDetector"},{"skill":"CloseDrawer"},{"skill":"Reset"},{"robot":"Surveillance-Robot"},{"skill":"StartSurveillance"},{"skill":"Patrol","location":"Storage Room"},{"skill":"DetectThreat"},{"skill":"AlertSecurity"},{"skill":"ReturnStartLocation"},{"skill":"ResetSystem"}]}
    ]
    output_format = input("Choose the output of the robot you want. (To use Python, write 'p', and to use JsonFormat, write 'j') : ")
    test = input("select user input for test.(Insert a comma ',' between numbers.) To test all, write 'a'. : ")
    correct_1 = {1 : [-1,-1], 2 : [-1,-1], 3 : [-1,-1], 4: [-1,-1], 5 : [-1,-1], 6 : [-1,-1], 7 : [-1,-1], 8 : [-1,-1], 9 : [-1,-1], 10 : [-1,-1], 11 : [-1,-1]}
    correct_2 = {1 : [-1,-1], 2 : [-1,-1], 3 : [-1,-1], 4: [-1,-1], 5 : [-1,-1], 6 : [-1,-1], 7 : [-1,-1], 8 : [-1,-1], 9 : [-1,-1], 10 : [-1,-1], 11 : [-1,-1]}
    correct_3 = {1 : [-1,-1], 2 : [-1,-1], 3 : [-1,-1], 4: [-1,-1], 5 : [-1,-1], 6 : [-1,-1], 7 : [-1,-1], 8 : [-1,-1], 9 : [-1,-1], 10 : [-1,-1], 11 : [-1,-1]}
    each_correct_1 = {1 : list(), 2 : list(), 3 : list(), 4: list(), 5 : list(), 6 : list(), 7 : list(), 8 : list(), 9 : list(), 10 : list(), 11 : list()}
    each_correct_2 = {1 : list(), 2 : list(), 3 : list(), 4: list(), 5 : list(), 6 : list(), 7 : list(), 8 : list(), 9 : list(), 10 : list(), 11 : list()}
    each_correct_3 = {1 : list(), 2 : list(), 3 : list(), 4: list(), 5 : list(), 6 : list(), 7 : list(), 8 : list(), 9 : list(), 10 : list(), 11 : list()}
    if test == 'a':
        command = list(range(1,len(total_command)+1))
    else:
        command = list(map(int,test.split(',')))
    print(test)
    trials = int(input("Specify the number of trials to test per task. : "))
    print(trials) 
    directory_1 = input("Specify the directory name to save case 1. : ")
    os.mkdir(f"log/{directory_1}")
    directory_2 = input("Specify the directory name to save case 2. : ")
    os.mkdir(f"log/{directory_2}")
    directory_3 = input("Specify the directory name to save case 3. : ")
    os.mkdir(f"log/{directory_3}")

    for scenario in range(2,3):
        for command_num in command:
            try_time = 0
            correct_time = 0
            for trial_num in range(0,trials):
                print(command_num,trial_num)
                
                print(total_command[command_num-1])    
                start = time.process_time()
        
                if scenario == 0:
                    stage1_prompt = '\n' + robot_case1
                elif scenario == 1:
                    stage1_prompt = '\n' + robot_case2
                elif scenario == 2:
                    stage1_prompt = '\n' + robot_case3 
                stage1_prompt += '\n' + stage1_rule # ablation study 시에 주석
                # stage1_prompt += '\n' + stage1_rule_no_strict # ablation study 시에 주석 풀기
                stage1_prompt += '\n' + Sample_of_task_decomposition_allocation_plan
                stage1_prompt += '\n user input :  ' + total_command[command_num-1]
                messages = [{"role": "user", "content": stage1_prompt}]
                res, text = LM(messages,"gpt-4o", max_tokens=4000, frequency_penalty=0.0, response_format = "text")
                step1_token = res["usage"]["total_tokens"]
                plan = text  # Save the received result
                print(plan)
                ##### 2 stage (Convert json format) #####
                if "CANNOT" in plan or "fail" in plan:
                    print("Task performance is impossible.")
                    step2_token = 0
                    jsondata =""
                else:
                    if output_format == 'j':
                        print ("Converting to json format...")
                        stage2_rule = open("prompt/multi_robot_stage2/stage2_rule.txt", "r").read()
                        Sample_of_Robot_language_format_conversion = open("prompt/multi_robot_stage2/Sample_of_Robot_language_format_conversion.txt", "r").read()
                        stage2_prompt = stage2_rule
                        stage2_prompt += '\n' + Sample_of_Robot_language_format_conversion
                        stage2_prompt += '\n' + plan
                        messages = [{"role": "user", "content": stage2_prompt}]
                        res, text = LM(messages,"gpt-4o-2024-11-20", max_tokens=4000, frequency_penalty=0.0, response_format = "json_format")
                        step2_token = res["usage"]["total_tokens"]
                        jsondata = text
                        print(jsondata)
                    
                        if jsondata != '':
                            result = json.loads(jsondata)
                        else:
                            result = jsondata
                    elif output_format == 'p':
                        print ("Converting to python format...")
                        stage2_rule = open("prompt/multi_robot_stage2/stage2_rule_python_test.txt", "r").read()
                        Sample_of_Robot_language_format_conversion = open("prompt/multi_robot_stage2/Sample_of_Robot_language_format_conversion_python_test.txt", "r").read()
                        stage2_prompt = stage2_rule
                        stage2_prompt += '\n' + Sample_of_Robot_language_format_conversion
                        stage2_prompt += '\n' + plan
                        messages = [{"role": "user", "content": stage2_prompt}]
                        res, text = LM(messages,"gpt-4o-2024-11-20", max_tokens=4000, frequency_penalty=0.0, response_format = "text")
                        step2_token = res["usage"]["total_tokens"]
                        result = text
                        print(result)
                

                end = time.process_time()
                runtime = end - start
                now = datetime.now() # current date and time
                date_time = now.strftime("%m-%d-%Y-%H-%M-%S")
                total_token = step1_token + step2_token
                try_time += 1

                if scenario == 0:
                    correct_time = evaluate_result(command_num, result, correct_answer_1, each_correct_1, correct_time, "ablation_study_sc1_10_2nd", total_command, plan, jsondata, runtime, total_token, trial_num)
                elif scenario == 1:
                    correct_time = evaluate_result(command_num, result, correct_answer_2, each_correct_2, correct_time, "ablation_study_sc2_10_2nd", total_command, plan, jsondata, runtime, total_token, trial_num)
                elif scenario == 2:
                    correct_time = evaluate_result(command_num, result, correct_answer_3, each_correct_3, correct_time, "ablation_study_sc3_10_2nd", total_command, plan, jsondata, runtime, total_token, trial_num)
            if scenario == 0:
                correct_1[command_num][0] = correct_time
                correct_1[command_num][1] = try_time
            elif scenario == 1:
                correct_2[command_num][0] = correct_time
                correct_2[command_num][1] = try_time
            elif scenario == 2:
                correct_3[command_num][0] = correct_time
                correct_3[command_num][1] = try_time
    print(correct_1)
    print(each_correct_1)
    print(correct_2)
    print(each_correct_2)
    print(correct_3)
    print(each_correct_3)

