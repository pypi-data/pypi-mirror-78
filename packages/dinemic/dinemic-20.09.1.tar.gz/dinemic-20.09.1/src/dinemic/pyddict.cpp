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

#include "pyddict.h"
#include "pydmodel.h"

#define PREPARE_MODELS Dinemic::DModel model(get_my_id(), py_store, py_sync, NULL, NULL);   \
    Dinemic::DModel *caller = NULL;                                                         \
    if (get_caller_id() != "") {                                                            \
        caller = new Dinemic::DModel(get_caller_id(), py_store, py_sync, NULL, NULL);       \
        model.set_caller(caller);                                                           \
    }

#define CLEANUP_MODELS if (caller != NULL) delete caller;

using namespace std;

PyDDict::PyDDict(const string &dict_name, const bool &is_encrypted)
    : name(dict_name),
      encrypted(is_encrypted)
{
}

PyDDict::PyDDict(const PyDDict &f)
    : name(f.name),
      encrypted(f.encrypted)
{
}

string PyDDict::get_caller_id() {
    return _caller_id;
}

string PyDDict::get_my_id() {
    // Get object_id property of this field. Should be set by map_fields of
    // PyDModel class, which is called by each constructor
    if (_object_id.length() == 0)
        throw Dinemic::DException(string("Object_id is not set for this field ") + name);

    return _object_id;
}

void PyDDict::set(string key, string value) {
    PREPARE_MODELS
    if (encrypted) {
        model.dict_set(name, key, model.encrypt(value));
    } else {
        model.dict_set(name, key, value);
    }
    CLEANUP_MODELS
}

void PyDDict::del(string key) {
    PREPARE_MODELS
    model.dict_del(name, key);
    CLEANUP_MODELS
}

string PyDDict::get(string key, string default_value) {
    PREPARE_MODELS
    string result;

    if (encrypted) {
        try {
            result = model.decrypt(model.dict_get(name, key, model.encrypt(default_value)));
        } catch (Dinemic::DEncryptFailed &e) {
            result = "[encrypted]";
        }
    } else {
        result = model.dict_get(name, key, default_value);
    }

    CLEANUP_MODELS
    return result;
}

boost::python::list PyDDict::keys() {
    PREPARE_MODELS
    vector<string> result_vector = model.dict_keys(name);

    //boost::python::object get_iter = boost::python::iterator<vector<string> >();
    //boost::python::object iter = get_iter(result_vector);
    boost::python::list result;

    for (auto item : result_vector) {
        result.append(item);
    }

    CLEANUP_MODELS
    return result;
}
