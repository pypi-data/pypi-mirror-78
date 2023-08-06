/**
Copyright (c) 2016-2019 cloudover.io ltd.

Licensee holding a valid commercial license for dinemic library may use it with
accordance to terms of the license agreement between cloudover.io ltd. and the
licensee, or on GNU Affero GPL v3 license terms.

Licensee not holding a valid commercial license for dinemic library may use it
under GNU Affero GPL v3 license.

Terms of GNU Affero GPL v3 license are available on following site:
https://www.gnu.PyDFieldorg/licenses/agpl-3.0.en.html
*/

#ifndef PYDLIST_H
#define PYDLIST_H

#include <string>
#include <boost/python.hpp>
#include <libdinemic/dmodel.h>

class PyDModel;

struct PyDList
{
    bool encrypted;
    std::string name;
    std::string _caller_id;
    std::string _object_id;

    PyDList(const std::string &list_name, const bool &is_encrypted);
    PyDList(const PyDList &f);

    /// Get value of object_id property set by constructor of PyDModel. This is
    /// way how PyDinemic passes obejct ID to DField/DList/DDict etc. from main
    /// model. When model is initialized, map_fields sets object_id property
    /// on each field to have access to encryption keys via DModel C++ class.
    std::string get_my_id();
    std::string get_caller_id();

    void append(const std::string &value);
    void insert(long position, std::string value);
    void set(long position, std::string value);
    void del(long position);
    long length();
    long index(std::string value);
    std::string at(long index);

};

#endif // PYDLIST_H
