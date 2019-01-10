#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    AXINTDATA VIEWER
    ~~~~~~~~~~~~~~~~
    Tool to display some AXINTDATA
    :copyright: 2018 - GLINCS-AXINT, see AUTHORS for more details
    :license: Proprietary and confidential, see LICENSE for more details
"""
import csv, datetime, os

import kivy

from kivy.app import App

from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

from kivy.adapters.listadapter import ListAdapter

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.listview import ListItemButton, ListView

from kivy.properties import ObjectProperty

import matplotlib.pyplot as plt

class SensorData:
	def __init__(self, date, value, probe, sensor):
		self.date = date
		self.value = value
		self.probe = probe
		self.sensor = sensor

class LoadDialog(FloatLayout):
	load = ObjectProperty(None)
	cancel = ObjectProperty(None)

class Root(FloatLayout):
	def dismiss_popup(self):
		self._popup.dismiss()

	def show_load(self):
		content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
		self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
		self._popup.open()

	def show_append(self):
		content = LoadDialog(load=self.append, cancel=self.dismiss_popup)
		self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
		self._popup.open()

	def load(self, path, filename):
		self.data = []

		self.append(path, filename)

	def remove_selection(self):
		adapter = self.ids.list_view.adapter

		if isinstance(adapter.selection, bool):
			return

		if len(adapter.selection) == 0:
			return

		del self.data[adapter.selection[0].index]
		self.updateListView()

	def append(self, path, filename):
		self.dismiss_popup()
		
		self.data.extend(self.extract_data_from_csv(filename[0]))

		self.ids.list_view.adapter.bind(on_selection_change=self.updateGraph)

		self.updateListView()

	def updateListView(self):
		theList = []
		for element in self.data:
			theList.append(element.probe + '_' + element.sensor + ' ' + element.date.strftime("%d-%m-%Y %Hh"))

		self.ids.list_view.item_strings = theList

	def updateGraph(self, adapter):

		if isinstance(adapter.selection, bool):
			return

		if len(adapter.selection) == 0:
			return

		selection = adapter.selection[0]

		self.plot_data(self.data[selection.index])

	def extract_data_from_csv(self, path):
		file = open(path, 'r')
		out = csv.reader(file, lineterminator='\n', delimiter=',', quotechar="\"", quoting=csv.QUOTE_ALL)

		all_data = []

		for row in out:
			if row[0] == 'Chan':
				for item in row[1:]:
					try:
						date = datetime.datetime.strptime(path[-18:-4], "%d-%m-%Y_%Hh")
						probe = item[6:13]
						sensor = item[14:16]
					except:
						date = datetime.datetime.strptime(item, "%d-%m-%Y_%Hh")
						probe = path[1:8]
						sensor = path[9:11]

					print(date, probe, sensor)

					obj = SensorData(date, {}, probe, sensor)
					all_data.append(obj)
			else:
				channel = int(row[0])

				for i in range(0, len(row[1:])):
					all_data[i].value[channel] = int(row[i + 1])

		return all_data

	def plot_data(self, data):
		plt.clf()
		x = [i for i in range(4096)]
		y = []

		for elt in x:
			y.append(data.value[elt])

		N = 50
		cumsum, y_mean = [0], []

		for i, yy in enumerate(y, 1):
			cumsum.append(cumsum[i-1] + yy)

			if i >= N:
				mean = (cumsum[i] - cumsum[i-N]) / N
				y_mean.append(mean)
		
		plt.scatter(x, y, s=0.1, c="r")
		plt.plot(x[int(N / 2): - (int(N / 2) - 1)], y_mean)
		plt.ylabel('Hits/h')
		plt.xlabel('Channel')
		plt.subplot_tool()

		plt.gcf()

		App.get_running_app().graphWidget.draw_idle()

class ViewerApp(App):
	def build(self):
		plt.plot([])
		plt.ylabel('Hits/h')
		plt.xlabel('Channel')
		plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)

		self.graphWidget = FigureCanvasKivyAgg(plt.gcf(), size_hint=(.8,1))

		App.get_running_app().root.ids.mainbox.add_widget(self.graphWidget)

if __name__ == '__main__':
	ViewerApp().run()
