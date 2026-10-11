"""
Bilingual (French/English) instructions and feedback texts for the Stroop experiment.
"""
from experiment import config_experiment

def build_instruction_text(key_color_map: dict[str, str]) -> str:
    """
    Generates the main instruction text dynamically based on the current key map.
    """
    lines = [
        "Appuyez sur la touche correspondant à la COULEUR de l'encre.",
        "Press the key corresponding to the INK COLOR.",
        ""
    ]
    
    color_fr = {"red": "ROUGE", "yellow": "JAUNE", "green": "VERT", "blue": "BLEU"}
    color_en = {"red": "(Red)", "yellow": "(Yellow)", "green": "(Green)", "blue": "(Blue)"}

    mapping_parts = []
    for key, color in key_color_map.items():
        fr_word = color_fr.get(color, color.upper())
        en_word = color_en.get(color, f"({color})")
        mapping_parts.append(f"[{key}] = {fr_word} {en_word}")

    mapping_str = "\n".join(mapping_parts)
    
    lines.append(mapping_str)
    lines.append("")
    lines.append("Ignorez le mot écrit. Répondez le plus rapidement possible.")
    lines.append("Ignore the written word. Respond as quickly as possible.")
    lines.append("\nAppuyez sur une touche pour commencer l'entraînement.")
    lines.append("Press any key to start the practice.")
    
    return "\n".join(lines)

def build_practice_feedback_text(mean_rt_ms: float, accuracy_pct: float) -> str:
    """
    Generates the feedback text after the practice block.
    """
    return (
        f"Fin de l'entraînement / End of practice.\n\n"
        f"Temps de réaction moyen / Mean RT: {round(mean_rt_ms)} ms\n"
        f"Précision / Accuracy: {round(accuracy_pct)} %\n\n"
        f"Appuyez sur une touche pour commencer le test.\n"
        f"Press any key to start the real test."
    )

def build_end_practice_text() -> str:
    """
    Generates the text for transitioning from practice to the real test.
    """
    return (
        "Appuyez sur une touche pour commencer le test réel.\n"
        "Press any key to start the real test."
    )

def build_end_experiment_text() -> str:
    """
    Generates the final thank you text.
    """
    return (
        "Merci pour votre participation !\n"
        "Thank you for your participation!\n\n"
        "Appuyez sur une touche pour quitter.\n"
        "Press any key to exit."
    )
