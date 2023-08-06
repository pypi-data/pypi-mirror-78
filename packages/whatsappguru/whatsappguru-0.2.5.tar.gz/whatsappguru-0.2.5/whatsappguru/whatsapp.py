"""
whatsapp
--------
This script contains
the WhatsApp class

Date: 2020-05-31

Author: Lorenzo Coacci
"""
# + + + + + Libraries + + + + +
# to manage regex
import re
# to manage dataframes
import pandas as pd
# import os
import os
# golog
from golog import (
    list_print, sev,
    warning_print,
    error_print, correct_filepath,
    filepath_exists
)
# optional packages
try:    
    # to manage emoji
    import emoji
    # uuid record of a message
    import uuid
    # to create progress bars
    from progressbar import progressbar
    # import iago for audio 2 text
    from iago import Iago
except ImportError as exc:
    print(
        f"""
        Some packages were not installed.
        Did you pip install everything? -> {str(exc)}
        """
    )
# + + + + + Libraries + + + + +


# + + + + + Settings + + + + +
HOME = os.path.expanduser("~")
# + + + + + Settings + + + + +


# + + + + + Classes + + + + +
class WhatsApp:
    """
    WhatsApp : A python class for WhatsApp

    Parameters
    ----------
    TODO : add params
    """
    def __init__(
        self,
        chat_folder_name="WhatsApp Chat - ",
        chat_file_name="_chat.txt",
        language='en-US',
        debug=False
    ):
        # - - Init WhatsApp - -
        self.debug = bool(debug)
        self.language = str(language)
        self.chat_file_name = str(chat_file_name)
        self.chat_folder_name = str(chat_folder_name)

    # + + + + + Chat MAIN + + + + +    
    @sev
    def chat_to_df(
        self,
        content, chat_from,
        min_lines_threshold=1000
    ):
        """
        RETURN : {
            "status": True/False, "error": error_msg,
            "value": df (DataFrame pandas)
        }
        converts a txt chat in a Data Frame according to a regex
    
        Parameters
        ----------
        content : string
            The string content of the chat .txt
        chat_from (optional) : string
            The chat provider
    
        Returns
        -------
        result : {
            "status": True/False,
            "error": error_msg,
            "value": df (DataFrame pandas)
        }
        """
        # get chat data
        if chat_from is None:
            error_print(f"Chat from is None")
            return None
        elif chat_from == "whatsapp":
            chat = self.parse_whatsapp(content)['value']
        elif chat_from == "wechat":
            # TODO
            pass
        elif chat_from == "tinder":
            # TODO
            pass
        elif chat_from == "messanger":
            # TODO
            pass
        elif chat_from == "slack":
            # TODO
            pass
        else:
            error_print(f"Chat {chat_from} not supported")
            return None
        
        # enough records?
        _len_chat = len(chat)
        if min_lines_threshold is not None:
            if _len_chat < min_lines_threshold:
                warning_print("This chat is too short for an analysis.")
        
        # - - to df - -
        df = pd.DataFrame(columns=[
            "datetime", "who", "message"
        ])
    
        # datetime to a decent format
        def correct_datetime(datetime_tuple):
                # unpack tuple
                date_string, time_string = datetime_tuple
    
                # correct date
                date_string_chunks = date_string.split('/')
                new_chunks = [
                    '0' + chunk if len(chunk) != 2 else chunk
                    for chunk in date_string_chunks
                ]
                # re build date string
                date_string = '/'.join(new_chunks)
    
                # correct time
                time_string_chunks = time_string.split(' ')[0].split(':')
                am_pm = time_string.split(' ')[1]
                new_chunks = [
                    '0' + chunk if len(chunk) != 2 else chunk
                    for chunk in time_string_chunks
                ]
                # re build date string
                time_string = ':'.join(new_chunks)
                time_string += " {}".format(am_pm)
    
                # datetime correct
                datetime_correct = date_string + ', ' + time_string
                return datetime_correct
    
        # remove decorators around media file path
        def correct_media(media_string):
            if "<attached " in media_string:
                media_string = media_string.replace('<attached ', '')
                media_string = media_string.replace('>', '')
                media_string = media_string.replace('\n', '')
                media_string = media_string.strip()
            return media_string
        
        # fill df
        for i in range(_len_chat):
            df = df.append(
                {
                    "datetime": correct_datetime((chat[i][0][0], chat[i][0][1])),
                    "who": chat[i][0][2],
                    "message": chat[i][1]
                },
                ignore_index=True,
                sort=False
            )
        
        def _clean_df(df):
            # - - format - -
            df['datetime'] = pd.to_datetime(
                df['datetime'], format='%m/%d/%y, %I:%M:%S %p'
            )
            df['who'] = df['who'].astype('category')
            df['message'] = [*map(correct_media, df['message'].values)]
            df['message'] = df['message'].astype('str')
            df['message'] = [*map(lambda x: x.replace('\u200e', ''), df['message'])]
    
            # - - add - -
            # generate msg uuids
            uuids = [uuid.uuid4() for _ in range(_len_chat)]
            # generate chat uuid
            chat_uuid = _len_chat*[uuid.uuid4()]
            # add id cols
            df["id"] = uuids
            df["chat_id"] = chat_uuid
            
            # - - chat people - -
            # find whos
            whos = list(set(list(df.who.values)))
            whos = [*map(lambda x: x.strip().lower().replace(' ', '_'), whos)]
            chat_people = _len_chat*[
                '<>'.join(whos)
            ]
            df["chat_people"] = chat_people
            
            return df
    
        # clean df
        df = _clean_df(df)
        return df

    @sev
    def read_chat(
        self,
        other_person_name,
        chat_folder_path,
        chat_from="whatsapp",
        audio_to_text=False,
        language=None,
        encoding='utf-8',
        raw_txt=False
    ):
        """
        RETURN : a dataframe with chat data (or raw text if raw_txt=True)

        Parameters
        ----------
        other_person_name : str
            The name of the other person in the chat with you
        chat_folder_path (optional) : str
            The path where the chat folder lives
        encoding (optional) : str
            The encoding to read the file
        raw_txt (optional) : bool
            Return a raw text instead of the df
        language (optional) : str
            The language for audio files (for speech recogn.)
        audio_to_text : bool
            Do you want to convert audio files to txt?

        Returns
        -------
        result : a dataframe with chat data
        """
        # read txt
        path = '/'.join(
            (
                str(chat_folder_path) if str(chat_folder_path)[-1] != '/' else str(chat_folder_path)[:-1],
                self.chat_folder_name + str(other_person_name)
            )
        )
        if chat_folder_path == "./":
            path = path.replace('./', '')
        # move to folder
        try:
            os.chdir(path)
        except Exception as exc:
            msg = ' '.join(
                (
                    f"Cannot change directory - your dir {path} does not exist -> {str(exc)}",
                    f"Remember : the folder name must match this pattern -> {self.chat_folder_name + str(other_person_name)}"
                )
            )
            print(msg)
            return None
        if self.debug:
            print("DEBUG: After ch dir command I am here ->" + os.getcwd())

        # read txt chat
        with open(self.chat_file_name, 'r', encoding=encoding) as f:
            content = f.read()

        if raw_txt:
            return content
    
        # content to df
        df = self.chat_to_df(content, chat_from=chat_from)['value']
    
        if audio_to_text:
            warning_print("Audio to txt function in BETA, only WAV supported - a file type conversion is needed")
            df = self.audio_to_message(df, language=language)['value']

        return df

    def read_chat_2(
        self,
        other_person_name,
        chat_folder_path,
        audio_to_text=False,
        language=None,
        encoding='utf-8',
        raw_txt=False
    ):
        """
        RETURN : a dataframe with chat data (or raw text if raw_txt=True)

        Parameters
        ----------
        other_person_name : str
            The name of the other person in the chat with you
        chat_folder_path (optional) : str
            The path where the chat folder lives
        encoding (optional) : str
            The encoding to read the file
        raw_txt (optional) : bool
            Return a raw text instead of the df
        language (optional) : str
            The language for audio files (for speech recogn.)
        audio_to_text : bool
            Do you want to convert audio files to txt?

        Returns
        -------
        result : a dataframe with chat data
        """
        # read txt
        path = '/'.join(
            (
                str(chat_folder_path) if str(chat_folder_path)[-1] != '/' else str(chat_folder_path)[:-1],
                self.chat_folder_name + str(other_person_name)
            )
        )
        if chat_folder_path == "./":
            path = path.replace('./', '')
        # move to folder
        try:
            os.chdir(path)
        except Exception as exc:
            msg = ' '.join(
                (
                    f"Cannot change directory - your dir {path} does not exist -> {str(exc)}",
                    f"Remember : the folder name must match this pattern -> {self.chat_folder_name + str(other_person_name)}"
                )
            )
            print(msg)
            return None
        if self.debug:
            print("DEBUG: After ch dir command I am here ->" + os.getcwd())

        # read txt chat
        with open(self.chat_file_name, 'r', encoding=encoding) as f:
            content = f.read()

        if raw_txt:
            return content

        # regex pattern
        regex_string =  "\[\d+/\d+/\d+, \d+:\d+:\d+ [A-Z]+\]\s+[a-zA-Z0-9]+\s?[a-zA-Z0-9]+\s?[a-zA-Z0-9]+\s?:\s+"
        pattern = re.compile(
           regex_string
        )

        # - - messages - -
        messages = re.split(
            regex_string,
            content
        )
        # remove first empty string
        messages = messages[1:]

        # - - labels - -
        labels = re.findall(pattern, content)

        # - - generate uuids - -
        uuids = [uuid.uuid4() for _ in range(len(messages))]

        # - - chat uuid - -
        chat_uuid = len(messages)*[uuid.uuid4()]
        # - - chat people - -
        chat_people = len(messages)*[self.my_name.lower().replace(' ', '_') + '<>' + other_person_name.lower().replace(' ', '_')]

        # - check -
        if len(messages) != len(labels):
            if self.debug:
                print(f"An error occured, len messages = {len(messages)} but len regex labels = {len(labels)}")
            raise ValueError(
                "Error while using regex pattern,",
                "labels and messages lenghts not matching"
            )
            return None

        # define df
        df = pd.DataFrame(columns=["id", "chat_id", "chat_people", "datetime", "who", "message"])

        # Fill id and messages
        df["id"] = uuids
        df["chat_id"] = chat_uuid
        df["chat_people"] = chat_people
        df["message"] = messages
        df["datetime"] = uuids
        df["who"] = labels

        # - - cleaning - -
        # datetime to a decent format
        def correct_datetime(datetime_tuple):
            # unpack tuple
            date_string, time_string = datetime_tuple

            # correct date
            date_string_chunks = date_string.split('/')
            new_chunks = [
                '0' + chunk if len(chunk) != 2 else chunk
                for chunk in date_string_chunks
            ]
            # re build date string
            date_string = '/'.join(new_chunks)

            # correct time
            time_string_chunks = time_string.split(' ')[0].split(':')
            am_pm = time_string.split(' ')[1]
            new_chunks = [
                '0' + chunk if len(chunk) != 2 else chunk
                for chunk in time_string_chunks
            ]
            # re build date string
            time_string = ':'.join(new_chunks)
            time_string += " {}".format(am_pm)

            # datetime correct
            datetime_correct = date_string + ', ' + time_string
            return datetime_correct

        # media in path
        def correct_media(media_string):
            if "<attached " in media_string:
                media_string = media_string.replace('<attached ', '')
                media_string = media_string.replace('>', '')
                media_string = media_string.replace('\n', '')
                media_string = media_string.strip()
            return media_string
        
        # - - cleaning - -

        # clean datetime
        dts = [record.split('] ')[0].replace('[', '').strip() for record in labels]
        dts = [(dt.split(', ')[0], dt.split(', ')[1]) for dt in dts]
        dts = [*map(correct_datetime, dts)]
        df["datetime"] = dts
        df['datetime'] = pd.to_datetime(df['datetime'], format='%m/%d/%y, %I:%M:%S %p')

        # clean who
        whos = [record.split('] ')[1].replace(':', '').strip() for record in labels]
        df["who"] = whos
        df['who'] = df['who'].astype('category')

        # clean media messages
        df['message'] = [*map(correct_media, df['message'].values)]
        df['message'] = df['message'].astype('str')
        df['message'] = [*map(lambda x: x.replace('\u200e', ''), df['message'])]

        if audio_to_text:
            warning_print("Audio to txt function in BETA, only WAV supported - a file type conversion is needed")
            df = self.audio_to_message(df, language=language)

        return df

    def read_chats(
        self,
        chat_folder_path,
        audio_to_text=False,
        language=None,
        encoding='utf-8',
        raw_txt=False
    ):
        """
        RETURN : a dataframe with chat data (or raw text if raw_txt=True)

        Parameters
        ----------
        chat_folder_path (optional) : str
            The path where the chat folder lives
        encoding (optional) : str
            The encoding to read the file
        raw_txt (optional) : bool
            Return a raw text instead of the df
        language (optional) : str
            The language for audio files (for speech recogn.)
        audio_to_text : bool
            Do you want to convert audio files to txt?

        Returns
        -------
        result : a dataframe with chat data
        """
        # read txt chats
        df = pd.DataFrame(columns=["id", "chat_id", "chat_people", "datetime", "who", "message"])

        # read txt chat
        path = correct_filepath(chat_folder_path, remove_slash=True)
        if chat_folder_path == "./":
            path = path.replace('./', '')
        # move to folder
        try:
            os.chdir(path)
        except Exception as e:
            msg = ' '.join(
                (
                    f"Cannot change directory - your dir {path} does not exist or has no chat folders -> {e}",
                    f"Remember : the folder name must match this pattern -> {self.chat_folder_name} Person Name"
                )
            )
            print(msg)
            return None
        if self.debug:
            print("DEBUG: After ch dir command I am here ->" + os.getcwd())
        # all dirs
        all_dirs_here = [name for name in os.listdir(".") if os.path.isdir(name)]
        all_dirs_chats = [folder for folder in all_dirs_here if self.chat_folder_name in folder]
        names = [*map(lambda x: x.split(' - ')[1], all_dirs_chats)]

        if not names:
            print("Cannot find any WhatsApp chat folder...\n")
            msg = ' '.join(
                (
                    f"Cannot change directory - your dir {path} does not have any chat folder\n",
                    f"Remember : the folder name must match this pattern -> {self.chat_folder_name} Person Name"
                )
            )
            print(msg)
            return None

        # names
        for name in names:
            df = df.append(
                self.read_chat(
                    name,
                    chat_folder_path=chat_folder_path,
                    audio_to_text=audio_to_text,
                    language=language,
                    encoding=encoding,
                    raw_txt=raw_txt
                ),
                ignore_index=True,
                sort=False
            )

        return df
    # + + + + + Chat MAIN + + + + +
    
    # + + + + + Chat Audio + + + + +
    @sev
    def audio_to_message(
        self, df, wav_folder,
        language=None,
    ):
        # use a copy of the df
        df_copy = df
        if language is None:
            language = self.language
        # init jarvis
        iago = Iago()
        # transform audio in txt
        audio_files_len = len([msg for msg in df_copy.message.values if '.opus' in msg])
        new_msg = []
        i = 0
        for msg in df_copy.message.values:
            if '.opus' in msg:
                try:
                    if self.debug:
                        print("\n - - - - - - - - - - - - - ")
                        print(" AUDIO {}/{} begin".format(str(i + 1), str(audio_files_len)))
                        info_print("Progress...")
                    # speech recognition
                    msg = msg.replace('.opus', '.wav')
                    result = iago.audio_to_text(
                        wav_folder + msg,
                        language=language,
                        show_debug=False
                    )
                    if not result['status']:
                        warning_print("File audio {} skipped! because -> {}".format(msg, result['error']))
                    msg = result['value']
                    if self.debug:
                        print("\n AUDIO TO TXT : ")
                        if msg is not None:
                            print(msg + '\n')
                        else:
                            print(None)
                        info_print("Done!")
                        print(" - - - - - - - - - - - - - \n")
                except Exception as e:
                    warning_print("File audio {} skipped! because -> {}".format(msg, result['error']), exception=e)
                # go on
                new_msg.append(msg)
                i += 1
            else:
                new_msg.append(msg)
        # redefine msg
        df_copy['message'] = new_msg

        return df_copy


        # + + + + + Chat Parsing + + + + +
    # + + + + + Chat Audio + + + + +

    # + + + + + Chat Parsing Algo + + + + +
    @sev
    def parse_whatsapp(self, content):
        """
        RETURN : {
            "status": True/False,
            "error": error_msg,
            "value": [(msg record 1), (msg record 2)]
        }
        converts a txt chat in a list of tuples with records
    
        Parameters
        ----------
        content : string
            The string content of the chat .txt
    
        Returns
        -------
        result : {
            "status": True/False,
            "error": error_msg,
            "value": [(msg record 1), (msg record 2)]
        }
        """
        # define regexs
        regex_string_labels_groups = "\[(\d+/\d+/\d+), (\d+:\d+:\d+ [AM|PM]+)]\s+(.[^:]+)\s?:\s"
        regex_string_messages_nogroups = "\[\d+/\d+/\d+, \d+:\d+:\d+ [AM|PM]+]\s+.[^:]+\s?:\s"
        # compile regexs
        pattern_labels = re.compile(regex_string_labels_groups)
        pattern_messages = re.compile(regex_string_messages_nogroups)
        
        # messagges
        messages = tuple(re.split(
            regex_string_messages_nogroups,
            content
        )[1:]) # ignore first empty msg
    
        # labels
        labels = re.findall(
            pattern_labels,
            content
        ) # tuples with labels
        
        if len(messages) != len(labels):
            return None
        
        result = [(labels[i], messages[i]) for i in range(len(messages))]
        return result
    # + + + + + Chat Parsing Algo + + + + +
# + + + + + Classes + + + + +
