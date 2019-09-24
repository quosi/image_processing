import PySimpleGUI as sg
import os
import cv2
from image_analyzer_video import video_processor

# layout

layout = [[sg.Text('Choose video to analyze:')],
          [sg.Text('Video file', size=(8, 1)), sg.InputText(), sg.FileBrowse()],
          [sg.Text('Choose threshold:')],
          [sg.Slider(range=(1, 20), orientation='h', size=(34, 20), default_value=4)],
          [sg.Submit(), sg.Cancel()]]

# create the window
window = sg.Window('QC tools - black edge analyzer', layout)

# read the window
event, values = window.Read()
print('value-0', values[0],'button pressed was', event)

# action/processing
window.Close()
print(video_processor(values[0]))

# check
print('value-0', values[0],'button pressed was', event)
print(values, event)
