#ifndef _OBJECT_FLEXVNETZ_SETTINGS_H_
#define _OBJECT_FLEXVNETZ_SETTINGS_H_

#include <Python.h>
#include <structmember.h>
#if (defined(_WIN32) || defined(__WIN32__))
    #ifndef USING_STUDIO_8
          #define USING_STUDIO_8 1
    #endif
    #include <icsnVC40.h>
#else
    #include <icsnVC40.h>
#endif

#include "defines.h"
#include "object_can_settings.h"
#include "object_lin_settings.h"
#include "object_swcan_settings.h"
#include "object_textapi_settings.h"
#include "object_uart_settings.h"
#include "object_iso9141_keyword2000_settings.h"
#include "object_canfd_settings.h"
#include "object_op_eth_general_settings.h"
#include "object_op_eth_settings.h"
#include "object_timesync_settings.h"

#define FLEXVNETZ_SETTINGS_OBJECT_NAME "FlexVnetzSettings"

typedef struct {
    PyObject_HEAD

    PyObject* can1;
    PyObject* can2;
    PyObject* can3;
    PyObject* can4;
    PyObject* can5;
    PyObject* can6;
    PyObject* can7;
    PyObject* canfd1;
    PyObject* canfd2;
    PyObject* canfd3;
    PyObject* canfd4;
    PyObject* canfd5;
    PyObject* canfd6;
    PyObject* canfd7;
    
    PyObject* ethernet;
    
    PyObject* timesync;
    PyObject* textapi;

    SFlexVnetzSettings s;
} flex_vnetz_settings_object;

static PyMemberDef flex_vnetz_settings_object_members[] = {
    { "perf_en", T_USHORT, offsetof(flex_vnetz_settings_object, s.perf_en), 0, "" },
    { "network_enabled_on_boot", T_USHORT, offsetof(flex_vnetz_settings_object, s.network_enabled_on_boot), 0, "" },
    { "misc_io_on_report_events", T_USHORT, offsetof(flex_vnetz_settings_object, s.misc_io_on_report_events), 0, "" },
    { "pwr_man_enable", T_USHORT, offsetof(flex_vnetz_settings_object, s.pwr_man_enable), 0, "" },
    { "iso15765_separation_time_offset", T_SHORT, offsetof(flex_vnetz_settings_object, s.iso15765_separation_time_offset), 0, "" },
    { "flex_mode", T_USHORT, offsetof(flex_vnetz_settings_object, s.flex_mode), 0, "" },
    { "flex_termination", T_USHORT, offsetof(flex_vnetz_settings_object, s.flex_termination), 0, "" },
    { "slaveVnetA", T_USHORT, offsetof(flex_vnetz_settings_object, s.slaveVnetA), 0, "" },
    { "termination_enables", T_USHORT, offsetof(flex_vnetz_settings_object, s.termination_enables), 0, "" },
    
    { "network_enables", T_USHORT, offsetof(flex_vnetz_settings_object, s.network_enables.network_enables), 0, "" },
    { "network_enables_2", T_USHORT, offsetof(flex_vnetz_settings_object, s.network_enables.network_enables_2), 0, "" },
    { "network_enables_3", T_USHORT, offsetof(flex_vnetz_settings_object, s.network_enables.network_enables_3), 0, "" },
    
    { "pwr_man_timeout", T_UINT, offsetof(flex_vnetz_settings_object, s.pwr_man_timeout), 0, "" },
    { "slaveVnetB", T_USHORT, offsetof(flex_vnetz_settings_object, s.slaveVnetB), 0, "" },
    
    { "can1", T_OBJECT_EX, offsetof(flex_vnetz_settings_object, can1), 0, MODULE_NAME "." CAN_SETTINGS_OBJECT_NAME" Object" },
    { "can2", T_OBJECT_EX, offsetof(flex_vnetz_settings_object, can2), 0, MODULE_NAME "." CAN_SETTINGS_OBJECT_NAME" Object" },
    { "can3", T_OBJECT_EX, offsetof(flex_vnetz_settings_object, can3), 0, MODULE_NAME "." CAN_SETTINGS_OBJECT_NAME" Object" },
    { "can4", T_OBJECT_EX, offsetof(flex_vnetz_settings_object, can4), 0, MODULE_NAME "." CAN_SETTINGS_OBJECT_NAME" Object" },
    { "can5", T_OBJECT_EX, offsetof(flex_vnetz_settings_object, can5), 0, MODULE_NAME "." CAN_SETTINGS_OBJECT_NAME" Object" },
    { "can6", T_OBJECT_EX, offsetof(flex_vnetz_settings_object, can6), 0, MODULE_NAME "." CAN_SETTINGS_OBJECT_NAME" Object" },
    { "can7", T_OBJECT_EX, offsetof(flex_vnetz_settings_object, can7), 0, MODULE_NAME "." CAN_SETTINGS_OBJECT_NAME" Object" },

    { "canfd1", T_OBJECT_EX, offsetof(flex_vnetz_settings_object, canfd1), 0, MODULE_NAME "." CANFD_SETTINGS_OBJECT_NAME" Object" },
    { "canfd2", T_OBJECT_EX, offsetof(flex_vnetz_settings_object, canfd2), 0, MODULE_NAME "." CANFD_SETTINGS_OBJECT_NAME" Object" },
    { "canfd3", T_OBJECT_EX, offsetof(flex_vnetz_settings_object, canfd3), 0, MODULE_NAME "." CANFD_SETTINGS_OBJECT_NAME" Object" },
    { "canfd4", T_OBJECT_EX, offsetof(flex_vnetz_settings_object, canfd4), 0, MODULE_NAME "." CANFD_SETTINGS_OBJECT_NAME" Object" },
    { "canfd5", T_OBJECT_EX, offsetof(flex_vnetz_settings_object, canfd5), 0, MODULE_NAME "." CANFD_SETTINGS_OBJECT_NAME" Object" },
    { "canfd6", T_OBJECT_EX, offsetof(flex_vnetz_settings_object, canfd6), 0, MODULE_NAME "." CANFD_SETTINGS_OBJECT_NAME" Object" },
    { "canfd7", T_OBJECT_EX, offsetof(flex_vnetz_settings_object, canfd7), 0, MODULE_NAME "." CANFD_SETTINGS_OBJECT_NAME" Object" },

    { "misc_io_initial_ddr", T_USHORT, offsetof(flex_vnetz_settings_object, s.misc_io_initial_ddr), 0, "" },
    { "misc_io_initial_latch", T_USHORT, offsetof(flex_vnetz_settings_object, s.misc_io_initial_latch), 0, "" },
    { "misc_io_report_period", T_USHORT, offsetof(flex_vnetz_settings_object, s.misc_io_report_period), 0, "" },
    
    { "misc_io_analog_enable", T_USHORT, offsetof(flex_vnetz_settings_object, s.misc_io_analog_enable), 0, "" },
    { "ain_sample_period", T_USHORT, offsetof(flex_vnetz_settings_object, s.ain_sample_period), 0, "" },
    { "ain_threshold", T_USHORT, offsetof(flex_vnetz_settings_object, s.ain_threshold), 0, "" },
    
    { "disableUsbCheckOnBoot", T_UINT, 0, 0, "" },
    { "enableLatencyTest", T_UINT, 0, 0, "" },
    { "busMessagesToAndroid", T_UINT, 0, 0, "" },
    { "enablePcEthernetComm", T_UINT, 0, 0, "" },
    { "reserved", T_UINT, 0, 0, "" },
    
    { NULL, 0, 0, 0, 0 },
};

static int flex_vnetz_settings_object_init(flex_vnetz_settings_object* self, PyObject* args, PyObject* kwds)
{
    // Initialize all struct values to 0
    memset(&(self->s), 0, sizeof(self->s));
    // Initialize Ethernet Objects
    self->opEthGen = PyObject_CallObject((PyObject*)&op_eth_general_settings_object_type, NULL);
    self->opEth1 = PyObject_CallObject((PyObject*)&op_eth_settings_object_type, NULL);
    self->opEth2 = PyObject_CallObject((PyObject*)&op_eth_settings_object_type, NULL);
    // Initialize Can Objects
    self->can1 = PyObject_CallObject((PyObject*)&can_settings_object_type, NULL);
    self->can2 = PyObject_CallObject((PyObject*)&can_settings_object_type, NULL);
    self->can3 = PyObject_CallObject((PyObject*)&can_settings_object_type, NULL);
    self->can4 = PyObject_CallObject((PyObject*)&can_settings_object_type, NULL);
    self->can5 = PyObject_CallObject((PyObject*)&can_settings_object_type, NULL);
    self->can6 = PyObject_CallObject((PyObject*)&can_settings_object_type, NULL);
    self->can7 = PyObject_CallObject((PyObject*)&can_settings_object_type, NULL);
    self->canfd1 = PyObject_CallObject((PyObject*)&canfd_settings_object_type, NULL);
    self->canfd2 = PyObject_CallObject((PyObject*)&canfd_settings_object_type, NULL);
    self->canfd3 = PyObject_CallObject((PyObject*)&canfd_settings_object_type, NULL);
    self->canfd4 = PyObject_CallObject((PyObject*)&canfd_settings_object_type, NULL);
    self->canfd5 = PyObject_CallObject((PyObject*)&canfd_settings_object_type, NULL);
    self->canfd6 = PyObject_CallObject((PyObject*)&canfd_settings_object_type, NULL);
    self->canfd7 = PyObject_CallObject((PyObject*)&canfd_settings_object_type, NULL);
    // Initialize TextAPI Objects
    self->textapi = PyObject_CallObject((PyObject*)&textapi_settings_object_type, NULL);
    // Initialize TIMESYNC Objects
    self->timesync = PyObject_CallObject((PyObject*)&timesync_settings_object_type, NULL);
    // Initialize ETHERNET_SETTINGS Objects
    self->ethernet = PyObject_CallObject((PyObject*)&ethernet_settings_object_type, NULL);
    return 0;
}

extern PyTypeObject flex_vnetz_settings_object_type;

// Copied from tupleobject.h
#define PyRADStar2Settings_Check(op) \
                 PyType_FastSubclass(Py_TYPE(op), Py_TPFLAGS_BASETYPE)
#define PyRADStar2Settings_CheckExact(op) (Py_TYPE(op) == &flex_vnetz_settings_object_type)

bool setup_flex_vnetz_settings_object(PyObject* module);

void flex_vnetz_settings_object_update_from_struct(PyObject* settings);
void flex_vnetz_settings_object_update_from_objects(PyObject* settings);

#endif // _OBJECT_FLEXVNETZ_SETTINGS_H_
