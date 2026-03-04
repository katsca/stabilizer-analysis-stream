import sys
import socket
import struct
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# Make stabilizer visible
sys.path.append(r"C:\Scratch\stabilizer\py")

from stabilizer.stream import Parser, AdcDecoder, DacDecoder, StabilizerStream


PORT = 64492

parser = Parser([
    AdcDecoder(n_sources=2),
    DacDecoder(n_sources=2),
])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", PORT))

print("Capturing...")

bufsize = 1416
buffers = [bytearray(bufsize) for i in range(10**5)]  # allocate buffer

for buffer in buffers:
    nbytes, addr = sock.recvfrom_into(buffer)

adc_samples_master = []
last_sequence = None
dropped_packets = 0
counter = 0

for data in buffers:
    if len(data) < 8:
        continue

    header_tuple = struct.unpack("<HBBI", data[:8])
    magic, format_if, batches, sequence = header_tuple

    if magic != 0x057B:
        continue

    # Packet loss detection
    if last_sequence is not None:
        if sequence != last_sequence:
            dropped_packets += (sequence - last_sequence - 1)
    last_sequence = sequence + batches

    header = StabilizerStream.header._make(header_tuple)
    frame = parser.set_frame(header, data[8:])
    values = frame.to_si()
    adc_samples = values[1]

    adc_samples_master.extend(adc_samples)
    counter += len(adc_samples)
sock.close()

print("Counter: ", counter)
adc_data = adc_samples_master[0:counter]
total_samples = len(adc_data)

print("Capture complete")
print("Dropped packets: ", dropped_packets)

loss_rate = dropped_packets / (last_sequence + 1)
print("Loss rate:", loss_rate * 100, "%")
sample_rate = 390.625e3 # Hz

print("Duration", total_samples/sample_rate, "s")

df = pd.DataFrame({
    "seq": np.arange(total_samples),
    "time": np.arange(total_samples) / sample_rate,
    "adc": adc_data
})
df.to_csv("./data/adc1_capture_10to5packets.csv", index=False)


# # Find FFT
# adc = np.array(adc_data)
# adc -= np.mean(adc)

# N = len(adc)
# fft = np.fft.rfft(adc)
# freqs = np.fft.rfftfreq(N, 1/sample_rate)

# plt.figure()
# plt.plot(freqs, np.abs(fft))
# plt.xlabel("Frequency (Hz)")
# plt.ylabel("Magnitude")
# plt.xlim(0, sample_rate/2)
# plt.show()

