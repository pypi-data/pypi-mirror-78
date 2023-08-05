
import c4d
from cioc4d.collapsible_section import CollapsibleSection
from cioc4d.widgets.text_grp import TextGrp
from ciocore.sequence import Sequence


class InfoSection(CollapsibleSection):
    ORDER = 40

    def __init__(self, dialog):

        self.frame_info_widget = None
        self.scout_info_widget = None
        super(InfoSection, self).__init__(dialog, "Info", collapse=True)

    def build(self):

        self.frame_info_widget = TextGrp(
            self.dialog, label="Frame info")

        self.scout_info_widget = TextGrp(
            self.dialog, label="Scout info")

    def populate(self):
        frames_info, scout_info = self._calculate()
        self.frame_info_widget.set_value(frames_info)
        self.scout_info_widget.set_value(scout_info)

    def on_plugin_message(self, widget_id, msg):
        frames_section = self.dialog.section("FramesSection")

        if widget_id in (
            frames_section.chunk_size_widget.int_field_id,
            frames_section.custom_range_widget.check_box_id,
            frames_section.custom_range_widget.text_field_id,
            frames_section.scout_frames_widget.check_box_id,
            frames_section.scout_frames_widget.text_field_id,
            c4d.EVMSG_CHANGE
        ):
            self.populate()

    def _calculate(self):

        frames_section = self.dialog.section("FramesSection")
        try:
            sequence = frames_section.get_sequence()
        except (ValueError, TypeError):
            return ("INVALID SEQUENCE", "INVALID SEQUENCE")
        scout_sequence = frames_section.get_scout_sequence(sequence)
        frame_count = len(sequence)
        task_count = sequence.chunk_count()

        frames_info = "{} --- tasks:{:d} --- frames:{:d}".format(
            sequence, task_count, frame_count)
        scout_info = "No scout frames"

        scout_task_count = 0
        scout_tasks_sequence = None
        if scout_sequence:
            scout_chunks = sequence.intersecting_chunks(scout_sequence)
            if scout_chunks:
                scout_tasks_sequence = Sequence.create(
                    ",".join(str(chunk) for chunk in scout_chunks))
                scout_task_count = len(scout_chunks)

                scout_info = "{} --- tasks:{:d} --- frames:{:d}".format(
                    scout_tasks_sequence, scout_task_count, len(scout_tasks_sequence))

        return (
            frames_info,
            scout_info
        )
