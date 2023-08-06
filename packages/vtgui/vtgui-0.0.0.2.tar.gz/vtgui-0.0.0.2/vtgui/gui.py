import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
import os
_root=os.path.dirname(__file__)
from wk import PointDict
g=PointDict()


class VirtualWidget:
    pass
def setAttributes(widget,kwargs):
    for k,v in kwargs.items():
        if k.startswith('on'):
            getattr(widget,k[2:]).connect(v)
        else:
            k='set'+k
            getattr(widget,k)(v)
    return widget
def addChild(widget,child):
    # print('adding %s to %s'%(child,widget))
    ws=(QWidget,QLabel,QLayout)
    assert isinstance(widget,ws)
    if isinstance(child,(QLayout,QHBoxLayout,QVBoxLayout)):
        widget.addLayout(child)
    elif isinstance(child,(QAction)):
        widget.addAction(child)
    elif isinstance(child,(QWidget)):
        widget.addWidget(child)
    elif isinstance(child,(VirtualWidget)):
        if isinstance(child,(VStretch)):
            widget.addStretch(child.size)
        elif isinstance(child,(VSpacing)):
            widget.addSpacing(child.size)
    else:
        raise

class VWidget:
    __qtwidget__=QWidget
    def __init__(self,*args,**kwargs):
        id=kwargs.pop('id',None)
        if id:
            self.id=id
            g[id]=self

        self.widget=self.makeRealWidget(*args)

        # print(self.__qtwidget__,self.widget)
        assert self.widget is not None
        self.setAttributes(kwargs)
    def makeRealWidget(self,*args):
        return self.__qtwidget__(*args)
    def __call__(self, *args):
        for child in args:
            if isinstance(child,(VWidget)):
                child=child.widget
            addChild(self.widget,child)
        return self
    def setAttributes(self,attrs):
        setAttributes(self.widget,attrs)
    def detach(self):
        return self.widget
class VVBoxLayout(VWidget):
    __qtwidget__ = QVBoxLayout
class VHBoxLayout(VWidget):
    __qtwidget__ = QHBoxLayout
class VLabel(VWidget):
    __qtwidget__ = QLabel
class VAction(VWidget):
    __qtwidget__ = QAction
class VLineEdit(VWidget):
    __qtwidget__ = QLineEdit
class VToolBar(VWidget):
    __qtwidget__ = QToolBar
class VComboBox(VWidget):
    __qtwidget__ = QComboBox
class VPushButton(VWidget):
    __qtwidget__ = QToolButton
    def makeRealWidget(self,text):
        btn=self.__qtwidget__()
        btn.setText(text)
        return btn
class VStretch(VirtualWidget):
    def __init__(self,size=10):
        self.size=size
class VSpacing(VirtualWidget):
    def __init__(self,size=10):
        self.size=size
