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

#include "module.h"

using namespace boost::python;
using namespace std;

Dinemic::Sync::SyncInterface *py_sync = NULL;
Dinemic::Store::StoreInterface *py_store = NULL;

void prepare() {
    py_store = new Dinemic::Store::RedisDriver();
    py_sync = new Dinemic::Sync::ZMQAvahi(py_store);
}

void launch() {
    if (NULL == py_store || NULL == py_sync)
        prepare();

    py_sync->start_agent();
}

void shutdown() {
    py_sync->stop_agent();
}

void cleanup() {
    if (NULL != py_store || NULL != py_sync)
        shutdown();
    if (NULL != py_sync)
        delete py_sync;
    if (NULL != py_store)
        delete py_store;
}

void dinemic_exception_to_py(Dinemic::DException const &x) {
    PyErr_SetString(PyExc_Exception, x.get_reason().c_str());
}


boost::python::list object_list(const std::string &filter) {
    boost::python::list r;

    for (std::string o : Dinemic::DModel::object_list(filter, py_store)) {
        r.append(o);
    }

    return r;
}

boost::python::list object_list_owned(const std::string &filter) {
    boost::python::list r;

    for (std::string o : Dinemic::DModel::object_list(filter, py_store)) {
        r.append(o);
    }

    return r;
}

void set_loglevel(string loglevel) {
    if (loglevel == "verbose")
        Dinemic::set_loglevel(Dinemic::loglevel_verbose);
    else if (loglevel == "debug")
        Dinemic::set_loglevel(Dinemic::loglevel_debug);
    else if (loglevel == "info")
        Dinemic::set_loglevel(Dinemic::loglevel_info);
    else if (loglevel == "error")
        Dinemic::set_loglevel(Dinemic::loglevel_error);
    else if (loglevel == "action")
        Dinemic::set_loglevel(Dinemic::loglevel_action);
    else if (loglevel == "none")
        Dinemic::set_loglevel(Dinemic::loglevel_none);
    else
        throw Dinemic::DException("Unknown loglevel");
}

namespace boost {
    namespace python {
        template <>
        struct has_back_reference<PyDModel>
          : boost::mpl::true_
        {};
//        template <>
//        struct has_back_reference<PyDFieldInstance>
//          : boost::mpl::true_
//        {};
//        template <>
//        struct has_back_reference<PyDList>
//          : boost::mpl::true_
//        {};
//        template <>
//        struct has_back_reference<PyDDict>
//          : boost::mpl::true_
//        {};
        template <>
        struct has_back_reference<PyAction>
          : boost::mpl::true_
        {};
    }
}

BOOST_PYTHON_MODULE(dinemic) {

    def("prepare", &prepare);
    def("launch", &launch);
    def("shutdown", &launch);
    def("cleanup", &cleanup);
    def("set_loglevel", &set_loglevel);
    def("object_list", &object_list);
    def("object_list_owned", &object_list_owned);

    register_exception_translator<Dinemic::DException>(dinemic_exception_to_py);

    class_ <PyDModel>("DModel", init<boost::python::list>(args("authorized_object_ids"), "Create new object in Dinemic database with authorized objects"))
            .def(init<string, string>(args("db_id", "caller_id"), "Recreate existing in Dinemic database object, from given full dabtabase id"))
            .def("get_id", &PyDModel::get_id)
            .def("get_db_id", &PyDModel::get_db_id)
            .def("get_model", &PyDModel::get_model)
            .def("is_read_authorized", &PyDModel::is_read_authorized)
            .def("append_read_authorized", &PyDModel::append_read_authorized)
            .def("revoke_read_authorized", &PyDModel::revoke_read_authorized)
            .def("is_update_authorized", &PyDModel::is_update_authorized)
            .def("append_update_authorized", &PyDModel::append_update_authorized)
            .def("revoke_update_authorized", &PyDModel::revoke_update_authorized)
            .def("set", &PyDModel::set)
            .def("get", &PyDModel::get)
            .def("delete", &PyDModel::del)
            .def("remove", &PyDModel::remove)
            .def("encrypt", &PyDModel::encrypt)
            .def("decrypt", &PyDModel::decrypt)
            .def("get_secret_encryption_key", &PyDModel::get_secret_encryption_key)
            .def("get_public_encryption_key", &PyDModel::get_public_encryption_key)
            .def("get_secret_sign_key", &PyDModel::get_secret_sign_key)
            .def("get_public_sign_key", &PyDModel::get_public_sign_key)
            .def("is_owned", &PyDModel::is_owned);
    class_<PyAction>("DAction", init<>("Inherit this class to create listener on certain changes being created in database. Use apply and revoke methods to set when listener should be called. For details check dinemic framework documentation.\n\n"
                     "Supported callbacks in DAction object is going to be created:\n"
                     " - on_create(object_id, key)\n"
                     "After object was created:\n"
                     " - on_created(object_id, key)\n"
                     " - on_owned_created(object_id, key)\n\n"
                     "Before field of object will be changed in local database:\n"
                     " - on_update(object_id, field, old_value, new_value)\n"
                     " - on_authorized_update(object_id, field, old_value, new_value)\n"
                     " - on_unauthorized_update(object_id, field, old_value, new_value)\n"
                     " - on_owned_update(object_id, field, old_value, new_value)\n\n"
                     "After field of object will be changed in local database:\n"
                     " - on_updated(object_id, field, old_value, new_value)\n"
                     " - on_authorized_updated(object_id, field, old_value, new_value)\n"
                     " - on_unauthorized_updated(object_id, field, old_value, new_value)\n"
                     " - on_owned_updated(object_id, field, old_value, new_value)\n\n"
                     "Before field will be removed:\n"
                     " - on_delete(object_id, field, value)\n"
                     " - on_authorized_delete(object_id, field, value)\n"
                     " - on_unauthorized_delete(object_id, field, value)\n"
                     " - on_owned_delete(object_id, field, value)\n\n"
                     "After field was removed from database:\n"
                     " - on_deleted(object_id, field, value)\n"
                     " - on_authorized_deleted(object_id, field, value)\n"
                     " - on_unauthorized_deleted(object_id, field, value)\n"
                     " - on_owned_deleted(object_id, field, value)\n\n"
                     "Before whole object is removed from local database:\n"
                     " - on_remove(object_id)\n"
                     " - on_authorized_remove(object_id)\n"
                     " - on_unauthorized_remove(object_id)\n"
                     " - on_owned_remove(object_id)\n\n"
                     "Changes signed by one of authorized keys will call *_authorized_* callbacks.\n"
                     "\n"
                     "Changes requested on locally owned objects (created on this machine, whichs private keys are available) will call *_owned_* callbacks."))
          .def("apply", &PyAction::py_apply)
          .def("revoke", &PyAction::py_revoke);
    class_<PyDField>("DField", init<string, bool>(args("field_name", "is_encrypted")))
          .def("set", &PyDField::set)
          .def("get", &PyDField::get)
          .def_readonly("field_name", &PyDField::name)
          .def_readonly("is_encrypted", &PyDField::encrypted)
          .def_readwrite("_caller_id", &PyDField::_caller_id)
          .def_readwrite("_object_id", &PyDField::_object_id);
    class_<PyDList>("DList", init<string, bool>(args("list_name", "is_encrypted")))
          .def("append", &PyDList::append)
          .def("at", &PyDList::at)
          .def("delete", &PyDList::del)
          .def("index", &PyDList::index)
          .def("insert", &PyDList::insert)
          .def("length", &PyDList::length)
          .def("set", &PyDList::set)
          .def_readonly("field_name", &PyDList::name)
          .def_readonly("is_encrypted", &PyDList::encrypted)
          .def_readwrite("_caller_id", &PyDList::_caller_id)
          .def_readwrite("_object_id", &PyDList::_object_id);
    class_<PyDDict>("DDict", init<string, bool>(args("dict_name", "is_encrypted")))
          .def("get", &PyDDict::get)
          .def("set", &PyDDict::set)
          .def("del", &PyDDict::del)
          .def("keys", &PyDDict::keys)
          .def_readonly("field_name", &PyDDict::name)
          .def_readonly("is_encrypted", &PyDDict::encrypted)
          .def_readwrite("_caller_id", &PyDDict::_caller_id)
          .def_readwrite("_object_id", &PyDDict::_object_id);
}
