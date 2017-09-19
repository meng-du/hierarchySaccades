#!/usr/bin/env python

#
# A skeleton file for PsychoPy experiments
# Author: Meng Du
# August 2017
#

from psychopy_util import *
from localizer_config import *
import random


def show_one_trial(color, duration, pos):
    presenter.show_two_fixations(duration=duration, color=color, pos=pos)


def validation(items):
    # check empty field
    for key in items.keys():
        if items[key] is None or len(items[key]) == 0:
            return False, str(key) + ' cannot be empty.'
    # everything is okay
    return True, ''


def randomization():
    times, positions = [], []
    distances = presenter.pixel2norm(DISTANCE)
    dist_jitters = presenter.pixel2norm(DISTANCE_MAX_JITTER)
    for _ in range(NUM_BLOCKS):
        # times
        tmp_num = (NUM_TRIALS_PER_BLOCK - NUM_TRIALS_PER_BLOCK / 3) / 2
        block_times = [FIXATION_TIMES[1] for _ in range(NUM_TRIALS_PER_BLOCK / 3)] + \
                      [FIXATION_TIMES[0] for _ in range(tmp_num)] + \
                      [FIXATION_TIMES[2] for _ in range(tmp_num)]
        assert(len(block_times) == NUM_TRIALS_PER_BLOCK)
        random.shuffle(block_times)
        times.append(block_times)
        # positions
        block_pos = [(0 + random.uniform(-dist_jitters[0], dist_jitters[0]),
                      distances[1] + random.uniform(-dist_jitters[1], dist_jitters[1]))
                     for _ in range(NUM_TRIALS_PER_BLOCK / 4)] + \
                    [(0 + random.uniform(-dist_jitters[0], dist_jitters[0]),
                      -distances[1] + random.uniform(-dist_jitters[1], dist_jitters[1]))
                     for _ in range(NUM_TRIALS_PER_BLOCK / 4)] + \
                    [(distances[0] + random.uniform(-dist_jitters[0], dist_jitters[0]),
                      0 + random.uniform(-dist_jitters[1], dist_jitters[1]))
                     for _ in range(NUM_TRIALS_PER_BLOCK / 4)] + \
                    [(-distances[0] + random.uniform(-dist_jitters[0], dist_jitters[0]),
                      0 + random.uniform(-dist_jitters[1], dist_jitters[1]))
                     for _ in range(NUM_TRIALS_PER_BLOCK / 4)]
        assert(len(block_pos) == NUM_TRIALS_PER_BLOCK - 2)
        random.shuffle(block_pos)
        block_pos.insert(0, (0, 0))
        block_pos.append((0, 0))
        positions.append(block_pos)
    return times, positions


if __name__ == '__main__':
    # subject ID dialog
    sinfo = {'ID': '', 'Mode': ['Exp', 'Test']}
    show_form_dialog(sinfo, validation, order=['ID', 'Mode'])
    sid = int(sinfo['ID'])

    # create log file
    infoLogger = DataLogger(LOG_FOLDER, str(sid) + '_localizer.log', 'info_logger', logging_info=True)
    # create window
    serial = SerialUtil(SERIAL_PORT, BAUD_RATE, logger='info_logger')
    presenter = Presenter(fullscreen=(sinfo['Mode'] == 'Exp'), info_logger='info_logger', serial=serial)

    # show instructions
    # get trial sequences
    time_seq, pos_seq = randomization()
    # show trials
    for b in range(NUM_BLOCKS):
        presenter.show_instructions('', next_page_text=None, duration=1, wait_trigger=True)  # TODO time between blocks?
        infoLogger.logger.info('Block ' + str(b) + ' fixations')
        for t in range(NUM_TRIALS_PER_BLOCK):
            show_one_trial(color=RED, duration=time_seq[b][t], pos=pos_seq[b][t])
        presenter.show_instructions('', next_page_text=None, duration=1, wait_trigger=True)  # TODO time between blocks?
        infoLogger.logger.info('Block ' + str(b) + ' saccades')
        for t in range(NUM_TRIALS_PER_BLOCK):
            show_one_trial(color=GREEN, duration=time_seq[b][t], pos=pos_seq[b][t])
    # end of experiment
    infoLogger.logger.info('End of experiment')