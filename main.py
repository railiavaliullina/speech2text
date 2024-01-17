import os
import json
import speech_recognition
from pydub import AudioSegment

from datetime import datetime
from argparse import ArgumentParser


def read_signal(file_path):
    """
    Reads .wav file

    :param file_path: path to input .wav file
    :return: signal
    """
    return AudioSegment.from_file(file_path, format="wav")


def audio_file_modification(signal, speed_scale, volume):
    """
    Changes signal speed and volume according to input arguments

    :param signal: input signal
    :param speed_scale: the audio speed scale (if scale = 1, speed will not change)
    :param volume: the audio volume in the format "+<dB value>" or "-<dB value>
    :return: modified by speed and volume signal
    """
    # speed modification
    sound_with_altered_frame_rate = signal._spawn(signal.raw_data,
                                                  overrides={"frame_rate": int(signal.frame_rate * speed_scale)})
    modified_by_speed_signal = sound_with_altered_frame_rate.set_frame_rate(signal.frame_rate)
    # volume modification
    sign, db_value = volume[0], float(volume[1:])
    if sign == '+':
        modified_by_volume_signal = modified_by_speed_signal + db_value
    elif sign == '-':
        modified_by_volume_signal = modified_by_speed_signal - db_value
    else:
        raise Exception
    return modified_by_volume_signal


def audio_to_text():
    """
    Transforms audio to text using speech_recognition library

    :return: recognised from audio text
    """
    recognizer = speech_recognition.Recognizer()
    audio_ex = speech_recognition.AudioFile(os.path.join(args.input_path, f'{args.lang}.wav'))
    with audio_ex as source:
        audiodata = recognizer.record(audio_ex)
    language = 'en-US' if args.lang == 'en' else 'ru-RU'
    text = recognizer.recognize_google(audio_data=audiodata, language=language)
    print('Speech recognition result:', text)
    return text


def save_signal(out_signal):
    """
    Saves result signal as .wav file

    :param out_signal: result signal
    :return: None
    """
    output_file_path = os.path.join(args.output_path, f'{now}.wav')
    out_signal.export(output_file_path, format="wav")


def log_result(recognised_text):
    """
    Logs recognised text and input arguments in JSON file

    :param recognised_text: recognised from audio text
    :return: None
    """
    output_file_path = os.path.join(args.output_path, f'{now}.json')

    log = vars(args)
    log['input_file_path'] = input_file_path
    log['recognised_text'] = recognised_text

    with open(output_file_path, 'w') as fp:
        json.dump(log, fp)

    print(f'Speech recognition result saved to: {output_file_path}')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--lang', default='en', help='Choose audiofile language from list ["en", "ru"]')
    parser.add_argument('--speed_scale', default='1.5',
                        help='Enter the audio speed scale (if scale = 1, speed will not change)')
    parser.add_argument('--volume', default='+5',
                        help='Enter the audio volume in the format "+<dB value>" or "-<dB value>"')
    parser.add_argument('--input_path', default='input_files')
    parser.add_argument('--output_path', default='output_files')
    args = parser.parse_args()

    now = datetime.strftime(datetime.now(), '%d%m%y_%H%M%S')
    input_file_path = os.path.join(args.input_path, f'{args.lang}.wav')

    # audio modification (speed, volume)
    signal = read_signal(input_file_path)
    modified_signal = audio_file_modification(signal, float(args.speed_scale), args.volume)
    save_signal(modified_signal)

    # speech recognition
    text = audio_to_text()
    log_result(text)
