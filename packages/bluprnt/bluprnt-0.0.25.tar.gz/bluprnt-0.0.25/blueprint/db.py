from google.cloud import firestore

client = firestore.Client()


class Types:
    WORKSPACES = "workspaces"
    CONFIGURATIONS = "configurations"
    STATES = "states"
    PARAM_SETS = "paramSets"


def _workspace(wid):
    return client.collection(Types.WORKSPACES).document(wid)


def _configuration(wid, cid):
    return _workspace(wid).collection(Types.CONFIGURATIONS).document(cid)


def _state(wid, cid, sid):
    return _configuration(wid, cid).collection(Types.STATES).document(sid)


def _param_set(wid, cid, sid, pid):
    return _state(wid, cid, sid).collection(Types.PARAM_SETS).document(pid)


def generate_id():
    return client.collection("").document().id


def add_workspace(wid, name):
    ref = _workspace(wid)
    ref.set({"name": name})
    return ref.id


def add_configuration(wid, name, cid):
    ref = _configuration(wid, cid)
    ref.set({"name": name})
    return ref.id


def add_state(wid, cid, sid, name):
    ref = _state(wid, cid, sid)
    ref.set({"name": name})
    return ref.id


def add_param_set(wid, cid, sid, pid, name):
    ref = _param_set(wid, cid, sid, pid)
    ref.set({"name": name})
    return ref.id


def get_workspace_by_name(name):
    query = client.collection(Types.WORKSPACES).where("name", "==", name).limit(1)
    result = next(query.stream(), None)
    return result.to_dict() if result else None


def get_configuration_by_name(wid, name):
    query = (
        _workspace(wid)
        .collection(Types.CONFIGURATIONS)
        .where("name", "==", name)
        .limit(1)
    )
    result = next(query.stream(), None)
    return result.to_dict() if result else None


def get_state_by_name(wid, cid, name):
    query = (
        _configuration(wid, cid)
        .collection(Types.STATES)
        .where("name", "==", name)
        .limit(1)
    )
    result = next(query.stream(), None)
    return result.to_dict() if result else None


def get_param_set_by_name(wid, cid, sid, name):
    query = (
        _state(wid, cid, sid)
        .collection(Types.PARAM_SETS)
        .where("name", "==", name)
        .limit(1)
    )
    result = next(query.stream(), None)
    return result.to_dict() if result else None
