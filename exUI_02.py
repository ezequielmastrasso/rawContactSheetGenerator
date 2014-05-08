import datetime
import cPickle
import pickle
import sys

from PyQt4 import QtGui, QtCore

class person(object):
    '''
    a custom data structure, for example purposes
    '''
    def __init__(self, name, dob, house_no):
        self.name = name
        self.dob = dob
        self.addr = "%d Rue de la Soleil"% house_no
    def __repr__(self):
        return "%s\n%s\n%s"% (self.name, self.dob, self.addr)

class simple_model(QtCore.QAbstractListModel):
    def __init__(self, parent=None):
        super(simple_model, self).__init__(parent)
        self.list = []
        for name, dob, house_no in (
        ("Neil", datetime.date(1969,12,9), 23),
        ("John", datetime.date(1952,5,3), 2543),
        ("Ilona", datetime.date(1975,4,6), 1)):
            self.list.append(person(name, dob, house_no))
        self.setSupportedDragActions(QtCore.Qt.MoveAction)

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.list)

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole: #show just the name
            person = self.list[index.row()]
            return QtCore.QVariant(person.name)
        elif role == QtCore.Qt.UserRole:  #return the whole python object
            person = self.list[index.row()]
            return person
        return QtCore.QVariant()

    def removeRow(self, position):
        self.list = self.list[:position] + self.list[position+1:]
        self.reset()

class dropZone(QtGui.QLabel):
    def __init__(self, parent=None):
        super(dropZone, self).__init__(parent)
        self.setMinimumSize(200,200)
        self.set_bg()
        self.setText("Drop Here")
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-person"):
            self.set_bg(True)
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-person"):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.set_bg()

    def dropEvent(self, event):
        data = event.mimeData()
        bstream = data.retrieveData("application/x-person",
            QtCore.QVariant.ByteArray)
        selected = pickle.loads(bstream.toByteArray())
        self.setText(str(selected))
        self.set_bg()
        event.accept()

    def set_bg(self, active=False):
        if active:
            val = "background:yellow;"
        else:
            val = "background:green;"
        self.setStyleSheet(val)


class draggableList(QtGui.QListView):
    '''
    a listView whose items can be moved
    '''
    def ___init__(self, parent=None):
        super(draggableList, self).__init__(parent)
        self.setDragEnabled(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-person"):
            event.setDropAction(QtCore.Qt.QMoveAction)
            event.accept()
        else:
            event.ignore()

    def startDrag(self, event):
        index = self.indexAt(event.pos())
        if not index.isValid():
            return

        ## selected is the relevant person object
        selected = self.model().data(index,QtCore.Qt.UserRole)

        ## convert to  a bytestream
        bstream = cPickle.dumps(selected)
        mimeData = QtCore.QMimeData()
        mimeData.setData("application/x-person", bstream)

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)

        # example 1 - the object itself

        pixmap = QtGui.QPixmap()
        pixmap = pixmap.grabWidget(self, self.rectForIndex(index))

        # example 2 -  a plain pixmap
        #pixmap = QtGui.QPixmap(100, self.height()/2)
        #pixmap.fill(QtGui.QColor("orange"))
        drag.setPixmap(pixmap)

        drag.setHotSpot(QtCore.QPoint(pixmap.width()/2, pixmap.height()/2))
        drag.setPixmap(pixmap)
        result = drag.start(QtCore.Qt.MoveAction)
        if result: # == QtCore.Qt.MoveAction:
            self.model().removeRow(index.row())

    def mouseMoveEvent(self, event):
        self.startDrag(event)

class testDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(testDialog, self).__init__(parent)
        self.setWindowTitle("Drag Drop Test")
        layout = QtGui.QGridLayout(self)

        label = QtGui.QLabel("Drag Name From This List")

        self.model = simple_model()
        self.listView = draggableList()
        self.listView.setModel(self.model)
        self.dz = dropZone()

        layout.addWidget(label,0,0)
        layout.addWidget(self.listView,1,0)
        layout.addWidget(self.dz,0,1,2,2)

if __name__ == "__main__":
    '''
    the try catch here is to ensure that the app exits cleanly no matter what
    makes life better for SPE
    '''
    try:
        app = QtGui.QApplication([])
        dl = testDialog()
        dl.exec_()
    except Exception, e:  #could use as e for python 2.6...
        print e
    sys.exit(app.closeAllWindows())