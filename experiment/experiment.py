"""
Main execution script for the Stroop experiment using PsychoPy.
"""
import os
import csv
from psychopy import visual, event, core, gui

from experiment import config_experiment
from experiment import stimuli
from experiment import instructions


def run() -> None:
    """Run the complete Stroop experiment."""
    
    # 1. DIÁLOGO DE COLETA DE DADOS DO PARTICIPANTE (METADADOS)
    dlg_info = {
        "Experimenter / Expérimentateur *": config_experiment.RESEARCHERS,
        "Age / Âge *": "",
        "Gender / Genre *": config_experiment.SEX_OPTIONS,
        "Native Language / Langue Maternelle *": config_experiment.L1_OPTIONS,
        "French Level / Niveau de Français *": config_experiment.FRENCH_LEVEL_OPTIONS,
        "Glasses or Contacts / Lunettes ou Lentilles *": config_experiment.GLASSES_OPTIONS
    }
    
    # Loop para garantir que o formulário seja preenchido (impede fechar no 'Enter' acidental)
    while True:
        dlg = gui.DlgFromDict(dictionary=dlg_info, title="Stroop Experiment - Metadata / Metadonnées")
        
        if not dlg.OK:
            print("Experiment cancelled by the user.")
            return
            
        # Check if any field was left completely blank
        if any(val == "" for val in dlg_info.values()):
            err = gui.Dlg(title="Error / Erreur")
            err.addText("Please fill in all fields marked with * \nVeuillez remplir tous les champs marqués d'un *")
            err.show()
            continue
            
        break
        
    researcher = dlg_info["Experimenter / Expérimentateur *"]
    participant_age = dlg_info["Age / Âge *"]
    participant_sex = dlg_info["Gender / Genre *"]
    l1_language = dlg_info["Native Language / Langue Maternelle *"]
    french_level_self = dlg_info["French Level / Niveau de Français *"]
    wearing_glasses = dlg_info["Glasses or Contacts / Lunettes ou Lentilles *"]
    
    # Check if they are native. If not, ask for certification.
    if "Native" not in french_level_self:
        dlg_cert_info = {
            "Certification (DELF/TCF) *": config_experiment.CERTIFICATION_OPTIONS
        }
        while True:
            dlg_cert = gui.DlgFromDict(dictionary=dlg_cert_info, title="French Certification / Certification de Français")
            
            if not dlg_cert.OK:
                print("Experiment cancelled by the user.")
                return
                
            if dlg_cert_info["Certification (DELF/TCF) *"] == "":
                err = gui.Dlg(title="Error / Erreur")
                err.addText("Please fill in all fields marked with * \nVeuillez remplir tous les champs marqués d'un *")
                err.show()
                continue
                
            break
            
        french_certification = dlg_cert_info["Certification (DELF/TCF) *"]
    else:
        french_certification = "Native / Natif"
    
    # 2. GERAÇÃO AUTOMÁTICA DE ID INVIOLÁVEL
    if not os.path.exists(config_experiment.OUTPUT_DIR):
        os.makedirs(config_experiment.OUTPUT_DIR)
        
    prefix = f"participant_{researcher}_"
    existing_files = [f for f in os.listdir(config_experiment.OUTPUT_DIR) if f.startswith(prefix) and f.endswith(".csv")]
    next_num = len(existing_files) + 1
    participant_id = f"{researcher}_{next_num:03d}"  # Ex: Lucas_001
    
    win = None
    try:
        # 3. SETUP
        win = visual.Window(
            size=config_experiment.WINDOW_SIZE,
            fullscr=config_experiment.FULLSCREEN,
            color=config_experiment.BG_COLOR,
            units="pix"
        )
        
        # Clock for measuring reaction times
        clock = core.Clock()
        
        # Reusable TextStim instances
        fixation_stim = visual.TextStim(
            win=win,
            text="+",
            color=config_experiment.TEXT_COLOR,
            height=config_experiment.STIMULUS_FONT_SIZE
        )
        
        instruction_stim = visual.TextStim(
            win=win,
            color=config_experiment.TEXT_COLOR,
            height=config_experiment.INSTRUCTION_FONT_SIZE,
            wrapWidth=int(config_experiment.WINDOW_SIZE[0] * 0.8)
        )
        
        stimulus_stim = visual.TextStim(
            win=win,
            height=config_experiment.STIMULUS_FONT_SIZE,
            bold=True,
            font='Arial'
        )
        
        # Generate trials
        practice_trials = stimuli.generate_practice_trials()
        experimental_trials = stimuli.generate_experimental_trials()
        
        # Buffer to store all results
        results_buffer = []
        
        # Helper to run a trial
        global_trial_counter = 1
        
        def run_trial(trial: dict, block_name: str) -> dict:
            nonlocal global_trial_counter
            
            # Show fixation
            fixation_stim.draw()
            win.flip()
            core.wait(config_experiment.FIXATION_DURATION)
            
            # Show stimulus
            stimulus_stim.text = trial["word"]
            stimulus_stim.color = trial["color"]
            stimulus_stim.draw()
            
            # Clear previous events and reset clock exactly when stimulus appears
            event.clearEvents()
            win.flip()
            clock.reset()
            
            # Wait for response
            keys = event.waitKeys(
                keyList=list(config_experiment.KEY_COLOR_MAP.keys()),
                maxWait=config_experiment.RESPONSE_TIMEOUT,
                timeStamped=clock
            )
            
            if keys:
                response, rt_sec = keys[0]
                rt_ms = rt_sec * 1000.0
            else:
                response = "none"
                rt_ms = (config_experiment.RESPONSE_TIMEOUT * 1000.0) if config_experiment.RESPONSE_TIMEOUT is not None else -1.0
            is_correct = 1 if response == trial["correct_response"] else 0
            
            # Blank screen (ISI)
            win.flip()
            core.wait(config_experiment.ISI_DURATION)
            
            trial_result = {
                "participant_id": participant_id,
                "age": participant_age,
                "sex": participant_sex,
                "l1_language": l1_language,
                "french_level_self": french_level_self,
                "french_certification": french_certification,
                "wearing_glasses": wearing_glasses,
                "trial_number": global_trial_counter,
                "block": block_name,
                "word": trial["word"],
                "color": trial["color"],
                "congruency": trial["congruency"],
                "correct_response": trial["correct_response"],
                "response": response,
                "response_time_ms": rt_ms,
                "correct": is_correct
            }
            
            global_trial_counter += 1
            return trial_result

        # 3. TELA DE INSTRUÇÕES
        instruction_stim.text = instructions.build_instruction_text(config_experiment.KEY_COLOR_MAP)
        instruction_stim.draw()
        win.flip()
        event.clearEvents()
        event.waitKeys()
        
        # 4. BLOCO DE TREINO
        practice_correct = 0
        practice_rts = []
        
        for trial in practice_trials:
            res = run_trial(trial, "practice")
            results_buffer.append(res)
            
            if res["response"] != "none":
                practice_rts.append(res["response_time_ms"])
            if res["correct"] == 1:
                practice_correct += 1
                
        # 5. FEEDBACK DO TREINO
        mean_rt = sum(practice_rts) / len(practice_rts) if practice_rts else 0.0
        accuracy = (practice_correct / len(practice_trials)) * 100.0 if practice_trials else 0.0
        
        instruction_stim.text = instructions.build_practice_feedback_text(mean_rt, accuracy)
        instruction_stim.draw()
        win.flip()
        event.clearEvents()
        event.waitKeys()
        
        # 6. TRANSIÇÃO
        instruction_stim.text = instructions.build_end_practice_text()
        instruction_stim.draw()
        win.flip()
        event.clearEvents()
        event.waitKeys()
        
        # 7. BLOCO EXPERIMENTAL
        for trial in experimental_trials:
            res = run_trial(trial, "experimental")
            results_buffer.append(res)
            
        # 8. TELA FINAL
        instruction_stim.text = instructions.build_end_experiment_text()
        instruction_stim.draw()
        win.flip()
        event.clearEvents()
        event.waitKeys()
        
        # 9. SALVAMENTO DO CSV
        if not os.path.exists(config_experiment.OUTPUT_DIR):
            os.makedirs(config_experiment.OUTPUT_DIR)
            
        filename = config_experiment.FILENAME_PATTERN.format(participant_id=participant_id)
        filepath = os.path.join(config_experiment.OUTPUT_DIR, filename)
        
        with open(filepath, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=config_experiment.CSV_COLUMNS)
            writer.writeheader()
            for row in results_buffer:
                writer.writerow(row)
                
    except Exception as e:
        import traceback
        print("\n\n=== ERRO NO EXPERIMENTO ===")
        traceback.print_exc()
        print("===========================\n\n")
        raise e
    finally:
        # 10. CLEANUP
        if win is not None:
            win.close()
        core.quit()
