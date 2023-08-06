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

#include "pydfield.h"
#include "pydmodel.h"

#define PREPARE_MODELS Dinemic::DModel model(get_my_id(), py_store, py_sync, NULL, NULL);   \
    Dinemic::DModel *caller = NULL;                                                         \
    if (get_caller_id() != "") {                                                            \
        caller = new Dinemic::DModel(get_caller_id(), py_store, py_sync, NULL, NULL);       \
        model.set_caller(caller);                                                           \
    }

#define CLEANUP_MODELS if (caller != NULL) delete caller;

using namespace std;

PyDField::PyDField(const string &field_name, const bool &is_encrypted)
    : name(field_name),
      encrypted(is_encrypted)
{
}

PyDField::PyDField(const PyDField &f)
    : name(f.name),
      encrypted(f.encrypted)
{
}

string PyDField::get_caller_id() {
    return _caller_id;
}

string PyDField::get_my_id() {
    // Get object_id property of this field. Should be set by map_fields of
    // PyDModel class, which is called by each constructor
    if (_object_id.length() == 0)
        throw Dinemic::DException(string("Object_id is not set for this field ") + name);

    return _object_id;
}

void PyDField::set(const string &value) {
    PREPARE_MODELS
    if (encrypted) {
        model.set(name, model.encrypt(value));
    } else {
        model.set(name, value);
    }
    CLEANUP_MODELS
}

std::string PyDField::get() {
    PREPARE_MODELS
    string result;
    if (encrypted) {
        try {
            result = model.decrypt(model.get(name));
        } catch (Dinemic::DEncryptFailed &e) {
            result = "[encrypted]";
        }
    } else {
        result = model.get(name);
    }
    CLEANUP_MODELS
    return result;
}
