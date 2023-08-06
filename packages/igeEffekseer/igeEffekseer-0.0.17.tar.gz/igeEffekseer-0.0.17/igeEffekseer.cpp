#include "igeEffekseer.h"
#include "igeEffekseer_doc_en.h"
#include "pyVectorMath.h"
#include <string>

static PyObject* onTextureLoaderCallBack = nullptr;
static std::map<std::string, TextureData*> textureData_map;

float* pyObjToFloat(PyObject* obj, float* f, int& d) {
	/*if (f) {
		for (int i = 0; i < d; i++) {
			f[i] = 0.0f;
		}
	}*/

	if (obj)
	{
		if (PyTuple_Check(obj)) {
			d = (int)PyTuple_Size(obj);
			if (d > 3) d = 3;
			for (int j = 0; j < d; j++) {
				PyObject* val = PyTuple_GET_ITEM(obj, j);
				f[j] = (float)PyFloat_AsDouble(val);
			}
		}
		else if (PyList_Check(obj)) {
			d = (int)PyList_Size(obj);
			if (d > 3) d = 3;
			for (int j = 0; j < d; j++) {
				PyObject* val = PyList_GET_ITEM(obj, j);
				f[j] = (float)PyFloat_AsDouble(val);
			}
		}
	}
	return f;
}

TextureData* effekseer_TextureLoader(TextureLoaderCallback loader)
{
	std::string name = loader.name;
	auto it = textureData_map.find(name);
	if (it != textureData_map.end())
	{
		return it->second;
	}

	PyObject* arglist;
	arglist = Py_BuildValue("(si)", loader.name, loader.type);
	PyObject* result = PyEval_CallObject(onTextureLoaderCallBack, arglist);

	TextureData* textureData = new TextureData();;
	if (result)
	{
		if (PyTuple_Check(result)) {
			int numAttr = (int)PyTuple_Size(result);
			if (numAttr != 4) {
				PyErr_SetString(PyExc_TypeError, "4 Parameters : width(int) | height(int) | texture_id(int) | has_mipmap(bool)");
				return NULL;
			}

			textureData->Width = PyLong_AsLong(PyTuple_GET_ITEM(result, 0));
			textureData->Height = PyLong_AsLong(PyTuple_GET_ITEM(result, 1));
			textureData->UserID = PyLong_AsLong(PyTuple_GET_ITEM(result, 2));
			textureData->HasMipmap = PyLong_AsLong(PyTuple_GET_ITEM(result, 3));

			textureData_map[name] = textureData;
		}
	}

	Py_DECREF(arglist);
	Py_XDECREF(result);

	return textureData;
}

PyObject* effekseer_new(PyTypeObject* type, PyObject* args, PyObject* kw)
{
	static char* kwlist[] = { "culling", "thread_number", NULL };

	effekseer_obj* self = NULL;
	int culling = false;
	int thread_number = 0;

	if (PyArg_ParseTupleAndKeywords(args, kw, "|ii", kwlist, &culling, &thread_number))
	{
		self = (effekseer_obj*)type->tp_alloc(type, 0);
		self->effekseer = new pyxieEffekseer();
		self->effekseer->init(culling, thread_number);
	}

	return (PyObject*)self;
}

void effekseer_dealloc(effekseer_obj* self)
{
	self->effekseer->release();
	Py_TYPE(self)->tp_free(self);
}

PyObject* effekseer_str(effekseer_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "effekseer object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

PyObject* effekseer_registerTextureLoader(PyTypeObject* type, PyObject* args)
{
	effekseer_obj* self = NULL;

	if (!PyArg_ParseTuple(args, "O", &onTextureLoaderCallBack))
		return NULL;

	if (!PyCallable_Check(onTextureLoaderCallBack))
	{
		PyErr_SetString(PyExc_TypeError, "Callback function must be a callable object!");
		return NULL;
	}
	Py_XINCREF(onTextureLoaderCallBack);

	pyxieEffekseer::setTextureLoader(effekseer_TextureLoader);

	Py_INCREF(Py_None);
	return Py_None;
}

PyObject* effekseer_Shoot(effekseer_obj* self, PyObject* args, PyObject* kwargs)
{
	static char* kwlist[] = { "proj", "view", "dt", "clear", "update", "render", "culling", NULL };

	float dt = 0.166666666667f;
	int clear = false;
	int update = true;
	int render = true;
	int culling = true;
	PyObject* mat_proj;
	PyObject* mat_view;
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OO|fiiii", kwlist , &mat_proj, &mat_view, &dt, &clear, &update, &render, &culling))
		return NULL;

	mat_obj* proj_obj = (mat_obj*)mat_proj;
	mat_obj* view_obj = (mat_obj*)mat_view;

	self->effekseer->SetRenderProjectionMatrix(proj_obj->m);
	self->effekseer->SetRenderViewMatrix(view_obj->m);	

	if (update)
	{
		self->effekseer->update(dt);
	}
	
	if (render)
	{
		self->effekseer->render(clear, culling);
	}	

	Py_INCREF(Py_None);
	return Py_None;
}

PyObject* effekseer_Add(effekseer_obj* self, PyObject* args, PyObject* kwargs)
{
	static char* kwlist[] = { "name", "loop", "position", "rotation", "scale", "target_position", "cache_only", NULL };

	PyObject* position = nullptr;
	PyObject* rotation = nullptr;
	PyObject* scale = nullptr;
	PyObject* target_position = nullptr;
	char* name;
	int loop = 0;
	int cache_only = 0;
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s|iOOOOi", kwlist, &name, &loop, &position, &rotation, &scale, &target_position , &cache_only)) return NULL;

	int d1 = 3;
	float pos_buff[3] = {0.0, 0.0, 0.0};
	float* pos = pyObjToFloat((PyObject*)position, pos_buff, d1);

	float rot_buff[3] = { 0.0, 0.0, 0.0 };
	float* rot = pyObjToFloat((PyObject*)rotation, rot_buff, d1);

	float scale_buff[3] = { 1.0, 1.0, 1.0 };
	float* scl = pyObjToFloat((PyObject*)scale, scale_buff, d1);

	float target_buff[3] = { 0.0, 0.0, 0.0 };
	float* target_pos = pyObjToFloat((PyObject*)target_position, target_buff, d1);

	int handle = self->effekseer->play(name , loop, *((Vector3D*)pos), *((Vector3D*)rot), *((Vector3D*)scl), *((Vector3D*)target_pos), cache_only);
	return PyLong_FromLong(handle);
}

PyObject* effekseer_Remove(effekseer_obj* self, PyObject* args)
{
	int handle = -1;
	if (!PyArg_ParseTuple(args, "i", &handle))
		return NULL;
	
	self->effekseer->stop(handle);

	Py_INCREF(Py_None);
	return Py_None;
}

PyObject* effekseer_Play(effekseer_obj* self, PyObject* args)
{
	int handle = -1;
	if (!PyArg_ParseTuple(args, "i", &handle))
		return NULL;

	self->effekseer->play(handle);

	Py_INCREF(Py_None);
	return Py_None;
}

PyObject* effekseer_StopAllEffects(effekseer_obj* self)
{
	self->effekseer->stopAll();

	Py_INCREF(Py_None);
	return Py_None;
}

PyObject* effekseer_SetTargetLocation(effekseer_obj* self, PyObject* args)
{
	int handle = -1;
	float x, y, z;
	if (!PyArg_ParseTuple(args, "ifff", &handle, &x, &y, &z))
		return NULL;
	
	self->effekseer->SetTargetLocation(handle, x, y, z);

	Py_INCREF(Py_None);
	return Py_None;
}

PyObject* effekseer_GetLocation(effekseer_obj* self, PyObject* args)
{
	int handle = -1;
	if (!PyArg_ParseTuple(args, "i", &handle))
		return NULL;

	auto location = self->effekseer->GetLocation(handle);
	PyObject* at = Py_BuildValue("(fff)", location.X, location.Y, location.Z);
	return at;
}

PyObject* effekseer_SetLocation(effekseer_obj* self, PyObject* args)
{
	int handle = -1;
	float x, y, z;
	if (!PyArg_ParseTuple(args, "ifff", &handle, &x, &y, &z))
		return NULL;

	self->effekseer->SetLocation(handle, x, y, z);

	Py_INCREF(Py_None);
	return Py_None;
}

PyObject* effekseer_SetRotation(effekseer_obj* self, PyObject* args)
{
	int handle = -1;
	float x, y, z;
	if (!PyArg_ParseTuple(args, "ifff", &handle, &x, &y, &z))
		return NULL;

	self->effekseer->SetRotation(handle, x, y, z);

	Py_INCREF(Py_None);
	return Py_None;
}

PyObject* effekseer_SetScale(effekseer_obj* self, PyObject* args)
{
	int handle = -1;
	float x, y, z;
	if (!PyArg_ParseTuple(args, "ifff", &handle, &x, &y, &z))
		return NULL;

	self->effekseer->SetScale(handle, x, y, z);

	Py_INCREF(Py_None);
	return Py_None;
}

PyObject* effekseer_SetColor(effekseer_obj* self, PyObject* args)
{
	int handle = -1;
	int red, green, blue, alpha;
	if (!PyArg_ParseTuple(args, "iiiii", &handle, &red, &green, &blue, &alpha))
		return NULL;

	self->effekseer->SetAllColor(handle, Color(red, green, blue, alpha));

	Py_INCREF(Py_None);
	return Py_None;
}

PyObject* effekseer_SetSpeed(effekseer_obj* self, PyObject* args)
{
	int handle = -1;
	float speed;
	if (!PyArg_ParseTuple(args, "if", &handle, &speed))
		return NULL;

	self->effekseer->SetSpeed(handle, speed);

	Py_INCREF(Py_None);
	return Py_None;
}

PyObject* effekseer_GetSpeed(effekseer_obj* self, PyObject* args)
{
	int handle = -1;
	if (!PyArg_ParseTuple(args, "i", &handle))
		return NULL;

	return PyFloat_FromDouble(self->effekseer->GetSpeed(handle));
}

PyObject* effekseer_IsPlaying(effekseer_obj* self, PyObject* args)
{
	int handle = -1;
	if (!PyArg_ParseTuple(args, "i", &handle))
		return NULL;

	return PyLong_FromLong(self->effekseer->IsPlaying(handle));
}

PyObject* effekseer_SetPause(effekseer_obj* self, PyObject* args)
{
	int handle = -1;
	int paused = 0;
	if (!PyArg_ParseTuple(args, "ii", &handle, &paused))
		return NULL;

	self->effekseer->SetPause(handle, paused);

	Py_INCREF(Py_None);
	return Py_None;
}

PyObject* effekseer_GetPause(effekseer_obj* self, PyObject* args)
{
	int handle = -1;
	if (!PyArg_ParseTuple(args, "i", &handle))
		return NULL;

	return PyLong_FromLong(self->effekseer->GetPause(handle));
}

PyObject* effekseer_SetShown(effekseer_obj* self, PyObject* args)
{
	int handle = -1;
	int shown = 0;
	int reset = 0;
	if (!PyArg_ParseTuple(args, "ii|i", &handle, &shown, &reset))
		return NULL;

	self->effekseer->SetShown(handle, shown, reset);

	Py_INCREF(Py_None);
	return Py_None;
}

PyObject* effekseer_GetShown(effekseer_obj* self, PyObject* args)
{
	int handle = -1;
	if (!PyArg_ParseTuple(args, "i", &handle))
		return NULL;

	return PyLong_FromLong(self->effekseer->GetShown(handle));
}

PyObject* effekseer_SetLoop(effekseer_obj* self, PyObject* args)
{
	int handle = -1;
	int loop = 0;
	if (!PyArg_ParseTuple(args, "ii", &handle, &loop))
		return NULL;

	self->effekseer->SetLoop(handle, loop);

	Py_INCREF(Py_None);
	return Py_None;
}

PyObject* effekseer_GetLoop(effekseer_obj* self, PyObject* args)
{
	int handle = -1;
	if (!PyArg_ParseTuple(args, "i", &handle))
		return NULL;

	return PyLong_FromLong(self->effekseer->GetLoop(handle));
}

PyObject* effekseer_DrawCallCount(effekseer_obj* self)
{
	return PyLong_FromLong(self->effekseer->getDrawcallCount());
}

PyObject* effekseer_DrawVertexCount(effekseer_obj* self)
{
	return PyLong_FromLong(self->effekseer->getDrawVertexCount());
}

PyObject* effekseer_UpdateTime(effekseer_obj* self)
{
	return PyLong_FromLong(self->effekseer->getUpdateTime());
}

PyObject* effekseer_DrawTime(effekseer_obj* self)
{
	return PyLong_FromLong(self->effekseer->getDrawTime());
}

PyObject* effekseer_getFramerate(effekseer_obj* self)
{
	return PyFloat_FromDouble(self->effekseer->GetFramerate());
}

int effekseer_setFramerate(effekseer_obj* self, PyObject* value)
{
	if (!(PyFloat_Check(value) || PyLong_Check(value))) {
		PyErr_SetString(PyExc_TypeError, "Only float value can be set to desired framerate.");
		return -1;
	}
	self->effekseer->SetFramerate((float)PyFloat_AsDouble(value));
	return 0;
}

PyObject* effekseer_GetInstanceCount(effekseer_obj* self, PyObject* args)
{
	int handle = -1;
	if (!PyArg_ParseTuple(args, "i", &handle))
		return NULL;

	return PyLong_FromLong(self->effekseer->getInstanceCount(handle));
}

PyObject* effekseer_GetTotalInstanceCount(effekseer_obj* self)
{
	return PyLong_FromLong(self->effekseer->getTotalInstanceCount());
}

PyObject* effekseer_GetDynamicInput(effekseer_obj* self, PyObject* args)
{
	int handle = -1;
	if (!PyArg_ParseTuple(args, "i", &handle))
		return NULL;

	float* dynamicInput = self->effekseer->getDynamicInput(handle);
	PyObject* obj = Py_BuildValue("(ffff)", dynamicInput[0], dynamicInput[1], dynamicInput[2], dynamicInput[3]);
	return obj;
}

PyObject* effekseer_SetDynamicInput(effekseer_obj* self, PyObject* args)
{
	int handle = -1;
	PyObject* input = nullptr;
	float x, y, z, w;
	if (!PyArg_ParseTuple(args, "iO", &handle, &input))
		return NULL;

	int d1 = 4;
	float buff[4] = { 0.0, 0.0, 0.0, 0.0 };
	float* input_obj = pyObjToFloat((PyObject*)input, buff, d1);

	self->effekseer->setDynamicInput(handle, input_obj);

	Py_INCREF(Py_None);
	return Py_None;
}

PyMethodDef effekseer_methods[] = {
	{ "texture_loader", (PyCFunction)effekseer_registerTextureLoader, METH_VARARGS, effekseerTextureLoader_doc },
	{ "shoot", (PyCFunction)effekseer_Shoot, METH_VARARGS | METH_KEYWORDS, effekseerShoot_doc },
	{ "add", (PyCFunction)effekseer_Add, METH_VARARGS | METH_KEYWORDS, effekseerAdd_doc },
	{ "remove", (PyCFunction)effekseer_Remove, METH_VARARGS, effekseerRemove_doc },
	{ "play", (PyCFunction)effekseer_Play, METH_VARARGS, effekseerPlay_doc },
	{ "stop_all_effects", (PyCFunction)effekseer_StopAllEffects, METH_NOARGS, effekseerStopAllEffects_doc },
	{ "drawcall_count", (PyCFunction)effekseer_DrawCallCount, METH_NOARGS, effekseerDrawCallCount_doc },
	{ "vertex_count", (PyCFunction)effekseer_DrawVertexCount, METH_NOARGS, effekseerDrawVertexCount_doc },
	{ "update_time", (PyCFunction)effekseer_UpdateTime, METH_NOARGS, effekseerUpdateTime_doc },
	{ "draw_time", (PyCFunction)effekseer_DrawTime, METH_NOARGS, effekseerDrawTime_doc },
	{ "set_target_location", (PyCFunction)effekseer_SetTargetLocation, METH_VARARGS, effekseerSetTargetLocation_doc },
	{ "get_location", (PyCFunction)effekseer_GetLocation, METH_VARARGS, effekseerGetLocation_doc },
	{ "set_location", (PyCFunction)effekseer_SetLocation, METH_VARARGS, effekseerSetLocation_doc },
	{ "set_rotation", (PyCFunction)effekseer_SetRotation, METH_VARARGS, effekseerSetRotation_doc },
	{ "set_scale", (PyCFunction)effekseer_SetScale, METH_VARARGS, effekseerSetScale_doc },
	{ "set_color", (PyCFunction)effekseer_SetColor, METH_VARARGS, effekseerSetColor_doc },
	{ "get_speed", (PyCFunction)effekseer_GetSpeed, METH_VARARGS, effekseerGetSpeed_doc },
	{ "set_speed", (PyCFunction)effekseer_SetSpeed, METH_VARARGS, effekseerSetSpeed_doc },
	{ "is_playing", (PyCFunction)effekseer_IsPlaying, METH_VARARGS, effekseerIsPlaying_doc },
	{ "set_pause", (PyCFunction)effekseer_SetPause, METH_VARARGS, effekseerSetPause_doc },
	{ "get_pause", (PyCFunction)effekseer_GetPause, METH_VARARGS, effekseerGetPause_doc },
	{ "set_shown", (PyCFunction)effekseer_SetShown, METH_VARARGS, effekseerSetShown_doc },
	{ "get_shown", (PyCFunction)effekseer_GetShown, METH_VARARGS, effekseerGetShown_doc },
	{ "set_loop", (PyCFunction)effekseer_SetLoop, METH_VARARGS, effekseerSetLoop_doc },
	{ "get_loop", (PyCFunction)effekseer_GetLoop, METH_VARARGS, effekseerGetLoop_doc },
	{ "instance_count", (PyCFunction)effekseer_GetInstanceCount, METH_VARARGS, effekseerInstanceCount_doc },
	{ "total_instance_count", (PyCFunction)effekseer_GetTotalInstanceCount, METH_NOARGS, effekseerGetTotalInstanceCount_doc },
	{ "set_dynamic_input", (PyCFunction)effekseer_SetDynamicInput, METH_VARARGS, effekseerSetDynamicInput_doc },
	{ "get_dynamic_input", (PyCFunction)effekseer_GetDynamicInput, METH_VARARGS, effekseerGetDynamicInput_doc },
	{ NULL,	NULL }
};

PyGetSetDef effekseer_getsets[] = {
	{ const_cast<char*>("framerate"), (getter)effekseer_getFramerate, (setter)effekseer_setFramerate, framerate_doc, NULL },
	{ NULL, NULL }
};

PyTypeObject EffekseerType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igeEffekseer",						/* tp_name */
	sizeof(effekseer_obj),				/* tp_basicsize */
	0,                                  /* tp_itemsize */
	(destructor)effekseer_dealloc,		/* tp_dealloc */
	0,                                  /* tp_print */
	0,							        /* tp_getattr */
	0,                                  /* tp_setattr */
	0,                                  /* tp_reserved */
	0,                                  /* tp_repr */
	0,					                /* tp_as_number */
	0,                                  /* tp_as_sequence */
	0,                                  /* tp_as_mapping */
	0,                                  /* tp_hash */
	0,                                  /* tp_call */
	(reprfunc)effekseer_str,			/* tp_str */
	0,                                  /* tp_getattro */
	0,                                  /* tp_setattro */
	0,                                  /* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,					/* tp_flags */
	0,									/* tp_doc */
	0,									/* tp_traverse */
	0,                                  /* tp_clear */
	0,                                  /* tp_richcompare */
	0,                                  /* tp_weaklistoffset */
	0,									/* tp_iter */
	0,									/* tp_iternext */
	effekseer_methods,					/* tp_methods */
	0,                                  /* tp_members */
	effekseer_getsets,					/* tp_getset */
	0,                                  /* tp_base */
	0,                                  /* tp_dict */
	0,                                  /* tp_descr_get */
	0,                                  /* tp_descr_set */
	0,                                  /* tp_dictoffset */
	0,                                  /* tp_init */
	0,                                  /* tp_alloc */
	effekseer_new,						/* tp_new */
	0,									/* tp_free */
};


static PyModuleDef effekseer_module = {
	PyModuleDef_HEAD_INIT,
	"igeEffekseer",							// Module name to use with Python import statements
	"Effekseer Module.",					// Module description
	0,
	effekseer_methods						// Structure that defines the methods of the module
};

PyMODINIT_FUNC PyInit_igeEffekseer() {
	PyObject* module = PyModule_Create(&effekseer_module);

	if (PyType_Ready(&EffekseerType) < 0) return NULL;

	Py_INCREF(&EffekseerType);
	PyModule_AddObject(module, "particle", (PyObject*)&EffekseerType);

	return module;
}