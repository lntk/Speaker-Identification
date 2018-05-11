import IdentificationServiceHttpClientHelper
import sys
import pickle
import numpy as np
import utils


subscription_key = "0e5a3e2ee0a1469894ae929e67bd6143"
# speaker_ids = {'khang':'9bfcfd68-b15f-48f9-ba1a-67187aa5ea45', 
#                 'duy':'1d5bde59-5384-412b-bbd3-39fbc287e6f3',
#                 'dat':'d6b97999-d2b6-435a-bdeb-637cb1576ab0',
#                 'hung':'12370ea3-210c-4fed-9487-a6b6c1d4a4e4',
#                 'quy':'679f8743-ff66-4c1b-9fa8-75d55632faf5'}


class SpeakerIdentification():
    def __init__(self):
        self.speaker_ids = self.load_speaker()
        self.identified_speaker = "Unknown"

    def load_speaker(self):
        with open('speaker_ids.txt', 'rb') as handle:
            speaker_ids = pickle.load(handle)
        return speaker_ids

    def save_speaker(self):
        with open('speaker_ids.txt', 'wb') as handle:
            pickle.dump(self.speaker_ids, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def delete_speaker(self, speaker_name):
        self.speaker_ids.pop(speaker_name, None)
        self.save_speaker()

    def create_profile(self, subscription_key, locale):
        """Creates a profile on the server.

        Arguments:
        subscription_key -- the subscription key string
        locale -- the locale string
        """
        helper = IdentificationServiceHttpClientHelper.IdentificationServiceHttpClientHelper(subscription_key)
        creation_response = helper.create_profile(locale)
        print('Profile ID = {0}'.format(creation_response.get_profile_id()))

        return creation_response.get_profile_id()

    def enroll_profile(self, subscription_key, profile_id, file_path, force_short_audio):
        """Enrolls a profile on the server.

        Arguments:
        subscription_key -- the subscription key string
        profile_id -- the profile ID of the profile to enroll
        file_path -- the path of the file to use for enrollment
        force_short_audio -- waive the recommended minimum audio limit needed for enrollment
        """
        helper = IdentificationServiceHttpClientHelper.IdentificationServiceHttpClientHelper(subscription_key)

        enrollment_response = helper.enroll_profile(
            profile_id,
            file_path,
            force_short_audio.lower() == "true")

        print('Total Enrollment Speech Time = {0}'.format(enrollment_response.get_total_speech_time()))
        print('Remaining Enrollment Time = {0}'.format(enrollment_response.get_remaining_speech_time()))
        print('Speech Time = {0}'.format(enrollment_response.get_speech_time()))
        print('Enrollment Status = {0}'.format(enrollment_response.get_enrollment_status()))

    def identify_file(self, subscription_key, file_path, force_short_audio, profile_ids):
        """Identify an audio file on the server.

        Arguments:
        subscription_key -- the subscription key string
        file_path -- the audio file path for identification
        profile_ids -- an array of test profile IDs strings
        force_short_audio -- waive the recommended minimum audio limit needed for enrollment
        """
        helper = IdentificationServiceHttpClientHelper.IdentificationServiceHttpClientHelper(subscription_key)

        identification_response = helper.identify_file(
            file_path, profile_ids,
            force_short_audio.lower() == "true")

        # print('Identified Speaker = {0}'.format(identification_response.get_identified_profile_id()))
        # print('Confidence = {0}'.format(identification_response.get_confidence()))
        return identification_response.get_identified_profile_id()

    # Enroll by recording
    def enroll(self):
        speaker = input("Start the enrollment. Type your name: ")

        # Add speaker to speaker list 
        self.speaker_ids[speaker] = self.create_profile(subscription_key, 'en-us')
        self.save_speaker()
        audio_path = "dataset\\enroll\\" + speaker + ".wav"
        utils.record(audio_path, 60)
        self.enroll_profile(subscription_key, self.speaker_ids[speaker], audio_path, "True")

    # Enroll by name, audio is ready in the dataset
    def enrollName(self, speaker, record_seconds):
        # Add speaker to speaker list 
        self.speaker_ids[speaker] = self.create_profile(subscription_key, 'en-us')
        self.save_speaker()
        audio_path = "dataset\\enroll\\" + speaker + ".wav"
        # record_seconds = 60
        utils.record(audio_path, record_seconds)
        print("Processing...")
        self.enroll_profile(subscription_key, self.speaker_ids[speaker], audio_path, "True")

    def enrollAudio(self, speaker):
        self.speaker_ids[speaker] = self.create_profile(subscription_key, 'en-us')
        self.save_speaker()
        audio_path = "dataset\\enroll\\" + speaker + ".wav"
        self.enroll_profile(subscription_key, self.speaker_ids[speaker], audio_path, "True")

    
    def identify(self):
        audio_path = "dataset\\identify\\speech.wav"
        utils.record(audio_path, 10)
        array_speaker_ids = np.asarray(list(self.speaker_ids.values())) 
        print("Processing...")
        speaker_id = self.identify_file(subscription_key, audio_path, "True", array_speaker_ids)
        found = False
        for speaker_name in self.speaker_ids.keys():
            if self.speaker_ids[speaker_name] == speaker_id:
                found = True
                print('Identified Speaker = ' + speaker_name)
                self.identified_speaker = speaker_name
                break

        if not found:
            print('Identified Speaker = Unknown')
            self.identified_speaker = "Unknown"

    # test by name, audio is ready in the dataset
    def testName(self, speaker):
        print(speaker + " is speaking.")
        x = np.random.randint(5) + 1
        audio_path = "dataset\\test\\" + speaker + str(x) + ".wav"
        array_speaker_ids = np.asarray(list(self.speaker_ids.values())) 
        speaker_id = self.identify_file(subscription_key, audio_path, "True", array_speaker_ids)
        found = False
        for speaker_name in self.speaker_ids.keys():
            if self.speaker_ids[speaker_name] == speaker_id:
                found = True
                print('Identified Speaker = ' + speaker_name)
                break

        if not found:
            print('Identified Speaker = Unknown') 

    # test by audio
    def testAudio(self, audio_path):
        array_speaker_ids = np.asarray(list(self.speaker_ids.values())) 
        print("Processing...")
        speaker_id = self.identify_file(subscription_key, audio_path, "True", array_speaker_ids)
        found = False
        for speaker_name in self.speaker_ids.keys():
            if self.speaker_ids[speaker_name] == speaker_id:
                found = True
                print('Identified Speaker = ' + speaker_name)
                self.identified_speaker = speaker_name
                break

        if not found:
            print('Identified Speaker = Unknown') 
            self.identified_speaker = 'Unknown'



# SpeakerIdentification.save_speaker()



