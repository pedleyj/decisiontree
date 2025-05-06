# Streamlit-based Decision Tool for Esophageal Cancer Choices
# Save this as app.py and run using `streamlit run app.py`

try:
    import streamlit as st
    import pandas as pd
    import graphviz
except ModuleNotFoundError:
    raise ModuleNotFoundError("This app requires Streamlit and Graphviz. Install them with `pip install streamlit graphviz`. Then run using `streamlit run app.py`.")

st.title("Esophageal Cancer Decision Tool")
st.markdown("""
This tool helps compare two options:

1. **Immediate surgery** (Esophagectomy)
2. **Watchful waiting** (Monitor and treat if cancer returns)

Enter your estimated probabilities and quality-of-life (QoL) scores (0 to 100) for each outcome to compare the expected values.
""")

st.header("1. Input Probabilities")
st.subheader("Immediate Surgery")
surg_cure = st.slider("Chance of cure (no recurrence) after surgery (%)", 0, 100, 70)
surg_recur_treatable = st.slider("Chance of recurrence (treatable) after surgery (%)", 0, 100, 20)
surg_recur_untreatable = st.slider("Chance of recurrence (untreatable) after surgery (%)", 0, 100, 10)

if surg_cure + surg_recur_treatable + surg_recur_untreatable != 100:
    st.warning("Surgery probabilities should total 100%.")

st.subheader("Wait and Monitor")
wait_no_recur = st.slider("Chance of no recurrence (ongoing remission) (%)", 0, 100, 50)
wait_recur_treatable = st.slider("Chance of recurrence (treatable) (%)", 0, 100, 30)
wait_recur_untreatable = st.slider("Chance of recurrence (untreatable) (%)", 0, 100, 20)

if wait_no_recur + wait_recur_treatable + wait_recur_untreatable != 100:
    st.warning("Watchful waiting probabilities should total 100%.")

st.header("2. Input Quality of Life (QoL) Values")
st.markdown("Rate each outcome from 0 (worst) to 100 (best).")

st.subheader("Surgery Outcomes")
qol_surg_cure = st.slider("QoL: Cured after surgery", 0, 100, 60)
qol_surg_recur_treatable = st.slider("QoL: Treatable recurrence after surgery", 0, 100, 40)
qol_surg_recur_untreatable = st.slider("QoL: Untreatable recurrence after surgery", 0, 100, 10)

st.subheader("Watch and Monitor Outcomes")
qol_wait_no_recur = st.slider("QoL: Ongoing remission (no surgery)", 0, 100, 90)
qol_wait_recur_treatable = st.slider("QoL: Treatable recurrence with later surgery or treatment", 0, 100, 50)
qol_wait_recur_untreatable = st.slider("QoL: Untreatable recurrence (wait path)", 0, 100, 10)

st.header("3. Results")

surgery_ev = (
    surg_cure * qol_surg_cure +
    surg_recur_treatable * qol_surg_recur_treatable +
    surg_recur_untreatable * qol_surg_recur_untreatable
) / 100

wait_ev = (
    wait_no_recur * qol_wait_no_recur +
    wait_recur_treatable * qol_wait_recur_treatable +
    wait_recur_untreatable * qol_wait_recur_untreatable
) / 100

results = pd.DataFrame({
    'Strategy': ['Immediate Surgery', 'Watch and Monitor'],
    'Expected Value': [surgery_ev, wait_ev]
})

st.bar_chart(results.set_index('Strategy'))

st.markdown("""
### Interpretation:
- Higher expected value = better average outcome based on your inputs.
- Remember, this is a **simplified model**. Discuss decisions with medical professionals.
""")

st.header("4. Visual Decision Tree")
dot = graphviz.Digraph(format='png')
dot.attr(rankdir='LR', fontsize='10', fontname='Helvetica')
dot.attr('node', shape='box', style='filled', fontname='Helvetica')

# Root decision node
dot.node("Start", "Decision: Surgery vs Wait", fillcolor="lightblue")

# Top-level choices with EVs
dot.node("Surgery", f"Immediate Surgery\nEV: {surgery_ev:.1f}", fillcolor="lightgrey")
dot.node("Wait", f"Watchful Waiting\nEV: {wait_ev:.1f}", fillcolor="lightgrey")
dot.edge("Start", "Surgery")
dot.edge("Start", "Wait")

# Helper to get color based on QoL value

def qol_color(q):
    if q >= 75:
        return "palegreen"
    elif q >= 40:
        return "khaki"
    else:
        return "lightcoral"

# Terminal nodes with outcomes and color-coded QoL
surgery_outcomes = [
    (f"Surg_Cured", f"Cured\n{surg_cure}%, QoL {qol_surg_cure}", qol_color(qol_surg_cure)),
    (f"Surg_Treatable", f"Treatable Recurrence\n{surg_recur_treatable}%, QoL {qol_surg_recur_treatable}", qol_color(qol_surg_recur_treatable)),
    (f"Surg_Untreatable", f"Untreatable\n{surg_recur_untreatable}%, QoL {qol_surg_recur_untreatable}", qol_color(qol_surg_recur_untreatable))
]

wait_outcomes = [
    (f"Wait_NoRecur", f"No Recurrence\n{wait_no_recur}%, QoL {qol_wait_no_recur}", qol_color(qol_wait_no_recur)),
    (f"Wait_Treatable", f"Treatable Recurrence\n{wait_recur_treatable}%, QoL {qol_wait_recur_treatable}", qol_color(qol_wait_recur_treatable)),
    (f"Wait_Untreatable", f"Untreatable\n{wait_recur_untreatable}%, QoL {qol_wait_recur_untreatable}", qol_color(qol_wait_recur_untreatable))
]

for node_id, label, color in surgery_outcomes:
    dot.node(node_id, label, fillcolor=color)
    dot.edge("Surgery", node_id)

for node_id, label, color in wait_outcomes:
    dot.node(node_id, label, fillcolor=color)
    dot.edge("Wait", node_id)

st.graphviz_chart(dot)