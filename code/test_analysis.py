import json
import os
import argparse
from pathlib import Path
from datetime import datetime
import time
import sys
sys.path.append('/home/serverpc/.local/lib/python3.8/site-packages')


if __name__ == "__main__":

## 최종 테스트용 user input ##

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

    correct = {1 : [-1,-1], 2 : [-1,-1], 3 : [-1,-1], 4: [-1,-1], 5 : [-1,-1], 6 : [-1,-1], 7 : [-1,-1], 8 : [-1,-1], 9 : [-1,-1], 10 : [-1,-1], 11 : [-1,-1], 12 : [-1,-1], 13 : [-1,-1]}
    each_correct = {1 : list(), 2 : list(), 3 : list(), 4: list(), 5 : list(), 6 : list(), 7 : list(), 8 : list(), 9 : list(), 10 : list(), 11 : list(), 12 : list(), 13 : list()}

    
    for i in range(1,12):
        try_time = 0
        correct_time = 0
        print("test  : " + str(i) + "\n")
        for j in range(0,20):
            with open(f"/home/serverpc/server_backend/robot_taskmanager_llm/log/final_case3_20_1st/test{i}_{j}.txt", "r") as f:
                example = f.read()
                # "2step output = " 이후부터 "runtime"까지 자르기
                start = example.find("2step output = ") + len("2step output = ")
                end = example.find("runtime")
                result = example[start:end].strip()
                jsondata = result
                # print(jsondata)
                
                if jsondata != '':
                    result = json.loads(jsondata)
                else:
                    result = jsondata
                
                try_time += 1
                if i == 2:
                    second_task = False
                    for a in task2_answer:
                        if a == result:
                            second_task = True    
                            break
                    if second_task == True:
                        correct_time += 1
                        each_correct[i].append(1)
                    else:
                        each_correct[i].append(0)
                else:
                    if correct_answer_3[i-1] == result:
                        correct_time += 1
                        each_correct[i].append(1)
                    else:
                        each_correct[i].append(0)
                        print("time : " + str(j))
                
            correct[i][0] = correct_time
            correct[i][1] = try_time
        print(correct)
        print(each_correct)