# Audio Module

## Purpose
The Audio Module handles all audio playback, including sound effects, music, voice communication, and 3D spatial audio positioning. It manages audio resources and provides immersive audio feedback for gameplay events.

## Components
- **Sound System** (`sound/`): Core audio playback and management
- **Game Sound System** (`gamesnd/`): Sound effect definitions and management
- **3D Audio**: Spatial positioning based on object locations
- **Audio Mixing**: Multiple simultaneous sound sources
- **Resource Management**: Loading, caching, and unloading audio
- **Environmental Effects**: Reverb and other audio processing
- **Voice Acting**: Character dialogue and mission briefings

## Dependencies
- **Core Entity Module**: 3D positioning of audio sources
- **Ship Module**: Ship-specific audio (engines, weapons)
- **Weapon Module**: Weapon firing sounds
- **Mission Module**: Mission-specific audio triggers
- **UI Module**: Interface sound effects

## C++ Components
- Sound loading and playback functions
- 3D spatial audio positioning
- Music playback and management
- Sound effect triggering and control
- Audio resource management
- `snd_load()`, `snd_play()`, `snd_stop()`: Sound management functions
- Sound property access functions
- 3D sound positioning functions

## Godot Equivalent Mapping

### Native GDScript Classes
```gdscript
# Audio manager for handling all audio in the game
class AudioManager:
    var master_bus: String = "Master"
    var music_bus: String = "Music"
    var sfx_bus: String = "SFX"
    var voice_bus: String = "Voice"
    
    var music_player: AudioStreamPlayer
    var ambient_player: AudioStreamPlayer
    var current_music: String = ""
    
    func _ready():
        # Initialize audio players
        setup_audio_players()
        
    func setup_audio_players():
        # Create music player
        music_player = AudioStreamPlayer.new()
        music_player.bus = music_bus
        music_player.autoplay = false
        add_child(music_player)
        
        # Create ambient player
        ambient_player = AudioStreamPlayer.new()
        ambient_player.bus = music_bus
        ambient_player.autoplay = false
        add_child(ambient_player)
        
    func play_sound(sound_name: String, position: Vector3 = Vector3.ZERO, 
                   entity: Node3D = null, volume: float = 1.0):
        # Play a 3D positional sound effect
        var sound_data = SoundDatabase.get_sound(sound_name)
        if sound_data == null:
            return
            
        var player = AudioStreamPlayer3D.new()
        player.stream = sound_data.audio_stream
        player.unit_db = linear_to_db(volume)
        player.max_distance = sound_data.max_distance
        player.bus = sfx_bus
        
        # Position the sound
        if entity != null:
            player.global_position = entity.global_position
        else:
            player.global_position = position
            
        add_child(player)
        player.play()
        
        # Auto-remove when finished
        player.connect("finished", Callable(player, "queue_free"))
        
    func play_music(music_name: String, loop: bool = true):
        # Play background music
        if music_name == current_music:
            return  # Already playing
            
        var music_data = SoundDatabase.get_music(music_name)
        if music_data == null:
            return
            
        music_player.stream = music_data.audio_stream
        music_player.stream.loop = loop
        music_player.play()
        current_music = music_name
        
    func stop_music():
        # Stop background music
        music_player.stop()
        current_music = ""
        
    func play_ambient(ambient_name: String, loop: bool = true):
        # Play ambient background sound
        var ambient_data = SoundDatabase.get_ambient(ambient_name)
        if ambient_data == null:
            return
            
        ambient_player.stream = ambient_data.audio_stream
        ambient_player.stream.loop = loop
        ambient_player.play()
        
    func stop_ambient():
        # Stop ambient sound
        ambient_player.stop()
        
    func play_voice(voice_line: String, character: String = ""):
        # Play voice acting line
        var voice_data = SoundDatabase.get_voice(voice_line, character)
        if voice_data == null:
            return
            
        var player = AudioStreamPlayer.new()
        player.stream = voice_data.audio_stream
        player.bus = voice_bus
        add_child(player)
        player.play()
        
        # Auto-remove when finished
        player.connect("finished", Callable(player, "queue_free"))
        
    func set_volume(bus_name: String, volume: float):
        # Set volume for an audio bus (0.0 to 1.0)
        var bus_index = AudioServer.get_bus_index(bus_name)
        if bus_index != -1:
            AudioServer.set_bus_volume_db(bus_index, linear_to_db(volume))

# Sound database for managing audio resources
class SoundDatabase:
    # Dictionaries mapping sound names to audio resources
    var sound_effects: Dictionary = {}
    var music_tracks: Dictionary = {}
    var ambient_sounds: Dictionary = {}
    var voice_lines: Dictionary = {}
    
    func _ready():
        # Load all sound definitions
        load_sound_definitions()
        
    func load_sound_definitions():
        # Load sound definitions from resources
        var sound_def_files = get_sound_definition_files()
        for file_path in sound_def_files:
            var sound_def = load(file_path)
            if sound_def is SoundDefinition:
                register_sound_definition(sound_def)
                
    func register_sound_definition(sound_def: SoundDefinition):
        # Register a sound definition in the appropriate dictionary
        match sound_def.sound_type:
            SoundDefinition.Type.SFX:
                sound_effects[sound_def.name] = sound_def
            SoundDefinition.Type.MUSIC:
                music_tracks[sound_def.name] = sound_def
            SoundDefinition.Type.AMBIENT:
                ambient_sounds[sound_def.name] = sound_def
            SoundDefinition.Type.VOICE:
                if not voice_lines.has(sound_def.name):
                    voice_lines[sound_def.name] = {}
                voice_lines[sound_def.name][sound_def.character] = sound_def
                
    func get_sound(sound_name: String) -> SoundDefinition:
        return sound_effects.get(sound_name, null)
        
    func get_music(music_name: String) -> SoundDefinition:
        return music_tracks.get(music_name, null)
        
    func get_ambient(ambient_name: String) -> SoundDefinition:
        return ambient_sounds.get(ambient_name, null)
        
    func get_voice(voice_line: String, character: String = "") -> SoundDefinition:
        if not voice_lines.has(voice_line):
            return null
            
        var character_voices = voice_lines[voice_line]
        # Return character-specific voice if available
        if character_voices.has(character):
            return character_voices[character]
        # Otherwise return default voice
        elif character_voices.has("default"):
            return character_voices["default"]
        # Return any available voice
        elif character_voices.size() > 0:
            return character_voices.values()[0]
            
        return null

# Sound definition resource
class SoundDefinition extends Resource:
    enum Type { SFX, MUSIC, AMBIENT, VOICE }
    
    @export var name: String
    @export var sound_type: Type
    @export var audio_stream: AudioStream
    @export var max_distance: float = 100.0  # For 3D sounds
    @export var character: String = ""  # For voice lines
    @export var priority: int = 0  # For sound importance
    @export var loop: bool = false
    
    func _init():
        resource_name = name

# 3D sound emitter component
class SoundEmitter3D extends Node3D:
    @export var sound_name: String
    @export var auto_play: bool = false
    @export var loop: bool = false
    @export var volume: float = 1.0
    @export var max_distance: float = 100.0
    
    var audio_player: AudioStreamPlayer3D
    
    func _ready():
        setup_audio_player()
        if auto_play:
            play()
            
    func setup_audio_player():
        audio_player = AudioStreamPlayer3D.new()
        var sound_data = SoundDatabase.get_sound(sound_name)
        if sound_data != null:
            audio_player.stream = sound_data.audio_stream
            audio_player.max_distance = sound_data.max_distance
        else:
            audio_player.max_distance = max_distance
            
        audio_player.unit_db = linear_to_db(volume)
        audio_player.bus = "SFX"
        add_child(audio_player)
        
    func play():
        if audio_player.stream != null:
            audio_player.play()
            
    func stop():
        audio_player.stop()
        
    func is_playing() -> bool:
        return audio_player.playing

# Dynamic music system for responsive background music
class DynamicMusicSystem:
    var current_context: String = "peaceful"
    var tension_level: float = 0.0  # 0.0 to 1.0
    var transition_speed: float = 0.1
    
    func _process(delta):
        update_music_based_on_context(delta)
        
    func update_music_based_on_context(delta):
        # Gradually change music based on game context
        var target_tension = calculate_target_tension()
        tension_level = move_toward(tension_level, target_tension, transition_speed * delta)
        
        # Select appropriate music based on tension and context
        var music_name = select_music_for_context(current_context, tension_level)
        if AudioManager.current_music != music_name:
            AudioManager.play_music(music_name)
            
    func calculate_target_tension() -> float:
        # Calculate tension based on combat, danger, etc.
        var tension = 0.0
        
        # Add tension from nearby enemies
        var nearby_enemies = get_nearby_enemies(GameManager.player_ship, 500.0)
        tension += nearby_enemies.size() * 0.1
        
        # Add tension from player damage
        if GameManager.player_ship != null:
            var damage_ratio = (GameManager.player_ship.shipClass.maxHullStrength - 
                              GameManager.player_ship.hullStrength) / 
                             GameManager.player_ship.shipClass.maxHullStrength
            tension += damage_ratio * 0.5
            
        return clamp(tension, 0.0, 1.0)
        
    func set_context(context: String):
        current_context = context
        
    func select_music_for_context(context: String, tension: float) -> String:
        # Select music based on context and tension level
        match context:
            "peaceful":
                return "exploration_theme"
            "combat":
                if tension < 0.3:
                    return "combat_intro"
                elif tension < 0.7:
                    return "combat_middle"
                else:
                    return "combat_intense"
            "briefing":
                return "briefing_theme"
            _:
                return "default_theme"
```

### TRES Resources
```ini
[gd_resource type="Resource" load_steps=3 format=2]

[ext_resource path="res://audio/sfx/laser_fire.ogg" type="AudioStream" id=1]

[resource]
resource_name = "Laser_Fire_Sound"
name = "laser_fire"
sound_type = 0  # SFX
audio_stream = ExtResource(1)
max_distance = 200.0
priority = 5
loop = false

[gd_resource type="Resource" load_steps=3 format=2]

[ext_resource path="res://audio/music/combat_theme.ogg" type="AudioStream" id=1]

[resource]
resource_name = "Combat_Music"
name = "combat_theme"
sound_type = 1  # MUSIC
audio_stream = ExtResource(1)
loop = true
```

### TSCN Scenes
```ini
[gd_scene load_steps=4 format=2]

[ext_resource path="res://scripts/sound_emitter_3d.gd" type="Script" id=1]
[ext_resource path="res://resources/laser_fire_sound.tres" type="Resource" id=2]
[ext_resource path="res://audio/sfx/laser_fire.ogg" type="AudioStream" id=3]

[node name="LaserSoundEmitter" type="Node3D"]
script = ExtResource(1)
sound_name = "laser_fire"
auto_play = false
loop = false
volume = 1.0
max_distance = 200.0

[node name="AudioStreamPlayer3D" type="AudioStreamPlayer3D" parent="."]
stream = ExtResource(3)
max_distance = 200.0
unit_db = 0.0
bus = "SFX"
```

### Implementation Notes
The Audio Module in Godot leverages:
1. **AudioStreamPlayer**: For 2D audio playback
2. **AudioStreamPlayer3D**: For positional 3D audio
3. **AudioServer**: For bus volume control and audio management
4. **Resources**: Sound definitions as data-driven configurations
5. **Signals**: For audio event handling
6. **Autoload**: AudioManager as a global singleton
7. **Scene System**: Audio emitters as scene components

This replaces the C++ audio system with Godot's built-in audio engine while preserving the same functionality. The implementation uses Godot's audio buses for volume control and the resource system for sound definitions, making it easy to manage and modify audio assets.