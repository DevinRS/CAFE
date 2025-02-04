import streamlit as st
import pandas as pd

# -- Session State --

# -- Fragments --
@st.fragment
def show_scorecard():
    with st.container(border=True):
        st.title("CAFE Scorecard 📝", anchor=False)
        age = st.slider("Age", 0, 100, 70, 1)
        delw = st.slider("Delayed Word Recall (0-5)", 0.0, 5.0, 4.5, 0.5)
        faq = st.slider("FAQ (0-30)", 0, 30, 2, 1)
        Apoe4 = st.selectbox("APOE", ["0", "1", "2"])
        age_score = 0
        if age >= 70:
            age_score += 2
        if age >= 77:
            age_score += 5
        delw_score = 0
        if delw <= 1.5:
            delw_score += 2
        if delw <= 3.5:
            delw_score += 2
        faq_score = 0
        if faq >= 1:
            faq_score += 2
        if faq >= 5:
            faq_score += 2
        Apoe4_score = 0
        if Apoe4 == "1":
            Apoe4_score += 2
        elif Apoe4 == "2":
            Apoe4_score += 2
        total_score = age_score + delw_score + faq_score + Apoe4_score
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Total Risk Points", anchor=False)  
            st.metric(label="Total Risk Points", value=f"{total_score} / 17")
            st.progress(total_score/17, text=f"Your total risk points: {total_score}/17")
        with col2:
            st.subheader("Total Risk Percentage", anchor=False)
            # make a dictionary for score to risk percentage conversion
            score_to_risk = {
                0: 0.5, 2: 2.3, 4: 9.6, 5: 18.3,
                6: 32.1, 7: 50.0, 8: 67.9, 9: 81.7,
                10: 90.4, 11: 95.2, 12: 97.7, 13: 98.9, 15: 99.8, 17: 99.9
            }
            # convert total_score to risk percentage
            total_percentage = score_to_risk[total_score]
            st.metric(label="Total Risk Percentage", value=f"{total_percentage}%")

    # make a pandas table for the scorecard point conversion (col: Feature, Score)
    if st.checkbox("Show Scorecard Point and Risk Conversion", value=False):
        st.subheader("Scorecard Point Conversion", anchor=False)
        point_data = {"Features": ["AGE >= 70", "AGE >= 77", "DELW <= 1.5", "DELW <= 3.5", "FAQ >= 1", "FAQ >= 5", "APOE4 >= 1"], "Score": [2, 5, 2, 2, 2, 2, 2]}
        point_df = pd.DataFrame(point_data)
        st.dataframe(point_df, use_container_width=True, hide_index=True)

        # make a pandas table for the scorecard risk percentage conversion (col: Score, Risk Percentage)
        st.subheader("Risk Percentage Conversion", anchor=False)
        risk_data = {"Score": [0, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 17], "Risk Percentage": ["0.5%", "2.3%", "9.6%", "18.3%", "32.1%", "50.0%", "67.9%", "81.7%", "90.4%", "95.2%", "97.7%", "98.9%", "99.8%", "99.9%"]}
        risk_df = pd.DataFrame(risk_data)
        st.dataframe(risk_df, use_container_width=True, hide_index=True)

    st.header("💊 Interpretation", anchor=False)
    st.subheader("Age", anchor=False)
    age_text = "Age is an important factor in assessing cognitive health risks because the likelihood of decline increases as we grow older. "
    if age < 70:
        age_text += "Since you are under 70, age does not contribute to your risk score in this case."
    elif age < 77:
        age_text += "Because you are 70 or older, age is considered a contributing factor to cognitive health risks."
    else:
        age_text += "Since you are 77 or older, age becomes a more significant factor in assessing cognitive health risks."
    st.write(age_text)
    st.subheader("Delayed Word Recall", anchor=False)
    delw_text = "We use a memory test called delayed word recall to evaluate how well you retain information after a short delay. "
    if delw <= 1.5:
        delw_text += "Since your score is 1.5 or lower, this suggests more noticeable difficulty in recalling information, which increases the risk score further. "
    elif delw <= 3.5:
        delw_text += "Because your score falls at or below 3.5, there is a mild concern about memory retention, which slightly increases your overall risk."
    else:
        delw_text += "Since your score is higher than 3.5, your memory retention appears to be within a healthy range, and this does not add to your risk score."
    st.write(delw_text)
    st.subheader("FAQ", anchor=False)
    faq_text = "This questionnaire helps assess your ability to complete daily tasks independently. "
    if faq < 1:
        faq_text += "Your score suggests that you are fully independent in daily activities, so this does not contribute to your risk score."
    elif faq < 5:
        faq_text += "Because your score is at least 1, it indicates that you may experience some mild difficulties in daily activities. However, since it is below 5, it does not suggest major impairment."
    else:
        faq_text += "A score of 5 or higher suggests more significant difficulties with daily tasks, which may indicate a greater impact on cognitive function."
    st.write(faq_text)
    st.subheader("APOE", anchor=False)
    Apoe4_text = "ApoE4 is a genetic marker that can influence the risk of developing cognitive decline. "
    if Apoe4 == "0":
        Apoe4_text += "Since you do not carry the ApoE4 gene, this does not contribute to your risk score."
    else:
        Apoe4_text += "Because you carry the ApoE4 gene, this is considered a risk factor for cognitive decline."
    st.write(Apoe4_text)
     

# -- Landing Page Section --
st.warning("This is only a demo! Results should not be used for any medical decisions.")
st.title("☕ CAFE Scorecard", anchor=False)
st.subheader("Cognitive, Age, Functioning, and Apolipoprotein E4 (CAFE)", anchor=False)
st.write("Detecting Alzheimer’s disease early can make a significant difference in treatment options and patient care. However, traditional diagnostic methods can be costly and complex, limiting accessibility for many individuals. Our Alzheimer’s Risk Scorecard offers a simple, interpretable, and effective way to estimate the likelihood of developing Alzheimer’s using readily available information.")
st.subheader("How It Works", anchor=False)
st.write("Our scoring system is built using data from 713 participants in the Alzheimer’s Disease Neuroimaging Initiative and is based on key cognitive test scores, informant-reported daily functioning, genetic risk factors, and demographics. Using interpretable machine learning with the FasterRisk algorithm, we have developed ten optimized scorecards with high predictive accuracy (AUC: 0.867–0.893).")
st.subheader("Why Use This Model?", anchor=False)
st.write("""
- 🏃 Fast & Accessible – Requires only a few simple inputs to generate an immediate risk estimate.
- ⚕️ Clinically Relevant – Developed from real patient data and validated across different feature combinations.
- 📜 Interpretable – Unlike black-box AI models, this scorecard provides clear, understandable risk scores.
- 🕑 Early Detection – Helps doctors and researchers assess risk before symptoms become severe.
         """)
if st.button('Get Started', use_container_width=True):
    show_scorecard()
    
    


