import streamlit as st
import pandas as pd
import json
import os
import datetime

# --- CONFIGURATION ---
DATA_FILE = "my_progress.json"
DREAM_COLLEGE = "AIIMS DELHI" 
USER_NAME = "Future Topper"

# --- MOTIVATIONAL QUOTES ---
QUOTES = [
    "It always seems impossible until it is done.",
    "Don't stop when you're tired. Stop when you're done.",
    "Your dream college is waiting for you.",
    "Discipline is doing what needs to be done, even if you don't want to do it.",
    "Pain is temporary. Glory is forever.",
    "The secret of your future is hidden in your daily routine.",
    "Suffer the pain of discipline or suffer the pain of regret.",
    "Success is the sum of small efforts, repeated day in and day out."
]

# --- FULL SYLLABUS DATA ---
INITIAL_DATA = {
    "Class 9 (Foundation)": {
        "Physics": ["Motion", "Force and Laws of Motion", "Gravitation", "Work and Energy", "Sound"],
        "Chemistry": ["Matter in Our Surroundings", "Is Matter Around Us Pure", "Atoms and Molecules", "Structure of the Atom"],
        "Biology": ["The Fundamental Unit of Life (Cell)", "Tissues", "Improvement in Food Resources"]
    },
    "Class 10 (Foundation)": {
        "Physics": ["Light: Reflection and Refraction", "The Human Eye", "Electricity", "Magnetic Effects of Electric Current"],
        "Chemistry": ["Chemical Reactions and Equations", "Acids, Bases and Salts", "Metals and Non-metals", "Carbon and its Compounds"],
        "Biology": ["Life Processes", "Control and Coordination", "How do Organisms Reproduce?", "Heredity", "Our Environment"]
    },
    "Class 11 (NEET Core)": {
        "Physics": ["Units and Measurements", "Motion in a Straight Line", "Motion in a Plane", "Laws of Motion", "Work, Energy and Power", "System of Particles and Rotational Motion", "Gravitation", "Mechanical Properties of Solids", "Mechanical Properties of Fluids", "Thermal Properties of Matter", "Thermodynamics", "Kinetic Theory", "Oscillations", "Waves"],
        "Chemistry": ["Some Basic Concepts of Chemistry", "Structure of Atom", "Classification of Elements", "Chemical Bonding", "Thermodynamics", "Equilibrium", "Redox Reactions", "Organic Chemistry: Basic Principles", "Hydrocarbons"],
        "Biology": ["The Living World", "Biological Classification", "Plant Kingdom", "Animal Kingdom", "Morphology of Flowering Plants", "Anatomy of Flowering Plants", "Structural Organisation in Animals", "Cell: The Unit of Life", "Biomolecules", "Cell Cycle and Cell Division", "Photosynthesis in Higher Plants", "Respiration in Plants", "Plant Growth and Development", "Breathing and Exchange of Gases", "Body Fluids and Circulation", "Excretory Products and their Elimination", "Locomotion and Movement", "Neural Control and Coordination", "Chemical Coordination"]
    },
    "Class 12 (NEET Core)": {
        "Physics": ["Electric Charges and Fields", "Electrostatic Potential and Capacitance", "Current Electricity", "Moving Charges and Magnetism", "Magnetism and Matter", "Electromagnetic Induction", "Alternating Current", "Electromagnetic Waves", "Ray Optics", "Wave Optics", "Dual Nature of Radiation", "Atoms", "Nuclei", "Semiconductor Electronics"],
        "Chemistry": ["Solutions", "Electrochemistry", "Chemical Kinetics", "d- and f- Block Elements", "Coordination Compounds", "Haloalkanes and Haloarenes", "Alcohols, Phenols and Ethers", "Aldehydes, Ketones and Carboxylic Acids", "Amines", "Biomolecules"],
        "Biology": ["Sexual Reproduction in Flowering Plants", "Human Reproduction", "Reproductive Health", "Principles of Inheritance and Variation", "Molecular Basis of Inheritance", "Evolution", "Human Health and Disease", "Microbes in Human Welfare", "Biotechnology: Principles and Processes", "Biotechnology and its Applications", "Organisms and Populations", "Ecosystem", "Biodiversity and Conservation"]
    }
}

# --- FUNCTIONS ---

def load_data():
    """Loads progress. Handles crashes if data is old/corrupted."""
    if not os.path.exists(DATA_FILE):
        return create_new_data()
    
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            # Simple check to see if data matches our new structure
            if "Class 9 (Foundation)" not in data:
                return create_new_data() # Reset if old structure found
            return data
    except:
        return create_new_data() # Reset if file is broken

def create_new_data():
    """Creates a fresh database based on INITIAL_DATA"""
    tracker = {}
    for grade, subjects in INITIAL_DATA.items():
        tracker[grade] = {}
        for sub, chapters in subjects.items():
            tracker[grade][sub] = {}
            for chap in chapters:
                tracker[grade][sub][chap] = {"Revision": False, "MCQ": False, "PYQ": False}
    with open(DATA_FILE, "w") as f:
        json.dump(tracker, f)
    return tracker

def save_data(data):
    """Saves current progress to JSON."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def get_daily_quote():
    day_of_year = datetime.datetime.now().timetuple().tm_yday
    return QUOTES[day_of_year % len(QUOTES)]

# --- APP LAYOUT ---

def main():
    st.set_page_config(page_title="Dream Tracker", page_icon="🎯", layout="wide")
    
    # Load Data
    progress_data = load_data()

    # Sidebar
    with st.sidebar:
        st.header(f"Welcome, {USER_NAME} 👋")
        st.info(f"📅 **Daily Motivation:**\n\n_{get_daily_quote()}_")
        st.divider()
        
        # Navigation
        st.write("### Navigation")
        # Ensure the keys are converted to a list for the selectbox
        class_list = list(progress_data.keys())
        selected_class = st.selectbox("Select Class", class_list)
        
        subject_list = list(progress_data[selected_class].keys())
        selected_subject = st.selectbox("Select Subject", subject_list)
        
        st.divider()
        if st.button("⚠ Reset All Progress"):
            if os.path.exists(DATA_FILE):
                os.remove(DATA_FILE)
                st.rerun()

    # Main Content
    st.title(f"🚀 Goal: {DREAM_COLLEGE}")
    
    # --- CALCULATE TOTAL PROGRESS ---
    total_tasks = 0
    completed_tasks = 0
    
    for grade in progress_data:
        for sub in progress_data[grade]:
            for chap in progress_data[grade][sub]:
                tasks = progress_data[grade][sub][chap]
                total_tasks += 3 
                if tasks["Revision"]: completed_tasks += 1
                if tasks["MCQ"]: completed_tasks += 1
                if tasks["PYQ"]: completed_tasks += 1

    overall_percentage = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    
    st.write(f"### Syllabus Completion: **{overall_percentage:.2f}%**")
    st.progress(overall_percentage / 100)

    if overall_percentage >= 100:
        st.balloons()
        st.success(f"🎉 YOU ARE READY FOR {DREAM_COLLEGE}!")

    st.divider()

    # --- CHAPTER LIST ---
    st.subheader(f"📚 {selected_class} - {selected_subject}")
    
    chapters_dict = progress_data[selected_class][selected_subject]
    
    for chapter, tasks in chapters_dict.items():
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
            
            with col1:
                st.markdown(f"**{chapter}**")
            
            # Checkboxes
            with col2:
                rev = st.checkbox("Revise", value=tasks["Revision"], key=f"{chapter}_rev")
            with col3:
                mcq = st.checkbox("MCQs", value=tasks["MCQ"], key=f"{chapter}_mcq")
            with col4:
                pyq = st.checkbox("PYQs", value=tasks["PYQ"], key=f"{chapter}_pyq")
            
            # Mini Progress
            chap_score = sum([rev, mcq, pyq])
            with col5:
                if chap_score == 3:
                    st.write("✅ Done")
                else:
                    st.write(f"{int((chap_score/3)*100)}%")

            # Save if changed
            if rev != tasks["Revision"] or mcq != tasks["MCQ"] or pyq != tasks["PYQ"]:
                progress_data[selected_class][selected_subject][chapter]["Revision"] = rev
                progress_data[selected_class][selected_subject][chapter]["MCQ"] = mcq
                progress_data[selected_class][selected_subject][chapter]["PYQ"] = pyq
                save_data(progress_data)
                st.rerun()
        st.divider()

if __name__ == "__main__":
    main()