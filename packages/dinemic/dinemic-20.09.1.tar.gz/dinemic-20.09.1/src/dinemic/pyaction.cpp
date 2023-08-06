/**
Copyright (c) 2016-2019 cloudover.io ltd.

Licensee holding a valid commercial license for dinemic library may use it with
accordance to terms of the license agreement between cloudover.io ltd. and the
licensee, or on GNU Affero GPL v3 license terms.

Licensee not holding a valid commercial license for dinemic library may use it
under GNU Affero GPL v3 license.

Terms of GNU Affero GPL v3 license are available on following site:
https://www.gnu.org/licenses/agpl-3.0.en.html
*/

#include "pyaction.h"
#include "module.h"

#define INIT_ACTION gstate = PyGILState_Ensure();

#define FINALIZE_ACTION  Py_DECREF(args); \
                         PyGILState_Release(gstate);

using namespace std;

PyAction::PyAction(PyObject *self_ptr)
    : self(self_ptr)
{
    if (py_sync == NULL || py_store == NULL) {
        throw Dinemic::DException("Dinemic is not initialized. Call dinemic.launch or dinemic.prepare first");
    }
}

PyAction::PyAction(PyObject *self_ptr, const PyAction &f)
    : self(self_ptr)
{
}

PyAction::~PyAction()
{
}

void PyAction::py_apply(const string &filter) {
    Py_XINCREF(self);
    py_sync->add_on_create_listener(filter, this);
    py_sync->add_on_created_listener(filter, this);
    py_sync->add_on_update_listener(filter, this);
    py_sync->add_on_updated_listener(filter, this);
    py_sync->add_on_delete_listener(filter, this);
    py_sync->add_on_deleted_listener(filter, this);
    py_sync->add_on_remove_listener(filter, this);
}

void PyAction::py_revoke(const string &filter) {
    py_sync->remove_on_create_listener(filter, this);
    py_sync->remove_on_created_listener(filter, this);
    py_sync->remove_on_update_listener(filter, this);
    py_sync->remove_on_updated_listener(filter, this);
    py_sync->remove_on_delete_listener(filter, this);
    py_sync->remove_on_deleted_listener(filter, this);
    py_sync->remove_on_remove_listener(filter, this);
    Py_XDECREF(self);
}

void PyAction::call_listener(const string &name, PyObject *args) {
    if (PyObject_HasAttrString(self, name.c_str())) {
        PyObject *method = PyObject_GetAttrString(self, name.c_str());
        PyObject *keywords = PyDict_New();
        if (keywords == NULL) {
            return;
        }
        if (args == NULL) {
            Py_DECREF(keywords);
            return;
        }
        if (method == NULL) {
            Py_DECREF(keywords);
            return;
        }

        PyObject *result = PyObject_Call(method, args, keywords);

        Py_DECREF(keywords);
        Py_XDECREF(method);
        Py_XDECREF(result);

        if (PyErr_Occurred()) {
            PyObject *exception, *v, *tb;
            PyErr_Fetch(&exception, &v, &tb);
            PyObject *pystr = PyObject_Str(v);
            Py_XDECREF(pystr);
            Py_XDECREF(exception);
            Py_XDECREF(v);
            Py_XDECREF(tb);

            Py_DECREF(args);
            PyGILState_Release(gstate);

            throw Dinemic::DUpdateRejected(string("Python threw an exception: ") + PyUnicode_AsUTF8(pystr));
        }
    }
}

void PyAction::on_create(Dinemic::DActionContext &context, const std::string &key) {
    INIT_ACTION
    PyObject *args = Py_BuildValue("ss", context.get_object_id().c_str(), key.c_str());
    call_listener("on_create", args);
    FINALIZE_ACTION
}

void PyAction::on_created(Dinemic::DActionContext &context, const std::string &key) {
    INIT_ACTION
    PyObject *args = Py_BuildValue("ss", context.get_object_id().c_str(), key.c_str());
    call_listener("on_created", args);
    FINALIZE_ACTION
}

void PyAction::on_owned_created(Dinemic::DActionContext &context, const std::string &key) {
    INIT_ACTION
    PyObject *args = Py_BuildValue("ss", context.get_object_id().c_str(), key.c_str());
    call_listener("on_owned_created", args);
    FINALIZE_ACTION
}

void PyAction::on_update(Dinemic::DActionContext &context, const string &key, const string &old_value, const string &new_value) {
    INIT_ACTION
    PyObject *args = Py_BuildValue("(ss#s#s#)", context.get_object_id().c_str(), key.c_str(), key.size(), old_value.c_str(), old_value.size(), new_value.c_str(), new_value.size());
    call_listener("on_update", args);
    FINALIZE_ACTION
}

void PyAction::on_authorized_update(Dinemic::DActionContext &context, const string &key, const string &old_value, const string &new_value) {
    INIT_ACTION
    PyObject *args = Py_BuildValue("(ss#s#s#)", context.get_object_id().c_str(), key.c_str(), key.size(), old_value.c_str(), old_value.size(), new_value.c_str(), new_value.size());
    call_listener("on_authorized_update", args);
    FINALIZE_ACTION
}

void PyAction::on_unauthorized_update(Dinemic::DActionContext &context, const string &key, const string &old_value, const string &new_value) {
    INIT_ACTION
    PyObject *args = Py_BuildValue("(ss#s#s#)", context.get_object_id().c_str(), key.c_str(), key.size(), old_value.c_str(), old_value.size(), new_value.c_str(), new_value.size());
    call_listener("on_unauthorized_update", args);
    FINALIZE_ACTION
}

void PyAction::on_owned_update(Dinemic::DActionContext &context, const string &key, const string &old_value, const string &new_value) {
    INIT_ACTION
    PyObject *args = Py_BuildValue("(ss#s#s#)", context.get_object_id().c_str(), key.c_str(), key.size(), old_value.c_str(), old_value.size(), new_value.c_str(), new_value.size());
    call_listener("on_owned_update", args);
    FINALIZE_ACTION
}

void PyAction::on_updated(Dinemic::DActionContext &context, const string &key, const string &old_value, const string &new_value) {
    INIT_ACTION
    PyObject *args = Py_BuildValue("(ss#s#s#)", context.get_object_id().c_str(), key.c_str(), key.size(), old_value.c_str(), old_value.size(), new_value.c_str(), new_value.size());
    call_listener("on_updated", args);
    FINALIZE_ACTION
}

void PyAction::on_authorized_updated(Dinemic::DActionContext &context, const string &key, const string &old_value, const string &new_value) {
    INIT_ACTION
    PyObject *args = Py_BuildValue("(ss#s#s#)", context.get_object_id().c_str(), key.c_str(), key.size(), old_value.c_str(), old_value.size(), new_value.c_str(), new_value.size());
    call_listener("on_authorized_updated", args);
    FINALIZE_ACTION
}

void PyAction::on_unauthorized_updated(Dinemic::DActionContext &context, const string &key, const string &old_value, const string &new_value) {
    INIT_ACTION
    PyObject *args = Py_BuildValue("(ss#s#s#)", context.get_object_id().c_str(), key.c_str(), key.size(), old_value.c_str(), old_value.size(), new_value.c_str(), new_value.size());
    call_listener("on_unauthorized_updated", args);
    FINALIZE_ACTION
}

void PyAction::on_owned_updated(Dinemic::DActionContext &context, const string &key, const string &old_value, const string &new_value) {
    INIT_ACTION
    PyObject *args = Py_BuildValue("(ss#s#s#)", context.get_object_id().c_str(), key.c_str(), key.size(), old_value.c_str(), old_value.size(), new_value.c_str(), new_value.size());
    call_listener("on_owned_updated", args);
    FINALIZE_ACTION
}

void PyAction::on_delete(Dinemic::DActionContext &context, const string &key, const string &value) {
    INIT_ACTION
    PyObject *args = Py_BuildValue("(ss#s#)", context.get_object_id().c_str(), key.c_str(), key.size(), value.c_str(), value.size());
    call_listener("on_delete", args);
    FINALIZE_ACTION
}

void PyAction::on_authorized_delete(Dinemic::DActionContext &context, const string &key, const string &value) {
    INIT_ACTION
    PyObject *args = Py_BuildValue("(ss#s#)", context.get_object_id().c_str(), key.c_str(), key.size(), value.c_str(), value.size());
    call_listener("on_authorized_delete", args);
    FINALIZE_ACTION
}

void PyAction::on_unauthorized_delete(Dinemic::DActionContext &context, const string &key, const string &value) {
    INIT_ACTION
    PyObject *args = Py_BuildValue("(ss#s#)", context.get_object_id().c_str(), key.c_str(), key.size(), value.c_str(), value.size());
    call_listener("on_unauthorized_delete", args);
    FINALIZE_ACTION
}

void PyAction::on_owned_delete(Dinemic::DActionContext &context, const string &key, const string &value) {
    INIT_ACTION
    PyObject *args = Py_BuildValue("(ss#s#)", context.get_object_id().c_str(), key.c_str(), key.size(), value.c_str(), value.size());
    call_listener("on_owned_delete", args);
    FINALIZE_ACTION
}

void PyAction::on_deleted(Dinemic::DActionContext &context, const string &key, const string &value) {
    INIT_ACTION
    PyObject *args = Py_BuildValue("(ss#s#)", context.get_object_id().c_str(), key.c_str(), key.size(), value.c_str(), value.size());
    call_listener("on_deleted", args);
    FINALIZE_ACTION
}

void PyAction::on_authorized_deleted(Dinemic::DActionContext &context, const string &key, const string &value) {
    INIT_ACTION
    PyObject *args = Py_BuildValue("(ss#s#)", context.get_object_id().c_str(), key.c_str(), key.size(), value.c_str(), value.size());
    call_listener("on_authorized_deleted", args);
    FINALIZE_ACTION
}

void PyAction::on_unauthorized_deleted(Dinemic::DActionContext &context, const string &key, const string &value) {
    INIT_ACTION
    PyObject *args = Py_BuildValue("(ss#s#)", context.get_object_id().c_str(), key.c_str(), key.size(), value.c_str(), value.size());
    call_listener("on_unauthorized_deleted", args);
    FINALIZE_ACTION
}

void PyAction::on_owned_deleted(Dinemic::DActionContext &context, const string &key, const string &value) {
    INIT_ACTION
    PyObject *args = Py_BuildValue("(ss#s#)", context.get_object_id().c_str(), key.c_str(), key.size(), value.c_str(), value.size());
    call_listener("on_owned_deleted", args);
    FINALIZE_ACTION
}

void PyAction::on_remove(Dinemic::DActionContext &context) {
    INIT_ACTION
    PyObject *args = Py_BuildValue("s", context.get_object_id().c_str());
    call_listener("on_remove", args);
    FINALIZE_ACTION
}

void PyAction::on_authorized_remove(Dinemic::DActionContext &context) {
    INIT_ACTION
    PyObject *args = Py_BuildValue("s", context.get_object_id().c_str());
    call_listener("on_authorized_remove", args);
    FINALIZE_ACTION
}

void PyAction::on_unauthorized_remove(Dinemic::DActionContext &context) {
    INIT_ACTION
    PyObject *args = Py_BuildValue("s", context.get_object_id().c_str());
    call_listener("on_unauthorized_remove", args);
    FINALIZE_ACTION
}

void PyAction::on_owned_remove(Dinemic::DActionContext &context) {
    INIT_ACTION
    PyObject *args = Py_BuildValue("s", context.get_object_id().c_str());
    call_listener("on_owned_remove", args);
    FINALIZE_ACTION
}
