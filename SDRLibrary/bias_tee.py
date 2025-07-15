# bias_tee.py - sterowanie zasilaniem Bias-Tee

class BiasTee:
    def __init__(self, sdr):
        self.sdr = sdr
        self.controlBiasTee("off")

    def getStatus(self):
        try:
            state = self.sdr.readSetting("bias_tx")
            return "on" if state == "true" else "off"
        except Exception as e:
            print("Error operation Bias-Tee: ", e)

    def controlBiasTee(self, action):
        try:
            if action.lower() == "on":
                self.sdr.writeSetting("bias_tx", "true")
            elif action.lower() == "off":
                self.sdr.writeSetting("bias_tx", "false")
            else:
                raise ValueError(f"Unsupported operation Bias-Tee: '{action}'")

        except Exception as e:
            print("Error operation Bias-Tee: ", e)