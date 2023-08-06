import os
from split_datalawyer.sentences.sentence_split import SentenceSplit

#files = ["example1.txt", "example2.txt", "example3.txt", "example4.txt", "example5.txt", "example6.txt", "example7.txt", "example8.txt", "example9.txt", "example10.txt"]
files = ["Acórdão_0010006-57.2020.5.03.0131-788ee38.txt"]
files_content = []

local_path = os.path.dirname(__file__)

for file in files:
    
    with open(os.path.join(local_path, file), "r", encoding="utf8") as fs:
        content = fs.read()
        files_content.append((file, content))

sentence_spliter = SentenceSplit(debug_log=True)

for file_content in files_content:
    
    text_splitted = sentence_spliter.get_sentences(file_content[1], split_by_semicolon=False)
    # Using stanza
    #text_splitted = sentence_spliter.get_sentences_with_stanza(file_content[1])
    result_file = os.path.join(local_path, file_content[0] + ".splitted")

    with open(result_file, "w", encoding='utf8') as fs:
        for text in text_splitted:
            fs.write(text + "\n")

sentence_spliter.generate_log()