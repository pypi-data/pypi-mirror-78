
import c4d
import os
import json
from contextlib import contextmanager
from ciocore import conductor_submit
from ciocore import CONFIG
import urlparse
import traceback
from ciocore.expander import Expander
from cioc4d import asset_cache
from ciocore.validator import Validator, ValidationError
from cioc4d import validation
 
SAVE_AS_DIALOG = 12218


@contextmanager
def transient_save(filepath, cleanup=True):
    doc = c4d.documents.GetActiveDocument()
    originalname = doc.GetDocumentName()
    originalpath = doc.GetDocumentPath()

    newname = os.path.basename(filepath)
    newpath = os.path.dirname(filepath)

    doc.SetDocumentName(newname)
    doc.SetDocumentPath(newpath)
    
    c4d.documents.SaveDocument(
        doc,
        filepath,
        saveflags=c4d.SAVEDOCUMENTFLAGS_AUTOSAVE,
        format=c4d.FORMAT_C4DEXPORT)
    doc.SetDocumentName(newname)
    doc.SetDocumentPath(newpath)

    yield
    doc.SetDocumentName(originalname)
    doc.SetDocumentPath(originalpath)
    
    if cleanup:
        try:
            os.remove(filepath)
        except OSError:
            c4d.WriteConsole("Couldn't cleanup file: {}".format(filepath))

def valid(dialog):
    try:
        validation.run(dialog)
    except ValidationError as ex:
        c4d.WriteConsole(str(ex))
        return False
    return True



def submit(dialog):
    asset_cache.clear()

    filepath, cleanup = _resolve_autosave_template(dialog)
    if filepath:
        with transient_save(filepath, cleanup=cleanup):
            # if valid(dialog):
            handle_submissions(dialog)
        return

    if needs_save():
        c4d.CallCommand(SAVE_AS_DIALOG)
    if needs_save():
        return
    # if valid(dialog):
    handle_submissions(dialog)


def needs_save():
    doc = c4d.documents.GetActiveDocument()
    return doc.GetChanged() or '' == doc.GetDocumentPath()


def _resolve_autosave_template(dialog):
    context = dialog.get_context()
    autosave_widget = dialog.section("AutosaveSection").widget
    do_autosave = autosave_widget.get_visible()
    template = autosave_widget.get_value()
    cleanup = autosave_widget.get_extra_check_value() and not dialog.section(
        "UploadOptionsSection").use_daemon_widget.get_value()

    if not context.get("docdir") and do_autosave:
        return (None, None)

    resolved_name = Expander(safe=True, **context).evaluate(template)

    return (resolved_name, cleanup)


def handle_submissions(dialog):
    submission = dialog.calculate_submission(max_tasks=-1, with_assets=True)
    if valid(dialog):
        response = do_submission(dialog, submission)
        show_submission_response(response)


def do_submission(dialog, submission):
 
    show_tracebacks = dialog.section("DiagnosticsSection").widget.get_value()
 
    try:
        remote_job = conductor_submit.Submit(submission)
        response, response_code = remote_job.main()
        return {"code": response_code, "response": response}
    except BaseException as ex:
        if show_tracebacks:
            msg = traceback.format_exc()
        else:
            msg = ex.message
        c4d.WriteConsole(msg)
        return{"code": "undefined", "response": msg}


def show_submission_response(response):
    if response.get("code") <= 201:
        # success
        success_uri = response["response"]["uri"].replace("jobs", "job")
        job_url = urlparse.urljoin(CONFIG["auth_url"], success_uri)

        c4d.WriteConsole("Use this URL to monitor your Conductor job {}".format(job_url))
        c4d.gui.MessageDialog( "Success: {}".format(job_url))
        return

    c4d.gui.MessageDialog( "Failure: {}".format(str(response["response"])))
