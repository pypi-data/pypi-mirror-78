"""Main module."""

import pronouncing
import syllables
import progressbar
import gpt_2_simple as gpt2

import logging

import urllib.request
import tarfile
import os
from progressist import ProgressBar

import random


class Generator:
    def __init__(self, log_level="INFO"):
        if "INFO" in log_level:
            logging.basicConfig(level=logging.INFO)
        elif "DEBUG" in log_level:
            logging.basicConfig(level=logging.DEBUG)
        self.sess = gpt2.start_tf_sess()
        self.load_or_download_run1()

    def generate(self, line_count=16):
        """
        generates line_count amount of lines. every second line will rhyme with the previous
        (the last word of every second line will rhyme with the last word of the previous line)
        maybe_todo: add rhyme scheme support (not just ababab...)
        :param line_count:
        :return:
        """
        logging.info("generating lines...")
        lines = [self.gen_next_non_rhyme_line()]
        for i in progressbar.progressbar(range(1, line_count)):
            last_line = lines[i - 1]
            logging.debug(f"gen line num: {i}, last_line: {last_line}")
            if i % 2 == 1:
                line = self.gen_next_rhyme_line(last_line)
            else:
                line = self.gen_next_non_rhyme_line()
            lines.append(line)
        logging.info("generating lines... done!")
        for line in lines:
            print(line)
        return lines

    def gen_next_non_rhyme_line(self):
        """
        returns a line that suffices the is_good metric
        :return:
        """
        good_lines = []
        tries_per_iteration = 100
        i = 0
        while len(good_lines) == 0:
            logging.debug(f"trying to generate line. try:{i}")
            i += 1
            temp_lines = gpt2.generate(
                self.sess,
                return_as_list=True,
                length=12,
                temperature=0.8,
                nsamples=tries_per_iteration,
                batch_size=tries_per_iteration
            )
            temp_lines = [x.strip() for x in temp_lines]
            for line in temp_lines:
                if self.is_good(line):
                    good_lines.append(line)
        return random.choice(good_lines)

    def gen_next_rhyme_line(self, last_line):
        """
        returns a line that suffices the is_good metric and rhymes with last_line
        :param last_line:
        :return:
        """
        good_lines = []
        tries_per_iteration = 100
        i = 0
        while len(good_lines) == 0:
            logging.debug(f"try:{i} to generate rhyming line on line: {last_line}.")
            i += 1
            temp_lines = gpt2.generate(
                self.sess,
                return_as_list=True,
                length=12,
                temperature=0.8,
                nsamples=tries_per_iteration,
                batch_size=tries_per_iteration
            )
            temp_lines = [x.strip() for x in temp_lines]
            last_word = last_line.split()[-1]
            for line in temp_lines:
                this_last_word = line.split()[-1]
                if self.is_good(line) and self.rhymes(last_word, this_last_word):
                    good_lines.append(line)
        return random.choice(good_lines)


    def load_or_download_run1(self):
        """
        tries to load "run1" (a custom gpt2 model trained on rapper lyrics scraped from genius.com)
        if this fails, it downloads this model and tries to load it again
        :return:
        """
        logging.debug("load_or_download_run1")
        try:
            logging.debug("trying to load model...")
            gpt2.load_gpt2(self.sess, run_name="run1")
        except FileNotFoundError:
            logging.debug("downloading model...")
            self.download_run1()
            gpt2.load_gpt2(self.sess, run_name="run1")

    def download_run1(self):
        """
        downloads a custom gpt2 model trained on rapper lyrics scraped from genius.com
        :return:
        """
        logging.debug("downloading custom rapper model...")
        url = "https://www.dropbox.com/s/mrg49n67mug6ha4/checkpoint_run1.tar?dl=1"
        bar = ProgressBar(template="dl run1 |{animation}| {done:B}/{total:B}")
        urllib.request.urlretrieve(url, "./run1.tar", reporthook=bar.on_urlretrieve)
        tar = tarfile.open("./run1.tar")
        tar.extractall()
        tar.close()
        os.remove("./run1.tar")

    def is_good(self, line):
        """
        defines a minimal metric for a "good" line
        # if line is empty or doesn't exist -> not good
        # if line is too short or too long -> not good
        # if there are (almost) no rhyme for the last word -> not good
        # if line is a multi-line line -> not good
        # if the line passed all checks it is good
        :param line:
        :return:
        """
        # if line is empty or doesn't exist -> not good
        if not line or len(line) == 0:
            return False

        # if line is too short or too long -> not good
        syl_count = syllables.estimate(line)
        if not 7 < syl_count < 18:
            return False

        # if there are (almost) no rhyme for the last word -> not good
        last_word = line.split()[-1]
        rhyme_list = pronouncing.rhymes(last_word)
        if not len(rhyme_list) > 20:
            return False

        # if line is a multi-line line -> not good
        if len(line.split("\n")) != 1:
            return False

        # if the line passed all checks it is good
        return True

    def rhymes(self, last_word, this_last_word):
        """
        :returns true if last_word rhymes with this_last_word
        :param last_word:
        :param this_last_word:
        :return:
        """
        return this_last_word in pronouncing.rhymes(last_word)
