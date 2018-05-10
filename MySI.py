import IdentificationServiceHttpClientHelper
import sys
import pickle
import numpy as np
import utils


subscription_key = "0e5a3e2ee0a1469894ae929e67bd6143"
speaker_ids = {}
temp = {'quy': '08857d31-bf0a-4c51-8641-a56990764f35', 'hung': '4270076b-81ff-494b-b20b-b01ac7e1a39c'}
identified_speaker = "Unknown"

def load_speaker():
    with open('speaker_ids.txt', 'rb') as handle:
        speaker_ids = pickle.load(handle)
    return speaker_ids

def save_speaker():
    global speaker_ids
    with open('speaker_ids.txt', 'wb') as handle:
        pickle.dump(speaker_ids, handle, protocol=pickle.HIGHEST_PROTOCOL)
def delete_speaker(speaker_name):
    global speaker_ids
    speaker_ids.pop(speaker_name, None)

def create_profile(subscription_key, locale):
    """Creates a profile on the server.

    Arguments:
    subscription_key -- the subscription key string
    locale -- the locale string
    """
    helper = IdentificationServiceHttpClientHelper.IdentificationServiceHttpClientHelper(
        subscription_key)

    creation_response = helper.create_profile(locale)

    print('Profile ID = {0}'.format(creation_response.get_profile_id()))

    return creation_response.get_profile_id()

def enroll_profile(subscription_key, profile_id, file_path, force_short_audio):
    """Enrolls a profile on the server.

    Arguments:
    subscription_key -- the subscription key string
    profile_id -- the profile ID of the profile to enroll
    file_path -- the path of the file to use for enrollment
    force_short_audio -- waive the recommended minimum audio limit needed for enrollment
    """
    helper = IdentificationServiceHttpClientHelper.IdentificationServiceHttpClientHelper(
        subscription_key)

    enrollment_response = helper.enroll_profile(
        profile_id,
        file_path,
        force_short_audio.lower() == "true")

    print('Total Enrollment Speech Time = {0}'.format(enrollment_response.get_total_speech_time()))
    print('Remaining Enrollment Time = {0}'.format(enrollment_response.get_remaining_speech_time()))
    print('Speech Time = {0}'.format(enrollment_response.get_speech_time()))
    print('Enrollment Status = {0}'.format(enrollment_response.get_enrollment_status()))

def identify_file(subscription_key, file_path, force_short_audio, profile_ids):
    """Identify an audio file on the server.

    Arguments:
    subscription_key -- the subscription key string
    file_path -- the audio file path for identification
    profile_ids -- an array of test profile IDs strings
    force_short_audio -- waive the recommended minimum audio limit needed for enrollment
    """
    helper = IdentificationServiceHttpClientHelper.IdentificationServiceHttpClientHelper(
        subscription_key)

    identification_response = helper.identify_file(
        file_path, profile_ids,
        force_short_audio.lower() == "true")

    # print('Identified Speaker = {0}'.format(identification_response.get_identified_profile_id()))
    # print('Confidence = {0}'.format(identification_response.get_confidence()))
    return identification_response.get_identified_profile_id()

def enroll():
    global speaker_ids
    speaker = input("Start the enrollment. Type your name: ")

    # Add speaker to speaker list 
    speaker_ids[speaker] = create_profile(subscription_key, 'en-us')
    save_speaker()
    audio_path = "dataset\\enroll\\" + speaker + ".wav"
    utils.record(audio_path, 60)
    enroll_profile(subscription_key, speaker_ids[speaker], audio_path, "True")

def enrollName(speaker, record_seconds):
    global speaker_ids
    # Add speaker to speaker list 
    speaker_ids[speaker] = create_profile(subscription_key, 'en-us')
    save_speaker()
    audio_path = "dataset\\enroll\\" + speaker + ".wav"
    # record_seconds = 60
    utils.record(audio_path, record_seconds)
    print("Processing...")
    enroll_profile(subscription_key, speaker_ids[speaker], audio_path, "True")

def enrollAudio(speaker):
    global speaker_ids
    speaker_ids[speaker] = create_profile(subscription_key, 'en-us')
    save_speaker()
    audio_path = "dataset\\enroll\\" + speaker + ".wav"
    enroll_profile(subscription_key, speaker_ids[speaker], audio_path, "True")

def identify():
    global identified_speaker
    audio_path = "dataset\\identify\\speech.wav"
    utils.record(audio_path, 10)
    speaker_ids = load_speaker()
    array_speaker_ids = np.asarray(list(speaker_ids.values())) 
    print("Processing...")
    speaker_id = identify_file(subscription_key, audio_path, "True", array_speaker_ids)
    found = False
    for speaker_name in speaker_ids.keys():
        if speaker_ids[speaker_name] == speaker_id:
            found = True
            print('Identified Speaker = ' + speaker_name)
            identified_speaker = speaker_name
            break

    if not found:
        print('Identified Speaker = Unknown')
        identified_speaker = "Unknown"

def testName(speaker):
    print(speaker + " is speaking.")
    x = np.random.randint(5) + 1
    audio_path = "dataset\\test\\" + speaker + str(x) + ".wav"
    speaker_ids = load_speaker()
    array_speaker_ids = np.asarray(list(speaker_ids.values())) 
    speaker_id = identify_file(subscription_key, audio_path, "True", array_speaker_ids)
    found = False
    for speaker_name in speaker_ids.keys():
        if speaker_ids[speaker_name] == speaker_id:
            found = True
            print('Identified Speaker = ' + speaker_name)
            break

    if not found:
        print('Identified Speaker = Unknown') 

def testAudio(audio_path):
    global identified_speaker
    speaker_ids = load_speaker()
    array_speaker_ids = np.asarray(list(speaker_ids.values())) 
    print("Processing...")
    speaker_id = identify_file(subscription_key, audio_path, "True", array_speaker_ids)
    found = False
    for speaker_name in speaker_ids.keys():
        if speaker_ids[speaker_name] == speaker_id:
            found = True
            print('Identified Speaker = ' + speaker_name)
            identified_speaker = speaker_name
            break

    if not found:
        print('Identified Speaker = Unknown') 
        identified_speaker = 'Unknown'







