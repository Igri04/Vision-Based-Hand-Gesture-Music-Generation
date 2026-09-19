
# This module generates musical tones and maps each hand gesture to a specific note.
# Tones are generated mathematically using sine waves at specific frequencies.

import pygame
import numpy as np

# Initialize the pygame audio mixer with stereo output (2 channels)
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

def generate_tone(frequency, duration=0.5, volume=0.5):
    """
    Generate a stereo sine wave tone at the given frequency.
    - frequency: pitch of the note in Hz (e.g. 261.63 = C4)
    - duration: how long the note plays in seconds
    - volume: loudness between 0.0 and 1.0
    """
    sample_rate = 44100
    samples = int(sample_rate * duration)
    t = np.linspace(0, duration, samples, False)
    # Generate sine wave and scale to 16-bit audio range
    wave = (np.sin(2 * np.pi * frequency * t) * volume * 32767).astype(np.int16)
    # Convert to stereo by duplicating the mono channel
    stereo_wave = np.column_stack((wave, wave))  
    sound = pygame.sndarray.make_sound(stereo_wave)
    return sound

# Map each gesture label to a musical note (C major chord)
# These are pre-generated at startup so there is no delay during live inference
GESTURE_SOUNDS = {
    "Open":    generate_tone(261.63),  # C4 - middle C
    "Close":   generate_tone(329.63),  # E4
    "Pointer": generate_tone(392.00),  # G4
    "OK":      generate_tone(523.25),  # C5
}

# Track the last gesture to avoid replaying the same sound repeatedly
last_gesture = None

def play_gesture_sound(gesture_label):
    """
    Play the sound associated with the detected gesture.
    Only triggers when the gesture changes, preventing continuous sound overlap.
    """
    global last_gesture
    if gesture_label in GESTURE_SOUNDS and gesture_label != last_gesture:
        GESTURE_SOUNDS[gesture_label].play()
        last_gesture = gesture_label