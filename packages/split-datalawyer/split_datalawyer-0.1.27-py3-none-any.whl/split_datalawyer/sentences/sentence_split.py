import pandas as pd
import os
import re

import stanza

from split_datalawyer.sentences.split_utils import split_by_sentence, split_by_break

__DEFAULT_STOP_PHRASES__ = 'stoppatterns.txt'
__ENDING_PUNCTUATION_TUPLE__ = tuple([".", ";", ":", "\"", "!", "?", ")"])
__REGEX_NUMERO_SECAO__ = re.compile(r"^[0-9]{1,}(\.[0-9]+)?\.$")  # "1.0", "4.2", etc


class SentenceSplit():

    def __init__(self, stop_patterns_path=__DEFAULT_STOP_PHRASES__, debug_log=False):

        self._list_stop_patterns = self._get_stop_patterns(stop_patterns_path)
        self._list_abbreviations = self._get_abbreviations()
        self._stanza_model = None
        self._debug_log = debug_log
        self._debug_messages = []

    def _log(self, message):
        if self._debug_log:
            self._debug_messages.append(message)

    def generate_log(self):
        if self._debug_log:
            with open("sentence_split_log.txt", mode='w', encoding='utf8') as log_file:
                for message in self._debug_messages:
                    log_file.write(message + "\n")

    def _get_abbreviations(self):
        abbreviations_path = os.path.join(self._get_local_directory(), "lista_abreviacoes.csv")
        f = open(abbreviations_path, "r", encoding='utf-8')
        abbreviations = f.readlines()
        f.close()

        return [x.replace("\n", "") + "." for x in abbreviations]

    def _get_local_directory(self):
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)

        return dname

    def _get_stop_patterns(self, stop_patterns_path):
        if stop_patterns_path == __DEFAULT_STOP_PHRASES__:
            stop_patterns_path = os.path.join(self._get_local_directory(), stop_patterns_path)

        f = open(stop_patterns_path, encoding='utf-8')
        phrase_list = f.readlines()
        f.close()

        return [re.compile(x.replace("\n", "")) for x in phrase_list]

    def _parenthesis_is_closed(self, phrase):
        if phrase != "":
            if phrase.count("(") > phrase.count(")") or phrase.rfind(")") < phrase.rfind("("):
                return False

        return True

    def _concat_inverted_phrases(self, df):
        df = df[df['final_text'] != ""]
        df = df.sort_values('index').reset_index(drop=True)

        for i in range(1, len(df['final_text'])):
            previous_text = df['final_text'][i - 1]
            current_text = df['final_text'][i]

            if current_text != "":
                if i + 1 < len(df['final_text']):
                    next_text = df['final_text'][i + 1]

                    previous_has_end = previous_text.endswith(__ENDING_PUNCTUATION_TUPLE__)
                    current_text_starts_lower = current_text[0].islower()
                    current_text_has_end = current_text.endswith(__ENDING_PUNCTUATION_TUPLE__)
                    next_has_not_end = not next_text.endswith(__ENDING_PUNCTUATION_TUPLE__)
                    next_text_is_not_option = re.match(r"^\w\)", next_text) is None

                    if current_text_starts_lower and \
                            current_text_has_end and \
                            previous_has_end and \
                            next_has_not_end and \
                            next_text_is_not_option:
                        df.at[i + 1, 'final_text'] = next_text + " " + current_text
                        df.at[i, 'final_text'] = ""
                        self._log("_concat_inverted_phrases: " + next_text + " " + current_text)

        return df

    def _concat_broken_phrases(self, df):
        continuation_terms = ["no", "na", "nos", "nas", "de", "do", "da", "dos", "das", ",", "sua", "pela"]
        df['final_text'] = df['text']
        last_index_with_text = None

        for i in range(len(df['final_text'])):
            current_text = df['final_text'][i].strip()

            if current_text == "":
                continue

            end_with_punctuation = current_text.endswith(__ENDING_PUNCTUATION_TUPLE__)
            all_text_upper = current_text.isupper() and len(current_text) > 1
            parenthesis_not_closed = not self._parenthesis_is_closed(current_text)
            search_phrase_continuation = ((not end_with_punctuation) and (not all_text_upper)) or (
                    parenthesis_not_closed and (not end_with_punctuation))
            phrase_has_continuation = False

            if last_index_with_text != None:
                last_text_processed = df['final_text'][last_index_with_text]

                if current_text.startswith(tuple(["(", "R$"])):
                    if last_text_processed.endswith(__ENDING_PUNCTUATION_TUPLE__):
                        df.at[last_index_with_text, 'final_text'] = " ".join([last_text_processed, current_text])
                        df.at[i, 'final_text'] = ""

                if __REGEX_NUMERO_SECAO__.match(last_text_processed):
                    df.at[last_index_with_text, 'final_text'] = " ".join([last_text_processed, current_text])
                    df.at[i, 'final_text'] = ""
                    self._log("")

            if search_phrase_continuation:
                phrases_parts_index = []
                previous_phrase_index = 1
                waiting_close_parenthesis = parenthesis_not_closed

                for j in range(i + 1, len(df['final_text'])):
                    next_text = df['final_text'][j]
                    next_text_was_duplicated = bool(df['duplicated'][j])

                    if (next_text == "" or next_text_was_duplicated):
                        previous_phrase_index = previous_phrase_index + 1
                        if next_text_was_duplicated:
                            self._log("_concat_broken_phrases: next_text_was_duplicated: " + next_text)
                        continue

                    previous_text = ""
                    if j - previous_phrase_index >= 0:
                        previous_text = df['final_text'][j - previous_phrase_index]

                    previous_ends_with_continuation = previous_text != "" and \
                                                      (previous_text.split()[-1] in continuation_terms)

                    if not waiting_close_parenthesis:
                        waiting_close_parenthesis = not self._parenthesis_is_closed(next_text)

                    # Not allow concatenate parts with high difference distance.
                    parts_not_too_long_distance = ((len(phrases_parts_index) > 0) and
                                                   max(phrases_parts_index) - j <= 5) \
                                                  or (j - i <= 5)

                    if (next_text.split()[0][0].islower() or
                        previous_ends_with_continuation or
                        waiting_close_parenthesis) and \
                            parts_not_too_long_distance:
                        phrases_parts_index.append(j)
                        next_text_end_not_with_abbreviation = not next_text.split()[-1] in self._list_abbreviations

                        if next_text.endswith(__ENDING_PUNCTUATION_TUPLE__) and \
                                next_text_end_not_with_abbreviation and \
                                waiting_close_parenthesis:
                            self._log("waiting_close_parenthesis: " + df['final_text'][j])

                        if waiting_close_parenthesis:
                            waiting_close_parenthesis = not (next_text.count(")") > next_text.count("("))

                        # go_concatenate = next_text.endswith(__ENDING_PUNCTUATION_TUPLE__) and next_text_end_not_with_abbreviation and (not waiting_close_parenthesis)
                        go_concatenate = next_text.endswith(
                            __ENDING_PUNCTUATION_TUPLE__) and next_text_end_not_with_abbreviation
                        if go_concatenate:
                            phrase_has_continuation = True
                            break
                    else:
                        if len(phrases_parts_index) > 0:
                            phrase_parts_log = "[" + "| ".join(
                                [df['final_text'][index] for index in phrases_parts_index]) + "]"

                            if (len(phrases_parts_index) >= 3) or parenthesis_not_closed:
                                phrase_has_continuation = True
                                self._log("_concat_broken_phrases: threshold pass: " + phrase_parts_log)
                            else:
                                self._log(
                                    "_concat_broken_phrases: ignored_parts: " + phrase_parts_log + " next_text: " + next_text)

                        break

                end_of_phrase = ""
                if phrase_has_continuation:
                    for part_index in phrases_parts_index:
                        phrase_part = df['final_text'][part_index]
                        end_of_phrase = end_of_phrase + " " + phrase_part
                        df.at[part_index, 'final_text'] = ""

                    if end_of_phrase != "":
                        df.at[i, 'final_text'] = current_text + " " + end_of_phrase.strip()

            last_index_with_text = i

        return df

    def _remove_small_phrases(self, df, minimium_word_count=3):
        if minimium_word_count > 0:
            df['final_text'] = df['text']

            for i in range(len(df['final_text'])):
                phrase_is_small = len(df['final_text'][i].split()) < minimium_word_count

                if phrase_is_small:
                    df.at[i, 'final_text'] = ""

        return df

    def _remove_duplicates(self, df, remove_stop_phrases):
        df = df[df['text'] != ""]
        df = df.sort_values(['text', 'index']).reset_index(drop=True)
        duplicated_phrases = list(df[df['duplicated']]['text'])
        self._log("_remove_duplicates: duplicated_phrases: [" + '| '.join(duplicated_phrases) + "]")

        previous_value = ""
        phrases_count = len(df['text'])
        for i in range(phrases_count):
            reserve_index = phrases_count - i - 1
            current_value = df['text'][reserve_index]

            both_equals = previous_value == current_value
            is_number_page = current_value.isdigit()
            if is_number_page:
                self._log("is_number_page: " + current_value)

            is_stop_phrase = remove_stop_phrases and any(
                regex.match(current_value) for regex in self._list_stop_patterns)

            remove_text = both_equals or is_number_page or is_stop_phrase

            if (remove_text):
                df.at[reserve_index, 'text'] = ""

            if (df['text'][reserve_index] != ""):
                previous_value = df['text'][reserve_index]

        df = df[df['text'] != ""]
        df = df.sort_values('index').reset_index(drop=True)

        return df

    def _split_by_punctuation(self, df, split_by_semicolon):
        column_name = 'text'

        if "final_text" in df.columns:
            column_name = 'final_text'

        df = df[df[column_name] != ""]

        phrase_list = []

        for index, row in df.iterrows():
            text = row[column_name]
            duplicated = row['duplicated']
            phrases = split_by_sentence(text, split_by_semicolon)
            phrase_list.extend([{"duplicated": duplicated, "text": phrase} for phrase in phrases])

        temp_object_list = [
            {'index': index, 'text': phrase_list[index]["text"], 'duplicated': phrase_list[index]["duplicated"]}
            for index in range(len(phrase_list))]

        df_splited = pd.DataFrame(temp_object_list)

        return df_splited

    def get_sentences(self, text, remove_duplicated=True, concat_phrases=True, concat_inverted_phrases=True,
                      remove_stop_phrases=True, minimium_word_count=0, split_by_semicolon=True):
        if (text is None) or text == "":
            return None

        df = self.get_sentences_with_index(text,
                                           remove_duplicated=remove_duplicated,
                                           concat_phrases=concat_phrases,
                                           concat_inverted_phrases=concat_inverted_phrases,
                                           remove_stop_phrases=remove_stop_phrases,
                                           minimium_word_count=minimium_word_count,
                                           split_by_semicolon=split_by_semicolon)

        if df is not None:
            column_name = 'text'

            if "final_text" in df.columns:
                column_name = 'final_text'

            df = df[df[column_name] != ""]
            sentences = list(df[column_name])

            return sentences

        return []

    def get_sentences_with_index(self, text, remove_duplicated=True, concat_phrases=True, concat_inverted_phrases=True,
                                 remove_stop_phrases=True, minimium_word_count=0, split_by_semicolon=True):
        if (text is None) or text == "":
            return None

        sentence_list = split_by_break(text)
        temp_object_list = [{'index': index, 'text': sentence_list[index]}
                            for index in range(len(sentence_list))]

        df = pd.DataFrame(temp_object_list)
        df = df[df['text'] != ""]

        if df.empty:
            return None

        # Mark duplicate text even if do not remove it.
        df['duplicated'] = df['text'].duplicated(False)

        if remove_duplicated:
            df = self._remove_duplicates(df, remove_stop_phrases)

        if df.empty:
            return None

        df = self._split_by_punctuation(df, split_by_semicolon)

        if concat_phrases:
            df = self._concat_broken_phrases(df)

            if concat_inverted_phrases:
                df = self._concat_inverted_phrases(df)

        if minimium_word_count > 0:
            df = self._remove_small_phrases(df, minimium_word_count)

        df = df[df['text'] != ""]
        df = df.sort_values('index').reset_index(drop=True)
        df['index'] = df.index

        return df

    def get_sentences_with_stanza(self, text):
        if (text is None) or text == "":
            return None

        if self._stanza_model is None:
            stanza.download('pt')

            self._stanza_model = stanza.Pipeline('pt', processors='tokenize')

        text = re.sub("\x0C", "\n", text)
        text = text.replace("\n", " ")

        sentences_result = []

        if text != "":
            doc = self._stanza_model(text)

            sentence_to_add = ""
            for i, sentence_obj in enumerate(doc.sentences):
                sentence = sentence_obj.text

                end_with_abbreviation = sentence.split()[-1] in self._list_abbreviations

                if end_with_abbreviation:
                    sentence_to_add = sentence + " "
                else:
                    sentence_to_add = sentence_to_add + sentence

                if not end_with_abbreviation:
                    sentences_result.append(sentence_to_add)
                    sentence_to_add = ""

        return sentences_result
