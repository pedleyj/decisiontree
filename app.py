# Streamlit-based Decision Tool for Esophageal Cancer Choices
# Save this as app.py and run using `streamlit run app.py`

try:
    import streamlit as st
    import pandas as pd
    import graphviz
except ModuleNotFoundError:
    raise ModuleNotFoundError("This app requires Streamlit and Graphviz. Install them with `pip install streamlit graphviz`. Then run using `streamlit run app.py`.")

st.set_page_config(layout="wide")

with st.sidebar:
    st.title("Esophageal Cancer Inputs")
    st.markdown("Enter probabilities and QoL ratings.")

    st.subheader("Immediate Surgery Probabilities")
    surg_cure = st.slider("Cure after surgery (%)", 0, 100, 70)
    surg_recur_treatable = st.slider("Treatable recurrence (%)", 0, 100, 20)
    surg_recur_untreatable = st.slider("Untreatable recurrence (%)", 0, 100, 10)

    st.subheader("Watch and Monitor Probabilities")
    wait_no_recur = st.slider("No recurrence (%)", 0, 100, 50)
    wait_recur_treatable = st.slider("Treatable recurrence (%)", 0, 100, 30)
    wait_recur_untreatable = st.slider("Untreatable recurrence (%)", 0, 100, 20)

    if surg_cure + surg_recur_treatable + surg_recur_untreatable != 100:
        st.warning("Surgery probabilities should total 100%.")
    if wait_no_recur + wait_recur_treatable + wait_recur_untreatable != 100:
        st.warning("Watchful waiting probabilities should total 100%.")

    st.subheader("QoL for Surgery Outcomes")
    qol_surg_cure = st.slider("QoL: Cured after surgery", 0, 100, 60)
    qol_surg_recur_treatable = st.slider("QoL: Treatable recurrence after surgery", 0, 100, 40)
    qol_surg_recur_untreatable = st.slider("QoL: Untreatable recurrence after surgery", 0, 100, 10)

    st.subheader("QoL for Watch Outcomes")
    qol_wait_no_recur = st.slider("QoL: No recurrence (no surgery)", 0, 100, 90)
    qol_wait_recur_treatable = st.slider("QoL: Treatable recurrence (watch)", 0, 100, 50)
    qol_wait_recur_untreatable = st.slider("QoL: Untreatable recurrence (watch)", 0, 100, 10)

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

st.header("Expected Values")
st.markdown(f"**Immediate Surgery:** Expected Value = {surgery_ev:.1f}")
st.markdown(f"**Watchful Waiting:** Expected Value = {wait_ev:.1f}")

st.header("Decision Tree")
dot = graphviz.Digraph(format='png')
dot.attr(rankdir='LR', fontsize='10', fontname='Helvetica')
dot.attr('node', shape='box', style='filled', fontname='Helvetica')

dot.node("Start", "Decision: Surgery vs Wait", fillcolor="lightblue")
dot.node("Surgery", f"Immediate Surgery\nEV: {surgery_ev:.1f}", fillcolor="lightgrey")
dot.node("Wait", f"Watchful Waiting\nEV: {wait_ev:.1f}", fillcolor="lightgrey")
dot.edge("Start", "Surgery")
dot.edge("Start", "Wait")

def qol_color(q):
    if q >= 75:
        return "palegreen"
    elif q >= 40:
        return "khaki"
    else:
        return "lightcoral"

surgery_outcomes = [
    ("Surg_Cured", f"Cured\n{surg_cure}%, QoL {qol_surg_cure}", qol_color(qol_surg_cure)),
    ("Surg_Treatable", f"Treatable Recurrence\n{surg_recur_treatable}%, QoL {qol_surg_recur_treatable}", qol_color(qol_surg_recur_treatable)),
    ("Surg_Untreatable", f"Untreatable\n{surg_recur_untreatable}%, QoL {qol_surg_recur_untreatable}", qol_color(qol_surg_recur_untreatable))
]

wait_outcomes = [
    ("Wait_NoRecur", f"No Recurrence\n{wait_no_recur}%, QoL {qol_wait_no_recur}", qol_color(qol_wait_no_recur)),
    ("Wait_Treatable", f"Treatable Recurrence\n{wait_recur_treatable}%, QoL {qol_wait_recur_treatable}", qol_color(qol_wait_recur_treatable)),
    ("Wait_Untreatable", f"Untreatable\n{wait_recur_untreatable}%, QoL {qol_wait_recur_untreatable}", qol_color(qol_wait_recur_untreatable))
]

for node_id, label, color in surgery_outcomes:
    dot.node(node_id, label, fillcolor=color)
    dot.edge("Surgery", node_id)

for node_id, label, color in wait_outcomes:
    dot.node(node_id, label, fillcolor=color)
    dot.edge("Wait", node_id)

st.graphviz_chart(dot)

st.markdown("""
### Interpretation:
- Higher expected value = better average outcome based on your inputs.
- Remember, this is a **simplified model**. Always consult medical professionals.
""")
