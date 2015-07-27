#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pystamps
----------------------------------

Tests for `pystamps` module.
"""


from pystamps import pystamps
from PySide import QtCore
import os

FILE_1 = os.path.join(
    'tests', 'mission_data', '2m132591087cfd1800p2977m2f1.img')
FILE_2 = os.path.join(
    'tests', 'mission_data', '2p129641989eth0361p2600r8m1.img')
FILE_3 = os.path.join(
    'tests', 'mission_data', '1p190678905erp64kcp2600l8c1.img')
FILE_4 = os.path.join(
    'tests', 'mission_data', 'r01090al.img')
FILE_5 = os.path.join(
    'tests', 'mission_data', '1p134482118erp0902p2600r8m1.img')
FILE_6 = os.path.join(
    'tests', 'mission_data', '58n3118.img')
FILE_7 = os.path.join(
    'tests', 'mission_data', '0047MH0000110010100214C00_DRCL.IMG')
NOT_SELECTED = (
    "QLabel {background-color: black; border: 3px solid rgb(240, 198, 0)}"
                )
SELECTED = (
    "QLabel {background-color: black; border: 3px solid rgb(255, 255, 255)}"
            )
TEST_DIR = os.path.join('tests', 'mission_data')


def test_ImageSet():
    image_set = pystamps.ImageSet(TEST_DIR)
    assert len(image_set.names) > 6
    assert len(image_set.inlist) > 6
    assert len(image_set.inlist) <= len(image_set.names)
    assert len(image_set.images) == 6
    assert not(FILE_7 in image_set.images)
    assert str(image_set.images[0]) == FILE_1
    assert str(image_set.images[1]) == FILE_2


def test_ImageStamp_1():
    image_set = pystamps.ImageSet(TEST_DIR)
    assert image_set.images[0].file_name == FILE_1
    assert image_set.images[0].row == 0
    assert image_set.images[0].column == 0
    assert image_set.images[0].position == (0, 0)
    assert not(image_set.images[0].selected)
    assert image_set.images[0].pds_compatible


def test_ImageStamp_2():
    stamp = pystamps.ImageStamp(FILE_2, 0, 1)
    assert stamp.file_name == FILE_2
    assert stamp.row == 0
    assert stamp.column == 1
    assert stamp.position == (0, 1)
    assert not(stamp.selected)
    assert stamp.pds_compatible


def test_ImageStamp_3():
    stamp = pystamps.ImageStamp(FILE_7, 10, 342)
    assert stamp.file_name == FILE_7
    assert stamp.row == 10
    assert stamp.column == 342
    assert not(stamp.pds_compatible)


def test_select_image_1(qtbot):
    image_set = pystamps.ImageSet(TEST_DIR)
    view = pystamps.ImageSetView(image_set.images)
    test_image_1 = view.images[0]
    image_1 = test_image_1.button
    qtbot.addWidget(image_1)
    # Test that the image was once not selected
    assert not(test_image_1.selected)
    assert test_image_1.container.styleSheet() == NOT_SELECTED
    qtbot.mouseClick(image_1, QtCore.Qt.LeftButton)
    # Test the image is now selected
    assert test_image_1.selected
    # Test the border changed
    assert test_image_1.container.styleSheet() == SELECTED
    qtbot.mouseClick(image_1, QtCore.Qt.LeftButton)
    # Test that the program unselects
    assert not(test_image_1.selected)
    assert test_image_1.container.styleSheet() == NOT_SELECTED


def test_select_image_2(qtbot):
    # Test Second Image
    image_set = pystamps.ImageSet(TEST_DIR)
    view = pystamps.ImageSetView(image_set.images)
    test_image_2 = view.images[1]
    image_2 = test_image_2.button
    qtbot.addWidget(image_2)
    # Test that the image was once not selected
    assert not(test_image_2.selected)
    assert test_image_2.container.styleSheet() == NOT_SELECTED
    qtbot.mouseClick(image_2, QtCore.Qt.LeftButton)
    # Test the image is now selected
    assert test_image_2.selected
    # Test the border changed
    assert test_image_2.container.styleSheet() == SELECTED
    qtbot.mouseClick(image_2, QtCore.Qt.LeftButton)
    # Test that the program unselects
    assert not(test_image_2.selected)
    assert test_image_2.container.styleSheet() == NOT_SELECTED


def test_select_all(qtbot):
    image_set = pystamps.ImageSet(TEST_DIR)
    window = pystamps.MainWindow(image_set.images)
    image_1 = window.images[0]
    image_2 = window.images[1]
    # Test both images were by default not selected
    assert not(image_1.selected)
    assert not(image_2.selected)
    assert window.selected_all_toggle
    assert image_1.container.styleSheet() == NOT_SELECTED
    assert image_2.container.styleSheet() == NOT_SELECTED
    window.select_all()
    # Test that both images were selected
    assert image_1.selected
    assert image_2.selected
    assert not(window.selected_all_toggle)
    assert image_1.container.styleSheet() == SELECTED
    assert image_2.container.styleSheet() == SELECTED
    # Test that all images are deselected again after one is deselected
    window.view
    button_1 = window.images[0].button
    qtbot.addWidget(button_1)
    qtbot.mouseClick(button_1, QtCore.Qt.LeftButton)
    assert not(image_1.selected)
    assert image_1.container.styleSheet() == NOT_SELECTED
    window.select_all()
    assert not(image_1.selected)
    assert not(image_2.selected)
    assert window.selected_all_toggle
    assert image_1.container.styleSheet() == NOT_SELECTED
    assert image_2.container.styleSheet() == NOT_SELECTED


def test_resize_wrap(qtbot):
    image_set = pystamps.ImageSet(TEST_DIR)
    window = pystamps.MainWindow(image_set.images)
    default_width = window.width()
    images = window.images
    # Test that items are correct before resize
    assert images[0].position == (0, 0)
    assert images[4].position == (1, 0)
    assert images[5].position == (1, 1)
    # Test items move to the right place after resizing window to be larger
    window.resize(default_width + default_width/4, window.height())
    assert window.width() > default_width
    assert images[0].position == (0, 0)
    assert images[4].position == (0, 4)
    assert images[5].position == (1, 0)
    window.resize(window.width() + default_width/4, window.height())
    assert images[0].position == (0, 0)
    assert images[4].position == (0, 4)
    assert images[5].position == (0, 5)
    # Test items move to the right place after resizing window to be smaller
    window.resize(window.width() - default_width/4, window.height())
    assert images[0].position == (0, 0)
    assert images[4].position == (0, 4)
    assert images[5].position == (1, 0)
    window.resize(window.width() - 3 * (default_width/4), window.height())
    assert images[0].position == (0, 0)
    assert images[1].position == (0, 1)
    assert images[2].position == (1, 0)
    assert images[3].position == (1, 1)
    assert images[4].position == (2, 0)
    assert images[5].position == (2, 1)
