import uuid

import ipywidgets as widgets
import traitlets
from ipyvue import VueTemplate
from traitlets import Unicode

from ._version import __version__


# See js/lib/kodexa.js for the frontend counterpart to this file.

@widgets.register
class KodexaNodeWidget(VueTemplate):
    """Kodexa Widget for Rendering Conten Nodes"""

    # Name of the widget view class in front-end
    _view_name = Unicode('KodexaView').tag(sync=True)

    # Name of the widget model class in front-end
    _model_name = Unicode('KodexaModel').tag(sync=True)

    # Name of the front-end module containing widget view
    _view_module = Unicode('kodexa-widget').tag(sync=True)

    # Name of the front-end module containing widget model
    _model_module = Unicode('kodexa-widget').tag(sync=True)

    # Version of the front-end module containing widget view
    _view_module_version = Unicode(__version__).tag(sync=True)
    # Version of the front-end module containing widget model
    _model_module_version = Unicode(__version__).tag(sync=True)

    node = traitlets.Dict().tag(sync=True)

    template = traitlets.Unicode('''
        <div>
           <kodexa-content-node 
                :node="node">
            </kodexa-content-node>
        </div>
    ''').tag(sync=True)

    def __init__(self, content_node):
        widgets.DOMWidget.__init__(self)
        self.node = content_node.to_dict()


@widgets.register
class KodexaDocumentWidget(VueTemplate):
    """Kodexa Widget for Rendering Documents"""

    # Name of the widget view class in front-end
    _view_name = Unicode('KodexaView').tag(sync=True)

    # Name of the widget model class in front-end
    _model_name = Unicode('KodexaModel').tag(sync=True)

    # Name of the front-end module containing widget view
    _view_module = Unicode('kodexa-widget').tag(sync=True)

    # Name of the front-end module containing widget model
    _model_module = Unicode('kodexa-widget').tag(sync=True)

    # Version of the front-end module containing widget view
    _view_module_version = Unicode(__version__).tag(sync=True)
    # Version of the front-end module containing widget model
    _model_module_version = Unicode(__version__).tag(sync=True)

    document_bytes = traitlets.Bytes().tag(sync=True)
    width = traitlets.Integer(600).tag(sync=True)
    height = traitlets.Integer(750).tag(sync=True)
    tags = traitlets.List(None, allow_none=True).tag(sync=True)
    hide_controls = traitlets.Bool(False).tag(sync=True)
    tooltip = traitlets.Bool(False).tag(sync=True)
    mixin = traitlets.Unicode(None, allow_none=True).tag(sync=True)
    options = traitlets.Dict({}).tag(sync=True)
    ref_id = traitlets.Unicode().tag(sync=True)

    def vue_update_tag(self, tag_update):
        print("updating tag " + self.ref_id)
        for tag in tag_update:
            for uuid in tag_update[tag]:
                for node in self.document.select('//*[uuid()="' + uuid + '"]'):
                    node.tag(tag)

    template = traitlets.Unicode('''
        <div>
        {{ref_id}}
           <kodexa-document 
                :refId="ref_id"
                :data-view="document_bytes" 
                :width="width" 
                :height="height" 
                :tooltip="tooltip"
                :tags="tags"
                :hide-controls="hide_controls"
                :options="options"
                @update="(tag_update) => update_tag(tag_update)"
                :mixin=mixin>
            </kodexa-document>
            
        </div>
    ''').tag(sync=True)

    def __init__(self, document, width=600, height=700, hide_controls=False, tooltip=False, mixin=None, options=None,
                 tags=None):

        widgets.DOMWidget.__init__(self)

        if options is None:
            options = {}
        self.ref_id = 'kdxa' + str(uuid.uuid4()).replace('-', '')
        self.document = document
        self.document_bytes = document.to_msgpack()
        self.width = width
        self.height = height
        self.hide_controls = hide_controls
        self.tooltip = tooltip
        self.mixin = mixin
        self.options = options
        self.tags = tags
