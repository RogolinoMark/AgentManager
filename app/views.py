from django.shortcuts import render
from django.http import JsonResponse
import json
from .Utilities.storage_interface import StorageInterface
from .Utilities.function_utils import Functions
from .Agents.task_creation_agent import TaskCreationAgent
from .Agents.prioritization_agent import PrioritizationAgent
from .Agents.execution_agent import ExecutionAgent

# storage = StorageInterface(False)
# taskCreationAgent = TaskCreationAgent()
# prioritizationAgent = PrioritizationAgent()
# executionAgent = ExecutionAgent()
storage = None
taskCreationAgent = None
prioritizationAgent = None
executionAgent = None

session_mode = "yes"
action_mode = "m"
# Create your views here.
def index(request):
    return render(request, 'index.html')


def session_management(request):
    global storage, taskCreationAgent, prioritizationAgent, executionAgent, session_mode
    if request.method == "POST":
        request_data = request.body.decode("utf-8")
        json_request_data = json.loads(request_data)
        session_mode = json_request_data['session']
        if session_mode == "yes":
            session_mode = False
        else:
            session_mode = True
        storage = StorageInterface(session_mode)
        taskCreationAgent = TaskCreationAgent()
        prioritizationAgent = PrioritizationAgent()
        executionAgent = ExecutionAgent()
        return JsonResponse({"response": session_mode})
    return JsonResponse({"response": "success"})

def mode_management(request):
    global storage, taskCreationAgent, prioritizationAgent, executionAgent, functions, action_mode
    print(taskCreationAgent)

    if request.method == "POST":
        request_data = request.body.decode("utf-8")
        json_request_data = json.loads(request_data)
        action_mode = json_request_data['mode']
        functions = Functions(mode=json_request_data['mode'], session_mode=session_mode)
        taskCreationAgent.run_task_creation_agent()

        # Prioritize task list
        tasklist, result = prioritizationAgent.run_prioritization_agent()
        print("TaskList", tasklist)
        return JsonResponse({"response": result})

    return JsonResponse({"response": "success"})

def feedback_management(request):
    global storage, taskCreationAgent, prioritizationAgent, executionAgent, functions, action_mode
    if request.method == "POST":
        feedback_signal = request.body.decode("utf-8")
        json_request_data = json.loads(feedback_signal)
        action = json_request_data['feedback']
        if action == "yes":
            storage = StorageInterface(session_mode)
            taskCreationAgent = TaskCreationAgent()
            prioritizationAgent = PrioritizationAgent()
            executionAgent = ExecutionAgent()
            functions = Functions(mode=action_mode, session_mode=session_mode)
            taskCreationAgent.run_task_creation_agent()
            tasklist, result = prioritizationAgent.run_prioritization_agent()
            return JsonResponse({"response": result})
        elif action == "automode":
            action_mode = "a"
            return JsonResponse({"response": "success"})
        else:
            storage = StorageInterface(session_mode)
            taskCreationAgent = TaskCreationAgent()
            prioritizationAgent = PrioritizationAgent()
            executionAgent = ExecutionAgent()
            functions = Functions(mode=action_mode, session_mode=session_mode)
            taskCreationAgent.run_task_creation_agent()
            tasklist, result = prioritizationAgent.run_prioritization_agent()
            return JsonResponse({"response": result})

def AddObjective(request):
    if request.method == "POST":
        objective_body = request.body.decode("utf-8")
        json_request_data = json.loads(objective_body)
        objective_str = json_request_data['objective']
        with open('Personas/default.json', 'r') as f:
            data = json.load(f)
        data["Objective"] = objective_str
        print(data)
        with open('Personas/default.json', 'w') as f:
            json.dump(data, f, indent=2)
        with open('app/Agents/Func/Personas/default.json', 'w') as f:
            json.dump(data, f, indent=2)
        with open('app/Agents/Func/Utilities/Personas/default.json', 'w') as f:
            json.dump(data, f, indent=2)
        with open('app/Utilities/Personas/default.json', 'w') as f:
            json.dump(data, f, indent=2)
        return JsonResponse({"response": "success"})

def AddApikey(request):
    global storage, taskCreationAgent, prioritizationAgent, executionAgent, functions, action_mode
    if request.method == "POST":
        objective_body = request.body.decode("utf-8")
        json_request_data = json.loads(objective_body)
        api_key = json_request_data['apikey']
        with open('Config/config.json', 'r') as f:
            config = json.load(f)
        config['openai']['apiKey'] = api_key
        with open('Config/config.json', 'w') as f:
            json.dump(config, f, indent=2)
        storage = StorageInterface(False)
        taskCreationAgent = TaskCreationAgent()
        prioritizationAgent = PrioritizationAgent()
        executionAgent = ExecutionAgent()
        return JsonResponse({"response": "success"})