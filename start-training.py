import requests
import random
import subprocess
import timea

API_TOKEN = 'your_groq_ai_token'
API_URL = 'https://api.groq.com/openai/v1/chat/completions'

welcome_messages = [
    "Welcome to the CKAD trainer!",
    "Ready to improve your Kubernetes skills?",
    "Start the test and prove your CKAD expertise!"
]

def generate_welcome_message():
    return random.choice(welcome_messages)

def generate_scenario():
    prompt = """Generate ten interconnected CKAD exam questions in English. For each:
1. Task description starting with "Task: "
2. Validation command starting with "Validation command: "
Separate questions with "---"
Example:
Task: Create a Pod named 'nginx' with image nginx:alpine and label 'app=web'
Validation command: kubectl get pod nginx -o jsonpath='{.metadata.labels.app}' | grep -q web"""

    headers = {'Authorization': f'Bearer {API_TOKEN}', 'Content-Type': 'application/json'}
    data = {
        'model': 'mixtral-8x7b-32768',
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 1000,
        'temperature': 0.5,
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result.get('choices', [{}])[0].get('message', {}).get('content', '')
    except Exception as e:
        print(f"Scenario generation error: {e}")
        return None

def parse_scenario(response):
    if not response:
        return []
    questions = []
    for section in response.split('---'):
        task, validation = None, None
        for line in section.split('\n'):
            if line.startswith('Task:'):
                task = line.replace('Task:', '').strip()
            elif line.startswith('Validation command:'):
                validation = line.replace('Validation command:', '').strip()
        if task and validation:
            questions.append({'task': task, 'validation': validation})
    return questions

def predefined_questions():
    return [
        {"task": "Create a Pod named 'nginx' with image nginx:alpine and label 'app=web'",
         "validation": "kubectl get pod nginx -o jsonpath='{.metadata.labels.app}' | grep -q web"},
        {"task": "Create a Deployment named 'frontend' with 3 replicas and image nginx:1.19",
         "validation": "kubectl get deployment frontend -o jsonpath='{.spec.replicas}' | grep -q 3"},
        {"task": "Expose the Deployment 'frontend' as a NodePort Service on port 80",
         "validation": "kubectl get service frontend -o jsonpath='{.spec.ports[0].port}' | grep -q 80"}
    ]

def validate_solution(validation_command):
    try:
        subprocess.run(validation_command, shell=True, check=True, 
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def generate_hint(task, validation_command):
    prompt = f"""The user failed this CKAD task:
Task: {task}
Validation command: {validation_command}
Generate a helpful hint (in English) explaining the key concept and relevant kubectl commands without revealing the direct solution."""

    headers = {'Authorization': f'Bearer {API_TOKEN}', 'Content-Type': 'application/json'}
    data = {
        'model': 'mixtral-8x7b-32768',
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 150,
        'temperature': 0.3,
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=15)
        result = response.json()
        return result.get('choices', [{}])[0].get('message', {}).get('content', "Hint unavailable.")
    except Exception as e:
        return "Hint unavailable. Check Kubernetes documentation."

def run_scenario(questions):
    for idx, q in enumerate(questions, 1):
        print(f"\n\033[1m*** Question {idx} ***\033[0m")
        print(f"\033[1mTask:\033[0m {q['task']}\n")
        
        attempts = 0
        while True:
            input("Press ENTER when you have completed the task...")
            
            if validate_solution(q['validation']):
                print("\n✅ Correct!")
                break
            else:
                attempts += 1
                print("\n❌ Validation failed. Generating hint...")
                print(f"\033[33m{generate_hint(q['task'], q['validation'])}\033[0m")
                
                if attempts >= 2:
                    print("\n💡 Suggested solution:")
                    print(f"Try: {q['validation']}")

def main():
    print("\033[1m" + generate_welcome_message() + "\033[0m")
    print("\n📌 Open a terminal with kubectl access ready before proceeding.\n")
    print("\n🚀 Preparing CKAD scenario...")
    scenario_raw = generate_scenario()
    
    questions = parse_scenario(scenario_raw) if scenario_raw else []
    
    if len(questions) < 10:
        questions.extend(predefined_questions()[:10 - len(questions)])
    
    input("\nPress ENTER to start the test...")
    
    run_scenario(questions)
    print("\n🎉 Training completed! Verify the created resources using: kubectl get all")

if __name__ == "__main__":
    main()
