#!/usr/bin/env python3
from glob import glob
from binascii import unhexlify, hexlify
import numpy as np
import os
import mmap
import struct
import logging

logger = logging.getLogger('parseLogger')


class ParsingException(Exception):
    pass


class Header():
    def __init__(self, masstart, massend, masstep, dslen):
        self.dslen = dslen
        self.masstart = masstart
        self.massend = massend
        self.masstep = masstep

    def __eq__(self, other):
        if not isinstance(other, Header):
            return NotImplemented
        return self.dslen == other.dslen and self.masstart == other.masstart\
            and self.massend == other.massend and self.masstep == other.masstep


class ScanHeads():
    def __init__(self):
        self.primers = []
        self.headers = []

    def add_scan(self, primer, header):
        if not(self.headers) or self.headers[-1] != header:
            self.primers.append([primer])
            self.headers.append(header)
        else:
            self.primers[-1].append(primer)

    def interpret_scan(self, mf, data_form, primer_pos):
        if data_form in {47, 57, 63}:
            dsstart = struct.unpack("<i", mf.read(4))[0] + primer_pos + 4
            dslen, masstart, massend, masstep = [], [], [], []
            fmt = "<ffdI"
            chunk = mf.read(struct.calcsize(fmt))
            delimiter = {47: unhexlify("FFFFFFFFFFFFFFFF0000E0FFFFFFEF3F"),
                         57: unhexlify("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"),
                         63: unhexlify("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")}
            while not chunk[:16] == delimiter[data_form]:
                rawhead = struct.unpack(fmt, chunk)
                for i in rawhead:
                    if not i > 0:
                        raise ParsingException(
                            "[ERROR] Illegal value encountered when parsing "
                            "at 0x{:x}".format(mf.tell()))
                for i,j in enumerate((masstart, massend, masstep)):
                    j.append(rawhead[i])
                dslen.append(int(rawhead[-1])-4*(len(dslen)+1)-np.sum(dslen))
                chunk = mf.read(struct.calcsize(fmt))
            header = Header(masstart, massend, masstep, dslen)
            self.add_scan(dsstart, header)
            if len(chunk) == struct.calcsize(fmt):
                cont = not struct.unpack("<i", chunk[16:])[0]
                return cont
            else:
                return False
        if data_form == 66:
            fmt = "<4xI24xffdd4xi4xi"
            chunk = mf.read(struct.calcsize(fmt))
            if len(chunk) < struct.calcsize(fmt):
                mf.seek(0)
                return False
            tot_len, first_m, last_m, first_m_d, step, arr32_len, arr_len2 \
                = struct.unpack(fmt, chunk)
            if first_m  == 0:
                logger.info("EOF! All scan heads mapped, last mapping discarded")
                return False
            for i in (tot_len, first_m, last_m, first_m_d, step, arr32_len, arr_len2):
                if not i > 0:
                    raise ParsingException(
                        "[ERROR] Illegal value encountered when parsing "
                        "at 0x{:x}".format(mf.tell()))
            dsstart = mf.tell()
            header = Header([first_m], [last_m], [step], [arr32_len*4])
            self.add_scan(dsstart, header)
            mf.seek(mf.tell()+arr32_len*4)
            return True


def get_data_format(mfile):
    finnig_header = b'\x01\xA1'+"Finnigan".encode("UTF-16")[2:]
    mfile.seek(0)
    if mfile.read(len(finnig_header)) == finnig_header:
        logger.info("Detected Finnigan .raw file header...")
        mfile.seek(mfile.tell()+16)
        if mfile.read(2) == b'\x08\x00':
            file_format = struct.unpack("<h", mfile.read(2))[0]
            logger.info("Data format version is {}".format(file_format))
            return file_format
        else:
            raise ParsingException(
                "[ERROR] File is unsupported, please submit your spectrum"
                "to the developer of this library")
    else:
        raise ParsingException(
                "[ERROR] File was not recognized"
                "as Finnigan .raw file!!")


def find_scan_primer(mfile, data_form):
    fmt = "<8h"
    mfile.seek(100)
    [year, month, dow, dom, h, m, s, ms] = np.zeros(8, dtype=int)
    while not (year > 1980 and 0 < month <= 12 and 0 <= dow < 7 and
               0 < dom <= 31 and 0 <= h < 24 and 0 <= m < 60 and
               0 <= s < 60 and 0 <= ms < 1000):
        mfile.seek(-14, 1)
        year, month, dow, dom, h, m, s, ms =\
            struct.unpack(fmt, mfile.read(struct.calcsize(fmt)))
    while mfile.read(4) in (unhexlify("00000000"), unhexlify("01000000")):
        continue
    mfile.seek(-4, 1)
    if data_form in {47, 57, 63, 66}:
        primer_pos = struct.unpack("<i", mfile.read(4))[0]
    else:
        raise ParsingException(
                "[ERROR] unknown data_form {}, exiting NOW!".format(data_form))
    return primer_pos


def ext_scan_heads(mf, data_form):
    primer_pos = find_scan_primer(mf, data_form)
    mf.seek(primer_pos)
    scannum = 1
    headers = ScanHeads()
    cont = True
    logger.info("Mapping headers")
    if data_form in {47, 57, 63}:
        if not mf.read(4) == unhexlify("00000000"):
            raise ParsingException(
                "[ERROR] Primer not located properly, exiting NOW!")
        while cont:
            try:
                while mf.read(4)[3] == 0x80:
                    continue
            except IndexError:
                break
            if len(mf) < (mf.tell() + 40):
                break
            mf.seek(-4, 1)
            datas = mf.read(8)
            mf.seek(-8, 1)
            if datas[7] == 0x80:
                mf.seek(4,1)
                continue
            elif (datas[:4] != unhexlify("00000000")) or not headers.primers:
                logger.debug("Mapping header of the scan #{}".format(scannum))
                cont = headers.interpret_scan(mf, data_form, primer_pos)
                scannum += 1
            else:
                raise ParsingException(
                    "[ERROR] Unknown data interrupt, exiting NOW!")
    elif data_form == 66:
        while cont:
            logger.debug("Mapping header of the scan #{}".format(scannum))
            cont = headers.interpret_scan(mf, data_form, primer_pos)
            scannum += 1
    else:
        raise ParsingException("[ERROR] unknown data_form {},"
                               "exiting NOW!".format(data_form))
    last_p = mf.tell()
    return headers, last_p


def get_chromatogram(mfile, look_from, data_form, tmp_folder, no_of_scans):
    pos = find_chrom_primer(mfile, look_from, data_form)
    temp_found = False
    if pos == int(-1):
        logger.warning("Did not find scan times in the original file\n"
                       "Looks like the scanning is in progress,"
                       "searching for the temp file")
        mfile = load_tmp_file(tmp_folder)
        mfile.seek(8)
        temp_found = True
    else:
        mfile.seek(pos+4)
    times = []
    intensities = []
    if data_form in {47, 63}:
        h_len = 72
        fmt = "<4s3idd"
        delim = "ffffffff"
        tpos = -2
        ipos = -1
    elif data_form == 57:
        h_len = 72
        fmt = "<4si8s6d4si"
        delim = "00000000"
        tpos = 3
        ipos = 4
    elif data_form == 66:
        h_len = 88
        fmt = "<4s3idd"
        delim = "ffffffff"
        tpos = -2
        ipos = -1
    else:
        raise ParsingException("[ERROR] unknown Machine Type {}, exiting NOW!"
                               .format(data_form))

    logger.info("Extracting scan times")

    fmt_size = struct.calcsize(fmt)
    next_measure = 1
    while 1:
        header = mfile.read(h_len)
        val = struct.unpack(fmt, header[:fmt_size])
        if data_form == 57 and val[0][2:] == struct.pack(
                "<h", 1+struct.unpack("<xxh", unhexlify(delim))[0]):
            delim = hexlify(struct.pack("<xxh", 1+struct.unpack(
                            "<xxh", unhexlify(delim))[0]))
        if ((val[0] == unhexlify(delim) or (
                data_form == 63 and val[0][:2] == unhexlify("0000")))
                and val[1] == next_measure):
            times.append(val[tpos])
            intensities.append(val[ipos])
            logger.debug("time of the scan #{} is {:.6} seconds"
                         .format(val[1], val[tpos]*60))
            next_measure += 1
        else:
            break
    if temp_found:
        logger.info("Cutting out chromatogram")
        times = times[:no_of_scans]
        intensities = intensities[:no_of_scans]
    if len(times) != no_of_scans:
        logger.critical("Number of times: {}, number of scans {}".format(
                        len(times), no_of_scans))
        raise ParsingException(
            "[ERROR] Number of times does not fit to number of scans")
    return np.array([times, intensities], dtype=np.float32)


def find_chrom_primer(mfile, look_from, data_form):
    if data_form in {47, 57, 63}:
        mfile.seek(mfile.find(unhexlify(
            "010000000000000001000000"), look_from - 4) + 28)
    elif data_form == 66:
        mfile.seek(mfile.find(unhexlify("0200000002000000"), look_from) + 8)
    else:
        raise ParsingException("[ERROR] unknown data_form {}, exiting NOW!"
                               .format(data_form))
    mpos = struct.unpack("<i", mfile.read(4))[0] + 4
    pos = mpos if (mpos > look_from and mpos < mfile.size()) else -1
    return pos


def load_tmp_file(tmp_folder):
    def read_tmp_file(tmp_file):
        inp = open(tmp_file, mode="rb")
        data = inp.read()
        inp.close()
        return data
    tmp_files = sorted(glob(tmp_folder+"/*"),
                       key=lambda tmpf: os.stat(tmpf).st_mtime,
                       reverse=True)
    for file in tmp_files:
        if read_tmp_file(file).find(unhexlify("ffffffff0100")) == 8:
            logger.info("Found temp file "+file)
            temp_data = open(file, "rb")
            return temp_data
    raise ParsingException("[ERROR] Valid .tmp file was not found")


def load_raw(raw_file,
             tmp_glob=r"C:/ProgramData/Thermo Scientific/Temp/*.tmp"):
    inf = open(raw_file, "rb")
    mf = mmap.mmap(inf.fileno(), 0, access=mmap.ACCESS_READ)
    data_format = get_data_format(mf)
    scan_heads, last_p = ext_scan_heads(mf, data_format)
    segments = [len(segment) for segment in scan_heads.primers]

    chromatogram = get_chromatogram(
            mf, last_p, data_format, tmp_glob, np.sum(segments))

    acqnum = 0
    spectra = []
    for header, primer in zip(scan_heads.headers, scan_heads.primers):
        acqnumstart = acqnum
        masses = np.concatenate([header.masstart[i]+np.arange(
            header.dslen[i]/4, dtype=np.float32)*header.masstep[i]
            for i in range(len(header.dslen))])
        matrix = np.empty((len(primer), int(
            np.sum(header.dslen)/4)), dtype=np.float32)
        for x, pos in enumerate(primer):
            mf.seek(pos)
            logger.info("Extracting the spectrum of the scan #{}"
                        .format(acqnum+1))
            acqnum += 1
            if data_format in {47, 57, 63}:
                #ugly, but works for now..
                values = np.concatenate(
                    [np.frombuffer(
                        mf.read(int(header.dslen[-1])+4), dtype=np.uint32)[:-1]
                        for i in range(len(header.dslen))])
                # old format is weird Int.
                # It needs to be reformed before pasted into matrix.
                matrix[x] = values-0x80000000
            elif data_format == 66:
                values = np.frombuffer(mf.read(header.dslen[-1]),
                                       dtype=np.float32)
                matrix[x] = values
            else:
                raise ParsingException("[ERROR] Data type not defined")
        chromsection = chromatogram.T[acqnumstart:acqnum].T
        spectra.append([chromsection, masses, matrix])
    inf.close()
    logger.info("Parsing done, hopefully in correct way")
    return spectra


#  working cajzls, delete when finishing
if __name__ == "__main__":
    logging.basicConfig()
    logger.setLevel("DEBUG")
    file_list = [("TSQ.raw", ""), ("LCQ.raw", ""), ("LTQ.raw", ""),
                 ("MAX.raw", ""), ("TSQsim.raw", ""), ("TSQ_pchan.RAW", ""),
                 ("LTQ_wip.RAW", "LTQ_temp"), ("TSQ_temp.RAW", "TSQ_temp"),
                 ("LTQ_pchan.RAW")]
    for i in file_list:
        print(i)
        load_raw(*i)
