"""
https://www.dropbox.com/s/mrg49n67mug6ha4/checkpoint_run1.tar?dl=0

first activate and
conda env create -f environment.yml
poetry install

"""

import argparse

import enlighten
import yaml
import lyricsgenius as genius
import fileinput
import json
import os
import re
from os import listdir
from os.path import isfile, join

from numba import cuda

import random
import gpt_2_simple as gpt2
import urllib.request
import tarfile
import progressbar
import pronouncing
import syllables

import torch
import numpy as np
from scipy.io.wavfile import write

try:
    import sox
except:
    raise ImportError("please install sox from https://sourceforge.net/projects/sox/files/sox/ \n"
                      "and generate pip install sox")


class Subscriber:
    def __init__(self, name):
        self.name = name

    def update(self, header, message):
        print('{} got message "{}"'.format(self.name, message))


class Publisher:
    def __init__(self):
        self.subscribers = set()

    def register(self, who):
        self.subscribers.add(who)

    def unregister(self, who):
        self.subscribers.discard(who)

    def dispatch(self, header, message):
        for subscriber in self.subscribers:
            subscriber.update(header, message)


class PrintEverythingView(Subscriber):
    def __init__(self, name):
        super().__init__(name)
        self.headers = []

    def update(self, header, message):
        if header not in self.headers:
            self.headers.append(header)
        c = PColor()
        if "scrape_info" in header:
            print(message)
        elif "log_line" in header:
            if "try:" in message:
                print(header, message)
            pass
        elif "add_line" in header:
            print(c.blue(message))
        elif "sync_line" in header:
            print(c.bold(c.blue(message)))
        elif "voice" in header:
            print(c.bold(c.green(message)))
        else:
            print(c.warn("header not recognized"))
            print(c.warn(message))


class GeneratorView(Subscriber):
    # todo
    def __init__(self, name):
        super().__init__(name)
        self.lines = []
        self.log = []
        self.update("init", "")

    def update(self, header, message):
        if "log_line" in header:
            self.log.append(message)
            if "try:" not in message:
                return
        # draw here


class Generator(Publisher):
    def __init__(self, lyric_file="generated/lyrics.txt", temp_file="generated/temp.txt",
                 r_name='run1', debug=True, view=None):
        super().__init__()
        self.lines = []
        self.lyric_file = lyric_file
        self.temp_file = temp_file
        self.i = 0
        self.log = []
        self.index = 0
        self.running = False
        self.debug = debug
        self.register(view)
        self.sess = gpt2.start_tf_sess()
        self.load_or_download_run1(r_name)

    def v_print(self, *args):
        self.dispatch("log_line", ' '.join([str(a) for a in args]))
        self.log.append(' '.join([str(a) for a in args]))

    def empty_file(self, file):
        with open(file, 'w') as f:
            f.write("")
            pass

    def read_line(self, file, index):
        with open(file, 'r', encoding='utf8', errors='ignore') as f:
            current_line = 1
            for li in f:
                if current_line == index:
                    return li
                current_line += 1

    def read_all_lines(self, file):
        with open(file, 'r', encoding='utf8', errors='ignore') as f:
            content = f.readlines()
            content = [x.strip() for x in content]
            return content

    def read_all_from_generated(self, file):
        with open(file, 'r', encoding='utf8', errors='ignore') as f:
            content = f.readlines()
            rl = []
            for li in content:
                if li and li.strip() and "=" not in li:
                    rl.append(li)
            return rl

    def is_good(self, li):
        if not li:
            return False

        syl_count = syllables.estimate(li)
        if not 7 < syl_count < 18:
            return False

        last_word = li.split()[-1]
        rhyme_list = pronouncing.rhymes(last_word)
        if not len(rhyme_list) > 20:
            return False

        self.v_print("GOOD!: ", li)
        self.v_print("syl:", syl_count, "\nrhymes", len(rhyme_list))

        return True

    def gen_next_rhyme_line(self, last_ln):
        self.v_print("gen_next_rhyme_line called", last_ln)
        other_last_word = last_ln.split()[-1]
        self.v_print(last_ln, other_last_word)
        rhyme_list = pronouncing.rhymes(other_last_word)
        possible = []

        tries = 100
        self.empty_file(self.temp_file)

        temp_lines = ["FAILED"]
        good_lines = []
        index = 0
        while "FAILED" in temp_lines or not good_lines:
            try:
                self.empty_file(self.temp_file)
                gpt2.generate_to_file(self.sess,
                                      prefix=last_ln,
                                      destination_path=self.temp_file,
                                      length=12,
                                      temperature=0.8,
                                      nsamples=tries,
                                      batch_size=tries
                                      )
                temp_lines = self.read_all_from_generated(self.temp_file)
            except:
                self.v_print("FAILED")
                temp_lines = ["FAILED"]
                pass
            for lin in temp_lines:
                if self.is_good(lin):
                    self.v_print("looking at line:", lin)
                    temp_last_word = lin.split()[-1]
                    if temp_last_word in rhyme_list:
                        possible.append(lin)
                        good_lines.append(lin)

            self.v_print("try:", index, "possible:", len(possible))
            index += 1

        this_line = random.choice(good_lines)
        self.v_print("THIS LINE:", this_line)
        self.v_print("Good Lines:", len(good_lines))
        for lin in good_lines:
            self.v_print(lin)
        return this_line

    def gen_next_non_rhyme_line(self):
        self.v_print("gen_next_non_rhyme_line called")
        tries = 100
        self.empty_file(self.temp_file)

        temp_lines = ["FAILED"]
        good_lines = []

        while "FAILED" in temp_lines or not good_lines:
            try:
                gpt2.generate_to_file(self.sess,
                                      destination_path=self.temp_file,
                                      length=12,
                                      temperature=0.8,
                                      nsamples=tries,
                                      batch_size=tries
                                      )
                temp_lines = self.read_all_from_generated(self.temp_file)
            except:
                self.v_print("FAILED")
                temp_lines = ["FAILED"]
                pass
            for lin in temp_lines:
                if self.is_good(lin):
                    good_lines.append(lin)

        this_line = random.choice(good_lines)
        self.v_print("THIS LINE:", this_line)
        self.v_print("Good Lines:", len(good_lines))
        for lin in good_lines:
            self.v_print(lin)
        return this_line

    def write_lines(self, file, lns):
        self.empty_file(file)
        self.v_print("writing file", file)
        with open(file, 'ab') as f:
            for ln in lns:
                f.write(ln.strip().__add__("\n").encode("ASCII", errors="ignore"))

    def dbg_gen_first_line(self):
        dbg_line_db = "lyricdb_working_archive.txt"
        lines = [line.strip() for line in open(dbg_line_db, 'r', errors="ignore")]
        rhyme_list = []
        line = ""
        while len(rhyme_list) < 20 or not line:
            line = random.choice(lines)
            if not line:
                continue
            else:
                last_word = line.split()[-1]
                rhyme_list = pronouncing.rhymes(last_word)
        return line

    def dbg_get_rhyming_line(self, real_line):
        self.v_print("get a rhyming line for:", real_line)
        rhyme_word = real_line.split()[-1]
        rhyme_list = pronouncing.rhymes(rhyme_word)
        rhyme_lines = []
        with open("lyricdb_working_archive.txt", 'r', encoding='utf8', errors='ignore') as filehandle:
            current_line = 1
            for line in filehandle:
                if line and line.strip():
                    this_word = line.split()[-1]
                    if this_word in rhyme_list:
                        rhyme_lines.append(line)
                current_line += 1
        self.v_print("rhyme lines:", len(rhyme_lines))
        if not rhyme_lines:
            return random.choice([line.strip() for line in open("lyricdb_working_archive.txt", 'r', errors="ignore")])
        else:
            return random.choice(rhyme_lines)

    def get_line(self, filename, line_number):
        with open(filename, 'r', encoding='utf8', errors='ignore') as filehandle:
            current_line = 1
            for line in filehandle:
                if current_line == line_number:
                    return line
                current_line += 1

    def run(self):
        self.running = True
        if self.debug:
            lines = [self.dbg_gen_first_line()]
        else:
            lines = [self.gen_next_non_rhyme_line()]
        self.dispatch("add_line", lines[0])
        for i in progressbar.progressbar(range(1, 16)):
            last_line = lines[i - 1]
            self.v_print("gen line no: ", i, "last_line: ", last_line)
            if i % 2 == 1:
                if self.debug:
                    line = self.dbg_get_rhyming_line(last_line)
                else:
                    self.v_print("try: line no: " + str(i))
                    line = self.gen_next_rhyme_line(last_line)
            else:
                if self.debug:
                    line = self.dbg_gen_first_line()
                else:
                    self.v_print("try: line no: " + str(i))
                    line = self.gen_next_non_rhyme_line()
            self.v_print("--------------------")
            self.v_print("APPENDING:", line, i)
            self.dispatch("add_line", line)
            self.v_print("--------------------")
            lines.append(line)
            self.index = i

        self.write_lines(self.lyric_file, lines)
        self.running = False
        self.dispatch("sync_lines", lines)
        self.sess.close()
        try:
            cuda.select_device(0)
            cuda.close()
        except:
            print("could not close cuda device 0")
            pass

        return lines

    def load_or_download_run1(self, r_name):
        self.v_print("load_or_download_run1")
        try:
            self.v_print("trying to load model...")
            gpt2.load_gpt2(self.sess, run_name=r_name)
        except FileNotFoundError:
            self.v_print("downloading model...")
            self.download_run1()
            gpt2.load_gpt2(self.sess, run_name=r_name)
        pass

    def download_run1(self):
        self.v_print("downloading model...")
        url = "https://www.dropbox.com/s/mrg49n67mug6ha4/checkpoint_run1.tar?dl=1"
        urllib.request.urlretrieve(url, "./run1.tar")
        tar = tarfile.open("./run1.tar")
        tar.extractall()
        tar.close()
        os.remove("./run1.tar")
        pass


class Scraper(Publisher):
    def __init__(self, artists, genius_key, bar):
        super().__init__()
        self.artists = artists
        self.genius_key = genius_key
        self.bar = bar

    def scrape(self):
        self.dispatch("scrape_info", "scraping...")
        # scrape
        self.dispatch("scrape_info", "geniusApiKey: " + self.genius_key)
        api = genius.Genius(self.genius_key)
        iter_artist = iter(self.artists)
        for artist in iter_artist:
            self.dispatch("scrape_info", "artist: " + artist)
            artist_api = api.search_artist(artist)
            try:
                artist_api.save_lyrics(overwrite=True)
            except:
                self.dispatch("scrape_error", "Oops! Cant download: " + artist)
            self.bar.update()

    def extract(self):
        """
        extract
        # "songs": [
        # {
        #  "lyrics": "verse..."
        #  } ,
        # ...
        # ]
        :return:
        """
        self.dispatch("scrape_info", "extracting .json to lyricdb.txt...")
        source_path = '.'
        source_files = [f for f in listdir(source_path) if isfile(join(source_path, f))]
        for file in source_files:
            if file.endswith('.json'):
                with open(file) as json_file:
                    data = json.load(json_file)
                    for p in data['songs']:
                        if p['lyrics']:
                            with open("lyricdb.txt", "ab") as myfile:
                                myfile.write(p['lyrics'].encode('ASCII'))

    def clean_folder(self):
        self.dispatch("scrape_info", "cleaning folder...")
        dir_name = "."
        test = os.listdir(dir_name)
        for item in test:
            if item.endswith(".json"):
                os.remove(os.path.join(dir_name, item))

    def clean_lyricdb(self):
        self.dispatch("scrape_info", "cleaning lyricdb file...")
        # clean
        # [intro: eminem] <- needs to be removed
        # ...
        for line in fileinput.input(r"lyricdb.txt", inplace=True):
            if not re.search(r"([^\w\d\s',<?>])", line):
                print(line, end="")


class PColor:
    def __init__(self):
        self.HEADER = '\033[95m'
        self.OK_BLUE = '\033[94m'
        self.OK_GREEN = '\033[92m'
        self.WARNING = '\033[93m'
        self.FAIL = '\033[91m'
        self.END_C = '\033[0m'
        self.BOLD = '\033[1m'
        self.UNDERLINE = '\033[4m'

    def header(self, message):
        return self.HEADER + str(message) + self.END_C

    def blue(self, message):
        return self.OK_BLUE + str(message) + self.END_C

    def green(self, message):
        return self.OK_GREEN + str(message) + self.END_C

    def warn(self, message):
        return self.WARNING + str(message) + self.END_C

    def fail(self, message):
        return self.FAIL + str(message) + self.END_C

    def bold(self, message):
        return self.BOLD + str(message) + self.END_C

    def underline(self, message):
        return self.UNDERLINE + str(message) + self.END_C


class Config:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        # self.parser.add_argument("name", help="name to greet") # mandatory : without - or -- :
        self.parser.add_argument("-c", "--config_file", type=str,
                                 help="file to read config from")

        self.args = self.parser.parse_args()

        if self.args.config_file:
            self.config = self.read_config()
        else:
            self.config = self.dialogue_config()

    def read_config(self):
        config = yaml.safe_load(open(self.args.config_file))
        return config

    def dialogue_config(self):
        config = {}
        # modules = ["scrape", "train", "generate", "voice", "beat"]
        run_order = 0

        inp = input("scrape lyrics? (y/N)\n> ")
        if inp == "y":
            artists = input(
                "list artists to scrape lyrics from (no white lines) eg.: mf-doom aesop-rock grimm-doza ...\n> ")
            # genius_key = input("please paste your genius api key from https://genius.com/api-clients\n> ")
            genius_key = "cE7Gq9g1QMDgDQtLYtEgbvCoLdSqmVFOq__Pma0NndWyAHRLPodOaHU4RpE1jy3R"
            config["scrape"] = {"artists": artists.split(" "),
                                "genius_key": genius_key,
                                "run_order": run_order}
            run_order += 1

        inp = input("train? (y/N)\n> ")
        if inp == "y":
            steps = int(input("for how many steps? (eg.: 1000)\n> "))
            config["train"] = {"run_order": run_order,
                               "steps": steps}
            run_order += 1

        inp = input("generate lyrics? (y/N)\n> ")
        if inp == "y":
            config["generate"] = {"run_order": run_order}
            run_order += 1

        inp = input("generate voice? (y/N)\n> ")
        if inp == "y":
            config["voice"] = {"run_order": run_order}
            run_order += 1

        inp = input("render with beat? (y/N)\n> ")
        if inp == "y":
            config["beat"] = {"run_order": run_order}
            run_order += 1

        with open('conf.yml', 'w') as outfile:
            yaml.dump(config, outfile, default_flow_style=False)

        return config


class Voice(Publisher):
    def __init__(self):
        super().__init__()
        self.tacotron2 = torch.hub.load('nvidia/DeepLearningExamples:torchhub', 'nvidia_tacotron2')
        self.tacotron2 = self.tacotron2.to('cuda')
        self.tacotron2.eval()
        self.waveglow = torch.hub.load('nvidia/DeepLearningExamples:torchhub', 'nvidia_waveglow')
        self.waveglow = self.waveglow.remove_weightnorm(self.waveglow)
        self.waveglow = self.waveglow.to('cuda')
        self.waveglow.eval()

    def v_print(self, *args):
        self.dispatch("log_line", ' '.join([str(a) for a in args]))

    def synthesize(self, lines):
        index = 0
        # self.dispatch("voice", str(lines))
        print("DEBUG", lines)
        for i in range(len(lines)):
            text = lines[i]
            self.dispatch("voice", " synthesizing: " + str(i) + " " + text)
            # preprocessing
            sequence = np.array(self.tacotron2.text_to_sequence(text, ['english_cleaners']))[None, :]
            sequence = torch.from_numpy(sequence).to(device='cuda', dtype=torch.int64)

            # generate the models
            with torch.no_grad():
                _, mel, _, _ = self.tacotron2.infer(sequence)
                audio = self.waveglow.infer(mel)
            audio_numpy = audio[0].data.cpu().numpy()
            rate = 22050

            write("./generated/sentences/audio" + str(index) + ".wav", rate, audio_numpy)
            index += 1

        sentence_dir = "./generated/sentences/"

        sentence_files = [sentence_dir + f for f in listdir(sentence_dir) if isfile(join(sentence_dir, f))]

        # self.dispatch("voice", sentence_files)
        # self.dispatch("voice", len(sentence_files))

        for sentence_file in sentence_files:
            file_name = "./generated/stretched_sentences/" + sentence_file.split("/")[-1]
            # self.dispatch("voice", file_name)
            self.tempo_stretch_bpm(sentence_file, file_name, 1, 90)

        stretched_dir = "./generated/stretched_sentences/"

        stretched_files = [stretched_dir + f for f in listdir(stretched_dir) if isfile(join(stretched_dir, f))]

        self.concat(stretched_files, "./generated/vocals.wav")
        self.dispatch("voice", "GENERATED ./generated/vocals.wav")

    def concat(self, files, path):
        sox.Combiner().build(files, "temp.wav", 'concatenate')
        self.v_print("building with:", path, "sample_rate_in=44100")
        tfm = sox.Transformer()
        tfm.convert(samplerate=44100, n_channels=1, bitdepth=16)
        tfm.contrast(75)
        tfm.build("temp.wav", path)
        os.remove("temp.wav")
        return path

    def stretch_bpm(self, loop, path, bars, bpm):
        self.v_print(loop, path, bars, bpm)
        length = sox.file_info.duration(loop)
        tfm = sox.Transformer()
        factor = (10 * (bars / 4) * (bpm / 90)) / length
        self.v_print("factor: ", factor)
        tfm.stretch(factor)
        tfm.build_file(loop, path)
        return path

    def tempo_stretch_bpm(self, loop, path, bars, bpm):
        self.v_print(loop, path, bars, bpm)
        length = sox.file_info.duration(loop)
        tfm = sox.Transformer()
        factor = length / (10 * (bars / 4) * (bpm / 90))
        self.v_print("factor: ", factor)
        tfm.tempo(factor)
        tfm.build_file(loop, path)
        return path


class Daw(object):
    def concat(self, files, path):
        sox.Combiner().build(files, path, 'concatenate')
        return path

    def mix(self, files, path):
        sox.Combiner().build(files, path, 'merge')
        return path


class P14:
    def __init__(self, config):
        self.config = config
        self.lines = []

    def run(self):
        print("generate")
        commands_to_run = sorted(self.config.items(), key=lambda k_v: k_v[1]['run_order'])
        print(commands_to_run)
        manager = enlighten.get_manager()
        command_bar = manager.counter(total=len(commands_to_run), desc='commands', unit='cmd')
        view = PrintEverythingView("view_name")
        for i in range(len(commands_to_run)):
            command = commands_to_run[i]
            if "scrape" in command:
                print("scraping...")
                dct = {}
                for x in command:
                    if isinstance(x, dict):
                        dct = x
                if not dct:
                    raise ValueError("cant read artists or genius key from config")
                artists = dct.get("artists")  # thrust for debug, has only 4 songs
                key = dct.get("genius_key")
                scrape_bar = manager.counter(total=len(artists), desc='scrape', unit='artists')
                scraper = Scraper(artists, key, scrape_bar)
                scraper.register(view)
                scraper.scrape()
                scraper.extract()
                scraper.clean_folder()
                scraper.clean_lyricdb()
            if "train" in command:
                file_name = "lyricdb.txt"

                gpt2.download_gpt2(model_name="124M")

                sess = gpt2.start_tf_sess()

                gpt2.finetune(sess,
                              dataset=file_name,
                              model_name='124M',
                              steps=1000,
                              restore_from='fresh',
                              run_name='run1',
                              print_every=10,
                              sample_every=200,
                              save_every=500,
                              overwrite=True
                              )
                print("train", command)
            if "generate" in command:
                print("generating...")
                gen = Generator(debug=False, view=view)
                self.lines.extend(gen.run())

            if "voice" in command:
                print("generating voice...")

                print(len(commands_to_run))
                generate_called = False
                for i in range(len(commands_to_run)):
                    print(i)
                    if "generate" in commands_to_run[i]:
                        print("___ GENERATE WAS CALLED B4 ___")
                        generate_called = True

                if not generate_called:
                    lines = self.read_lines("generated/lyrics.txt")
                    self.lines.extend(lines)
                # todo check line order and clenup print statements or dispatches
                voice = Voice()
                voice.register(view)
                print("DEBUG_DEBUG", self.lines)
                voice.synthesize(self.lines)

            if "beat" in command:
                daw = Daw()
                beat = ["./generated/beat.wav", "./generated/beat.wav"]
                song = ["./generated/vocals.wav", "./generated/temp_beat.wav"]
                daw.concat(beat, "./generated/temp_beat.wav")
                daw.mix(song, "./generated/song.wav")
            command_bar.update()
        print(view.headers)
        manager.stop()

    def read_lines(self, file):
        with open(file, 'r', encoding='utf8', errors='ignore') as f:
            content = f.readlines()
            content = [x.strip() for x in content]
            return content


if __name__ == '__main__':
    conf = Config()
    controller = P14(conf.config)
    controller.run()
