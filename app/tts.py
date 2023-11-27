from mmi import MMIClient, LifeCycleEvent, EMMA

class TTS():

    def __init__(self, IMAdd=None, FusionAdd=None):
        self.mmiCli = MMIClient(IMAdd, FusionAdd)

    def sendToVoice(self, message):
        speak = "\"<speak version=\"1.0\" xmlns=\"http://www.w3.org/2001/10/synthesis\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://www.w3.org/2001/10/synthesis http://www.w3.org/TR/speech-synthesis/synthesis.xsd\" xml:lang=\"pt-PT\"><p>" + message + "</p></speak>\""
        self.mmiCli.sendToIM(LifeCycleEvent("APPSPEECH", "IM", "text-1", "ctx-1").doStartRequest(EMMA("text-", "text", "command", 1, 0).setValue(speak)))