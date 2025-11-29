#!/usr/bin/python3

from scipy.stats import entropy
import numpy as np
import os
import sys
import cv2

# Path containing images of flags:
PATH = "wikimedia_images"
# Name of final ranking list:
OUTPUT = "flag_ranking.txt"


def get_images(path):
    files = []
    images = []
    image_archive = {}
    for (dirpath, dirnames, filenames) in os.walk(path):
        files.extend(filenames)
        break
    file = files[0]
    file = os.path.join(path, file)
    image = cv2.imread(file)

    for filename in files: 
        #File name cleaning. Should be omitted if difference source is used:
        filename_formatted = filename[len("250px-Flag_of_"):filename.index('.')]
        image_archive[filename_formatted] = cv2.imread(os.path.join(path, filename))
    return image_archive


class Priority_Queue:
    def __init__(self):
        self.queue = [] # List shall hold tupel (name, entropy value)

    def is_empty(self):
        return len(self.queue) == 0

    def get_size(self):
        return len(self.queue)

    def purge(self):
        self.queue = []

    def insert(self, label, value):
        item = (label, value)
        self.queue.append(item)
        self._shift_up(len(self.queue)-1)

    def push(self, label, value):
        self.insert(label, value)

    def pop(self):
        size = len(self.queue)
        result = 0
        if size == 0:
            result = None
        else:
            label = self.queue[0][0]
            value = self.queue[0][1]
            self.queue[0] = self.queue[size - 1]
            self.queue.pop()
            self._shift_down(0)
            return (label, value)


    def get_min(self):
        result = 0
        if self.is_empty():
            result = None 
        else: 
            label = self.queue[0][0] 
            value = self.queue[0][1]
        return result


    def _get_p(self, index):
        return (index - 1) // 2
    def _get_lc(self, index):
        return (index * 2) + 1
    def _get_rc(self, index):
        return (index * 2) + 2


    def _shift_up(self, value):
        while (value>0 and self.queue[self._get_p(value)][1] > self.queue[value][1]):
               temp = self.queue[self._get_p(value)]
               self.queue[self._get_p(value)] = self.queue[value]
               self.queue[value] = temp
               value = self._get_p(value)

    def _shift_down(self, value):
        min_index = value
        l = self._get_lc(value)
        r = self._get_rc(value)
        if l < len(self.queue) and self.queue[l][1] < self.queue[min_index][1]:
            min_index = l
        if r < len(self.queue) and self.queue[r][1] < self.queue[min_index][1]:
            min_index = r
        if value != min_index:
           temp = self.queue[value]
           self.queue[value] = self.queue[min_index]
           self.queue[min_index] = temp
           self._shift_down(min_index)



def color_weighted_spectral_entropy(image):
    b_channel, g_channel, r_channel = cv2.split(image)
    
    # Calculate spectral entropy for each channel
    def channel_spectral_entropy(channel):
        f_transform = np.fft.fft2(channel)
        f_shifted = np.fft.fftshift(f_transform)
        magnitude_spectrum = np.abs(f_shifted)
        if np.sum(magnitude_spectrum) > 0:
            normalized = magnitude_spectrum / np.sum(magnitude_spectrum)
        else:
            normalized = magnitude_spectrum
        # Entropy calculation with color channel weighting
        epsilon = 1e-10
        entropy = -np.sum(normalized * np.log2(normalized + epsilon))
        
        return entropy
    
    weighted_entropy = (
        0.333 * channel_spectral_entropy(b_channel) +
        0.333 * channel_spectral_entropy(g_channel) +
        0.333 * channel_spectral_entropy(r_channel)
    )
    
    return float(weighted_entropy)

if __name__ == "__main__":
    queue = Priority_Queue()
    images = get_images(PATH)
    # Both 'white_field' and 'random_distribution' are for sanity checks. Former should be on top and latter on bottom.
    white_field = np.ones_like(images["Chad"]) * 255
    random_distribution = np.random.randint(254, size=(167, 250, 3)) + 1
    white_entropy = color_weighted_spectral_entropy(white_field)
    rando_entropy = color_weighted_spectral_entropy(random_distribution)
    queue.push("white_field", white_entropy)
    queue.push("random_distribution", rando_entropy)
    for image_name, image in images.items():
        r = color_weighted_spectral_entropy(image)
        queue.push(image_name, r)

    i = 0

    with open(OUTPUT, 'w') as f:
        f.write(f"Nations' flag entropy ranking (n={queue.get_size()}). \nImage source: Wikimedia.\n\n")
        while not queue.is_empty():
            q_result = queue.pop()
            f.write(f"{i}\t{q_result[0]}\t\t\t{q_result[1]}\n")
            i += 1


