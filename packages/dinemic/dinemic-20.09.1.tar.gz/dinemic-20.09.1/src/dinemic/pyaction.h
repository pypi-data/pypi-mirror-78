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

#ifndef PYACTION_H
#define PYACTION_H

#include <boost/python.hpp>
#include <libdinemic/daction.h>

class PyAction : public Dinemic::DAction
{
    PyObject *self;
    PyGILState_STATE gstate;
    void call_listener(const std::string &name, PyObject *args);

public:
    PyAction(PyObject *self_ptr);
    PyAction(PyObject *self_ptr, const PyAction &f);
    ~PyAction();

    void py_apply(const std::string &filter);
    void py_revoke(const std::string &filter);

    // Create
    void on_create(Dinemic::DActionContext &context, const std::string &key);
    void on_created(Dinemic::DActionContext &context, const std::string &key);
    void on_owned_created(Dinemic::DActionContext &context, const std::string &key);

    // Update
    void on_update(Dinemic::DActionContext &context, const std::string &key, const std::string &old_value, const std::string &new_value);
    void on_authorized_update(Dinemic::DActionContext &context, const std::string &key, const std::string &old_value, const std::string &new_value);
    void on_unauthorized_update(Dinemic::DActionContext &context, const std::string &key, const std::string &old_value, const std::string &new_value);
    void on_owned_update(Dinemic::DActionContext &context, const std::string &key, const std::string &old_value, const std::string &new_value);

    // Updated
    void on_updated(Dinemic::DActionContext &context, const std::string &key, const std::string &old_value, const std::string &new_value);
    void on_authorized_updated(Dinemic::DActionContext &context, const std::string &key, const std::string &old_value, const std::string &new_value);
    void on_unauthorized_updated(Dinemic::DActionContext &context, const std::string &key, const std::string &old_value, const std::string &new_value);
    void on_owned_updated(Dinemic::DActionContext &context, const std::string &key, const std::string &old_value, const std::string &new_value);

    // Delete
    void on_delete(Dinemic::DActionContext &context, const std::string &key, const std::string &value);
    void on_authorized_delete(Dinemic::DActionContext &context, const std::string &key, const std::string &value);
    void on_unauthorized_delete(Dinemic::DActionContext &context, const std::string &key, const std::string &value);
    void on_owned_delete(Dinemic::DActionContext &context, const std::string &key, const std::string &value);

    // Deleted
    void on_deleted(Dinemic::DActionContext &context, const std::string &key, const std::string &value);
    void on_authorized_deleted(Dinemic::DActionContext &context, const std::string &key, const std::string &value);
    void on_unauthorized_deleted(Dinemic::DActionContext &context, const std::string &key, const std::string &value);
    void on_owned_deleted(Dinemic::DActionContext &context, const std::string &key, const std::string &value);

    // Remove
    void on_remove(Dinemic::DActionContext &context);
    void on_authorized_remove(Dinemic::DActionContext &context);
    void on_unauthorized_remove(Dinemic::DActionContext &context);
    void on_owned_remove(Dinemic::DActionContext &context);
};

#endif // PYACTION_H
