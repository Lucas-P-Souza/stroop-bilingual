"""
Configuration file for the Stroop experiment.
Edit these values to customize the experiment behavior, keys, and display.
"""

# 1. KEY_COLOR_MAP
# Maps keyboard keys to color names
KEY_COLOR_MAP: dict[str, str] = {
    "r": "red",
    "b": "blue",
    "g": "green",
    "y": "yellow"
}

# 2. WORD_MEANING_MAP
# Maps French words to the colors they semantically mean
WORD_MEANING_MAP: dict[str, str] = {
    "ROUGE": "red",
    "BLEU": "blue",
    "VERT": "green",
    "JAUNE": "yellow"
}

# 3. Temporização (Timing)
FIXATION_DURATION: float = 0.5
ISI_DURATION: float = 2.0
RESPONSE_TIMEOUT: float = float('inf')

# 4. Número de trials (Trial counts)
N_PRACTICE_TRIALS: int = 8
N_EXPERIMENTAL_REPETITIONS: int = 5

# 5. Display
WINDOW_SIZE: tuple[int, int] = (1024, 768)
FULLSCREEN: bool = True
BG_COLOR: str = "white"
TEXT_COLOR: str = "black"
STIMULUS_FONT_SIZE: int = 72
INSTRUCTION_FONT_SIZE: int = 28

# 6. Variáveis de Metadados / Metadata Variables (Questionário)
L1_OPTIONS: list[str] = ["", "Portuguese / Portugais", "Spanish / Espagnol", "English / Anglais", "Arabic / Arabe", "Chinese / Chinois", "Italian / Italien", "German / Allemand", "Russian / Russe", "French / Français", "Other / Autre"]
SEX_OPTIONS: list[str] = ["", "Female / Femme", "Male / Homme", "Other / Autre", "Prefer not to say / Préfère ne pas le dire"]
FRENCH_LEVEL_OPTIONS: list[str] = ["", "Beginner / Débutant", "Intermediate / Intermédiaire", "Advanced / Avancé", "Fluent / Courant", "Native / Natif"]
CERTIFICATION_OPTIONS: list[str] = ["", "None / Aucune", "A1", "A2", "B1", "B2", "C1", "C2"]
GLASSES_OPTIONS: list[str] = ["", "No / Non", "Yes, currently wearing / Oui, je les porte actuellement", "Yes, but NOT wearing now / Oui, mais je ne les porte pas"]

# 7. Saída (Output)
RESEARCHERS: list[str] = ["", "Lucas", "Paulo", "Samuel", "Bilal"]
OUTPUT_DIR: str = "data/"
FILENAME_PATTERN: str = "participant_{participant_id}.csv"

# 8. Reprodutibilidade (Reproducibility)
RANDOM_SEED: int | None = None

# 9. CSV_COLUMNS
CSV_COLUMNS: list[str] = [
    "participant_id",
    "age",
    "sex",
    "l1_language",
    "french_level_self",
    "french_certification",
    "wearing_glasses",
    "trial_number",
    "block",
    "word",
    "color",
    "congruency",
    "correct_response",
    "response",
    "response_time_ms",
    "correct"
]

# Validation block
_word_colors = set(WORD_MEANING_MAP.values())
_key_colors = set(KEY_COLOR_MAP.values())

# Check that all semantic colors have an associated key
if not _word_colors.issubset(_key_colors):
    raise ValueError("Validation failed: Not all colors in WORD_MEANING_MAP exist in KEY_COLOR_MAP values.")

# Check for duplicate keys in KEY_COLOR_MAP (keys in a dict are implicitly unique, but let's check for duplicate color targets if needed, though multiple keys for same color might be valid. The prompt says "Verificar que não há teclas duplicadas no KEY_COLOR_MAP", a dict inherently enforces unique keys, but we can check if keys are distinct).
if len(KEY_COLOR_MAP) != len(set(KEY_COLOR_MAP.keys())):
    raise ValueError("Validation failed: Duplicate keys found in KEY_COLOR_MAP.")
