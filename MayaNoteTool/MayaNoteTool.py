from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Tool)

        self.setWindowTitle('Maya Note Tool')
        self.resize(300, 300)
        self.qpte_infos = QtWidgets.QPlainTextEdit(self)
        self.setCentralWidget(self.qpte_infos)

        self.node_name:str = "myMayaNote"
        self.attr_name:str = "userNote"
        
        currentContent = self.get_content()
        self.qpte_infos.setPlainText(currentContent)
        self.qpte_infos.textChanged.connect(self.update_note)

    def update_note(self) -> None:
        currentText = self.qpte_infos.toPlainText()
        self.store_note(currentText)

    def store_note(self, pText:str) -> None:
        nodeNote = self.get_node_note(True)
        if not cmds.attributeQuery(self.attr_name, node=nodeNote[0], exists=True):
            cmds.addAttr(nodeNote[0], ln=self.attr_name, dataType="string")
        cmds.setAttr(f"{nodeNote[0]}.{self.attr_name}", pText, type='string')

    def get_content(self) -> str:
        nodeNote = self.get_node_note()
        if nodeNote:
            content = cmds.getAttr(f"{nodeNote[0]}.{self.attr_name}")
            return content if content is not None else ""

    def get_node_note(self, pCreate:bool=False) -> list:
        nodeNote = cmds.ls(self.node_name, type="network")
        if nodeNote:
            return nodeNote
        else:
            if pCreate:
                return [cmds.createNode("network", name=self.node_name)]

if __name__ == "__main__":
    try:
        mayaNoteTool.deleteLater()
    except NameError as e:
        pass
    mayaNoteTool = MainWindow(parent=maya_main_window())
    mayaNoteTool.show()