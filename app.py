import streamlit as st
import pandas as pd
import datetime
from streamlit_gsheets import GSheetsConnection

# --- CONFIGURATION ---
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

# --- FULL SYLLABUS DATA (Structure Only) ---
INITIAL_DATA = {
    "Class 9 (Foundation)": {
        "Physics": ["Motion", "Force and Laws of Motion", "Gravitation", "Work and Energy", "Sound"],
        "Chemistry": ["Matter in Our Surroundings", "Is Matter Around Us Pure", "Atoms and Molecules", "Structure of the Atom"],
        "Biology": ["The Fundamental Unit of Life (Cell)", "Tissues", "Improvement in Food Resources"]
    },
    "Class 10 (Foundation)": {
        "Physics": ["Light: Reflection and Refraction", "The Human Eye", "Electricity", "Magnetic Effects of Electric Current"],
        "Chemistry": ["Chemical Reactions and Equations", "Acids, Bases and Salts", "Metals and Non-metals", "Carbon and its Compounds"],
        "Biology": ["Life Processes", "Control and Coordination", "How do Organisms Reproduce", "Heredity", "Our Environment"]
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

# --- GOOGLE SHEETS FUNCTIONS ---

def get_data():
    """Fetches data from Google Sheets or initializes it if empty."""
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    try:
        # Try to read the existing data
        df = conn.read()
        # If the sheet is empty or new, df might be empty. Check structure.
        if df.empty or "Chapter" not in df.columns:
            return reset_data(conn)
        return df
    except:
        # If any error (file not found/empty), reset
        return reset_data(conn)

def reset_data(conn):
    """Creates the initial database structure and uploads to Sheets."""
    rows = []
    for grade, subjects in INITIAL_DATA.items():
        for sub, chapters in subjects.items():
            for chap in chapters:
                rows.append({
                    "Class": grade,
                    "Subject": sub,
                    "Chapter": chap,
                    "Revision": False,
                    "MCQ": False,
                    "PYQ": False
                })
    
    df = pd.DataFrame(rows)
    conn.update(data=df)
    st.cache_data.clear() # Clear cache to ensure reload
    return df

def update_data(df):
    """Updates the Google Sheet with the modified dataframe."""
    conn = st.connection("gsheets", type=GSheetsConnection)
    conn.update(data=df)
    st.cache_data.clear()

def get_daily_quote():
    day_of_year = datetime.datetime.now().timetuple().tm_yday
    return QUOTES[day_of_year % len(QUOTES)]

# --- APP LAYOUT ---

def main():
    st.set_page_config(page_title="Dream Tracker", page_icon="🎯", layout="wide")
    
    # 1. Load Data
    df = get_data()

    # Sidebar
    with st.sidebar:
        st.header(f"Welcome, {USER_NAME} 👋")
        st.info(f"📅 **Daily Motivation:**\n\n_{get_daily_quote()}_")
        st.divider()
        
        # Navigation
        st.write("### Navigation")
        
        class_list = df["Class"].unique().tolist()
        # sort explicitly to keep order if possible, or just use unique
        selected_class = st.selectbox("Select Class", class_list)
        
        subject_list = df[df["Class"] == selected_class]["Subject"].unique().tolist()
        selected_subject = st.selectbox("Select Subject", subject_list)
        
        st.divider()
        if st.button("⚠ Reset All Progress (Clear Sheet)"):
            conn = st.connection("gsheets", type=GSheetsConnection)
            reset_data(conn)
            st.rerun()

    # Main Content
    st.title(f"🚀 Goal: {DREAM_COLLEGE}")
    
    # --- CALCULATE TOTAL PROGRESS ---
    # Convert True/False columns to numeric (1/0) for calculation
    total_tasks = len(df) * 3
    completed_rev = df["Revision"].sum()
    completed_mcq = df["MCQ"].sum()
    completed_pyq = df["PYQ"].sum()
    
    completed_tasks = completed_rev + completed_mcq + completed_pyq
    overall_percentage = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    
    st.write(f"### Syllabus Completion: **{overall_percentage:.2f}%**")
    st.progress(overall_percentage / 100)

    if overall_percentage >= 100:
        st.balloons()
        st.success(f"🎉 YOU ARE READY FOR {DREAM_COLLEGE}!")

    st.divider()

    # --- CHAPTER LIST ---
    st.subheader(f"📚 {selected_class} - {selected_subject}")
    
    # Filter data for current view
    # We create a copy to edit, then push back to main df
    current_view = df[(df["Class"] == selected_class) & (df["Subject"] == selected_subject)].copy()
    
    changes_made = False

    for index, row in current_view.iterrows():
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
            
            with col1:
                st.markdown(f"**{row['Chapter']}**")
            
            # Checkboxes
            # We use the unique index from the dataframe as the key
            rev = st.checkbox("Revise", value=bool(row["Revision"]), key=f"{index}_rev")
            mcq = st.checkbox("MCQs", value=bool(row["MCQ"]), key=f"{index}_mcq")
            pyq = st.checkbox("PYQs", value=bool(row["PYQ"]), key=f"{index}_pyq")
            
            # Mini Progress
            chap_score = sum([rev, mcq, pyq])
            with col5:
                if chap_score == 3:
                    st.write("✅ Done")
                else:
                    st.write(f"{int((chap_score/3)*100)}%")

            # Check for changes
            if rev != row["Revision"] or mcq != row["MCQ"] or pyq != row["PYQ"]:
                df.at[index, "Revision"] = rev
                df.at[index, "MCQ"] = mcq
                df.at[index, "PYQ"] = pyq
                changes_made = True

        st.divider()

    # Save logic outside the loop to batch updates (faster)
    if changes_made:
        update_data(df)
        st.rerun()

if __name__ == "__main__":
    main()