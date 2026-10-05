# 🧠 Bilingual Stroop Task - Experiment Simulator

Welcome! Thank you for participating in this cognitive psychology experiment measuring the Stroop effect in French. 
You don't need to be a programmer to run this test. Just follow the step-by-step tutorial below.

---

## 🛠️ Step-by-Step Tutorial

### Step 1: Get the Experiment Files
Choose the method that works best for you:

**Option A: Download ZIP (For non-programmers)**
1. At the top right of this GitHub page, click the green button that says **"<> Code"**.
2. From the dropdown menu, click **"Download ZIP"**.
3. Save the file to your computer and **Extract (Unzip)** it by right-clicking the file and selecting "Extract All...".

**Option B: Clone with Git (For developers)**
If you use Git, simply open your terminal and run:
```bash
git clone https://github.com/Lucas-P-Souza/stroop-bilingual.git
cd stroop-bilingual
```

### Step 2: Check your Python Installation
The experiment requires Python to run. 
* **If you already have Python installed:** You can skip to Step 3.
* **If you don't have Python:** 
  1. Go to [python.org/downloads](https://www.python.org/downloads/) and download the latest version (3.9 to 3.11 recommended).
  2. Start the installer.
  3. ⚠️ **CRITICAL STEP (Windows):** At the very bottom of the first installation screen, **you MUST check the box that says "Add Python to PATH"** before clicking Install. If you forget this, the experiment will not open!

### Step 3: Run the Experiment
Choose your operating system:

**🟦 For Windows:**
1. Inside the experiment folder, find the file named `run_windows.bat`.
2. **Double-click** it. 
3. A black terminal screen will open, automatically install the necessary components (PsychoPy), and launch the game. *(Note: This might take a minute or two on the first run).*

**🍎 For Mac / Linux:**
1. Open your Terminal application.
2. Navigate to the experiment folder (e.g., `cd Downloads/projet_recherce`).
3. Run the setup script by typing: `./run_mac_linux.sh`

### Step 4: Send the Data Back
Once you finish the task, the game will close automatically. 
1. Look inside the experiment folder and open the **`data/`** folder.
2. You will find a file named `participant_YourName_00X.csv`.
3. Please send this `.csv` file back to the researcher (Lucas) via WhatsApp or Email.

---
Thank you for your contribution to science! 🔬
