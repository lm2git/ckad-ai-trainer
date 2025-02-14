# 🚀 CKAD AI Trainer - Kubernetes AI Trainer ![Kubernetes Logo](https://upload.wikimedia.org/wikipedia/commons/3/39/Kubernetes_logo_without_workmark.svg)

## 📌 Introduction
This script generates practice questions for the **CKAD (Certified Kubernetes Application Developer)** exam using the **Groq API**. It helps you enhance your Kubernetes skills by simulating real-world tasks with automatic validation.

---

## 🎯 Features
- 📖 **Generates CKAD questions** based on official topics
- ✅ **Automatically verifies answers** with `kubectl` commands
- 💡 **Provides intelligent hints** in case of mistakes
- 🔥 **Reveals full solution** after 4 failed attempts
- ⏳ **Optimized response time** using AI-powered API

---

## 🛠️ Prerequisites

Ensure you have:
- 🐧 Linux or 🖥️ macOS with `kubectl` access
- 🔄 Connection to a Kubernetes cluster
- 🛠️ Python 3 installed
- 📦 Required dependencies: `requests`
- 🔑 API Token for **Groq**

Install dependencies with:
```bash
pip install requests
```

---

## 🚀 Usage

First of all, add your personal groq APIKEY in file ckad_trainer.py
```bash
API_TOKEN = 'your-api-token'
```



1️⃣ **Run the script:**
```bash
python ckad_trainer.py
```

2️⃣ **Follow on-screen instructions** and solve Kubernetes tasks.

3️⃣ **Verify answers**: The script will automatically check your work.

4️⃣ **Receive hints** if your answer is incorrect.

5️⃣ **Get the full solution** after 4 failed attempts.

6️⃣ **Complete the test and verify created resources:**
```bash
kubectl get all
```

---

## 📷 Example Execution

![Example CKAD Trainer](https://upload.wikimedia.org/wikipedia/commons/b/b8/Kubectl_output.png)

---

## 📂 Script Structure

```plaintext
ckad_trainer.py
│── 📌 Question generation
│── 🔍 Automatic validation
│── 💡 Hints and solutions
│── 🔄 Execution loop with 10 questions
```

---

## 📢 Notes
- The script uses the `mixtral-8x7b-32768` model to generate questions and hints.
- Questions cover various CKAD topics such as **pod scheduling, networking, configuration, and troubleshooting**.
- A running Kubernetes cluster is required to test responses.

---

## 🎉 Contribute
Have ideas to improve the script? Feel free to open an **issue** or submit a **pull request**!

---

🚀 **Happy training and good luck with your CKAD exam!**

