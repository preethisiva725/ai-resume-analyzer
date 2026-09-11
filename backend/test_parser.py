from app.services.document_parser import extract_text

file_path = r"C:\Users\Admin\ai-resume-analyzer\backend\uploads\Preethi_S_Resume.pdf"

text = extract_text(file_path)

print("----- EXTRACTED TEXT -----")
print(text)
print("----- END OF TEXT -----")