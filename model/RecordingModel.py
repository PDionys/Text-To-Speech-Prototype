
class RecordingModel:

    def __init__(self):
        self.isRecording = False
        self.recordedData = None

        self.settingsButtonsID = [
            ['save', 'settings'],
            ['temp1', 'temp2']
        ]
        self.settingsButtonsIcon = [
            'resources\\save_70dp_FFFFFF_FILL0_wght400_GRAD0_opsz48.svg',
            'resources\\settings_70dp_FFFFFF_FILL0_wght400_GRAD0_opsz48.svg',
            'resources\\bug_report_24dp_FFFFFF_FILL0_wght400_GRAD0_opsz24.svg',
            'resources\\bug_report_24dp_FFFFFF_FILL0_wght400_GRAD0_opsz24.svg'
        ]
        
        self.saveMethods = ['Зразок голосу для копіювання', 'Навчальні данні для нової моделі']