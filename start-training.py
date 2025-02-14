import requests
import random
import subprocess
import time

API_TOKEN = 'your-api-token'
API_URL = 'https://api.groq.com/openai/v1/chat/completions'

domain_topics = [
    "Application Design and Build",
    "Application Deployment",
    "Application Observability and Maintenance",
    "Application Environment, Configuration and Security",
    "Services and Networking",
    "Storage and Volume Management",
    "Troubleshooting and Diagnostics",
    "Workloads & Scheduling",
    "Networking and Gateway API",
    "Cluster Architecture and Extensions"
]

welcome_messages = [
    "Welcome to the CKAD trainer!",
    "Ready to improve your Kubernetes skills?",
    "Start the test and prove your CKAD expertise!"
]

def generate_welcome_message():
    return random.choice(welcome_messages)

def generate_question():
    topic = random.choice(domain_topics)
    prompt = f"""Generate a single CKAD exam question about {topic} in English. Provide:
1. Task description starting with \"Task: \"
2. Validation command starting with \"Validation command: \"
Example:
Task: Create a Pod named 'nginx' with image nginx:alpine and label 'app=web'
Validation command: kubectl get pod nginx -o jsonpath='{{.metadata.labels.app}}' | grep -q web"""

    headers = {'Authorization': f'Bearer {API_TOKEN}', 'Content-Type': 'application/json'}
    data = {
        'model': 'mixtral-8x7b-32768',
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 300,
        'temperature': 0.7,
    }

    while True:
        try:
            response = requests.post(API_URL, headers=headers, json=data, timeout=90)
            response.raise_for_status()
            result = response.json()
            content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            task, validation = parse_question(content)
            if task and validation:
                return task, validation
        except Exception as e:
            print("Waiting for a valid question...")
        time.sleep(10)

def parse_question(response):
    if not response:
        return None, None
    task, validation = None, None
    for line in response.split('\n'):
        if line.startswith('Task:'):
            task = line.replace('Task:', '').strip()
        elif line.startswith('Validation command:'):
            validation = line.replace('Validation command:', '').strip()
    return task, validation

def validate_solution(validation_command):
    try:
        subprocess.run(validation_command, shell=True, check=True, 
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def generate_hint_or_solution(task, validation_command, attempts):
    if attempts < 4:
        prompt = f"""The user failed this CKAD task:
Task: {task}
Validation command: {validation_command}
Generate a helpful hint (in English) explaining the key concept and relevant kubectl commands without revealing the direct solution."""
        max_tokens = 150
    else:
        prompt = f"""The user failed this CKAD task multiple times:
Task: {task}
Validation command: {validation_command}
Provide the exact kubectl command or YAML manifest to solve it."""
        max_tokens = 300

    headers = {'Authorization': f'Bearer {API_TOKEN}', 'Content-Type': 'application/json'}
    data = {
        'model': 'mixtral-8x7b-32768',
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': max_tokens,
        'temperature': 0.4,
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=15)
        result = response.json()
        return result.get('choices', [{}])[0].get('message', {}).get('content', "Hint unavailable.")
    except Exception as e:
        return "Hint unavailable. Check Kubernetes documentation."

def run_scenario():
    for idx in range(1, 11):
        print(f"\n\033[1m*** Question {idx} ***\033[0m")
        task, validation = generate_question()
        print(f"\033[1mTask:\033[0m {task}\n")
        
        attempts = 0
        while True:
            input("Press ENTER when you have completed the task...")
            
            if validate_solution(validation):
                print("\n✅ Correct!")
                break
            else:
                attempts += 1
                print("\n❌ Validation failed.")
                print(f"\033[33m{generate_hint_or_solution(task, validation, attempts)}\033[0m")
                
                if attempts >= 4:
                    print("\n💡 Full solution:")
                    print(f"Try: {validation}")

def main():
    print("\033[1m" + generate_welcome_message() + "\033[0m")
    print("\n📌 Open a terminal with kubectl access ready before proceeding.\n")
    input("\nPress ENTER to start the test...")
    run_scenario()
    print("\n🎉 Training completed! Verify the created resources using: kubectl get all")

if __name__ == "__main__":
    main()
