import sys
import SoapySDR
import logging
from flask import Flask, jsonify
from SDRLibrary import sdr_scan, BiasTee, SpectrumScanner

SoapySDR.setLogLevel(SoapySDR.SOAPY_SDR_FATAL)
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sdr = SoapySDR.Device()
bias_tee = None

help = """
    METHOD  ENDPOINT            DESCRIPTION
    PUT     /biastee/<action>   - on/off Bias-Tee
    GET     /biastee/status     - get state Bias-Tee
    GET     /help               - help
    POST    /scan/<start_freq>/<stop_freq>/<step_freq>/<sample_rate>/<gain>/<n_samples>/<channel>  - scan spectrum
    """
@app.route('/')
def home():
    return jsonify({"message": f"Hello from SDR service! \n {help}"})

@app.route('/biastee/status', methods=['GET'])
def bias_tee_status():
    return jsonify({"message": f"Bias-Tee status: {bias_tee.getStatus()}"})

@app.route('/biastee/<action>', methods=['PUT'])
def bias_tee_control(action):
    try:
        bias_tee.controlBiasTee(action)
        return jsonify({"message": f"Bias-Tee status set on: {bias_tee.getStatus()}"})
    except TypeError as ex:
        return jsonify({"message": str(ex)})
    except Exception as ex:
        return jsonify({"message": f"Bias-Tee status error: {ex}"})

@app.route('/scan/<start_freq>/<stop_freq>/<step_freq>/<sample_rate>/<gain>/<n_samples>/<channel>', methods=['POST'])
def scan_spectrum(start_freq, stop_freq, step_freq, sample_rate, gain, n_samples, channel):
    try:
        spectrumScanner = SpectrumScanner(sdr, start_freq, stop_freq, step_freq, sample_rate, gain, n_samples, channel)
        logger.info("Starting spectrum scan. Please wait...")
        spectrumScanner.scan()
        logger.info("Success spectrum scan.")
        return jsonify({"message": f"Results: {spectrumScanner.scan()} "})  #Add send file with plot, mean and max signal

    except ValueError as ex:
        return jsonify({"message": str(ex)})
    except Exception as ex:
        return jsonify({"message": str(ex)})

@app.route('/help', methods=['GET'])
def get_help():
    return jsonify({"message": f"{help}"})

if __name__ == '__main__':
    app.run(debug=True)

    try:
        sdr = SoapySDR.Device()
        bias_tee = BiasTee(sdr)
    except Exception as e:
        sys.exit(f"Connection error with SDR: {e}")

    driver = sdr.getDriverKey().lower()
    logger.info(f"Used driver SDR: {driver}")

    # Wymagany: HackRF
    # if driver != "hackrf":
    #    sys.exit(f"Brak obslugiwanego SDR - wymagany 'hackrf', wykryto '{driver}'.")






'''
    try:
        start_freq  = input_float("Start freq  (Hz): ")
        stop_freq   = input_float("Stop freq   (Hz): ")
        step_freq   = input_float("Step        (Hz): ")
        sample_rate = input_float("Sample rate (Hz): ")
        gain        = input_float("Gain        (dB): ")
        n_samples   = int(input_float("Sample count: "))

                print("» Rozpoczynam skanowanie...  (Ctrl+C aby przerwac)")
                sdr_scan.scan_band(sdr, sample_rate, gain, n_samples,
                                   start_freq, stop_freq, step_freq)
                print("» Skanowanie zakonczone.\n")

            except KeyboardInterrupt:
                print("» Skanowanie przerwane.\n")
            except Exception as err:
                print("Blad podczas skanowania:", err)




def input_float(msg):
    while True:
        try:
            val = input(msg).strip()

            if not val:
                print("Anulowano.\n")
                raise KeyboardInterrupt

            return float(val)

        except ValueError:
            print("Wpisz poprawna liczbe")


def main():
    # Polaczenie z SDR
    try:
        sdr = SoapySDR.Device()
        bias_tee = BiasTee(sdr)
    except Exception as e:
        sys.exit(f"Blad polaczenia z SDR: {e}")

    driver = sdr.getDriverKey().lower()
    print(f"Uzywany sterownik SDR: {driver}")

    # Wymagany: HackRF
    #if driver != "hackrf":
    #    sys.exit(f"Brak obslugiwanego SDR - wymagany 'hackrf', wykryto '{driver}'.")

    print(">>> Wpisz 'help' aby zobaczyc komendy.")

    while True:
        try:
            cmd = input(">>> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nExit.")
            break

        # Sterowanie Bias-Tee
        if cmd.startswith("bias "):
            try:
                action = cmd.split(maxsplit=1)[1]
            except IndexError:
                print("Uzycie: bias on|off|status")
                continue
            try:
                bias_tee.control_bias_tee(sdr, action)
            except Exception as err:
                print("Blad Bias-Tee:", err)
            continue


        # Skanowanie + wykres
        if cmd == "scan":
            try:
                start_freq  = input_float("Start freq  (Hz): ")
                stop_freq   = input_float("Stop freq   (Hz): ")
                step_freq   = input_float("Step        (Hz): ")
                sample_rate = input_float("Sample rate (Hz): ")
                gain        = input_float("Gain        (dB): ")
                n_samples   = int(input_float("Sample count: "))

                print("» Rozpoczynam skanowanie...  (Ctrl+C aby przerwac)")
                sdr_scan.scan_band(sdr, sample_rate, gain, n_samples,
                                   start_freq, stop_freq, step_freq)
                print("» Skanowanie zakonczone.\n")

            except KeyboardInterrupt:
                print("» Skanowanie przerwane.\n")
            except Exception as err:
                print("Blad podczas skanowania:", err)


        else:
            print("Nieznane polecenie. Wpisz 'help'.")
'''