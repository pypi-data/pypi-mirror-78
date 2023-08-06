from warpseq.server.packet import CommandPacket, ResponsePacket
from warpseq.server.mailbox import Message
from warpseq.server.widgets import Widgets, textbox, select, multiple, button, toggle, rangebox
import json

from warpseq.pages.device import DeviceBuilder
from warpseq.pages.scale import ScaleBuilder
from warpseq.pages.song import SongBuilder
from warpseq.pages.instrument import InstrumentBuilder
from warpseq.pages.scene import SceneBuilder
from warpseq.pages.track import TrackBuilder
from warpseq.pages.pattern import PatternBuilder
from warpseq.pages.transform import TransformBuilder
from warpseq.pages.data_pool import DataPoolBuilder

BUILDERS = dict(
    song=SongBuilder,
    device=DeviceBuilder,
    scale=ScaleBuilder,
    instrument=InstrumentBuilder,
    scene=SceneBuilder,
    track=TrackBuilder,
    pattern=PatternBuilder,
    transform=TransformBuilder,
    data_pool=DataPoolBuilder
)

# BOOKMARK: ADD NEW PAGES HERE

class PageBuilder(object):

    __slots__ = ('templar', 'mailbox', 'widgets')

    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self, templar=None, mailbox=None):

        self.templar = templar
        self.mailbox = mailbox
        widgets = Widgets(templar=self.templar, pages=self)
        self.templar.register('widgets',widgets)
        self.widgets = widgets

    # ------------------------------------------------------------------------------------------------------------------

    def _ask_engine(self, data):

        response = self.mailbox.send_message_and_wait_for_reply(Message(data)).body
        data = json.loads(response)
        pkt = ResponsePacket.from_dict(data)
        assert pkt.ok
        return pkt.data

    # ------------------------------------------------------------------------------------------------------------------

    def _list(self, cmd):
        pkt = CommandPacket(cmd=cmd)
        return self._ask_engine(pkt.to_dict())

    # ------------------------------------------------------------------------------------------------------------------

    def _get_item(self, cmd, item):
        pkt = CommandPacket(cmd=cmd, id=item)
        return self._ask_engine(pkt.to_dict())

    # ------------------------------------------------------------------------------------------------------------------

    def render(self, category, item):

        if category == 'switcher':
            return self.handle_switcher(category, item)
        if item == 'list':
            return self.handle_lists(category, item)
        elif category == 'grid':
            return self.handle_grid(category, item)
        else:
            return self.handle_edit(category, item)

    # ------------------------------------------------------------------------------------------------------------------

    def handle_lists(self, category, item):

        if category in [ 'song', 'grid' ]:
            return ""
        title = "%ss" % category.title()
        items = self._list("list_%s" % category)
        print("LIST RESPONSE: %s" % items)
        return self.templar.render('nav2/list.j2', dict(items=items, category=category, title=title))

    # ------------------------------------------------------------------------------------------------------------------

    def handle_switcher(self, category, item):
        data = dict()
        return self.templar.render('nav1/%s.j2' % category, data)

    # ------------------------------------------------------------------------------------------------------------------

    def handle_grid(self, category, item):
        data = dict()
        return self.templar.render('workspace/%s.j2' % category, data)

    # ------------------------------------------------------------------------------------------------------------------

    def handle_edit(self, category, item):

        data = self._get_item("get_%s" % category, item)

        print("**** SERVER DATA: %s" % data)

        data["new"] = False

        #print("from server: %s" % data)
        data["category"] = category
        builder = BUILDERS[category]
        data.update(builder.build(data["name"], self.widgets, data))
        if 'obj_id' not in data:
            # this happens for song...
            data['obj_id'] = 0
        data["grid"] = builder.has_grid()
        return self.templar.render('workspace/generic.j2', data)