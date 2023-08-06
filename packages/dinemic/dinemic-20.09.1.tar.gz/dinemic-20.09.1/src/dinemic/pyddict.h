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

#ifndef PYDDICT_H
#define PYDDICT_H

#include <string>
#include <boost/python.hpp>
#include <libdinemic/dmodel.h>

class PyDModel;

struct PyDDict
{
    bool encrypted;
    std::string name;
    std::string _caller_id;
    std::string _object_id;

    PyDDict(const std::string &dict_name, const bool &is_encrypted);
    PyDDict(const PyDDict &f);

    /// Get value of object_id property set by constructor of PyDModel. This is
    /// way how PyDinemic passes obejct ID to DField/DList/DDict etc. from main
    /// model. When model is initialized, map_fields sets object_id property
    /// on each field to have access to encryption keys via DModel C++ class.
    std::string get_my_id();
    std::string get_caller_id();

    std::string get(std::string key, std::string default_value);
    void set(std::string key, std::string value);
    void del(std::string key);
    boost::python::list keys();

};

#endif // PYDDICT_H
