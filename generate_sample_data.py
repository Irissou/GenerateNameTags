"""Generate a fully synthetic registration file with the same columns as the real
Google-Form export used for the conference (no real people, no real abstracts).

    python generate_sample_data.py
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
N = 40

first = ["Alex", "Maria", "Jonas", "Priya", "Liam", "Sofia", "Chen", "Amara", "Lukas", "Elena",
         "Omar", "Hannah", "Mateo", "Yuki", "Nora", "Ivan", "Leila", "Oscar", "Mina", "Tariq"]
last = ["Larsen", "Rossi", "Nakamura", "Okafor", "Novak", "Silva", "Haddad", "Berg", "Kowalski",
        "Moreau", "Patel", "Jensen", "Alvarez", "Fischer", "Tanaka", "Dubois", "Kim", "Hansen"]
departments = [
    "Northern Lights University / Department of Astronomy",
    "Example Institute of Technology / Space Research",
    "University of Examplia / Physics and Astronomy",
    "Fjordland University / Cosmology Group",
    "Alpine Observatory / Extragalactic Group",
    "Lakeside University / Department of Physics",
]
career = ["PhD student", "Postdoc", "Assistant professor", "Professor", "Master student"]
gender = ["Female", "Male", "Non-binary", "Prefer not to say"]
diets = ["No dietary requirement"] * 5 + ["Vegetarian", "Vegan", "Gluten-free"]
allergies = [np.nan] * 7 + ["Nuts", "Lactose", "Shellfish"]

topics = ["galaxy clusters", "gravitational lensing", "star-forming galaxies", "dark matter halos",
          "quasar absorption lines", "cosmic voids", "the intergalactic medium", "high-redshift galaxies"]
methods = ["a Bayesian framework", "deep learning", "mock catalogues", "integral-field spectroscopy",
           "a new calibration pipeline", "forward modelling"]
sentences = [
    "We present a new analysis of {t} using {m}.",
    "Our approach reduces systematic uncertainties by a factor of two compared to earlier work.",
    "We discuss implications for current models and outline prospects for upcoming surveys.",
]

names = set()
while len(names) < N:
    names.add(f"{rng.choice(first)} {rng.choice(last)}")
names = sorted(names)
rng.shuffle(names)

rows = []
for i, name in enumerate(names):
    talk = rng.random() < 0.6
    t, m = rng.choice(topics), rng.choice(methods)
    rows.append({
        "Tidsstempel": f"2023/11/{rng.integers(1, 29):02d} {rng.integers(8, 20):02d}:{rng.integers(0, 60):02d}:{rng.integers(0, 60):02d}",
        "Name": name,
        "Email address ": name.lower().replace(" ", ".") + "@example.org",
        "Department": rng.choice(departments),
        "Career level": rng.choice(career),
        "Gender": rng.choice(gender),
        "Would you like to give an oral presentation?": "Yes" if talk else "No",
        "Title": f"Studying {t} with {m}" if talk else np.nan,
        "Abstract": " ".join(s.format(t=t, m=m) for s in sentences) if talk else np.nan,
        "Dietary requirement": rng.choice(diets),
        "If any allergies, then please list them here": rng.choice(allergies),
    })

df = pd.DataFrame(rows)
# one person who registered twice (the notebooks de-duplicate on e-mail)
df = pd.concat([df, df.iloc[[3]]], ignore_index=True)
df.to_csv("data/sample_registrations.csv", index=False)
print(df.shape, (df["Would you like to give an oral presentation?"] == "Yes").sum(), "talks")
