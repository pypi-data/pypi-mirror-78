import abc
import importlib
import inspect
import os
import re

import c4d
from cioc4d import asset_cache
# from ciocore.expander import Expander
from ciocore.gpath import Path
from ciocore.gpath_list import GLOBBABLE_REGEX, PathList
from ciocore.validator import ValidationError, Validator
from cioc4d.conductor_dialog import DEFAULT_TASK_TEMPLATE

class ValidateUploadDaemon(Validator):
    def run(self, _):
        dialog = self._submitter
        use_daemon = dialog.section(
            "UploadOptionsSection").use_daemon_widget.get_value()
        if not use_daemon:
            return

        msg = "This submission expects an uploader daemon to be running.\n After you press submit you can open a shell and type: 'conductor uploader'"

        location = (dialog.section(
            "LocationSection").widget.get_value() or "").strip()
        if location:
            msg = "This submission expects an uploader daemon to be running and set to a specific location tag.\nAfter you press OK you can open a shell and type: 'conductor uploader --location {}'".format(
                location)

        self.add_notice(msg)
        # By also writing the message to the console, the user can copy paste
        # `conductor uploader --location blah`.
        c4d.WriteConsole(msg)


class ValidateTaskCount(Validator):
    def run(self, _):
        dialog = self._submitter
        count = dialog.section("InfoSection").frame_count
        if count > 1000:
            self.add_notice(
                "This submission contains over 1000 tasks ({}). Are you sure this is correct?".format(count))


class ValidateDestinationDirectoryClash(Validator):
    def run(self, _):
        dialog = self._submitter

        dest = dialog.section("GeneralSection").resolve_destination_path()

        # Validate path containment without drive letters
        dest_path = Path(dest).posix_path(with_drive=False)
 
        for gpath in asset_cache.data(self._submitter):
            asset_path = gpath.posix_path(with_drive=False)
            if asset_path.startswith(dest_path):
                c4d.WriteConsole("Some of your upload assets exist in the specified output destination directory\n. {} contains {}".format(
                    dest_path, asset_path))
                self.add_error(
                    "The destination directory for rendered output contains assets that are in the upload list. This can cause your render to fail. See the script editor for details.")
                break
            if dest_path.startswith(asset_path):
                c4d.WriteConsole("You are trying to upload a directory that contains your destination directory.\n. {} contains {}".format(
                    asset_path, dest_path))
                self.add_error(
                    "One of your assets is a directory that contains the specified output destination directory. This will cause your render to fail. See the script editor for details.")
                break


class ValidateRenderToDestinationDirectory(Validator):
    def run(self, _):
        # TODO, break this up into its component parts

        dialog = self._submitter
  
        dest = dialog.section("GeneralSection").resolve_destination_path()
        dest_path = Path(dest).posix_path(with_drive=False)

        task_template_widget = dialog.section("TaskSection").widget
        task_template_visible = task_template_widget.get_visible()

        task_template = task_template_widget.get_value() if task_template_visible else DEFAULT_TASK_TEMPLATE 
        
        document = c4d.documents.GetActiveDocument()

        render_data = document.GetActiveRenderData()
        if not render_data[c4d.RDATA_GLOBALSAVE]:
            self.add_warning(
                "Saving images is not enabled in Render settings. Your render will most likely fail.")
            return

        do_image_save = render_data[c4d.RDATA_SAVEIMAGE]
        do_multipass_save = render_data[c4d.RDATA_MULTIPASS_SAVEIMAGE] and render_data[c4d.RDATA_MULTIPASS_ENABLE]

        self._validate_image(
            "image",
            "-oimage",
            task_template,
            do_image_save,
            c4d.RDATA_PATH,
            dest_path,
            document,
            render_data
        )

        self._validate_image(
            "multi-image",
            "-omultipass",
            task_template,
            do_multipass_save,
            c4d.RDATA_MULTIPASS_FILENAME,
            dest_path,
            document,
            render_data
        )

    def _validate_image(
            self,
            label,
            override_flag,
            task_template,
            do_save,
            c4d_filename_id,
            dest_path,
            document,
            render_data):


        common_help =   """If you continue, your submission will probably fail. 
Images should be written somewhere below the Destination Directory. 
You should change either the path in Render Settings, or the Conductor destination directory."""


        if override_flag in task_template:
            self.add_notice(
                """Your task template overrides the Render Settings image path with the {} flag. 
This is fine, but please ensure it points to a writable directory. 
It should be somewhere inside the Destination Directory. Check the Preview pane.""".format(override_flag))
            return

        image_path = render_data[c4d_filename_id]

        if not (image_path and do_save):
            self.add_notice(
                "This file does not specify an output {}. ".format(label))
            return

        try:
            if Path(image_path).relative:
                image_path = os.path.join(
                    document.GetDocumentPath(), image_path)

            image_path = Path(image_path).posix_path(with_drive=False)

            if not image_path.startswith(dest_path):
                self.add_warning(
                    """The {} path you've set in Render Settings does not point to a writable location.
{}""".format(label, common_help))
            return
        except ValueError:
            self.add_warning(
                """The {} path set in Render Settings is not a valid path.
{}""".format(label, common_help))

class ValidateMissingExtraAssets(Validator):

    def run(self, _):

        missing = []
        for gpath in self._submitter.section("AssetsSection").pathlist:
            pp = gpath.posix_path()
            if not os.path.exists(pp):
                missing.append(pp)

        if missing:
            self.add_warning(
                "Some of the assets specified in the Extra Assets section do not exist on disk. See the console for details. You can continue if you don't need them.")

            c4d.WriteConsole("----- Conductor Asset Validation -------\n")
            for asset in missing:
                c4d.WriteConsole("Missing: {}\n".format(asset))


class ValidateDontSaveVideoPosts(Validator):

    GI_AUTOSAVE_ID = 3804
    AO_AUTOSAVE_ID = 2204
    AO_USE_CACHE_ID = 2000

    def run(self, _):
        document = c4d.documents.GetActiveDocument()
        render_data = document.GetActiveRenderData()
        vp = render_data.GetFirstVideoPost()
        while (vp):
            if vp.CheckType(c4d.VPglobalillumination):
                self._validate_video_post(
                    vp, "Global Illumination", self.GI_AUTOSAVE_ID)
            elif vp.CheckType(c4d.VPambientocclusion):
                self._validate_video_post(
                    vp, "Ambient occlusion", self.AO_AUTOSAVE_ID, self.AO_USE_CACHE_ID)
            vp = vp.GetNext()

    def _validate_video_post(self, vp, label, *ids):
        if vp.GetBit(c4d.BIT_VPDISABLED):
            return
        container = vp.GetDataInstance()
        for element_id in ids:
            if not container[element_id]:
                return

        self.add_warning(
            "{} Auto Save is set to ON. You should turn it off for the render, otherwise it may try to write files in a read-only directory and cause the render to fail".format(label))


# Implement more validators here
####################################
####################################


def run(dialog, submitting=True):

    errors, warnings, notices = _run_validators(dialog)

    if errors:
        msg = ""
        msg += "Some errors would cause the submission to fail:\n\n" + \
            "\n".join(errors)+"\n"
        c4d.gui.MessageDialog(msg,  type=c4d.GEMB_OK)
        raise ValidationError(msg)
    if notices or warnings:
        if submitting:
            msg = "Would you like to continue this submission?\n\n"
            dialog_type = c4d.GEMB_OKCANCEL
        else:
            msg = "Validate only.\n\n"
            dialog_type = c4d.GEMB_OK

        if warnings:
            msg += "Please check the warnings below:\n\n" + \
                "\n\n".join(["[WARN]:{}".format(w) for w in warnings]) + "\n\n"
        if notices:
            msg += "Please check the notices below:\n\n" + \
                "\n\n".join(["[INFO]:{}".format(n) for n in notices]) + "\n\n"

        result = c4d.gui.MessageDialog(msg, type=dialog_type)
        if result != c4d.GEMB_R_OK:
            c4d.WriteConsole("Submission cancelled by user.\n")
            raise ValidationError(msg)
    # Either there were no  messages, or the user clicked Continue (OK)


def _run_validators(dialog):
    # Eventually we will handle takes here
    takename = "Main"
    validators = [plugin(dialog) for plugin in Validator.plugins()]
    for validator in validators:
        validator.run(takename)

    errors = list(set.union(*[validator.errors for validator in validators]))
    warnings = list(
        set.union(*[validator.warnings for validator in validators]))
    notices = list(set.union(*[validator.notices for validator in validators]))
    return errors, warnings, notices
