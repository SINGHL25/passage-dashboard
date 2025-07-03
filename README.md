# 🚦 Passage Dashboard

**Simple Streamlit dashboard** to visualize transaction volume, SU alarms, and traffic flow using tolling system logs.

## 📊 Features

- Upload `.txt` or `.log` files
- Auto-extract:
  - `TR START` and `TR END` (transaction start/end)
  - `SU ERROR` or SU loss logs
  - Passage ID, timestamp, and traffic volume
- Dashboard includes:
  - Bar chart of transaction counts
  - SU alarm trend
  - Traffic flow volume per passage ID

## 🚀 Quick Start

### 🔧 Install dependencies

```bash
pip install -r requirements.txt
```

### ▶️ Run Streamlit app

```bash
streamlit run app.py
```

## 📂 Sample Log Format

```
2025-07-03 09:12:26 TR START passage=TP10 device=SU1
2025-07-03 09:12:45 TR END passage=TP10 device=SU1
2025-07-03 09:13:01 SU ERROR passage=TP10 device=SU1
```

## 📷 Dashboard Preview

_(Add screenshot.png if you wish)_

## 🛠 Tech Stack

- **Python 3**
- **Streamlit**
- **Pandas**
- **Matplotlib**

## 📧 Contact

Built by [Your Name] | [your@email.com]

MIT License
