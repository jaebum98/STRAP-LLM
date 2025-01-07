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
    openai.api_key = " " # input api key

if __name__ == "__main__":
    set_api_key()
    plan = ""
    robot_case1 = open("robot/robot_case1.txt", "r").read()
    robot_case2 = open("robot/robot_case2.txt", "r").read()
    robot_case3 = open("robot/robot_case3.txt", "r").read()

    ##### 1 stage (skill sequence strategy) #####
    stage1_rule = open("prompt/multi_robot_stage1/stage1_rule.txt", "r").read()
    Sample_of_task_decomposition_allocation_plan = open("prompt/multi_robot_stage1/Sample_of_task_decomposition_allocation_plan.txt", "r").read()


## experiment user input ##
    total_test = ["Deliver tray 1 to 8109, tray 8 to 8111, tray 9 to 8222, tray 6 to 8205, tray 2 to 8323, and tray 3 to 8304 , tray 5 to 8101 in that order.",
            "Deliver tray 1 to 8109, tray 3 to 8111, tray 2 to 8101 in that order.",
            "Deliver TV to 8310.",
            "Can you disinfect 8301?",
            "I want to take a picture, can you take a picture and send it to 010-1234-5678?",
            "Can you clean 8202 and deliver Icecream to the same place?",
            "can you guide me to 8333?",
            "Can you patrol to 8222?",
            "Place the laptop on bed.",
            "Slice the lettuce, trash the mug and switch off the light switch",
            "Give me the Harry Potter book from the drawer and patrol to 8101."
    ]
## predicted correct answer
    correct_answer_1 = [
        {"Action json Sequence": [{"robot":"Delivery-Robot-1"},{"skill":"MoveTo","location":"8109"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray1"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"8111"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray8"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"1floorev_front"},{"skill":"PreparetoCallElevator","location":"1floorev_in"},{"skill":"CallElevator","floor":"1","direction":"Up"},{"skill":"CheckinsideElevator"},{"skill":"MoveTo","location":"1floorev_in"},{"skill":"MoveElevator","floor":"2"},{"skill":"MoveTo","location":"8222"},{"skill":"Detect","direction":"right"},{"skill":"MoveRobotArm","item":"tray9"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"8205"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray6"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"2floorev_front"},{"skill":"PreparetoCallElevator","location":"2floorev_in"},{"skill":"CallElevator","floor":"2","direction":"Up"},{"skill":"CheckinsideElevator"},{"skill":"MoveTo","location":"2floorev_in"},{"skill":"MoveElevator","floor":"3"},{"skill":"MoveTo","location":"8323"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray2"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"8304"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray3"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"3floorev_front"},{"skill":"PreparetoCallElevator","location":"3floorev_in"},{"skill":"CallElevator","floor":"3","direction":"Down"},{"skill":"CheckinsideElevator"},{"skill":"MoveTo","location":"3floorev_in"},{"skill":"MoveElevator","floor":"1"},{"skill":"MoveTo","location":"8101"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray5"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"8100"}]},
        {"Action json Sequence": [{"robot":"Delivery-Robot-1"},{"skill":"MoveTo","location":"8109"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray1"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"8111"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray3"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"8101"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray2"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"8100"}]},
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
        {"Action json Sequence": [{"robot":"Delivery-Robot-1"},{"skill":"MoveTo","location":"8109"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray1"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"8111"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray8"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"1floorev_front"},{"skill":"PreparetoCallElevator","location":"1floorev_in"},{"skill":"CallElevator","floor":"1","direction":"Up"},{"skill":"CheckinsideElevator"},{"skill":"MoveTo","location":"1floorev_in"},{"skill":"MoveElevator","floor":"2"},{"skill":"MoveTo","location":"8222"},{"skill":"Detect","direction":"right"},{"skill":"MoveRobotArm","item":"tray9"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"8205"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray6"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"2floorev_front"},{"skill":"PreparetoCallElevator","location":"2floorev_in"},{"skill":"CallElevator","floor":"2","direction":"Up"},{"skill":"CheckinsideElevator"},{"skill":"MoveTo","location":"2floorev_in"},{"skill":"MoveElevator","floor":"3"},{"skill":"MoveTo","location":"8323"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray2"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"8304"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray3"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"3floorev_front"},{"skill":"PreparetoCallElevator","location":"3floorev_in"},{"skill":"CallElevator","floor":"3","direction":"Down"},{"skill":"CheckinsideElevator"},{"skill":"MoveTo","location":"3floorev_in"},{"skill":"MoveElevator","floor":"1"},{"skill":"MoveTo","location":"8101"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray5"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"8100"}]},
        {"Action json Sequence": [{"robot":"Delivery-Robot-1"},{"skill":"MoveTo","location":"8109"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray1"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"8111"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray3"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"8101"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray2"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"8100"}]},
        '',
        {"Action json Sequence": [{"robot":"AID-Robot"},{"skill":"DriveTo","location":"1floorev_front"},{"skill":"PreparetoCallElevator","location":"1floorev_in"},{"skill":"CallElevator","floor":"1","direction":"Up"},{"skill":"CheckinsideElevator"},{"skill":"DriveTo","location":"1floorev_in"},{"skill":"MoveElevator","floor":"3"},{"skill":"DriveTo","location":"8301"},{"skill":"Spray"},{"skill":"DriveTo","location":"3floorev_front"},{"skill":"PreparetoCallElevator","location":"3floorev_in"},{"skill":"CallElevator","floor":"3","direction":"Down"},{"skill":"CheckinsideElevator"},{"skill":"DriveTo","location":"3floorev_in"},{"skill":"MoveElevator","floor":"1"},{"skill":"DriveTo","location":"8100"}]},
        {"Action json Sequence": [{"robot":"Guide-Robot"},{"skill":"VoiceOutput","messages":"I will take a picture in 5 seconds."},{"skill":"TakePicture"},{"skill":"SendPicture","address":"010-1234-5678"},{"skill":"VoiceOutput","messages":"Transmission is complete."}]},
        {"Action json Sequence": [{"robot":"Clean-Robot"},{"skill":"MoveTo","location":"8202"},{"skill":"CleanUp"},{"skill":"MoveTo","location":"8200"},{"robot":"Delivery-Robot-3"},{"skill":"MoveTo","location":"1floorev_front"},{"skill":"PreparetoCallElevator","location":"1floorev_in"},{"skill":"CallElevator","floor":"1","direction":"Up"},{"skill":"CheckinsideElevator"},{"skill":"MoveTo","location":"1floorev_in"},{"skill":"MoveElevator","floor":"2"},{"skill":"MoveTo","location":"8202"}, {"skill":"Detect"},{"skill":"MoveRobotArm","item":"Icecream"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"2floorev_front"},{"skill":"PreparetoCallElevator","location":"2floorev_in"},{"skill":"CallElevator","floor":"2","direction":"Down"},{"skill":"CheckinsideElevator"},{"skill":"MoveTo","location":"2floorev_in"},{"skill":"MoveElevator","floor":"1"},{"skill":"MoveTo","location":"8100"}]},
        '',
        '',
        '',
        '',
        ''
    ]
    correct_answer_3 = [
        {"Action json Sequence": [{"robot":"Delivery-Robot-1"},{"skill":"MoveTo","location":"8109"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray1"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"8111"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray8"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"1floorev_front"},{"skill":"PreparetoCallElevator","location":"1floorev_in"},{"skill":"CallElevator","floor":"1","direction":"Up"},{"skill":"CheckinsideElevator"},{"skill":"MoveTo","location":"1floorev_in"},{"skill":"MoveElevator","floor":"2"},{"skill":"MoveTo","location":"8222"},{"skill":"Detect","direction":"right"},{"skill":"MoveRobotArm","item":"tray9"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"8205"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray6"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"2floorev_front"},{"skill":"PreparetoCallElevator","location":"2floorev_in"},{"skill":"CallElevator","floor":"2","direction":"Up"},{"skill":"CheckinsideElevator"},{"skill":"MoveTo","location":"2floorev_in"},{"skill":"MoveElevator","floor":"3"},{"skill":"MoveTo","location":"8323"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray2"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"8304"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray3"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"3floorev_front"},{"skill":"PreparetoCallElevator","location":"3floorev_in"},{"skill":"CallElevator","floor":"3","direction":"Down"},{"skill":"CheckinsideElevator"},{"skill":"MoveTo","location":"3floorev_in"},{"skill":"MoveElevator","floor":"1"},{"skill":"MoveTo","location":"8101"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray5"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"8100"}]},
        {"Action json Sequence": [{"robot":"Delivery-Robot-1"},{"skill":"MoveTo","location":"8109"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray1"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"8111"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray3"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"8101"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray2"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"8100"}]},
        '',
        {"Action json Sequence": [{"robot":"AID-Robot"},{"skill":"DriveTo","location":"1floorev_front"},{"skill":"PreparetoCallElevator","location":"1floorev_in"},{"skill":"CallElevator","floor":"1","direction":"Up"},{"skill":"CheckinsideElevator"},{"skill":"DriveTo","location":"1floorev_in"},{"skill":"MoveElevator","floor":"3"},{"skill":"DriveTo","location":"8301"},{"skill":"Spray"},{"skill":"DriveTo","location":"3floorev_front"},{"skill":"PreparetoCallElevator","location":"3floorev_in"},{"skill":"CallElevator","floor":"3","direction":"Down"},{"skill":"CheckinsideElevator"},{"skill":"DriveTo","location":"3floorev_in"},{"skill":"MoveElevator","floor":"1"},{"skill":"DriveTo","location":"8100"}]},
        {"Action json Sequence": [{"robot":"Guide-Robot"},{"skill":"VoiceOutput","messages":"I will take a picture in 5 seconds."},{"skill":"TakePicture"},{"skill":"SendPicture","address":"010-1234-5678"},{"skill":"VoiceOutput","messages":"Transmission is complete."}]},
        {"Action json Sequence": [{"robot":"Clean-Robot"},{"skill":"MoveTo","location":"8202"},{"skill":"CleanUp"},{"skill":"MoveTo","location":"8200"},{"robot":"Delivery-Robot-3"},{"skill":"MoveTo","location":"1floorev_front"},{"skill":"PreparetoCallElevator","location":"1floorev_in"},{"skill":"CallElevator","floor":"1","direction":"Up"},{"skill":"CheckinsideElevator"},{"skill":"MoveTo","location":"1floorev_in"},{"skill":"MoveElevator","floor":"2"},{"skill":"MoveTo","location":"8202"}, {"skill":"Detect"},{"skill":"MoveRobotArm","item":"Icecream"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"2floorev_front"},{"skill":"PreparetoCallElevator","location":"2floorev_in"},{"skill":"CallElevator","floor":"2","direction":"Down"},{"skill":"CheckinsideElevator"},{"skill":"MoveTo","location":"2floorev_in"},{"skill":"MoveElevator","floor":"1"},{"skill":"MoveTo","location":"8100"}]},
        '',
        '',
        {"Action json Sequence": [{"robot":"Home-Service-Robot-3"},{"skill":"GoTo","object":"laptop"},{"skill":"Pickup","object":"laptop"},{"skill":"GoTo","object":"bed"},{"skill":"Put","object":"laptop"},{"skill":"ReturnHome"}]},
        {"Action json Sequence": [{"robot":"Home-Service-Robot-1"},{"skill":"GoTo","object":"Lettuce"},{"skill":"Pickup","object":"Lettuce"},{"skill":"GoTo","object":"CounterTop"},{"skill":"Put","object":"Lettuce"},{"skill":"GoTo","object":"Knife"},{"skill":"Pickup","object":"Knife"},{"skill":"GoTo","object":"CounterTop"},{"skill":"Slice","object":"Lettuce"},{"skill":"Put","object":"Knife"},{"skill":"ReturnHome"},{"robot":"Home-Service-Robot-3"},{"skill":"GoTo","object":"Mug"},{"skill":"Pickup","object":"Mug"},{"skill":"GoTo","object":"GarbageCan"},{"skill":"Throw","object":"Mug"},{"skill":"ReturnHome"},{"robot":"Home-Service-Robot-2"},{"skill":"GoTo","object":"LightSwitch"},{"skill":"Switchoff","object":"LightSwitch"},{"skill":"ReturnHome"}]},
        {"Action json Sequence": [{"robot":"Library-Robot"},{"skill":"StartCollabot"},{"skill":"OpenDrawer","book":"Harry Potter"}, {"skill":"ExecuteDrawerDetector"},{"skill":"CloseDrawer"},{"skill":"Reset"},{"robot":"Surveillance-Robot"},{"skill":"StartSurveillance"},{"skill":"Patrol","location":"8101"},{"skill":"DetectThreat"},{"skill":"AlertSecurity"},{"skill" : "ReturnStartLocation"},{"skill":"ResetSystem"}]}
    ]
    task2_answer = [
        {"Action json Sequence": [{"robot":"Delivery-Robot-1"},{"skill":"MoveTo","location":"8109"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray1"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"8111"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray3"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"8101"},{"skill":"Detect","direction":"left"},{"skill":"MoveRobotArm","item":"tray2"},{"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"8100"}]},
        {"Action json Sequence": [{"robot":"Delivery-Robot-2"},{"skill":"MoveTo","location":"8109"},{"skill":"MoveRobotArm","item":"tray1"},{"skill":"MoveTo","location":"8111"},{"skill":"MoveRobotArm","item":"tray3"},{"skill":"MoveTo","location":"8101"},{"skill":"MoveRobotArm","item":"tray2"},{"skill":"MoveTo","location":"8100"}]},
        {"Action json Sequence": [{"robot":"Delivery-Robot-1"},{"skill":"MoveTo","location":"8109"}, {"skill" : "Detect", "direction" : "left"}, {"skill":"MoveRobotArm","item": "tray1"}, {"skill" : "FoldRobotArm"},{"skill":"MoveTo","location":"8100"},{"robot":"Delivery-Robot-2"},{"skill":"MoveTo","location":"8111"}, {"skill":"MoveRobotArm","item": "tray3"},{"skill":"MoveTo","location":"8101"}, {"skill":"MoveRobotArm","item": "tray2"},{"skill":"MoveTo","location":"8100"}]},
        {"Action json Sequence": [{"robot":"Delivery-Robot-1"},{"skill":"MoveTo","location":"8109"}, {"skill":"Detect","direction":"left"}, {"skill":"MoveRobotArm","item":"tray1"}, {"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"8111"}, {"skill":"Detect","direction":"left"}, {"skill":"MoveRobotArm","item":"tray3"}, {"skill":"FoldRobotArm"},{"skill":"MoveTo","location":"8100"},{"robot":"Delivery-Robot-2"},{"skill":"MoveTo","location":"8101"}, {"skill":"MoveRobotArm","item":"tray2"},{"skill":"MoveTo","location":"8100"}]}    
    ]


    
    test = input("select user input for test.(Insert a comma ',' between numbers.) To test all, write 'a'. : ")
    correct_1 = {1 : [-1,-1], 2 : [-1,-1], 3 : [-1,-1], 4: [-1,-1], 5 : [-1,-1], 6 : [-1,-1], 7 : [-1,-1], 8 : [-1,-1], 9 : [-1,-1], 10 : [-1,-1], 11 : [-1,-1], 12 : [-1,-1], 13 : [-1,-1]}
    correct_2 = {1 : [-1,-1], 2 : [-1,-1], 3 : [-1,-1], 4: [-1,-1], 5 : [-1,-1], 6 : [-1,-1], 7 : [-1,-1], 8 : [-1,-1], 9 : [-1,-1], 10 : [-1,-1], 11 : [-1,-1], 12 : [-1,-1], 13 : [-1,-1]}
    correct_3 = {1 : [-1,-1], 2 : [-1,-1], 3 : [-1,-1], 4: [-1,-1], 5 : [-1,-1], 6 : [-1,-1], 7 : [-1,-1], 8 : [-1,-1], 9 : [-1,-1], 10 : [-1,-1], 11 : [-1,-1], 12 : [-1,-1], 13 : [-1,-1]}
    each_correct_1 = {1 : list(), 2 : list(), 3 : list(), 4: list(), 5 : list(), 6 : list(), 7 : list(), 8 : list(), 9 : list(), 10 : list(), 11 : list(), 12 : list(), 13 : list()}
    each_correct_2 = {1 : list(), 2 : list(), 3 : list(), 4: list(), 5 : list(), 6 : list(), 7 : list(), 8 : list(), 9 : list(), 10 : list(), 11 : list(), 12 : list(), 13 : list()}
    each_correct_3 = {1 : list(), 2 : list(), 3 : list(), 4: list(), 5 : list(), 6 : list(), 7 : list(), 8 : list(), 9 : list(), 10 : list(), 11 : list(), 12 : list(), 13 : list()}
    if test == 'a':
        test= list(range(1,len(total_test)+1))
    else:
        test = list(map(int,test.split(',')))
    print(test)
    times = int(input("Specify the number of times to test per task. : "))
    print(times) 
    directory_1 = input("Specify the directory name to save case 1. : ")
    os.mkdir(f"log/{directory_1}")
    directory_2 = input("Specify the directory name to save case 2. : ")
    os.mkdir(f"log/{directory_2}")
    directory_3 = input("Specify the directory name to save case 3. : ")
    os.mkdir(f"log/{directory_3}")

    for k in range(0,1):
        for i in test:
            try_time = 0
            correct_time = 0
            for j in range(0,times):
                print(i,j)
                
                print(total_test[i-1])    
                start = time.process_time()
        
                if k == 0:
                    stage1_prompt = '\n' + robot_case1
                elif k == 1:
                    stage1_prompt = '\n' + robot_case2
                elif k == 2:
                    stage1_prompt = '\n' + robot_case3 
                stage1_prompt += '\n' + stage1_rule
                stage1_prompt += '\n' + Sample_of_task_decomposition_allocation_plan
                stage1_prompt += '\n user input :  ' + total_test[i-1]
                messages = [{"role": "user", "content": stage1_prompt}]
                res, text = LM(messages,"gpt-4o", max_tokens=4000, frequency_penalty=0.0, response_format = "text")
                step1_token = res["usage"]["total_tokens"]
                plan = text  # Save the received result
                print(plan)
                ##### 2 stage (Convert json format) #####
                if "cannot" in plan or "fail" in plan:
                    print("Task performance is impossible.")
                    step2_token = 0
                    jsondata =""
                else:
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
                end = time.process_time()
                runtime = end - start
                now = datetime.now() # current date and time
                date_time = now.strftime("%m-%d-%Y-%H-%M-%S")
                total_token = step1_token + step2_token
                try_time += 1

                if k == 0:
                    if i == 2:
                        second_task = False
                        for a in task2_answer:
                            if a == result:
                                second_task = True    
                                break
                        if second_task == True:
                            correct_time += 1
                            each_correct_1[i].append(1)
                        else:
                            each_correct_1[i].append(0)
                    else:
                        if correct_answer_1[i-1] == result:
                            correct_time += 1
                            each_correct_1[i].append(1)
                        else:
                            each_correct_1[i].append(0)
                    print(each_correct_1)
                    with open(f"log/{directory_1}/test{i}_{j}.txt", 'w') as d:
                        d.write("\ninput = " + total_test[i-1])
                        d.write("\n1step output = " + plan)
                        d.write("\n2step output = " + jsondata)
                        d.write("\nruntime = " + str(runtime))
                        d.write("\ntotal_token = " + str(total_token))
                elif k == 1:
                    if i == 2:
                        second_task = False
                        for a in task2_answer:
                            if a == result:
                                second_task = True    
                                break
                        if second_task == True:
                            correct_time += 1
                            each_correct_2[i].append(1)
                        else:
                            each_correct_2[i].append(0)
                    else:
                        if correct_answer_2[i-1] == result:
                            correct_time += 1
                            each_correct_2[i].append(1)
                        else:
                            each_correct_2[i].append(0)
                    print(each_correct_2)
                    with open(f"log/{directory_2}/test{i}_{j}.txt", 'w') as d:
                        d.write("\ninput = " + total_test[i-1])
                        d.write("\n1step output = " + plan)
                        d.write("\n2step output = " + jsondata)
                        d.write("\nruntime = " + str(runtime))
                        d.write("\ntotal_token = " + str(total_token))
                elif k == 2:
                    if i == 2:
                        second_task = False
                        for a in task2_answer:
                            if a == result:
                                second_task = True    
                                break
                        if second_task == True:
                            correct_time += 1
                            each_correct_3[i].append(1)
                        else:
                            each_correct_3[i].append(0)
                    else:
                        if correct_answer_3[i-1] == result:
                            correct_time += 1
                            each_correct_3[i].append(1)
                        else:
                            each_correct_3[i].append(0)
                    print(each_correct_3)
                    with open(f"log/{directory_3}/test{i}_{j}.txt", 'w') as d:
                        d.write("\ninput = " + total_test[i-1])
                        d.write("\n1step output = " + plan)
                        d.write("\n2step output = " + jsondata)
                        d.write("\nruntime = " + str(runtime))
                        d.write("\ntotal_token = " + str(total_token))
            if k == 0:
                correct_1[i][0] = correct_time
                correct_1[i][1] = try_time
            elif k == 1:
                correct_2[i][0] = correct_time
                correct_2[i][1] = try_time
            elif k == 2:
                correct_3[i][0] = correct_time
                correct_3[i][1] = try_time
    print(correct_1)
    print(each_correct_1)
    print(correct_2)
    print(each_correct_2)
    print(correct_3)
    print(each_correct_3)
