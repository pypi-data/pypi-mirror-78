
#if defined _WIN32
#   include <glew.h>
#   include <gl/gl.h>
#   include <gl/glu.h>
#	include <wglew.h>
#endif

#include "pyxieEffekseer.h"
#include <string>

TextureLoaderFunc pyxieEffekseer::textureLoaderFunc = nullptr;
static const char* effekseer_extension = ".efk";

class pyxieTextureLoader : public TextureLoader
{
public:
	pyxieTextureLoader();
	virtual ~pyxieTextureLoader();

public:
	TextureData* Load(const EFK_CHAR* path, TextureType textureType) override;
	void Unload(TextureData* data) override;
};


pyxieTextureLoader::pyxieTextureLoader()
{
}

pyxieTextureLoader::~pyxieTextureLoader()
{
}

static std::u16string getFilenameWithoutExt(const char16_t* path)
{
	int start = 0;
	int end = 0;

	for (int i = start; path[i] != 0; i++)
	{
		if (path[i] == u'.')
		{
			end = i;
		}
	}

	std::vector<char16_t> ret;

	for (int i = start; i < end; i++)
	{
		ret.push_back(path[i]);
	}
	ret.push_back(0);

	return std::u16string(ret.data());
}

TextureData* pyxieTextureLoader::Load(const EFK_CHAR* path, TextureType textureType)
{
	auto _path = getFilenameWithoutExt(path);	

	char path_[300];
	ConvertUtf16ToUtf8((int8_t*)path_, 300, (const int16_t*)_path.c_str());
	if (pyxieEffekseer::textureLoaderFunc != nullptr)
	{
		TextureLoaderCallback callback = { path_ , TextureLoaderType::LOAD};
		auto textureData = pyxieEffekseer::textureLoaderFunc(callback);

		return textureData;
	}
	return new TextureData();
}

void pyxieTextureLoader::Unload(TextureData* data)
{

}

pyxieEffekseer::pyxieEffekseer()
	: manager(nullptr)
	, renderer(nullptr)
	, desiredFramerate(60.0)
	, nextHandle(0)
	, culling_enabled(false)
{
}

pyxieEffekseer::~pyxieEffekseer()
{
	effect_map.clear();
}

void pyxieEffekseer::init(bool culling_enable, int thread_number)
{	
#if defined(_WIN32)
	renderer = EffekseerRendererGL::Renderer::Create(4000, EffekseerRendererGL::OpenGLDeviceType::OpenGL3);
#else
    // larger buffer make the application more slower
    #if defined(__ANDROID__)
	renderer = EffekseerRendererGL::Renderer::Create(600, EffekseerRendererGL::OpenGLDeviceType::OpenGLES3);
    #else
    renderer = EffekseerRendererGL::Renderer::Create(4000, EffekseerRendererGL::OpenGLDeviceType::OpenGLES3);
    #endif
#endif
	renderer->SetTextureUVStyle(UVStyle::VerticalFlipped);	// adapt with igeCore.texture

	manager = Manager::Create(4000);

	manager->SetSpriteRenderer(renderer->CreateSpriteRenderer());
	manager->SetRibbonRenderer(renderer->CreateRibbonRenderer());
	manager->SetRingRenderer(renderer->CreateRingRenderer());
	manager->SetTrackRenderer(renderer->CreateTrackRenderer());
	manager->SetModelRenderer(renderer->CreateModelRenderer());

	manager->SetTextureLoader(new pyxieTextureLoader()); //renderer->CreateTextureLoader() || new pyxieTextureLoader()
	manager->SetModelLoader(renderer->CreateModelLoader());
	manager->SetMaterialLoader(renderer->CreateMaterialLoader());

	if (culling_enable)
	{
		manager->CreateCullingWorld(1000.0f, 1000.0f, 1000.0f, 5);
		culling_enabled = culling_enable;
	}

	if (thread_number > 1)
	{
		manager->LaunchWorkerThreads(thread_number);
	}
}

void pyxieEffekseer::release()
{
	for (auto it = effect_map.begin(); it != effect_map.end(); it++)
	{
		(*it).second.effect->Release();
	}
	effect_map.clear();

	if (manager != nullptr)
	{
		manager->Destroy();
		manager = nullptr;
	}

	if (renderer != nullptr)
	{
		renderer->Destroy();
		renderer = nullptr;
	}
}

void pyxieEffekseer::update(float dt)
{
	renderer->SetProjectionMatrix(projection_mat);
	renderer->SetCameraMatrix(view_mat);

	auto it = effect_map.begin();
	auto it_end = effect_map.end();

	while(it != it_end)
	{	
		Handle handle = (*it).second.handle;
		if (!manager->Exists(handle))
		{
			if ((*it).second.isLooping)
			{
				if ((*it).second.isShown)
				{
					auto effect = (*it).second.effect;
					Handle hd = manager->Play(effect, (*it).second.position);
					manager->SetRotation(hd, (*it).second.rotation.X, (*it).second.rotation.Y, (*it).second.rotation.Z);
					manager->SetScale(hd, (*it).second.scale.X, (*it).second.scale.Y, (*it).second.scale.Z);
					manager->SetTargetLocation(hd, (*it).second.target_position.X, (*it).second.target_position.Y, (*it).second.target_position.Z);					
					for (int i = 0; i < 4; i++)
					{
						manager->SetDynamicInput(hd, i, (*it).second.dynamic_inputs[i]);
					}
					effect->AddRef();

					effect_map[(*it).first].handle = hd;
				}
				++it;				
			}
			else
			{
				(*it).second.effect->Release();
				effect_map.erase(it++);
			}
		}
		else
		{
			++it;
		}
	}

	manager->Update(desiredFramerate * dt);	
}

void pyxieEffekseer::play(Handle handle)
{	
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		auto effect = it->second.effect;
		auto position = it->second.position;
		auto rotation = it->second.rotation;
		auto scale = it->second.scale;
		auto target_position = it->second.target_position;

		Handle hd = manager->Play(effect, position);
		manager->SetLocation(hd, position);
		manager->SetRotation(hd, rotation.X, rotation.Y, rotation.Z);
		manager->SetScale(hd, scale.X, scale.Y, scale.Z);
		manager->SetTargetLocation(hd, target_position.X, target_position.Y, target_position.Z);

		effect_map[handle].handle = hd;
	}
}

uint32_t pyxieEffekseer::play(const char* name, bool loop, const Effekseer::Vector3D& position, const Vector3D& rotation, const Vector3D& scale, const Vector3D& target_position, bool cache_only)
{
	uint32_t handle = nextHandle;	
	nextHandle++;

	std::string platform = PlatformOverride(name);

	EFK_CHAR path[300];
	ConvertUtf8ToUtf16(path, 300, platform.c_str());

	auto _effect = Effect::Create(manager, path);
	if (_effect == nullptr)	//fallback
	{
		ConvertUtf8ToUtf16(path, 300, name);
		_effect = Effect::Create(manager, path);
		if (_effect == nullptr)	//need the extension
		{
			std::string original = std::string(name) + effekseer_extension;
			ConvertUtf8ToUtf16(path, 300, original.c_str());
			_effect = Effect::Create(manager, path);
		}
	}
	int hd = -1;
	if (!cache_only)
	{
		hd = manager->Play(_effect, position);

		manager->SetLocation(hd, position);
		manager->SetRotation(hd, rotation.X, rotation.Y, rotation.Z);
		manager->SetScale(hd, scale.X, scale.Y, scale.Z);
		manager->SetTargetLocation(hd, target_position.X, target_position.Y, target_position.Z);
	}
	effect_map[handle] = { hd, _effect, loop, true, position, rotation, scale, target_position };

	_effect->AddRef();
	
	return handle;
}

void pyxieEffekseer::stop(int handle)
{
	Handle hd = 0;
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		hd = (*it).second.handle;
		(*it).second.effect->Release();
		effect_map.erase(it);
	}
	
	if (manager->Exists(hd))
	{
		manager->StopEffect(hd);
	}
}

void pyxieEffekseer::stopAll()
{
	manager->StopAllEffects();

	for (auto it = effect_map.begin(); it != effect_map.end(); it++)
	{
		(*it).second.effect->Release();
	}
	effect_map.clear();
}

void pyxieEffekseer::clearScreen()
{
    glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT);
}

void pyxieEffekseer::setup(bool isClear)
{
#if defined(__ANDROID__) || TARGET_OS_IPHONE
    int fbo = 0;
    glGetIntegerv(GL_FRAMEBUFFER_BINDING, &fbo);
    glBindFramebuffer(GL_FRAMEBUFFER, fbo);    
#endif

	if (isClear)
	{
		clearScreen();
	}
}

void pyxieEffekseer::render(bool isClear, bool culling_override)
{
	setup(isClear);

	renderer->BeginRendering();
	if (culling_enabled && culling_override)
	{
		manager->CalcCulling(renderer->GetCameraProjectionMatrix(), false);
	}
	manager->Draw();
	renderer->EndRendering();
}

int32_t pyxieEffekseer::getDrawcallCount()
{
	int32_t count = renderer->GetDrawCallCount();
	renderer->ResetDrawCallCount();

	return count;
}

int32_t pyxieEffekseer::getDrawVertexCount()
{
	int32_t count = renderer->GetDrawVertexCount();
	renderer->ResetDrawVertexCount();

	return count;
}

int32_t pyxieEffekseer::getUpdateTime()
{
	return manager->GetUpdateTime();
}

int32_t pyxieEffekseer::getDrawTime()
{
	return manager->GetDrawTime();
}

int32_t pyxieEffekseer::getInstanceCount(Handle handle)
{
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		Handle hd = it->second.handle;
		return manager->GetInstanceCount(hd);
	}
	return 0;
}

int32_t pyxieEffekseer::getTotalInstanceCount()
{
	return manager->GetTotalInstanceCount();
}

void pyxieEffekseer::setTextureLoader(TextureLoaderFunc loader)
{
	textureLoaderFunc = loader;
}

void pyxieEffekseer::SetTargetLocation(Handle handle, float x, float y, float z)
{
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		Handle hd = it->second.handle;
		it->second.target_position = Vector3D(x, y, z);
		manager->SetTargetLocation(hd, x, y, z);
	}	
}

const Vector3D& pyxieEffekseer::GetLocation(Handle handle)
{
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		Handle hd = it->second.handle;
		return manager->GetLocation(hd);
	}	
}
void pyxieEffekseer::SetLocation(Handle handle, float x, float y, float z)
{
	SetLocation(handle, Vector3D(x, y, z));
}

void pyxieEffekseer::SetLocation(Handle handle, const Vector3D& location)
{
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		it->second.position = location;
		Handle hd = it->second.handle;
		manager->SetLocation(hd, location);
	}
}

void pyxieEffekseer::SetRotation(Handle handle, float x, float y, float z)
{
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		it->second.rotation = Vector3D(x, y, z);
		Handle hd = it->second.handle;
		manager->SetRotation(hd, x, y, z);
	}
}

void pyxieEffekseer::SetScale(Handle handle, float x, float y, float z)
{	
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		it->second.scale = Vector3D(x, y, z);
		Handle hd = it->second.handle;
		manager->SetScale(hd, x, y, z);
	}
}

void pyxieEffekseer::SetAllColor(Handle handle, Color color)
{
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		Handle hd = it->second.handle;
		manager->SetAllColor(hd, color);
	}	
}

void pyxieEffekseer::SetSpeed(Handle handle, float speed)
{
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		Handle hd = it->second.handle;
		manager->SetSpeed(hd, speed);
	}	
}

float pyxieEffekseer::GetSpeed(Handle handle)
{
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		Handle hd = it->second.handle;
		return manager->GetSpeed(hd);
	}
	return 0.0;	
}

bool pyxieEffekseer::IsPlaying(Handle handle)
{
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		Handle hd = it->second.handle;
		return manager->Exists(hd);
	}
	return false;
}

void pyxieEffekseer::SetPause(Handle handle, bool paused)
{
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		Handle hd = it->second.handle;
		manager->SetPaused(hd, paused);
	}
}

bool pyxieEffekseer::GetPause(Handle handle)
{
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		Handle hd = it->second.handle;
		return manager->GetPaused(hd);
	}
	return false;	
}

void pyxieEffekseer::SetShown(Handle handle, bool shown, bool reset)
{
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		it->second.isShown = shown;
		Handle hd = it->second.handle;
		manager->SetShown(hd, shown);
		if (reset)
		{
			manager->UpdateHandleToMoveToFrame(hd, 0);
		}
	}	
}

bool pyxieEffekseer::GetShown(Handle handle)
{
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		Handle hd = it->second.handle;
		return manager->GetShown(hd);
	}
	return false;
}

void pyxieEffekseer::SetLoop(Handle handle, bool loop)
{
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		it->second.isLooping = loop;
	}
}

bool pyxieEffekseer::GetLoop(Handle handle)
{
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		return it->second.isLooping;
	}
	return false;
}

void pyxieEffekseer::SetRenderProjectionMatrix(float* projection)
{
	memcpy(projection_mat.Values, projection, sizeof(float) * 16);
}

void pyxieEffekseer::SetRenderViewMatrix(float* view_inv)
{
	memcpy(view_mat.Values, view_inv, sizeof(float) * 16);
}

void pyxieEffekseer::setDynamicInput(uint32_t handle, float* value)
{
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		memcpy(it->second.dynamic_inputs, value, sizeof(float) * 4);
		Handle hd = it->second.handle;
		for (int i = 0; i < 4; i++)
		{
			manager->SetDynamicInput(hd, i, value[i]);
		}
	}
}

float* pyxieEffekseer::getDynamicInput(uint32_t handle)
{
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		return it->second.dynamic_inputs;
	}
	float buff[4] = { 0.0, 0.0, 0.0, 0.0 };
	return buff;
}

std::string pyxieEffekseer::PlatformOverride(const char* name)
{
	std::string result = name;
	auto found = result.find_last_of(".");
	if (found != std::string::npos && result.substr(found) == effekseer_extension)
	{
		return result;
	}
#if defined(__ANDROID__)
	result = result + "_android" + effekseer_extension;
#elif TARGET_OS_IPHONE
	result = result + "_ios" + effekseer_extension;
#else
	result = result + "_win" + effekseer_extension;
#endif
	return result;
}