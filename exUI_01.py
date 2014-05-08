import sys
from PyQt4 import QtGui, QtCore

class TestTreeView(QtGui.QTreeView):
    def __init__(self, parent = None):
        super(TestTreeView, self).__init__(parent)
        self.setDragEnabled(True)

    def startDrag(self, dropAction):
        print('tree start drag')

        icon = QtGui.QIcon('/home/image.png')
        pixmap = icon.pixmap(64, 64)

        mime = QtCore.QMimeData()
        mime.setData('application/x-item', '???')

        drag = QtGui.QDrag(self)
        drag.setMimeData(mime)        
        drag.setHotSpot(QtCore.QPoint(pixmap.width()/2, pixmap.height()/2))
        drag.setPixmap(pixmap)        
        drag.start(QtCore.Qt.CopyAction)

class TestGraphicsView(QtGui.QGraphicsView): 
    def __init__(self, parent = None):
        super(TestGraphicsView, self).__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        print('graphics view drag enter')
        if (event.mimeData().hasFormat('application/x-item')):
            event.acceptProposedAction()
            print('accepted')
        else:
            event.ignore()    

    def dropEvent(self, event): 
        print('graphics view drop')
        event.acceptProposedAction()                 

class MainForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        self.model = QtGui.QStandardItemModel()

        for k in range(0, 4):
            parentItem = self.model.invisibleRootItem()
            for i in range(0, 4):
                item = QtGui.QStandardItem(QtCore.QString("item %0 %1").arg(k).arg(i))
                parentItem.appendRow(item)
                parentItem = item

        self.setMinimumSize(300, 400)

        self.view = TestTreeView(self)
        self.view.setModel(self.model)
        self.view.setMinimumSize(300, 200)

        self.graphicsView = TestGraphicsView(self)
        self.graphicsView.setGeometry(0, 210, 300, 400)        

        self.layout = QtGui.QVBoxLayout(self.centralWidget())        
        self.layout.addWidget(self.view)
        self.layout.addWidget(self.graphicsView)

def main():
    app = QtGui.QApplication(sys.argv)
    form = MainForm()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main() 