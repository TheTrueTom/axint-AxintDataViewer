# Axint Data Viewer
Tool to display data provided by the axintdata-extract tool

## Requirements
- kivy, kivy.garden, kivy.deps.sdl2, kivy.deps.glew
- matplotlib
- garden install matplotib --kivy

## Compilation
- PC: Run pyinstaller main.spec in the app folder (don't forget to change relevant paths in the spec file)
- Max/unix: not tested

## Usage
- Open to open a new csv file
- Append to add the content of a csv file to the current data
- When a row is selected, click Delete to remove row. Deleting a row won't remove it from the csv file

## Licence

The MIT License (MIT)

Copyright (c) 2019 Thomas Brichart

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
