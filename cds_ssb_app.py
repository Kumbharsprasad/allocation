import streamlit as st

# Class definition
class CDS_SSB_alloc:
    def __init__(self, gk, eng, mth, gender, preference):
        self.gk = gk
        self.eng = eng
        self.mth = mth
        self.gender = gender.lower()
        self.preference = [pref.upper() for pref in preference]

    def calculate_total(self):
        return self.gk + self.eng + self.mth

    def get_cutoffs(self):
        return {
            'AFA': 156,
            'IMA': 137,
            'INA': 122,
            'OTA': 88
        }

    def allocate_ssb(self):
        total = self.calculate_total()
        written_cutoffs = self.get_cutoffs()

        if self.gender == 'female':
            if self.preference != ['OTA']:
                return "❌ Women are only eligible for OTA."
            if (self.gk + self.eng) >= written_cutoffs['OTA']:
                return "✅ You are qualified for OTA SSB."
            else:
                return "❌ Not qualified for OTA."

        elif self.gender == 'male':
            if 'OTA' in self.preference[:-1] and len(self.preference) > 1:
                return "⚠️ Error: For males applying to multiple academies, OTA must be the last preference."

            for pref in self.preference:
                if pref == 'AFA' and total >= written_cutoffs['AFA']:
                    return "✅ You are alloted SSB for Indian Air Force (AFA)."
                elif pref == 'IMA' and total >= written_cutoffs['IMA']:
                    return "✅ You are alloted SSB for Indian Army (IMA)."
                elif pref == 'INA' and total >= written_cutoffs['INA']:
                    return "✅ You are alloted SSB for Indian Navy (INA)."
                elif pref == 'OTA' and (self.gk + self.eng) >= written_cutoffs['OTA']:
                    return "✅ You are alloted SSB for Indian Army (OTA)."
            return "❌ You did not qualify for any SSB."

        else:
            return "❗ Invalid gender. Use 'male' or 'female'."

# Streamlit UI
st.title("CDS SSB Allocation Predictor")

gk = st.number_input("Enter GK Marks", min_value=0, max_value=100)
eng = st.number_input("Enter English Marks", min_value=0, max_value=100)
mth = st.number_input("Enter Math Marks", min_value=0, max_value=100)
gender = st.selectbox("Select Gender", ["male", "female"])
preference = st.multiselect(
    "Enter your preferences (in order)",
    ["AFA", "IMA", "INA", "OTA"]
)

if st.button("Check SSB Allocation"):
    if len(preference) == 0:
        st.warning("Please select at least one preference.")
    else:
        candidate = CDS_SSB_alloc(gk, eng, mth, gender, preference)
        result = candidate.allocate_ssb()
        total_score = candidate.calculate_total()
        cutoffs = candidate.get_cutoffs()

        st.success(result)
        st.info(f"🧮 Your Total Score: **{total_score}** (GK + English + Math = {gk} + {eng} + {mth})")
        st.markdown("### 📊 Cutoffs Considered")
        st.write({
            "AFA (Air Force)": cutoffs['AFA'],
            "IMA (Army)": cutoffs['IMA'],
            "INA (Navy)": cutoffs['INA'],
            "OTA (Officers Training Academy)": cutoffs['OTA']
        })
