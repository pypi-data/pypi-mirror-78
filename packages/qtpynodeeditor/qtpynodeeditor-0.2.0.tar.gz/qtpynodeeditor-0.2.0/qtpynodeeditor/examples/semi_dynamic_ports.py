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

    _input_ports = 5
    _output_ports = 1

    def __init__(self, style=None, parent=None):
        super().__init__(style=style, parent=parent)
        self._number = None

    @property
    def num_ports(self):
        return {
            PortType.input: self._input_ports,
            PortType.output: self._output_ports,
        }

    @property
    def data_type(self):
        return {
            'input': {i: MyNodeData.data_type for i in range(self._input_ports)},
            'output': {i: MyNodeData.data_type for i in range(self._output_ports)},
        }

    @property
    def port_caption(self):
        return {
            'input': {i: f'caption{i}' for i in range(self._input_ports)},
            'output': {i: f'caption{i}' for i in range(self._output_ports)},
        }

    @property
    def port_caption_visible(self):
        return {
            'input': {i: True for i in range(self._input_ports)},
            'output': {i: True for i in range(self._output_ports)},
        }

    def out_data(self, port):
        return MyNodeData()

    def set_in_data(self, node_data, port):
        ...

    # def embedded_widget(self):
    #     return self._input_line_edit


def main(app):
    registry = qtpynodeeditor.DataModelRegistry()
    registry.register_model(MyDataModel, category='My Category')
    scene = qtpynodeeditor.FlowScene(registry=registry)

    view = qtpynodeeditor.FlowView(scene)
    view.setWindowTitle("Style example")
    view.resize(800, 600)

    node = scene.create_node(MyDataModel)
    node.model._input_ports = 1
    node.model._output_ports = 1

    node = scene.create_node(MyDataModel)
    node.model._input_ports = 5
    node.model._output_ports = 5
    return scene, view, [node]


if __name__ == '__main__':
    logging.basicConfig(level='DEBUG')
    app = QtWidgets.QApplication([])
    scene, view, nodes = main(app)
    view.show()
    app.exec_()
