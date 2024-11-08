
class RecordingModel:

    def __init__(self):
        self.isRecording = False
        self.recordedData = None

        self.microphone = 1
        self.outputDevice = 4
        self.volume = 0
        self.rate = 44100

        self.settingsButtonsID = [
            ['save', 'settings'],
            ['equalizer', 'effects']
        ]
        self.settingsButtonsIcon = [
            'resources\\save_70dp_FFFFFF_FILL0_wght400_GRAD0_opsz48.svg',
            'resources\\settings_70dp_FFFFFF_FILL0_wght400_GRAD0_opsz48.svg',
            'resources\\equalizer_70dp_FFFFFF_FILL0_wght400_GRAD0_opsz48.svg',
            'resources\\edit_audio_70dp_FFFFFF_FILL0_wght400_GRAD0_opsz48.svg'
        ]
        
        self.saveMethods = ['Зразок голосу для копіювання', 'Навчальні данні для нової моделі']