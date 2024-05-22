import json
import traceback
from PyPDF2 import PdfReader

def ReadFile(file):
    try:
        if file.name.endswith(".pdf"):
            pdf_reader = PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() if page.extract_text() else ""
            return text
        elif file.name.endswith(".txt"):
            return file.read().decode('utf-8')
        else:
            raise Exception('Unsupported file format. Please use only PDF and text files.')
    except Exception as e:
        raise Exception('Error while reading the file: ' + str(e))

def GetTableData(quiz_str):
    try:
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []
        for key, value in quiz_dict.items():
            mcq = value["mcq"]
            options = " || ".join(
                [f"{option}: {option_value}" for option, option_value in value["options"].items()]
            )
            correct = value["correct"]
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})
        return quiz_table_data
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False
