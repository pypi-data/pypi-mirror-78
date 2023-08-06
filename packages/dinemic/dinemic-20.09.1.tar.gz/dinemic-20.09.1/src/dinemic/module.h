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

#ifndef MODULE_H
#define MODULE_H

#include <libdinemic/dmodel.h>
#include <libdinemic/store/redisdriver.h>
#include <libdinemic/sync/zeromqsync.h>
#include <libdinemic/sync/zmqavahi.h>

#include "pydmodel.h"
#include "pyaction.h"
#include "pydfield.h"
#include "pydlist.h"
#include "pyddict.h"

class PyDModel;
class PyAction;

extern Dinemic::Sync::SyncInterface *py_sync;
extern Dinemic::Store::StoreInterface *py_store;

void launch();
void shutdown();
void set_loglevel(std::string loglevel);
void dinemic_exception_to_py(Dinemic::DException const &x);

#endif // MODULE_H
