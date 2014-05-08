import sys
from PyQt4 import QtCore,QtGui
from PyQt4.QtCore import QTimeLine
from functools import partial

class ExtendedQLabel( QtGui.QLabel ):
    """
    A class of QLabel with added custom signal slots
    """
    def __init( self,parent ):
        QtGui.QLabel.__init__( self,parent )


    def mouseReleaseEvent( self,ev ):
        """
        Setups the mouseRelease signal
        Connect to this Using
        QtCore.SIGNAL( 'clicked()' ), func)
        """
        self.emit( QtCore.SIGNAL( 'clicked()' ) )



class Dialog( QtGui.QDialog ):

    def __init__( self,parent = None):
        super( Dialog,self ).__init__( parent )

        self.resize( 1150,350 )

        #LAYOUTS!
        #top horizontal row
        layout_root = QtGui.QVBoxLayout()
        layout_top = QtGui.QHBoxLayout()
        layout_root.addLayout( layout_top )

        self.layout_middle = QtGui.QVBoxLayout()

        layout_buttons = QtGui.QVBoxLayout()
        layout_buttons_Top = QtGui.QHBoxLayout()

        #middle layout, vertical to hold the 3 column options row
        layout_previz = QtGui.QVBoxLayout()


        layout_top.addLayout( layout_previz )

        layout_top.addLayout( self.layout_middle )

        layout_buttons.addLayout( layout_buttons_Top )

        selectFilesButton = QtGui.QPushButton( "selectFiles" )
        previzButton = QtGui.QPushButton( "previz" )
        runButton = QtGui.QPushButton( "run" )

        layout_buttons_Top.addWidget( selectFilesButton )
        layout_buttons_Top.addWidget( previzButton )
        layout_buttons_Top.addWidget( runButton )

        self.viewMiscButtonQPlainTextEdit = QtGui.QPlainTextEdit()
        self.progressBar = QtGui.QProgressBar()
        self.progressBar.setValue( 0 )


        i = 0
        self.optionQGroupBox = []
        optionCharQLabel=[]
        optionQLabel = []
        self.layout_exifOption = []
        frameStyle = QtGui.QFrame.Sunken | QtGui.QFrame.Panel
        for row in range( 0,9 ):
            print "b"
            self.layout_exifOption.append( QtGui.QHBoxLayout() )
            self.layout_middle.addLayout( self.layout_exifOption[row] )
            self.optionQGroupBox.append( QtGui.QGroupBox() )

            optionCharQLabel.append( ExtendedQLabel() )
            optionQLabel.append( ExtendedQLabel() )

            optionCharQLabel[i].setParent( self.optionQGroupBox[i] )
            optionCharQLabel[i].setParent( self.optionQGroupBox[i] )
            optionQLabel[i].setParent( self.optionQGroupBox[i] )

            self.optionQGroupBox[i].setTitle( str(row) )
            self.optionQGroupBox[i].setCheckable( 1 )
            self.optionQGroupBox[i].setFixedHeight( 51 )
            self.optionQGroupBox[i].setAlignment(0)

            optionCharQLabel[i].move( 8,25 )
            optionQLabel[i].move( 40,25 )

            optionCharQLabel[i].setText( "txt2" )

            optionQLabel[i].setText( "text3" )

            optionQLabel[i].setFrameStyle( frameStyle )

            optionCharQLabel[i].setFixedWidth( 20 )
            optionQLabel[i].setFixedWidth( 90 )

            self.layout_exifOption[row].addWidget( self.optionQGroupBox[i] )
            i=i+1

        #bottom layout
        self.setLayout( layout_root )
        self.setWindowTitle( self.tr( "LAAAAAA" ) )
        self.layout_middle.addLayout( layout_buttons )

if __name__ == '__main__':
    app = QtGui.QApplication( sys.argv )
    dialog = Dialog( )
    sys.exit( dialog.exec_() )