import logging

from qtpy import QtWidgets, QtGui

import qtpynodeeditor
from qtpynodeeditor import (NodeData, NodeDataModel, NodeDataType, PortType,
                            StyleCollection)

class MyNodeData(NodeData):
    data_type = NodeDataType(id='MyNodeData', name='My Node Data')


class MyDataModel(NodeDataModel):
    name = 'MyDataModel'
    caption = 'Caption'
    caption_visible = True

    _input_ports = 1
    _max_input_ports = 100

    data_type = {
        'input': {i: MyNodeData.data_type for i in range(_max_input_ports)},
        'output': {i: MyNodeData.data_type for i in range(_max_input_ports)},
    }
    port_caption = {
        'input': {i: f'caption{i}' for i in range(_max_input_ports)},
        'output': {i: f'caption{i}' for i in range(_max_input_ports)},
    }
    port_caption_visible = {
        'input': {i: True for i in range(_max_input_ports)},
        'output': {i: True for i in range(_max_input_ports)},
    }

    def __init__(self, style=None, parent=None):
        super().__init__(style=style, parent=parent)
        self._number = None
        self._input_line_edit = QtWidgets.QLineEdit()
        self._input_line_edit.setValidator(
            QtGui.QIntValidator(bottom=1, top=self._max_input_ports)
        )
        self._input_line_edit.setMaximumSize(self._input_line_edit.sizeHint())
        self._input_line_edit.textChanged.connect(self.change_input_port_count)
        self._input_line_edit.setText(str(self._input_ports))

    def change_input_port_count(self, count):
        self._input_ports = int(count)
        print('change', self._input_ports)
        MyDataModel._input_ports = int(count)

    @property
    def num_ports(self):
        return {
            PortType.input: self._input_ports,
            PortType.output: 3,
        }

    def out_data(self, port):
        return MyNodeData()

    def set_in_data(self, node_data, port):
        ...

    def embedded_widget(self):
        return self._input_line_edit


def main(app):
    registry = qtpynodeeditor.DataModelRegistry()
    registry.register_model(MyDataModel, category='My Category')
    scene = qtpynodeeditor.FlowScene(registry=registry)

    view = qtpynodeeditor.FlowView(scene)
    view.setWindowTitle("Style example")
    view.resize(800, 600)

    node = scene.create_node(MyDataModel)
    return scene, view, [node]


if __name__ == '__main__':
    logging.basicConfig(level='DEBUG')
    app = QtWidgets.QApplication([])
    scene, view, nodes = main(app)
    view.show()
    app.exec_()
