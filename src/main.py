# coding: UTF-8

from pydub import AudioSegment
import matplotlib.pyplot as plt

import array
import subprocess
import struct
from collections import namedtuple

WavSubChunk = namedtuple("WavSubChunk", ["id", "position", "size"])
WavData = namedtuple("WavData", ["audio_format", "channels", "sample_rate",
                                 "bits_per_sample", "raw_data"])

ARRAY_TYPES = {
    8: "b",
    16: "h",
    32: "i",
}


def get_array_type(bit_depth, signed=True):
    t = ARRAY_TYPES[bit_depth]
    if not signed:
        t = t.upper()
    return t


def read_wav_audio(data, headers=None):
    if not headers:
        headers = extract_wav_headers(data)

    fmt = [x for x in headers if x.id == b"fmt "]
    if not fmt or fmt[0].size < 16:
        raise Exception("Couldn't find fmt header in wav data")

    fmt = fmt[0]
    pos = fmt.position + 8
    audio_format = struct.unpack_from("<H", data[pos:pos + 2])[0]
    if audio_format != 1 and audio_format != 0xFFFE:
        raise Exception("Unknown audio format 0x%X in wav data" % audio_format)

    channels = struct.unpack_from("<H", data[pos + 2:pos + 4])[0]
    sample_rate = struct.unpack_from("<I", data[pos + 4:pos + 8])[0]
    bits_per_sample = struct.unpack_from("<H", data[pos + 14:pos + 16])[0]

    data_hdr = headers[-1]
    if data_hdr.id != b"data":
        raise Exception("Couldn't find data header in wav data")

    pos = data_hdr.position + 8
    return WavData(audio_format, channels, sample_rate, bits_per_sample,
                   data[pos:pos + data_hdr.size])


def extract_wav_headers(data):
    # def search_subchunk(data, subchunk_id):
    pos = 12  # The size of the RIFF chunk descriptor
    subchunks = []
    while pos + 8 <= len(data) and len(subchunks) < 10:
        subchunk_id = data[pos:pos + 4]
        subchunk_size = struct.unpack_from("<I", data[pos + 4:pos + 8])[0]
        subchunks.append(WavSubChunk(subchunk_id, pos, subchunk_size))
        if subchunk_id == b"data":
            # "data" is the last subchunk
            break
        pos += subchunk_size + 8

    return subchunks


def fix_wav_headers(data):
    headers = extract_wav_headers(data)
    if not headers or headers[-1].id != b"data":
        return

    # TODO: Handle huge files in some other way
    if len(data) > 2**32:
        raise Exception("Unable to process >4GB files")

    # Set the file size in the RIFF chunk descriptor
    data[4:8] = struct.pack("<I", len(data) - 8)

    # Set the data size in the data subchunk
    pos = headers[-1].position
    data[pos + 4:pos + 8] = struct.pack("<I", len(data) - pos - 8)


def get_waveform_by_ffmpeg(path):
    p = subprocess.Popen(["ffmpeg", "-i", path, "-f", "wav", "-"],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, _ = p.communicate()

    out = bytearray(out)
    fix_wav_headers(out)
    out = bytes(out)
    out = read_wav_audio(out)

    typecode = get_array_type(out.bits_per_sample)
    return array.array(typecode, out.raw_data)


def get_waveform_by_pydub(path):
    sound = AudioSegment.from_file(path, "mp3")
    return sound.get_array_of_samples()


if __name__ == "__main__":
    path = "./assets/MissFireSystem.mp3"
    waveform1 = get_waveform_by_ffmpeg(path)
    waveform2 = get_waveform_by_pydub(path)

    # plt.plot(waveform1)
    # plt.plot(waveform2)
    # plt.show()

    assert waveform1 == waveform2, "waveform1 and waveform2 are not equal."
