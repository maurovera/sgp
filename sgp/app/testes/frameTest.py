import os 
import unittest
import Widget
       
class DefaultWidgetSizeTestCase(unittest.TestCase):
    def runTest(self):
        widget = Widget("The widget")
        assert widget.size() == (50,50), 'incorrect default size'