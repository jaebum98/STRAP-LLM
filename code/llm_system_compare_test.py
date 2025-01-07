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

    robot = open("robot/compare_test_robot.txt", "r").read()

    ##### 1 stage (skill sequence strategy) #####
    stage1_rule = open("prompt_ct/multi_robot_stage1/Compare_test_stage1_rule.txt", "r").read()
    Sample_of_task_decomposition_allocation_plan = open("prompt_ct/multi_robot_stage1/Compare_test_Sample_of_task_decomposition_allocation_plan.txt", "r").read()

    # nl = "Put apple in fridge and switch off the light" # Existing robot commands
    nl = "Play with the puppy and check its health" # New robot commands
    print(nl)

    start = time.time()
    stage1_prompt = '\n' + robot
    stage1_prompt += '\n' + stage1_rule
    stage1_prompt += '\n' + Sample_of_task_decomposition_allocation_plan
    stage1_prompt += '\n user input :  ' + nl

    messages = [{"role": "user", "content": stage1_prompt}]
    res, text = LM(messages,"gpt-4o-2024-11-20", max_tokens=4000, frequency_penalty=0.0, response_format = "text")
    step1_token = res["usage"]["total_tokens"]
    plan = text  # Save the received result
    print(plan)
    ##### 2 stage (Convert python function format) #####
    if "cannot" in plan or "fail" in plan:
        print("Task performance is impossible.")
        step2_token = 0
        jsondata =""
    else:
        print ("Converting to python function format...")
        stage2_rule = open("prompt_ct/multi_robot_stage2/Compare_test_stage2_rule.txt", "r").read()
        Sample_of_Robot_language_format_conversion = open("prompt_ct/multi_robot_stage2/Compare_test_Sample_of_Robot_language_format_conversion.txt", "r").read()
        stage2_prompt = stage2_rule
        stage2_prompt += '\n' + Sample_of_Robot_language_format_conversion
        stage2_prompt += '\n' + plan
        messages = [{"role": "user", "content": stage2_prompt}]
        res, text = LM(messages,"gpt-4o-2024-11-20", max_tokens=4000, frequency_penalty=0.0, response_format = "text")
        step2_token = res["usage"]["total_tokens"]
        jsondata = text
        print(jsondata)
    
    end = time.time()
    runtime = end - start
    now = datetime.now() # current date and time
    date_time = now.strftime("%m-%d-%Y-%H-%M-%S")
    total_token = step1_token + step2_token
    print("token usage : ",total_token)
    print("execution time : %ds"  %(runtime))