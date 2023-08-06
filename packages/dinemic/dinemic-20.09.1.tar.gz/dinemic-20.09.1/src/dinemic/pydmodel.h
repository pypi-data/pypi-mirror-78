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

#ifndef PYDMODEL_H
#define PYDMODEL_H

#include <string>
#include <boost/python.hpp>
#include <libdinemic/dmodel.h>
#include <libdinemic/store/redisdriver.h>
#include <libdinemic/sync/zeromqsync.h>

#include "module.h"

struct PyDModel
{
    PyObject *self;
    Dinemic::DModel obj;
    Dinemic::DModel *caller;

    PyDModel(PyObject *self_ptr, boost::python::list authorized_objects);
    PyDModel(PyObject *self_ptr, std::string db_id, std::string caller_id);
    PyDModel(PyObject *self_ptr, std::string db_id);
    PyDModel(PyObject *self_ptr, const PyDModel &o);
    virtual ~PyDModel();

    std::string get_id();
    std::string get_db_id();
    std::string get_model();

    void set(std::string key, std::string value);
    std::string get(std::string key, std::string default_value="");
    void del(std::string key);
    void remove();

    std::string encrypt(const std::string &value);
    std::string decrypt(const std::string &value);

    bool is_read_authorized(const std::string &object_id);
    void append_read_authorized(const std::string &object_id);
    void revoke_read_authorized(const std::string &object_id);
    bool is_update_authorized(const std::string &object_id);
    void append_update_authorized(const std::string &object_id);
    void revoke_update_authorized(const std::string &object_id);

    std::string get_public_sign_key();
    std::string get_secret_sign_key();
    std::string get_public_encryption_key();
    std::string get_secret_encryption_key();
    bool is_owned();

    /// Map all fields from derived classes to instance of this object. Crypto-
    /// graphic credentials of this object will be used to encrypt/devrypt
    /// data of the field. This method is used only internally, by PyDModel
    void map_fields();
};

#endif // PYDMODEL_H
