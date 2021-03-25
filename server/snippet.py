from dbmodels import Workspace


def add_training_progress(workspace_id, dict_):
    Workspace.objects(workspace_id=workspace_id).update_one(state=dict_).save()
