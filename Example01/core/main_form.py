from PyPDF2 import PdfReader
import pandas as pd
from IPython.display import display
import numpy as np
import os


def extract_data(file_path: str = "data/report_lovegood.pdf"):
	reader = PdfReader(file_path)

	fields = reader.get_fields()
	data = {key: value.get('/V', '') for key, value in fields.items()}
	#for name, field in fields.items():
	#	print(f"{name}: {field.get('/V', '')}")
	#print(data)

	data = pd.DataFrame([data])
	data = data.loc[:, ~(data == "").all()]
	#display(data)
	#for _, row in data.iterrows():
	#	print(row)
	return data


def transform_data(data):
	metadata = {}
	row_data = {}

	for key, value in data.items():
		value = clean_val(value[0])

		# falls wir "Row" im key haben, handelt es sich um tabellarische Information...
		if "Row" in key:
			
			# alle mögliche Präfixe durchlaufen
			for prefix in ["NameRow", "DescriptionRow", "Starting DateRow", "Ending DateRow"]:


				if key.startswith(prefix):

					# "Row" aus dem Präfix entfernen
					field_name = prefix.replace("Row", "")

					# "NameRow", "DescriptionRow", etc. entfernen -> nur die Zeilennummer bleibt übrig
					row_idx = key.replace(prefix, "")
					if row_idx.isdigit():
						row_idx = int(row_idx)
						if row_idx not in row_data:
							row_data[row_idx] = {}
						row_data[row_idx][field_name] = value
					break
		
		# ... ansonsten sind es Metadaten
		else:
			metadata[key] = value

	# alles in ein pandas dataframe überschreiben
	tabulardata_df = pd.DataFrame.from_dict(row_data, orient="index").dropna(how="all")
	metadata_df = pd.DataFrame.from_dict(metadata, orient="index").dropna(how="all")
	return metadata_df, tabulardata_df


def load_data(data: list[pd.DataFrame, pd.DataFrame], save_path: str, file_name: str):
	os.makedirs(save_path, exist_ok=True)

	# dataframes als csv-files speichern
	metadata_path = os.path.join(save_path, f"{file_name}_metadata.csv")
	data[0].to_csv(metadata_path, index=True)
	print("Metadata saved to:", metadata_path)

	tabulardata_path = os.path.join(save_path, f"{file_name}_tabulardata.csv")
	data[1].to_csv(tabulardata_path, index=True)
	print("Tabular data saved to:", tabulardata_path)
	return print("Loading successful.")


def clean_val(value):
	choices = ["Yes", "No"]

	# falls der Eintrag nur ein Wort lang ist, handelt es sich vermutlich um Ja/Nein Antworten
	one_word = len(value.split())<2

	mask = [name in value for name in choices if one_word]
	if any(mask):
		choice = choices[np.where(mask)[0][0]]
		return choice
	else:
		return value


def process_form(file_name: str = "report_lovegood", save_dir: str = "data/results"):

	file_path = os.path.join("data", f"{file_name}.pdf")
	data = extract_data(file_path)
	transformed_data = transform_data(data)
	load_data(transformed_data, save_dir, file_name)

	

if __name__ == "__main__":
	process_form(file_name="report_lovegood")
	process_form(file_name="report_weasley")