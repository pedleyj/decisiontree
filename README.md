# Esophageal Cancer Decision Tool

This is a simple, interactive [Streamlit](https://streamlit.io/) app designed to help patients and caregivers evaluate two approaches to treating esophageal cancer following chemo and radiation:

1. **Immediate Surgery** (Esophagectomy)
2. **Watchful Waiting** (monitor for recurrence and treat if needed)

The tool allows users to input probabilities and quality-of-life estimates for each potential outcome and visualize the decision using expected values and a decision tree.

## 🔧 Features

- Customizable probability sliders for each path.
- Quality of life (QoL) ratings for every outcome.
- Calculation of expected value (EV) for each strategy.
- Visual bar chart comparing options.
- Color-coded decision tree diagram with QoL and EVs.

## 🚀 Getting Started

### Requirements

- Python 3.8+
- pip (Python package manager)

### Installation

Clone this repository or download the files, then install the required packages:

```bash
pip install -r requirements.txt
