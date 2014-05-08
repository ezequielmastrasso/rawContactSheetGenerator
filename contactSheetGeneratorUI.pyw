from PyQt4 import QtCore, QtGui




class DragWidget(QtGui.QFrame):
    i=0
    def __init__(self, parent=None,Main=False,width=200,height=200):
        super(DragWidget, self).__init__(parent)

        self.setMinimumSize(width, height)
        self.setFrameStyle(QtGui.QFrame.Sunken | QtGui.QFrame.StyledPanel)
        self.setAcceptDrops(True)

        if Main:
            self.makeIcon("resources/ISO.png")
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-dnditemdata"):
            if event.source() == self:
                event.setDropAction(QtCore.Qt.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
        else:
            event.ignore()

    dragMoveEvent = dragEnterEvent
    def makeIcon(self, image):
        icon = QtGui.QLabel(self)
        icon.setPixmap(QtGui.QPixmap(image))
        icon.move(0, 0)
        icon.show()
        icon.setText(str(self.i))
        #icon.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/x-dnditemdata"):
            itemData = event.mimeData().data("application/x-dnditemdata")
            dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.ReadOnly)

            pixmap = QtGui.QPixmap()
            offset = QtCore.QPoint()
            dataStream >> pixmap >> offset
            print "HERE",event.source()

            newIcon = QtGui.QLabel(self)
            newIcon.setPixmap(pixmap)
            newIcon.move(event.pos() - offset)
            newIcon.show()
            #newIcon.setAttribute(QtCore.Qt.WA_DeleteOnClose)

            newIcon.setText(str(self.i+5))
#            print newIcon.pos()
#            print newIcon
#            print newIcon.text

            if event.source() == self:
                event.setDropAction(QtCore.Qt.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
        else:
            event.ignore()

    def mousePressEvent(self, event):
        child = self.childAt(event.pos())
        if not child:
            return

        pixmap = QtGui.QPixmap(child.pixmap())

        itemData = QtCore.QByteArray()
        dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.WriteOnly)
        dataStream << pixmap << QtCore.QPoint(event.pos() - child.pos())

        mimeData = QtCore.QMimeData()
        mimeData.setData("application/x-dnditemdata", itemData)

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos() - child.pos())

        tempPixmap = QtGui.QPixmap(pixmap)
        painter = QtGui.QPainter()
        painter.begin(tempPixmap)
        painter.fillRect(pixmap.rect(), QtGui.QColor(127, 0, 0, 127))
        painter.end()

        child.setPixmap(tempPixmap)
        print child.pos()
        print child

        if drag.exec_(QtCore.Qt.MoveAction | QtCore.Qt.MoveAction, QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction:
            child.close()
        else:
            child.show()
            child.setPixmap(pixmap)


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    mainWidget = QtGui.QWidget()
    horizontalLayout = QtGui.QHBoxLayout()
    horizontalLayout.addWidget(DragWidget(width=450,height=350))
    horizontalLayout.addWidget(DragWidget(Main=True,width=200,height=200))
    horizontalLayout.addWidget(DragWidget(width=200,height=350))

    mainWidget.setLayout(horizontalLayout)
    mainWidget.setWindowTitle(QtCore.QObject.tr(mainWidget, "Draggable EXIF"))
    mainWidget.show()

    sys.exit(app.exec_())
