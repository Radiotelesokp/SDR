# bias_tee.py - sterowanie zasilaniem Bias-Tee

def control_bias_tee(sdr, action):
    try:
        if action == "status":
            state = sdr.readSetting("bias_tx")
            print("Bias-Tee status:", "ON" if state == "true" else "OFF")

        elif action == "on":
            sdr.writeSetting("bias_tx", "true")
            print("Bias-Tee zostal wlaczony.")

        elif action == "off":
            sdr.writeSetting("bias_tx", "false")
            print("Bias-Tee zostal wylaczony.")

        else:
            print("Pominieto sterowanie Bias-Tee.")

    except Exception as e:
        print("Blad operacji Bias-Tee:", e)