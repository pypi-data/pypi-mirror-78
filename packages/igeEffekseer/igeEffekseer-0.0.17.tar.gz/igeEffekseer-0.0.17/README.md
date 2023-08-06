# igeEffekseer

C++ extension Effekseer for 3D and 2D games.

## Before running this tutorial, you have to install igeEffekseer
	[pip install igeEffekseer]
    

## The Editor
Get from link : https://effekseer.github.io/en/download.html

## Tutorial
https://github.com/indigames/pyxieTutorials/tree/dev/igeEffekseer

## Support

- Effeck : .efk
- Texture : .pyxi

## APIs
### Functions
- static
	- texture_loader
		- set the texture loader callback
		- use igeCore as a helper to load the texture then give back the texture information (width, height, id, has_mipmap)
		```python
		textures = {}
		def f_texture_loader(name, type):
			print('f_texture_loader - ' + name)
			tex = core.texture(name)    
			textures[name] = tex
			return (tex.width, tex.height, tex.id, tex.numMips > 1)

		igeEffekseer.texture_loader(f_texture_loader)
		```

- getset
	```python
	_particle = igeEffekseer.particle()
	```	
	- framerate
		- the desired framerate
		- __60__ fps as default
		```python
		_particle.framerate = 60.0
		```
- particle
	```python
	_particle = igeEffekseer.particle()
	```
	- shoot
		- update then render the effekseer system
		- *shoot(delta_time, clean_screen)*
			- delta_time : float
			- clean_screen : bool optional
		```python
		_particle.shoot(core.getElapsedTime())
		```
	- add
		- add the effect to the effekseer system
		- *handle = _particle.add(name, loop, position, rotation, scale)*
			- name : string
				- the effect string path
			- loop : bool optional
				- *Optional* Is looping or not
			- position : tuple
				- *Optional* The position optional
            - rotation : tuple
				- *Optional* The rotation optional
            - scale : tuple
				- *Optional* The scale optional
		```python
		_distortion_handle = _particle.add(name='Simple_Distortion.efk', loop=True, position=(0.0, 0.0, 0.0))
		```
	- remove
		- remove the effect from effekseer system
		- *_particle.remove(handle)*
			- handle : int
				- the effect handle
		```python
		_particle.remove(_distortion_hd)
		```
	- stop_all_effects
		- remove | stop all the effect from effekseer system
		```python
		_particle.stop_all_effects()
		```
	- set_target_location
		- set target location for the effect handle
		- *_particle.set_target_location(handle, x, y, z)*
			- handle : int
				- the effect handle
			- x, y, z : float location
	- get_location
		- get location from the effect handle
		- *result = _particle.get_location(handle)*
			- handle : int
				- the effect handle
			- result : tuple location
	- set_location
		- set location for the effect handle
		- *_particle.set_location(handle, x, y, z)*
			- handle : int
				- the effect handle
			- x, y, z : float location
	- set_rotation
		- set rotation for the effect handle
		- *_particle.set_rotation(handle, x, y, z)*
			- handle : int
				- the effect handle
			- x, y, z : float rotation
	- set_scale
		- set scale for the effect handle
		- *_particle.set_scale(handle, x, y, z)*
			- handle : int
				- the effect handle
			- x, y, z : float scale
	- set_color
		- set scale for the effect handle
		- *_particle.set_scale(handle, red, green, blue, alpha)*
			- handle : int
				- the effect handle
			- red, green, blue, alpha : int value channel (0-255)
	- get_speed
		- get speed from the effect handle
		- *result = _particle.get_speed(handle)*
			- handle : int
				- the effect handle
			- result : float speed
	- set_speed
		- set speed for the effect handle
		- *_particle.set_speed(handle, speed)*
			- handle : int
				- the effect handle
			- speed : float value
	- is_playing
		- checking the effect is playing
		- *result = _particle.is_playing(handle)*
			- handle : int
				- the effect handle
			- result : bool. True if the effect is playing
	- set_pause
		- pause the effect handle
		- *_particle.set_pause(handle, paused)*
			- handle : int
				- the effect handle
			- paused : bool value
	- get_pause
		- get the pause status from the effect handle
		- *result = _particle.get_pause(handle)*
			- handle : int
				- the effect handle
			- result : bool value
	- set_shown
		- switch between show or hide of the effect handle
		- *_particle.set_shown(handle, shown)*
			- handle : int
				- the effect handle
			- shown : bool value
	- get_shown
		- get the show status from the effect handle
		- *result = _particle.get_shown(handle)*
			- handle : int
				- the effect handle
			- result : bool value
	- set_loop
		- loop (true / false)
		- *_particle.set_loop(handle, loop)*
			- handle : int
				- the effect handle
			- loop : bool value
	- get_loop
		- get the loop status from the effect handle
		- *result = _particle.get_loop(handle)*
			- handle : int
				- the effect handle
			- result : bool value
- statistic
	- drawcall_count
		- return the drawcall count
		- *count = _particle.drawcall_count()*
	- vertex_count
		- return the draw vertex count
		- *count = _particle.vertex_count()*
	- update_time
		- return the update time take
		- *time = _particle.update_time()*
		- time : int (micro second)
	- draw_time
		- return the draw time take
		- *time = _particle.draw_time()*
		- time : int (micro second)