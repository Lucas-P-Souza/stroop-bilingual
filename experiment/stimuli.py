"""
Generates trial lists for the Stroop experiment based on configuration.
"""
import random
from typing import Any
from experiment import config_experiment

def generate_factorial_table() -> list[dict[str, Any]]:
    """
    Generates all combinations of stimuli from the config.
    Returns a list of trial dictionaries.
    """
    trials = []
    
    # Invert key mapping to easily find the correct key for a given color
    color_to_key = {color: key for key, color in config_experiment.KEY_COLOR_MAP.items()}
    
    for word, meaning_color in config_experiment.WORD_MEANING_MAP.items():
        for display_color in config_experiment.KEY_COLOR_MAP.values():
            congruency = "congruent" if meaning_color == display_color else "incongruent"
            
            # The correct response is based on the display color, not the word's meaning
            correct_response = color_to_key[display_color]
            
            trials.append({
                "word": word,
                "color": display_color,
                "congruency": congruency,
                "correct_response": correct_response
            })
            
    return trials

def generate_practice_trials(seed: int | None = None) -> list[dict[str, Any]]:
    """
    Returns a randomized list of N_PRACTICE_TRIALS trials sampled from the factorial table.
    """
    use_seed = seed if seed is not None else config_experiment.RANDOM_SEED
    rng = random.Random(use_seed)
    
    factorial_table = generate_factorial_table()
    practice_trials = []
    
    # If practice trials are more than the factorial table, we repeat the table
    while len(practice_trials) < config_experiment.N_PRACTICE_TRIALS:
        shuffled_table = list(factorial_table)
        rng.shuffle(shuffled_table)
        practice_trials.extend(shuffled_table)
        
    # Trim to exact requested length
    return practice_trials[:config_experiment.N_PRACTICE_TRIALS]

def generate_experimental_trials(seed: int | None = None) -> list[dict[str, Any]]:
    """
    Repeats the factorial table N_EXPERIMENTAL_REPETITIONS times and randomizes.
    Adds a 1-indexed trial_number.
    """
    use_seed = seed if seed is not None else config_experiment.RANDOM_SEED
    rng = random.Random(use_seed)
    
    factorial_table = generate_factorial_table()
    experimental_trials = []
    
    for _ in range(config_experiment.N_EXPERIMENTAL_REPETITIONS):
        experimental_trials.extend(factorial_table)
        
    rng.shuffle(experimental_trials)
    
    # Add trial numbers
    for idx, trial in enumerate(experimental_trials):
        # Create a new dict to avoid modifying the original factorial table references
        experimental_trials[idx] = trial.copy()
        experimental_trials[idx]["trial_number"] = idx + 1
        
    return experimental_trials
