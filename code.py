import pandas as pd
import numpy as np

# Notes data from the user
notes_data = [
    ("Nawā", "G", 1200),
    ("tīk Ḥijāz", "G half flat", 1150),
    ("Ḥijāz", "F sharp", 1100),
    ("nīm Ḥijāz", "F half sharp", 1050),
    ("Jahārkāh", "F", 1000),
    ("tīk Būsalik", "E half sharp", 950),
    ("Būsalik", "E", 900),
    ("Sīkāh", "E half flat", 850),
    ("Kurd", "E flat", 800),
    ("nīm Kurd", "D half sharp", 750),
    ("Dūkāh", "D", 700),
    ("tīk Zirkūlāh", "D half flat", 650),
    ("Zirkūlāh", "D flat", 600),
    ("nīm Zirkūlāh", "C half sharp", 550),
    ("Rāst", "C", 500),
    ("tīk Kawasht", "B half sharp", 450),
    ("Kawasht", "B", 400),
    ("‘Irāq", "B half flat", 350),
    ("‘Ajam ‘Ushayrān", "B flat", 300),
    ("nīm ‘Ajam ‘Ushayrān", "A half sharp", 250),
    ("‘Ushayrān", "A", 200),
    ("qarār tīk Ḥiṣār", "A half flat", 150),
    ("qarār Ḥiṣār", "A flat", 100),
    ("qarār nīm Ḥiṣār", "G half sharp", 50),
    ("Yakāh", "G", 0),
]

# Reference frequency for A4 = 440 Hz at 0 cents
A4_freq = 440
A4_cents = 0  # Since we define A4 as reference

# Shift the table so that A (200 cents in the table) = A4 = 440 Hz
# We compute the frequency based on the cents difference to 200
def compute_frequency(cents_from_lowest):
    cents_diff_from_A4 = cents_from_lowest - 200
    return round(A4_freq * 2 ** (cents_diff_from_A4 / 1200), 2)

# Compute frequency for each note
data_with_freq = [
    (arabic, english, cents, compute_frequency(cents)) for arabic, english, cents in notes_data
]

# Convert to DataFrame
df = pd.DataFrame(data_with_freq, columns=["Arabic name", "English name", "Distance from lowest note in cents", "Frequency (Hz)"])
df.head()
