# Antigravity Bank - Workshop Prerequisites

This repository contains the prerequisite codebase for the **Antigravity 2.0 & CLI in the SDLC** workshop. It features a mock banking web dashboard designed to demonstrate the inner-loop developer flow, background cron-based automation, and custom agent policies using Google Antigravity.

---

## 📂 Project Layout

- `fake_bank/`: The core mock banking application built with **Python 3** and **Flask**.
  - `main.py`: Application entrypoint containing mock account balances and transaction data.
  - `templates/index.html`: Responsive, beautiful dashboard UI styled with Tailwind CSS.
  - `requirements.txt`: Python package dependencies.
- `.gitignore`: Configured to exclude python bytecode, virtual environments, and system-specific files.

---

## 🚀 Getting Started (Run Locally)

This project has been updated to run standalone on standard Python without requiring any Blaze build systems.

### 1. Setup Python Virtual Environment
Navigate to the application folder and create a clean environment:
```bash
cd fake_bank
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies
Install Flask from PyPI:
```bash
pip install -r requirements.txt
```

### 3. Run the Server
Launch the Flask development server:
```bash
python main.py
```

The bank dashboard will be live at **`http://127.0.0.1:5000`**.

---

## 🎓 Workshop Overview

During the workshop, you will:
1. **Inner-Loop Dev (Role A):** Use the **Antigravity Hub (UI)** to add live stock rates, start the server, and automatically verify features using browser screenshots.
2. **Outer-Loop Gov (Role B):** Use the **Antigravity CLI (`agy`)** to define team policies in `.agents/AGENTS.md` and schedule a background review cron task.
3. **Automated Review:** Watch a background agent automatically spot rule violations and post line-level comments on your open GitHub PR.
