# Crank-Nicolson Delta Hedging

---

## 📚 Overview
This repository demonstrates how the **Crank-Nicolson (CK) method** can be applied for **dynamic delta hedging** and compares it with a **sliding window Binomial Tree delta hedging method**. A more comprehensive report is available in **Report.pdf**. This was a final project for FRE-GY 6083 (NYU Tandon)

### 🎯 Objective
Initially, our goal was to design a trading strategy leveraging the **Crank-Nicolson method** for deriving implied volatility to assist in **High-Frequency Trading (HFT)** decisions. However, due to the lack of readily available HFT options data and the need to align the project with **Risk Management principles**, we opted to focus on **delta hedging strategies**.

---

## 🛠️ Methodology

### ⚙️ Crank-Nicolson Method
- Numerical method used to solve partial differential equations.
- Applied to dynamically hedge options positions by solving the **Black-Scholes PDE**.

### 📊 Sliding Window Binomial Tree
- Used as a comparative method.
- Simulates price movements using discrete steps.
- Allows for delta recalibration at each node.

---

## 📈 Comparison
Both methods are compared in terms of:
- **Hedging accuracy** (Max drawdown and volatility of returns)
- **Computational efficiency** (Time to run the function)
- **Sensitivity to volatility and price movements** (Volatility of returns)

---
```
## 📌 Notebook Descriptions
- **CN_Convergence** and **欢迎使用_Colaboratory 的副本**: Both demonstrate the **convergence of the Crank-Nicolson method**. Changing the price grid boundaries will affect convergence.
- **CN_Hedging**: Focuses on **timing performance**, though it doesn't accurately price options. Surprisingly, it performs well in hedging metrics.
- **CN_hedging_accurate_predictions**: Accurate implementation of the **Crank-Nicolson method**.
- **BinTree_Hedging**: Implementation of the **sliding window binomial tree delta hedging**.

---

## 📦 Requirements
To run the project, install the necessary Python libraries:
```bash
pip install -r requirements.txt
```

---

## 📊 Results
The results demonstrate the strengths and weaknesses of both hedging strategies under varying market conditions. Further details can be found in the **Report.pdf** document.

---

## 🚀 Future Improvements
- Inclusion of a **main script** to run everything at once.
- Integration of **real-time HFT options data**.
- Further optimization of the **Crank-Nicolson algorithm** for live trading environments.
- Expansion into other **numerical methods for hedging**.

---

## 👥 Contributors
- **Thomas101Shen**
- **Sylviayq955**
- **Yina** *(Contact details available in Report.pdf)*
