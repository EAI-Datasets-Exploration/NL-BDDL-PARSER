import configparser
import json
import tkinter as tk
from tkinter import messagebox, Scrollbar, Text

from nl_bddl_parser.annotations_gui.helper import get_unique_commands


def run_gui(annotation_config_fp: str):
    # Load your dataset (assuming you have a CSV with a 'Text' column)
    config = configparser.ConfigParser()
    config.read(annotation_config_fp)

    # Load Configuration Variables
    dataset_dir_path = config["paths"]["dataset_dir_path"]
    results_dir = config["paths"]["results_dir"]

    dataset_name = config["experiment"]["dataset_name"]

    with open(f"{dataset_dir_path}metadata.json", "r", encoding="utf-8") as json_file:
        # The metadata file referenced here is contained in the repo:
        # dataset-download-scripts package hosted in the larger GitHub group.
        metadata_dict = json.load(json_file)

    ds_path = metadata_dict[dataset_name]

    nl_column = "nl_instructions"

    # Begin text feature processing
    df = get_unique_commands(dataset_dir_path + ds_path, nl_column=nl_column)

    class AnnotationApp:
        def __init__(self, root):
            self.root = root
            self.root.title("Text Annotation Tool")

            # Configure the grid layout to expand widgets when resized
            root.grid_columnconfigure(0, weight=1)
            root.grid_rowconfigure(1, weight=1)

            self.current_index = 0

            # Display the original text
            self.text_label = tk.Label(
                root, text="Text to annotate", wraplength=400, justify="left"
            )
            self.text_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

            # Text field for multi-line annotation
            self.annotation_textbox = Text(root, width=50, height=10, wrap="word")
            self.annotation_textbox.grid(
                row=1, column=0, padx=10, pady=10, sticky="nsew"
            )

            # Add a vertical scrollbar for the annotation textbox
            self.scrollbar = Scrollbar(root, command=self.annotation_textbox.yview)
            self.scrollbar.grid(row=1, column=1, sticky="ns")
            self.annotation_textbox.config(yscrollcommand=self.scrollbar.set)

            # Button to save annotation
            self.save_button = tk.Button(
                root, text="Save Annotation", command=self.save_annotation
            )
            self.save_button.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

            # Button to go to the next text
            self.next_button = tk.Button(root, text="Next Text", command=self.next_text)
            self.next_button.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

            # Display the first text
            self.display_text()

        def display_text(self):
            if self.current_index < len(df):
                text = df.loc[self.current_index, nl_column]
                self.text_label.config(text=text)
                self.annotation_textbox.delete("1.0", tk.END)
            else:
                self.text_label.config(text="No more text to annotate.")
                self.annotation_textbox.config(state="disabled")

        def save_annotation(self):
            if self.current_index < len(df):
                annotation = self.annotation_textbox.get(
                    "1.0", tk.END
                ).strip()  # Get multiline input
                text = df.loc[self.current_index, nl_column]

                # Save the text and annotation to a CSV file

                with open(
                    f"{results_dir}/{dataset_name}_annotations.csv",
                    "a",
                    encoding="utf-8",
                ) as f:
                    f.write(f'"{text}","{annotation}"\n')

                messagebox.showinfo("Saved", "Annotation saved successfully!")

        def next_text(self):
            self.current_index += 1
            self.display_text()

    # Create the main window
    root = tk.Tk()

    # Set the window to a larger size (optional)
    root.geometry("600x400")

    app = AnnotationApp(root)
    root.mainloop()
