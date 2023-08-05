
import re

import c4d
from cioc4d.collapsible_section import CollapsibleSection
from cioc4d.widgets.hidable_text_field_grp import HidableTextFieldGrp
from cioc4d.widgets.int_field_grp import IntFieldGrp
from ciocore.sequence import Sequence


class FramesSection(CollapsibleSection):
    ORDER = 30

    def __init__(self, dialog):

        self.chunk_size_widget = None
        self.custom_range_widget = None
        self.scout_frames_widget = None

        super(FramesSection, self).__init__(dialog, "Frames", collapse=True)

    def build(self):

        self.chunk_size_widget = IntFieldGrp(self.dialog, label="Chunk Size")

        self.custom_range_widget = HidableTextFieldGrp(
            self.dialog, label="Use Custom Range",
            placeholder="e.g. 1-50x2")

        self.scout_frames_widget = HidableTextFieldGrp(
            self.dialog, label="Use Scout Frames",
            placeholder="e.g. auto:3")

    def populate(self):
        self.chunk_size_widget.set_value(2)

        self.custom_range_widget.set_value("1-100")
        self.custom_range_widget.set_visibility(True)

        self.scout_frames_widget.set_value("auto:5")
        self.scout_frames_widget.set_visibility(True)

    def on_plugin_message(self, widget_id, msg):
        if widget_id == self.custom_range_widget.check_box_id:
            self.custom_range_widget.set_visibility()
        if widget_id == self.scout_frames_widget.check_box_id:
            self.scout_frames_widget.set_visibility()

    # TODO: Move some of this logic and the equivalent in ciomaya over to ciocore

    def get_sequence(self):

        chunk_size = self.chunk_size_widget.get_value()
        use_custom_range = self.custom_range_widget.get_visible()
        if use_custom_range:
            custom_range = self.custom_range_widget.get_value()
            return Sequence.create(custom_range, chunk_size=chunk_size, chunk_strategy="progressions")

        document = c4d.documents.GetActiveDocument()
        render_data = document.GetActiveRenderData()          # Get the current renderdata
        fps = document.GetFps()
        start_frame = render_data[c4d.RDATA_FRAMEFROM].GetFrame(fps)
        end_frame = render_data[c4d.RDATA_FRAMETO].GetFrame(fps)
        frame_step = render_data[c4d.RDATA_FRAMESTEP]

        return Sequence.create(start_frame, end_frame, frame_step, chunk_size=chunk_size, chunk_strategy="progressions")

    def get_scout_sequence(self, main_sequence):

        use_scout_frames = self.scout_frames_widget.get_visible()
        if not use_scout_frames:
            return
        scout_frames = self.scout_frames_widget.get_value()

        match = re.compile(r"^auto[, :]+(\d+)$").match(scout_frames)
        if match:
            samples = int(match.group(1))
            return main_sequence.subsample(samples)

        try:
            return Sequence.create(scout_frames)
        except (ValueError, TypeError):
            return
